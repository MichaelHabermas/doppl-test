#!/usr/bin/env python3
"""
Minimal OpenRouter Fusion demo with critic loop.

Pipeline per round:
  panel (2 models) → fusion judge → final answer → critic (score + clarifying questions)
If the critic rejects, the next round gets the feedback injected and fusion runs again.

Use --html to write a self-contained trace page for live demo / projector.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from fusion_common import panel_to_trace, parse_json_response
from html_trace import write_trace_html

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_HTML = Path("fusion_trace.html")
DEFAULT_ROUNDS = 2
PASS_SCORE = 7
console = Console()

DEFAULT_PROMPT = """We're building "Room Vitals" — a small sensor kit you stick in a new room.

What metrics should we track, and what's the one direction we should ship first?

Keep it practical. We're a 2-person team with 2 weeks."""

PANEL_MODELS = [
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
]

JUDGE_MODEL = "google/gemini-2.5-flash"
FINAL_MODEL = "openai/gpt-4o-mini"
CRITIC_MODEL = "google/gemini-2.5-flash"

JUDGE_SYSTEM = """You are a fusion judge. You receive answers from multiple AI models on the same prompt.

Do NOT merge their answers into one essay. Compare them and return ONLY valid JSON with this shape:
{
  "consensus": ["points most models agree on"],
  "contradictions": [{"topic": "...", "views": ["model A says...", "model B says..."]}],
  "unique_insights": [{"from": "model label", "insight": "..."}],
  "blind_spots": ["things none of the models addressed"],
  "clarifying_questions": ["questions we must answer before committing to a direction"],
  "recommended_direction": "one sentence — best direction IF we had to decide now, with caveats"
}

Be concise. Prioritize surfacing clarifying_questions when the prompt is underspecified."""

FINAL_SYSTEM = """You write the final answer for the user.

You receive a structured fusion analysis (consensus, contradictions, blind spots, clarifying questions).
Ground your answer in that analysis.

Structure your reply as:
1. **Decision** — one clear recommended direction (with confidence level: low/medium/high)
2. **Why** — 2-3 bullets citing consensus vs disagreement
3. **Clarifying questions** — the top 3 questions to ask before building (copy from analysis if good)
4. **Next step** — one concrete action for this week

Keep it under 250 words."""

CRITIC_SYSTEM = """You are an adversarial critic on a red-team panel. Your job is to score how well a proposed answer
handles an underspecified prompt — NOT to rewrite the answer.

Return ONLY valid JSON:
{
  "verdict": "pass" or "needs_revision",
  "score": 1-10,
  "scores": {
    "addresses_prompt": 1-10,
    "practicality": 1-10,
    "handles_ambiguity": 1-10,
    "actionability": 1-10
  },
  "strengths": ["what the answer did well"],
  "weaknesses": ["specific gaps, hand-waving, or overconfidence"],
  "clarifying_questions": ["questions the answer SHOULD have asked or answered but didn't"],
  "what_would_make_this_pass": "one concrete sentence — what a revised answer must do"
}

Scoring guide:
- 8-10 + verdict pass: answer explicitly states assumptions, doesn't overcommit, actionable
- 5-7 + needs_revision: direction might be ok but ambiguity was glossed over
- 1-4 + needs_revision: wrong room type assumed, fantasy scope, or ignores constraints

Be harsh on overconfidence when the original prompt was vague. Prefer needs_revision unless the answer
honestly handles uncertainty."""


def api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        console.print("[red]Missing OPENROUTER_API_KEY[/red] — copy .env.example to .env and add your key.")
        sys.exit(1)
    return key


def chat(
    client: httpx.Client,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.4,
    extra: dict[str, Any] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if extra:
        payload.update(extra)

    response = client.post(OPENROUTER_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def run_panel(client: httpx.Client, prompt: str) -> list[tuple[str, str]]:
    def ask(model: str) -> tuple[str, str]:
        content = chat(
            client,
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Answer directly and practically. If the prompt is ambiguous, say what you're assuming.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return model, content

    results: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=len(PANEL_MODELS)) as pool:
        futures = {pool.submit(ask, m): m for m in PANEL_MODELS}
        for future in as_completed(futures):
            results.append(future.result())

    order = {m: i for i, m in enumerate(PANEL_MODELS)}
    results.sort(key=lambda pair: order.get(pair[0], 99))
    return results


def run_judge(client: httpx.Client, prompt: str, panel: list[tuple[str, str]]) -> dict[str, Any]:
    panel_text = "\n\n".join(f"--- {label} ---\n{answer}" for label, answer in panel)
    raw = chat(
        client,
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": f"Original prompt:\n{prompt}\n\nPanel responses:\n{panel_text}"},
        ],
        temperature=0.2,
    )
    return parse_json_response(raw)


def run_final(client: httpx.Client, prompt: str, analysis: dict[str, Any]) -> str:
    return chat(
        client,
        model=FINAL_MODEL,
        messages=[
            {"role": "system", "content": FINAL_SYSTEM},
            {
                "role": "user",
                "content": f"Original prompt:\n{prompt}\n\nFusion analysis:\n{json.dumps(analysis, indent=2)}",
            },
        ],
        temperature=0.3,
    )


def run_critic(
    client: httpx.Client,
    *,
    original_prompt: str,
    round_prompt: str,
    analysis: dict[str, Any],
    final: str,
    round_num: int,
) -> dict[str, Any]:
    raw = chat(
        client,
        model=CRITIC_MODEL,
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Original user prompt:\n{original_prompt}\n\n"
                    f"Round {round_num} prompt (may include prior feedback):\n{round_prompt}\n\n"
                    f"Fusion analysis that informed the answer:\n{json.dumps(analysis, indent=2)}\n\n"
                    f"Proposed answer to critique:\n{final}"
                ),
            },
        ],
        temperature=0.2,
    )
    return parse_json_response(raw)


def critic_passes(critic: dict[str, Any]) -> bool:
    if critic.get("parse_error"):
        return False
    verdict = str(critic.get("verdict", "")).lower()
    score = critic.get("score")
    if verdict == "pass":
        return True
    if isinstance(score, (int, float)) and score >= PASS_SCORE:
        return True
    return False


def build_next_prompt(original: str, final: str, critic: dict[str, Any], round_num: int) -> str:
    weaknesses = critic.get("weaknesses") or []
    questions = critic.get("clarifying_questions") or []
    fix = critic.get("what_would_make_this_pass", "")

    weakness_block = "\n".join(f"- {w}" for w in weaknesses) or "- (none listed)"
    question_block = "\n".join(f"- {q}" for q in questions) or "- (none listed)"

    return f"""{original}

---
GENERATION {round_num} — CRITIC FEEDBACK (revise your recommendation):

Previous answer:
{final}

Weaknesses the critic found:
{weakness_block}

Clarifying questions you must address explicitly (state your assumptions):
{question_block}

What would make this pass: {fix}

Revise: pick ONE direction, state what room/use-case you're assuming, and keep it shippable in 2 weeks."""


def run_fusion_round(
    client: httpx.Client,
    *,
    original_prompt: str,
    round_prompt: str,
    round_num: int,
) -> dict[str, Any]:
    console.rule(f"[bold cyan]Round {round_num} — Step 1: Panel[/bold cyan]")
    panel = run_panel(client, round_prompt)
    for model, answer in panel:
        console.print(Panel(answer, title=f"[green]{model.split('/')[-1]}[/green]", border_style="green"))

    console.rule(f"[bold cyan]Round {round_num} — Step 2: Fusion judge[/bold cyan]")
    analysis = run_judge(client, round_prompt, panel)
    console.print(Syntax(json.dumps(analysis, indent=2), "json", theme="monokai", line_numbers=False))

    console.rule(f"[bold cyan]Round {round_num} — Step 3: Decision[/bold cyan]")
    final = run_final(client, round_prompt, analysis)
    console.print(Panel(final, title="[bold white]Decision[/bold white]", border_style="cyan"))

    console.rule(f"[bold red]Round {round_num} — Step 4: Critic[/bold red]")
    critic = run_critic(
        client,
        original_prompt=original_prompt,
        round_prompt=round_prompt,
        analysis=analysis,
        final=final,
        round_num=round_num,
    )
    console.print(Syntax(json.dumps(critic, indent=2), "json", theme="monokai", line_numbers=False))

    passed = critic_passes(critic)
    verdict = critic.get("verdict", "?")
    score = critic.get("score", "?")
    if passed:
        console.print(f"[bold green]Critic: PASS[/bold green] (score {score})")
    else:
        console.print(f"[bold yellow]Critic: NEEDS REVISION[/bold yellow] (score {score}, verdict {verdict})")
        if critic.get("clarifying_questions"):
            console.print("\n[bold yellow]Critic's clarifying questions:[/bold yellow]")
            for q in critic["clarifying_questions"]:
                console.print(f"  • {q}")

    return {
        "round": round_num,
        "prompt_used": round_prompt,
        "panel": panel_to_trace(panel),
        "analysis": analysis,
        "final": final,
        "critic": critic,
        "passed": passed,
    }


def run_loop(client: httpx.Client, prompt: str, max_rounds: int) -> dict[str, Any]:
    rounds: list[dict[str, Any]] = []
    round_prompt = prompt

    for n in range(1, max_rounds + 1):
        if n > 1:
            console.print()
            console.rule(f"[bold magenta]↻ Loop — generation {n}[/bold magenta]")

        round_data = run_fusion_round(
            client,
            original_prompt=prompt,
            round_prompt=round_prompt,
            round_num=n,
        )
        rounds.append(round_data)

        if round_data["passed"]:
            console.print(f"\n[green]Stopping — critic passed at round {n}[/green]")
            break

        if n < max_rounds:
            round_prompt = build_next_prompt(prompt, round_data["final"], round_data["critic"], n)
            console.print(f"\n[dim]Feeding critic feedback into round {n + 1}…[/dim]")
        else:
            console.print(f"\n[yellow]Max rounds ({max_rounds}) reached — shipping best attempt[/yellow]")

    last = rounds[-1]
    return {
        "prompt": prompt,
        "rounds": rounds,
        "panel": last["panel"],
        "analysis": last["analysis"],
        "final": last["final"],
        "critic": last["critic"],
        "total_rounds": len(rounds),
        "passed": last["passed"],
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def run_official(client: httpx.Client, prompt: str) -> str:
    console.print("[dim]Calling openrouter/fusion (general-budget)…[/dim]\n")
    answer = chat(
        client,
        model="openrouter/fusion",
        messages=[{"role": "user", "content": prompt}],
        extra={
            "plugins": [
                {
                    "id": "fusion",
                    "preset": "general-budget",
                    "analysis_models": [f"~{PANEL_MODELS[0]}", f"~{PANEL_MODELS[1]}"],
                }
            ]
        },
    )
    console.print(Panel(answer, title="[bold white]OpenRouter Fusion[/bold white]", border_style="magenta"))
    return answer


def write_html_trace(trace: dict[str, Any], html_path: Path, open_browser: bool) -> None:
    out = write_trace_html(html_path, trace)
    console.print(f"\n[green]Trace written →[/green] [link=file://{out}]{out}[/link]")
    if open_browser:
        webbrowser.open(out.as_uri())


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenRouter Fusion demo with critic loop")
    parser.add_argument(
        "--mode",
        choices=["transparent", "official", "both"],
        default="transparent",
        help="transparent = DIY fusion loop; official = OpenRouter Fusion API",
    )
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Vague prompts work best")
    parser.add_argument(
        "--rounds",
        type=int,
        default=DEFAULT_ROUNDS,
        help=f"Max fusion+critic rounds (default {DEFAULT_ROUNDS})",
    )
    parser.add_argument(
        "--html",
        nargs="?",
        const=str(DEFAULT_HTML),
        default=None,
        metavar="PATH",
        help=f"Write trace HTML (default: {DEFAULT_HTML})",
    )
    parser.add_argument("--open", action="store_true", help="Open HTML trace in browser")
    args = parser.parse_args()
    key = api_key()

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/doppl-test/fusion-demo",
        "X-Title": "Doppl Fusion Demo",
    }

    console.print(Panel(args.prompt, title="[bold]Prompt[/bold]", border_style="blue"))

    trace: dict[str, Any] | None = None

    with httpx.Client(headers=headers, timeout=180.0) as client:
        if args.mode in ("transparent", "both"):
            trace = run_loop(client, args.prompt, max(1, args.rounds))
        if args.mode == "both":
            console.print()
        if args.mode in ("official", "both"):
            official = run_official(client, args.prompt)
            if trace is None:
                trace = {
                    "prompt": args.prompt,
                    "rounds": [],
                    "final": official,
                    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                }
            else:
                trace["official"] = official

    if args.html and trace is not None:
        write_html_trace(trace, Path(args.html), args.open)
    elif args.open and not args.html:
        console.print("[yellow]--open requires --html[/yellow]")


if __name__ == "__main__":
    main()
