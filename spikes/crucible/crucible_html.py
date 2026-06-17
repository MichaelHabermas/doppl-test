"""Render a crucible run as a self-contained HTML trace — the witnessable
extended aphenome. A picture is worth a thousand tokens: the revision ledger and
preserved tension should be legible at a glance for the whole Agarden team.
"""

from __future__ import annotations

import html
from typing import Any

_CSS = """
:root {
  --bg:#0b0e13; --surface:#141a22; --surface2:#1b232e; --border:#2a3544;
  --text:#e8edf4; --muted:#8b9bb0; --accent:#c084fc; --green:#3dd68c;
  --yellow:#f5c451; --magenta:#e879c9; --red:#fb7185; --blue:#60a5fa;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); line-height:1.55;
  font-family:"SF Pro Text","Segoe UI",system-ui,sans-serif; }
.wrap { max-width:1040px; margin:0 auto; padding:2.5rem 1.25rem 5rem; }
header h1 { font-size:1.7rem; margin:0 0 .3rem; font-weight:680; }
header p { color:var(--muted); margin:0 0 1rem; }
.prompt { background:var(--surface); border:1px solid var(--border);
  border-left:3px solid var(--accent); border-radius:10px; padding:1rem 1.15rem;
  white-space:pre-wrap; font-size:.95rem; margin:1rem 0 2rem; }
.rule { display:flex; align-items:center; gap:.6rem; margin:2.2rem 0 1rem;
  text-transform:uppercase; letter-spacing:.09em; font-size:.74rem; font-weight:700; }
.rule::after { content:""; flex:1; height:1px; background:var(--border); }
.spawner { color:var(--blue); } .openings { color:var(--green); }
.turns { color:var(--yellow); } .finals { color:var(--magenta); } .judge { color:var(--red); }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:1rem; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.1rem; }
.card h3 { margin:0 0 .55rem; font-size:.92rem; display:flex; align-items:center; gap:.5rem; }
.tag { font-size:.66rem; font-weight:700; padding:.12rem .5rem; border-radius:999px;
  background:var(--surface2); color:var(--muted); border:1px solid var(--border);
  text-transform:uppercase; letter-spacing:.05em; }
.body { white-space:pre-wrap; font-size:.875rem; color:#d4dce6; }
.ledger { margin-top:.6rem; border-top:1px dashed var(--border); padding-top:.6rem; font-size:.84rem; }
.ledger dt { color:var(--accent); font-size:.68rem; text-transform:uppercase;
  letter-spacing:.06em; margin-top:.5rem; font-weight:700; }
.ledger dd { margin:.15rem 0 0; color:#d4dce6; }
.changed-nothing dd.changed { color:var(--muted); font-style:italic; }
.verdict { background:var(--surface); border:1px solid var(--border); border-radius:12px;
  padding:1.15rem 1.25rem; }
.score { font-size:2rem; font-weight:750; }
.pass { color:var(--green); } .fail { color:var(--yellow); }
.chips { display:flex; flex-wrap:wrap; gap:.4rem; margin:.5rem 0; }
.chip { font-size:.78rem; padding:.25rem .6rem; border-radius:8px; background:var(--surface2);
  border:1px solid var(--border); }
.chip.tension { border-color:#5b4a1f; color:var(--yellow); }
.chip.flip { border-color:#5b1f28; color:var(--red); }
.empty { color:var(--muted); font-style:italic; font-size:.82rem; }
.surviving { background:var(--surface2); border-left:3px solid var(--green);
  border-radius:8px; padding:.8rem 1rem; margin:.6rem 0; }
.meta { color:var(--muted); font-size:.78rem; margin-top:.4rem; }
.flow { display:flex; flex-wrap:wrap; gap:.4rem; font-size:.78rem; margin:.4rem 0 0; }
.flow span { padding:.25rem .6rem; border-radius:999px; border:1px solid var(--border);
  background:var(--surface); }
.flow .arrow { border:none; background:none; color:var(--muted); }
.nav { position:sticky; top:0; z-index:10; background:rgba(11,14,19,.85);
  backdrop-filter:blur(8px); border-bottom:1px solid var(--border);
  padding:.6rem 1.25rem; display:flex; gap:1rem; align-items:center; font-size:.82rem; }
.nav a { color:var(--accent); text-decoration:none; }
.nav a:hover { text-decoration:underline; }
.nav .sep { color:var(--muted); }
"""


def _e(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _debater_name(debaters: list[dict[str, Any]], did: str) -> tuple[str, str]:
    for d in debaters:
        if d.get("id") == did:
            return str(d.get("name", did)), str(d.get("archetype", ""))
    return did, ""


def _spawner_block(plan: dict[str, Any]) -> str:
    count = _e(plan.get("count", "?"))
    reasoning = _e(plan.get("reasoning", ""))
    rows = []
    for entry in plan.get("roster", []) or []:
        rows.append(
            f'<div class="chip">{_e(entry.get("archetype",""))} — {_e(entry.get("why",""))}</div>'
        )
    fallback = ""
    if plan.get("fallback"):
        fallback = f'<p class="meta">⚠ {_e(plan["fallback"])}</p>'
    return (
        f'<div class="card"><h3>Spawner decision <span class="tag">{count} spawncidences</span></h3>'
        f'<div class="body">{reasoning}</div>'
        f'<div class="chips">{"".join(rows)}</div>{fallback}</div>'
    )


def _ledger_block(payload: dict[str, Any]) -> str:
    if payload.get("parse_error"):
        return f'<div class="body">{_e(payload.get("raw_output",""))}</div>'
    final = _e(payload.get("final_position", ""))
    conf = _e(payload.get("confidence", ""))
    ledger = payload.get("revision_ledger", {}) or {}
    changed = str(ledger.get("changed", "")).strip().lower()
    nothing = changed in {"", "nothing", "none"}
    cls = "ledger changed-nothing" if nothing else "ledger"
    return (
        f'<div class="body">{final}</div>'
        f'<p class="meta">confidence: {conf}</p>'
        f'<dl class="{cls}">'
        f"<dt>held before</dt><dd>{_e(ledger.get('held_before',''))}</dd>"
        f"<dt>changed</dt><dd class=\"changed\">{_e(ledger.get('changed',''))}</dd>"
        f"<dt>evidence moved me</dt><dd>{_e(ledger.get('evidence_moved_me',''))}</dd>"
        f"<dt>still reject</dt><dd>{_e(ledger.get('still_reject',''))}</dd>"
        "</dl>"
    )


def _verdict_block(judge: dict[str, Any]) -> str:
    if judge.get("parse_error"):
        return f'<div class="verdict"><div class="body">{_e(judge.get("raw_output",""))}</div></div>'
    score = judge.get("score", "?")
    verdict = str(judge.get("verdict", "?"))
    passed = verdict.startswith("pass")
    klass = "pass" if passed else "fail"
    consensus = str(judge.get("consensus_quality", "")).strip()
    consensus_note = _e(judge.get("consensus_note", ""))
    consensus_html = ""
    if consensus:
        cclass = "fail" if consensus == "herded" else ""
        consensus_html = (
            f'<p class="meta"><b>Consensus quality:</b> '
            f'<span class="{cclass}">{_e(consensus)}</span> — {consensus_note}</p>'
        )
    tension = judge.get("unresolved_tension", []) or []
    flips = judge.get("performative_flips", []) or []
    best = judge.get("best_revision", {}) or {}

    tension_html = (
        "".join(f'<div class="chip tension">{_e(t)}</div>' for t in tension)
        or '<span class="empty">none preserved — watch for consensus-collapse</span>'
    )
    flips_html = (
        "".join(f'<div class="chip flip">{_e(f)}</div>' for f in flips)
        or '<span class="empty">none flagged</span>'
    )
    best_html = ""
    if best:
        best_html = (
            f'<p class="meta"><b>Best revision:</b> {_e(best.get("who",""))} — '
            f'{_e(best.get("what_changed",""))} '
            f'({"earned" if best.get("earned") else "unearned"})</p>'
        )
    return (
        '<div class="verdict">'
        f'<div class="score {klass}">{_e(score)}/10 · {_e(verdict)}</div>'
        f"{consensus_html}"
        f'<div class="surviving"><b>Surviving idea:</b> {_e(judge.get("surviving_idea",""))}'
        f'<p class="meta">{_e(judge.get("why_it_survived",""))}</p></div>'
        f"{best_html}"
        '<p class="meta"><b>Unresolved tension (the prize):</b></p>'
        f'<div class="chips">{tension_html}</div>'
        '<p class="meta"><b>Performative flips:</b></p>'
        f'<div class="chips">{flips_html}</div>'
        "</div>"
    )


def render_crucible_html(trace: dict[str, Any]) -> str:
    debaters = trace.get("debaters", []) or []
    openings = trace.get("openings", {}) or {}
    transcript = trace.get("transcript", []) or []
    finals = trace.get("finals", {}) or {}

    def _dis(d: dict[str, Any]) -> str:
        val = d.get("disagreeableness")
        return f' · dis {float(val):.2f}' if isinstance(val, (int, float)) else ""

    opening_cards = []
    for d in debaters:
        did = d.get("id")
        opening_cards.append(
            f'<div class="card"><h3>{_e(d.get("name"))} '
            f'<span class="tag">{_e(d.get("archetype"))}</span></h3>'
            f'<div class="body">{_e(openings.get(did,""))}</div>'
            f'<p class="meta">{_e(d.get("model"))}{_dis(d)}</p></div>'
        )

    turn_sections = []
    for i, turn in enumerate(transcript, start=1):
        cards = []
        for did, text in turn.items():
            name, arch = _debater_name(debaters, did)
            cards.append(
                f'<div class="card"><h3>{_e(name)} <span class="tag">{_e(arch)}</span></h3>'
                f'<div class="body">{_e(text)}</div></div>'
            )
        turn_sections.append(
            f'<div class="rule turns">Turn {i} — object · steal · change-test</div>'
            f'<div class="grid">{"".join(cards)}</div>'
        )

    final_cards = []
    for d in debaters:
        did = d.get("id")
        final_cards.append(
            f'<div class="card"><h3>{_e(d.get("name"))} '
            f'<span class="tag">{_e(d.get("archetype"))}</span></h3>'
            f"{_ledger_block(finals.get(did, {}))}</div>"
        )

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Doppl Crucible Trace</title><style>{_CSS}</style></head>
<body>
<nav class="nav"><a href="../../index.html">&#8962; Agarden index</a>
<span class="sep">/</span><span>crucible spawncidence</span></nav>
<div class="wrap">
<header><h1>Crucible — belief-revision trace</h1>
<p>Spawner → openings → object/steal/change-test → finals + revision ledger → judge</p>
<div class="flow"><span>Spawn</span><span class="arrow">→</span><span>Open</span>
<span class="arrow">→</span><span>Argue</span><span class="arrow">→</span>
<span>Revise</span><span class="arrow">→</span><span>Judge</span></div></header>
<div class="prompt">{_e(trace.get("prompt",""))}</div>
<div class="rule spawner">Spawner — deciding the room</div>
{_spawner_block(trace.get("spawner_plan", {}) or {})}
<div class="rule openings">Openings</div>
<div class="grid">{"".join(opening_cards)}</div>
{"".join(turn_sections)}
<div class="rule finals">Finals + revision ledgers</div>
<div class="grid">{"".join(final_cards)}</div>
<div class="rule judge">Judge — scored the whole conversation</div>
{_verdict_block(trace.get("judge", {}) or {})}
</div></body></html>"""


def write_crucible_html(trace: dict[str, Any], path: str) -> str:
    out = render_crucible_html(trace)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    return path
