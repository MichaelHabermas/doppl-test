#!/usr/bin/env python3
"""
OpenRouter Fusion demo with agenome breeding.

Gen 1: two Rule-of-Cool parent agenomes → fusion judge → decision → critic.
On critic fail: breed a child agenome on blind spots (not prompt retry).
Gen 2+: child agenome answers directly, critic again.

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

from agenome import (
    Agenome,
    agenome_panel_entry,
    breed_child,
    default_parent_pair,
    format_lineage_json,
    lineage_record,
    run_agenome,
)
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


def make_client() -> httpx.Client:
    return httpx.Client(
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/doppl-test/fusion-demo",
            "X-Title": "Doppl Fusion Demo",
        },
        timeout=180.0,
    )


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


def run_agenome_panel(
    client: httpx.Client,
    prompt: str,
    parents: tuple[Agenome, Agenome],
) -> tuple[list[dict[str, Any]], tuple[Agenome, Agenome]]:
    parent_a, parent_b = parents

    def ask(genome: Agenome) -> dict[str, Any]:
        answer = run_agenome(chat, client, genome, prompt)
        return agenome_panel_entry(genome, answer)

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(ask, g): g for g in (parent_a, parent_b)}
        for future in as_completed(futures):
            results.append(future.result())

    order = {parent_a.id: 0, parent_b.id: 1}
    results.sort(key=lambda entry: order.get(str(entry.get("agenome_id")), 99))
    return results, (parent_a, parent_b)


def panel_for_judge(panel: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return [
        (str(entry.get("label") or entry.get("model", "Model")), str(entry.get("answer", "")))
        for entry in panel
    ]


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


def run_fusion_round(
    client: httpx.Client,
    *,
    original_prompt: str,
    round_prompt: str,
    round_num: int,
    parents: tuple[Agenome, Agenome] | None = None,
) -> dict[str, Any]:
    if parents is None:
        parents = default_parent_pair()

    console.rule(f"[bold cyan]Round {round_num} — Step 1: Parent agenomes[/bold cyan]")
    panel, parent_pair = run_agenome_panel(client, round_prompt, parents)
    for entry in panel:
        label = str(entry.get("label", "Parent"))
        console.print(Panel(str(entry.get("answer", "")), title=f"[green]{label}[/green]", border_style="green"))

    console.rule(f"[bold cyan]Round {round_num} — Step 2: Fusion judge[/bold cyan]")
    analysis = run_judge(client, round_prompt, panel_for_judge(panel))
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
        "mode": "fusion",
        "prompt_used": round_prompt,
        "panel": panel_to_trace(panel),
        "parents": [g.to_dict() for g in parent_pair],
        "analysis": analysis,
        "final": final,
        "critic": critic,
        "passed": passed,
    }


def run_offspring_round(
    client: httpx.Client,
    *,
    original_prompt: str,
    child: Agenome,
    round_num: int,
    lineage: dict[str, Any],
) -> dict[str, Any]:
    console.rule(f"[bold magenta]Round {round_num} — Breeding event[/bold magenta]")
    console.print(Syntax(format_lineage_json(lineage), "json", theme="monokai", line_numbers=False))

    console.rule(f"[bold cyan]Round {round_num} — Child agenome answers[/bold cyan]")
    console.print(Panel(child.name, title="[bold]Offspring[/bold]", border_style="magenta"))
    final = run_agenome(chat, client, child, original_prompt)
    console.print(Panel(final, title="[bold white]Decision[/bold white]", border_style="cyan"))

    console.rule(f"[bold red]Round {round_num} — Critic[/bold red]")
    critic = run_critic(
        client,
        original_prompt=original_prompt,
        round_prompt=original_prompt,
        analysis={"blind_spots": child.primary_mandate, "offspring_mandate": True},
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

    return {
        "round": round_num,
        "mode": "offspring",
        "prompt_used": original_prompt,
        "lineage": lineage,
        "offspring": {
            "agenome": child.to_dict(),
            "answer": final,
        },
        "panel": [],
        "analysis": {"primary_mandate": child.primary_mandate},
        "final": final,
        "critic": critic,
        "passed": passed,
    }


def run_loop(client: httpx.Client, prompt: str, max_rounds: int) -> dict[str, Any]:
    rounds: list[dict[str, Any]] = []
    parents = default_parent_pair()
    child: Agenome | None = None
    lineage: dict[str, Any] | None = None

    for n in range(1, max_rounds + 1):
        if n > 1:
            console.print()
            console.rule(f"[bold magenta]↻ Generation {n} — offspring run[/bold magenta]")

        if n == 1 or child is None:
            round_data = run_fusion_round(
                client,
                original_prompt=prompt,
                round_prompt=prompt,
                round_num=n,
                parents=parents,
            )
        else:
            round_data = run_offspring_round(
                client,
                original_prompt=prompt,
                child=child,
                round_num=n,
                lineage=lineage or {},
            )

        rounds.append(round_data)

        if round_data["passed"]:
            console.print(f"\n[green]Stopping — critic passed at round {n}[/green]")
            break

        if n < max_rounds and round_data.get("mode") == "fusion":
            parent_a, parent_b = parents
            child, mandate = breed_child(
                parent_a,
                parent_b,
                round_data["analysis"],
                round_data["critic"],
                child_generation=n + 1,
            )
            lineage = lineage_record(parent_a, parent_b, child, mandate)
            console.print(
                f"\n[dim]Bred child agenome [bold]{child.name}[/bold] "
                f"on {len(mandate)} blind-spot mandate(s)…[/dim]"
            )
        elif n < max_rounds:
            console.print(f"\n[yellow]Offspring still failed — no further breeding in this demo[/yellow]")
            break
        else:
            console.print(f"\n[yellow]Max rounds ({max_rounds}) reached — shipping best attempt[/yellow]")

    last = rounds[-1]
    return {
        "prompt": prompt,
        "rounds": rounds,
        "lineage": lineage,
        "panel": last.get("panel") or [],
        "analysis": last.get("analysis") or {},
        "final": last.get("final", ""),
        "critic": last.get("critic") or {},
        "total_rounds": len(rounds),
        "passed": last.get("passed", False),
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
        "--no-html",
        action="store_true",
        help="Skip writing the HTML trace (default: write fusion_trace.html)",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Don't open the trace in your browser (default: open after run)",
    )
    parser.add_argument(
        "--html",
        default=str(DEFAULT_HTML),
        metavar="PATH",
        help=f"HTML output path (default: {DEFAULT_HTML})",
    )
    args = parser.parse_args()

    console.print(Panel(args.prompt, title="[bold]Prompt[/bold]", border_style="blue"))

    trace: dict[str, Any] | None = None

    with make_client() as client:
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

    if not args.no_html and trace is not None:
        write_html_trace(trace, Path(args.html), open_browser=not args.no_open)


if __name__ == "__main__":
    main()
