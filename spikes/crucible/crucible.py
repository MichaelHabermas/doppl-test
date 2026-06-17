#!/usr/bin/env python3
"""Belief-revision crucible — a competing L2 spawner to the genotype path.

Loop topology under test: instead of breeding on blind spots, put cheap models
in a structured argument and measure *belief revision under pressure*.

  1. Spawner decides how many debaters (spawncidences) to instantiate and which
     ecological archetypes to use — within a metabolism cap.
  2. Each debater emits a private OPENING position (structured).
  3. Fixed-protocol turns with MANDATORY moves: one concrete objection, steal one
     point from a peer, and state what would change their mind.
  4. Each debater emits a FINAL position + a REVISION LEDGER (the first-class
     artifact: what I held, what changed, what moved me, what I still reject).
  5. A judge scores final idea + revision quality + unresolved tension — not
     rhetorical victory.

This spike is mortal. Its job is to be witnessed, leave a trace, and collapse to
a lesson. See ../../TREATISE.md (§ VII loop-topology crossover, § II two geometries).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from crucible_html import write_crucible_html

load_dotenv()

console = Console()

CHEAP_MODELS = ["google/gemini-2.5-flash", "openai/gpt-4o-mini"]
SPAWNER_MODEL = "google/gemini-2.5-flash"
JUDGE_MODEL = "google/gemini-2.5-flash"
DEFAULT_HTML = "crucible_trace.html"


@dataclass
class Backend:
    """Where calls go. OpenRouter by default; a local OpenAI-compatible
    endpoint (Ollama / LM Studio serving Gemma 4, Hermes, Pi, etc.) when --local."""

    base_url: str
    model_override: str | None
    requires_key: bool


# Set once in main(); read by chat(). Default is OpenRouter.
_BACKEND = Backend(base_url="https://openrouter.ai/api/v1", model_override=None, requires_key=True)


def resolve_backend(local: bool) -> Backend:
    if local:
        base = os.environ.get("LOCAL_BASE_URL", "http://localhost:11434/v1").rstrip("/")
        model = os.environ.get("LOCAL_MODEL", "gemma4")
        return Backend(base_url=base, model_override=model, requires_key=False)
    base = os.environ.get("CRUCIBLE_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    return Backend(base_url=base, model_override=os.environ.get("CRUCIBLE_MODEL") or None, requires_key=True)

DEFAULT_PROMPT = """We're building "Room Vitals" — a small sensor kit you stick in a new room.

What metrics should we track, and what's the one direction we should ship first?

Keep it practical. We're a 2-person team with 2 weeks."""

SPAWNCIDENCE_CAP = 5  # metabolism: explore the madness, cap the combinatorics


@dataclass
class Debater:
    """A crucible participant — an ecological-archetype Fusant with a stance temperament.

    `disagreeableness` (0..1) is the anti-herding dial: how hard this voice resists
    convergence-for-its-own-sake. Cooperation is the dominant strategy, but dissenters
    provoke the mutation that keeps the room off the mean.
    """

    id: str
    name: str
    model: str
    archetype: str
    persona: str
    temperament: str  # how it argues
    disagreeableness: float = 0.5  # 0 = eager synthesizer, 1 = stubborn dissenter

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Ecological (Aecological) archetypes the spawner may draw from (treatise § V).
ARCHETYPE_POOL: dict[str, dict[str, Any]] = {
    "transfer-hunter": {
        "name": "Transfer Hunter",
        "persona": "veteran engineer hunting cross-domain analogies that crack the problem",
        "temperament": "bold, pushes a non-obvious transplant; defends it but will concede on feasibility",
        "disagreeableness": 0.5,
    },
    "feasibility-hawk": {
        "name": "Feasibility Hawk",
        "persona": "startup CTO obsessed with 2-week shippability and real constraints",
        "temperament": "kills fantasy scope; concedes when a bold idea is actually cheap",
        "disagreeableness": 0.55,
    },
    "falsifier": {
        "name": "Falsifier",
        "persona": "wolf-hunter who sincerely looks for the flaw others are hiding from",
        "temperament": "skeptical, demands the failure mode; relents only when a real falsification test is offered",
        "disagreeableness": 0.85,
    },
    "contrarian": {
        "name": "Contrarian",
        "persona": "designer who rejects the obvious direction and names the buried assumption",
        "temperament": "argues the opposite on principle but must change its mind if out-reasoned",
        "disagreeableness": 0.8,
    },
    "zeitgeist-reader": {
        "name": "Zeitgeist Reader",
        "persona": "growth strategist sensing what the moment rewards and what the room actually wants",
        "temperament": "synthesizer; tries to steal the best from each and reframe",
        "disagreeableness": 0.3,
    },
}

DEFAULT_ROSTER = ["transfer-hunter", "feasibility-hawk", "falsifier"]

REVISION_CONTRACT = """Return ONLY valid JSON:
{
  "final_position": "your single best surviving idea, one clear direction (<=120 words)",
  "confidence": "low|medium|high",
  "revision_ledger": {
    "held_before": "what you argued in your opening",
    "changed": "what you actually changed (or 'nothing' — be honest)",
    "evidence_moved_me": "the specific peer point or argument that moved you (or 'none')",
    "still_reject": "what you still refuse to concede, and why"
  }
}"""


def api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        console.print(
            "[red]Missing OPENROUTER_API_KEY[/red] — copy .env.example to .env "
            "(or rely on a repo-root/sibling .env) and add your key. "
            "Or run with --local to use a local model (Gemma 4 via Ollama/LM Studio)."
        )
        sys.exit(1)
    return key


def make_client(backend: Backend) -> httpx.Client:
    headers = {
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/doppl-test/crucible",
        "X-Title": "Doppl Crucible Spike",
    }
    if backend.requires_key:
        headers["Authorization"] = f"Bearer {api_key()}"
    return httpx.Client(headers=headers, timeout=180.0)


def chat(
    client: httpx.Client,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.5,
) -> str:
    payload: dict[str, Any] = {
        "model": _BACKEND.model_override or model,
        "messages": messages,
        "temperature": temperature,
    }
    response = client.post(f"{_BACKEND.base_url}/chat/completions", json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def parse_json_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw_output": raw, "parse_error": True}


SPAWNER_SYSTEM = """You are the Crucible Spawner. You decide the composition of a debate room.

You have LATITUDE to choose how many debaters to instantiate (your "spawncidences")
and which ecological archetypes to use — but you pay a metabolism cost, so spend
only what the prompt's difficulty justifies. A vague, high-stakes prompt may warrant
more voices; a narrow one needs fewer.

Available archetypes (id: description):
{pool}

Return ONLY valid JSON:
{{
  "count": <int between 2 and {cap}>,
  "reasoning": "one sentence on why this many and this mix",
  "roster": [{{"archetype": "<id from the pool>", "why": "what this voice is here to stress-test"}}]
}}

roster length MUST equal count. Prefer a Falsifier when the prompt invites confident slop."""


def run_spawner(client: httpx.Client, prompt: str, cap: int) -> dict[str, Any]:
    pool_text = "\n".join(f"- {aid}: {meta['persona']}" for aid, meta in ARCHETYPE_POOL.items())
    raw = chat(
        client,
        model=SPAWNER_MODEL,
        messages=[
            {"role": "system", "content": SPAWNER_SYSTEM.format(pool=pool_text, cap=cap)},
            {"role": "user", "content": f"Prompt to debate:\n{prompt}"},
        ],
        temperature=0.4,
    )
    return parse_json_response(raw)


def build_roster(
    spawner_plan: dict[str, Any], cap: int, dissent_floor: float = 0.0
) -> tuple[list[Debater], dict[str, Any]]:
    roster_spec = spawner_plan.get("roster") or []
    chosen_ids: list[str] = []
    for entry in roster_spec:
        aid = str(entry.get("archetype", "")).strip()
        if aid in ARCHETYPE_POOL:
            chosen_ids.append(aid)

    if not chosen_ids:
        chosen_ids = list(DEFAULT_ROSTER)
        spawner_plan = {**spawner_plan, "fallback": "spawner output unusable — used DEFAULT_ROSTER"}

    chosen_ids = chosen_ids[:cap]
    if len(chosen_ids) < 2:
        chosen_ids = list(DEFAULT_ROSTER)[:max(2, len(chosen_ids))]

    debaters: list[Debater] = []
    for i, aid in enumerate(chosen_ids):
        meta = ARCHETYPE_POOL[aid]
        base = float(meta.get("disagreeableness", 0.5))
        debaters.append(
            Debater(
                id=f"{aid}-{i}",
                name=meta["name"],
                model=CHEAP_MODELS[i % len(CHEAP_MODELS)],
                archetype=aid,
                persona=meta["persona"],
                temperament=meta["temperament"],
                disagreeableness=max(base, dissent_floor),
            )
        )
    return debaters, spawner_plan


def _dissent_clause(disagreeableness: float) -> str:
    if disagreeableness >= 0.75:
        return (
            "Your disagreeableness is HIGH. Hold your ground hard. Do not converge to be "
            "agreeable. If the room is herding toward one answer, that is your cue to attack "
            "its weakest assumption or steelman the rejected option. Concede ONLY to a real "
            "argument or a falsification test — never to social pressure."
        )
    if disagreeableness >= 0.45:
        return (
            "Your disagreeableness is MODERATE. Cooperate, but keep at least one real crux alive. "
            "If you agree, say exactly why — and name what you'd still need to be sure."
        )
    return (
        "Your disagreeableness is LOW. You are a synthesizer — but synthesis is not capitulation. "
        "Fuse the strongest points, and still flag any tension you are papering over."
    )


def debater_system(debater: Debater) -> str:
    return f"""You are {debater.name}, a Fusant in an idea crucible.

Persona: {debater.persona}
Temperament: {debater.temperament}

{_dissent_clause(debater.disagreeableness)}

Rules of this room:
- You have a real point of view and you argue it with personality.
- You are NOT disagreeable for its own sake. Disagreement must carry persuasion.
- You may change your mind — that is a strength here, not a loss — but only for a real reason.
- Premature consensus is the enemy. Regression to the mean is a failure, not a success.
- Be concise. This is a working room, not an essay."""


def run_openings(client: httpx.Client, prompt: str, debaters: list[Debater]) -> dict[str, str]:
    def ask(d: Debater) -> tuple[str, str]:
        text = chat(
            client,
            model=d.model,
            messages=[
                {"role": "system", "content": debater_system(d)},
                {
                    "role": "user",
                    "content": (
                        f"Prompt:\n{prompt}\n\n"
                        "Give your OPENING position. Structure:\n"
                        "CLAIM: one direction you'd ship.\n"
                        "WHY: 2 bullets.\n"
                        "RISK: the one thing that could make you wrong.\n"
                        "Keep under 120 words."
                    ),
                },
            ],
            temperature=0.6,
        )
        return d.id, text

    out: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(4, len(debaters))) as pool:
        for fut in as_completed([pool.submit(ask, d) for d in debaters]):
            did, text = fut.result()
            out[did] = text
    return out


def format_room(debaters: list[Debater], latest: dict[str, str], exclude_id: str) -> str:
    blocks = []
    for d in debaters:
        if d.id == exclude_id:
            continue
        blocks.append(f"--- {d.name} ---\n{latest.get(d.id, '(no statement yet)')}")
    return "\n\n".join(blocks)


def run_turn(
    client: httpx.Client,
    prompt: str,
    debaters: list[Debater],
    latest: dict[str, str],
    turn_num: int,
) -> dict[str, str]:
    def ask(d: Debater) -> tuple[str, str]:
        room = format_room(debaters, latest, d.id)
        text = chat(
            client,
            model=d.model,
            messages=[
                {"role": "system", "content": debater_system(d)},
                {
                    "role": "user",
                    "content": (
                        f"Prompt:\n{prompt}\n\n"
                        f"What the others just said:\n{room}\n\n"
                        f"This is turn {turn_num}. You MUST do all four moves:\n"
                        "1. OBJECT: one concrete objection to a specific peer (name them).\n"
                        "2. STEAL: one genuinely good point you take from a peer.\n"
                        "3. CHANGE-TEST: state exactly what would change your mind.\n"
                        "4. HOLD-OR-FOLD: if the room is converging, either name the crux that is "
                        "still unresolved, or steelman the option being abandoned — do NOT just agree.\n"
                        "Then give your updated stance in one line. Under 150 words."
                    ),
                },
            ],
            # Higher disagreeableness => a touch more divergence in sampling.
            temperature=0.55 + 0.25 * d.disagreeableness,
        )
        return d.id, text

    out: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(4, len(debaters))) as pool:
        for fut in as_completed([pool.submit(ask, d) for d in debaters]):
            did, text = fut.result()
            out[did] = text
    return out


def run_finals(
    client: httpx.Client,
    prompt: str,
    debaters: list[Debater],
    opening: dict[str, str],
    latest: dict[str, str],
) -> dict[str, dict[str, Any]]:
    def ask(d: Debater) -> tuple[str, dict[str, Any]]:
        room = format_room(debaters, latest, d.id)
        raw = chat(
            client,
            model=d.model,
            messages=[
                {"role": "system", "content": debater_system(d)},
                {
                    "role": "user",
                    "content": (
                        f"Prompt:\n{prompt}\n\n"
                        f"Your opening was:\n{opening.get(d.id, '')}\n\n"
                        f"Where the room ended up:\n{room}\n\n"
                        f"{REVISION_CONTRACT}"
                    ),
                },
            ],
            temperature=0.4,
        )
        return d.id, parse_json_response(raw)

    out: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=min(4, len(debaters))) as pool:
        for fut in as_completed([pool.submit(ask, d) for d in debaters]):
            did, parsed = fut.result()
            out[did] = parsed
    return out


JUDGE_SYSTEM = """You are the crucible judge. You read an entire debate, not just the final answers.

CONSENSUS IS NOT QUALITY. A room that quickly agreed may have regressed to the mean.
Distinguish:
- "resolved": agreement reached by genuinely defeating the alternatives with argument/evidence.
- "herded": agreement reached by social convergence — nobody really tested the weak points.

Do NOT reward whoever was loudest or whoever flip-flopped most. Reward:
- the strongest SURVIVING idea after pressure,
- EARNED revision (changed mind for a real reason vs. performative agreement),
- honestly preserved disagreement (unresolved tension that is real, not laziness).

Scoring discipline:
- If consensus_quality is "herded" OR unresolved_tension is empty AND the prompt was hard,
  the score MUST NOT exceed 6, and verdict should lean "needs-revision".
- An empty unresolved_tension on a genuinely contested prompt is a red flag, not a win.

Return ONLY valid JSON:
{
  "surviving_idea": "the single best idea that survived the crucible (<=120 words)",
  "why_it_survived": "what pressure it withstood",
  "consensus_quality": "resolved|herded|mixed",
  "consensus_note": "one line: was agreement earned or social?",
  "best_revision": {"who": "debater name", "what_changed": "...", "earned": true},
  "performative_flips": ["debaters who changed their mind without a real reason, if any"],
  "unresolved_tension": ["real disagreements still standing and worth keeping"],
  "score": <int 1-10 for the room's epistemic quality>,
  "verdict": "pass|needs-revision"
}"""


def run_judge(
    client: httpx.Client,
    prompt: str,
    debaters: list[Debater],
    opening: dict[str, str],
    transcript: list[dict[str, str]],
    finals: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    name_by_id = {d.id: d.name for d in debaters}
    parts = [f"PROMPT:\n{prompt}\n", "OPENINGS:"]
    for d in debaters:
        parts.append(f"[{d.name}] {opening.get(d.id, '')}")
    for t, turn in enumerate(transcript, start=1):
        parts.append(f"\nTURN {t}:")
        for did, text in turn.items():
            parts.append(f"[{name_by_id.get(did, did)}] {text}")
    parts.append("\nFINALS (with revision ledgers):")
    for did, payload in finals.items():
        parts.append(f"[{name_by_id.get(did, did)}] {json.dumps(payload)}")

    raw = chat(
        client,
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": "\n".join(parts)},
        ],
        temperature=0.2,
    )
    return parse_json_response(raw)


def run_crucible(
    client: httpx.Client,
    prompt: str,
    *,
    turns: int,
    forced_count: int | None,
    use_spawner: bool,
    cap: int,
    dissent_floor: float = 0.0,
) -> dict[str, Any]:
    console.rule("[bold cyan]Spawner — deciding the room[/bold cyan]")
    if use_spawner:
        plan = run_spawner(client, prompt, cap)
    else:
        plan = {"count": forced_count or len(DEFAULT_ROSTER), "reasoning": "spawner disabled", "roster": [{"archetype": a, "why": "default"} for a in DEFAULT_ROSTER]}

    if forced_count is not None and plan.get("roster"):
        plan["roster"] = plan["roster"][:forced_count]
        plan["count"] = len(plan["roster"])

    debaters, plan = build_roster(plan, cap, dissent_floor)
    console.print(Syntax(json.dumps(plan, indent=2), "json", theme="monokai", line_numbers=False))
    console.print(
        "[dim]Spawned "
        + ", ".join(f"{d.name} (dis={d.disagreeableness:.2f})" for d in debaters)
        + "[/dim]"
    )

    console.rule("[bold cyan]Openings[/bold cyan]")
    opening = run_openings(client, prompt, debaters)
    for d in debaters:
        console.print(Panel(opening[d.id], title=f"[green]{d.name}[/green]", border_style="green"))

    latest = dict(opening)
    transcript: list[dict[str, str]] = []
    for t in range(1, turns + 1):
        console.rule(f"[bold yellow]Turn {t} — object / steal / change-test[/bold yellow]")
        turn = run_turn(client, prompt, debaters, latest, t)
        transcript.append(turn)
        latest = turn
        for d in debaters:
            console.print(Panel(turn[d.id], title=f"[yellow]{d.name}[/yellow]", border_style="yellow"))

    console.rule("[bold magenta]Finals + revision ledgers[/bold magenta]")
    finals = run_finals(client, prompt, debaters, opening, latest)
    for d in debaters:
        console.print(
            Panel(
                json.dumps(finals[d.id], indent=2),
                title=f"[magenta]{d.name}[/magenta]",
                border_style="magenta",
            )
        )

    console.rule("[bold red]Judge — scores the whole conversation[/bold red]")
    verdict = run_judge(client, prompt, debaters, opening, transcript, finals)
    console.print(Syntax(json.dumps(verdict, indent=2), "json", theme="monokai", line_numbers=False))

    score = verdict.get("score", "?")
    v = verdict.get("verdict", "?")
    if str(v).startswith("pass"):
        console.print(f"[bold green]Crucible: PASS[/bold green] (score {score})")
    else:
        console.print(f"[bold yellow]Crucible: NEEDS REVISION[/bold yellow] (score {score})")

    return {
        "prompt": prompt,
        "spawner_plan": plan,
        "debaters": [d.to_dict() for d in debaters],
        "openings": opening,
        "transcript": transcript,
        "finals": finals,
        "judge": verdict,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Belief-revision crucible spike")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="The idea/question to put in the crucible")
    parser.add_argument("--turns", type=int, default=2, help="Number of argument turns (default 2)")
    parser.add_argument(
        "--debaters",
        type=int,
        default=None,
        help="Force debater count (overrides spawner latitude)",
    )
    parser.add_argument("--no-spawner", action="store_true", help="Skip the spawner; use the default roster")
    parser.add_argument(
        "--dissent",
        type=float,
        default=0.0,
        help="Anti-herding floor 0..1 — raises every Fusant's disagreeableness to at least this",
    )
    parser.add_argument("--cap", type=int, default=SPAWNCIDENCE_CAP, help="Metabolism cap on spawncidences")
    parser.add_argument("--json-out", default=None, help="Write the full trace JSON to this path")
    parser.add_argument("--html", action="store_true", help="Write a witnessable HTML trace and open it")
    parser.add_argument("--html-out", default=DEFAULT_HTML, help="HTML trace output path")
    parser.add_argument("--no-open", action="store_true", help="With --html, don't open the browser")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use a local OpenAI-compatible model (Gemma 4 via Ollama/LM Studio). "
        "Honors LOCAL_BASE_URL + LOCAL_MODEL env.",
    )
    args = parser.parse_args()

    global _BACKEND
    _BACKEND = resolve_backend(args.local)
    if args.local:
        console.print(f"[dim]Local backend: {_BACKEND.base_url} · model={_BACKEND.model_override}[/dim]")

    cap = max(2, min(args.cap, 8))
    dissent_floor = max(0.0, min(args.dissent, 1.0))
    with make_client(_BACKEND) as client:
        trace = run_crucible(
            client,
            args.prompt.strip(),
            turns=max(1, args.turns),
            forced_count=args.debaters,
            use_spawner=not args.no_spawner,
            cap=cap,
            dissent_floor=dissent_floor,
        )

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(trace, fh, indent=2)
        console.print(f"[dim]Wrote trace JSON → {args.json_out}[/dim]")

    if args.html:
        path = write_crucible_html(trace, args.html_out)
        console.print(f"[dim]Wrote HTML trace → {path}[/dim]")
        refresh_root_index()
        if not args.no_open:
            webbrowser.open(Path(path).resolve().as_uri())


def refresh_root_index() -> None:
    """Best-effort: rebuild the root Agarden index so the new trace is navigable."""
    builder = Path(__file__).resolve().parents[2] / "build_index.py"
    if not builder.exists():
        return
    try:
        subprocess.run([sys.executable, str(builder)], check=False, capture_output=True)
        console.print("[dim]Refreshed root index.html[/dim]")
    except OSError:
        pass


if __name__ == "__main__":
    main()
