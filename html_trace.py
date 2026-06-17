"""Self-contained HTML trace for Fusion demo (panel → judge → decision → critic loop)."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def render_trace_html(trace: dict[str, Any]) -> str:
    return _render(trace)


def write_trace_html(path: Path, trace: dict[str, Any]) -> Path:
    path = path.resolve()
    path.write_text(render_trace_html(trace), encoding="utf-8")
    return path


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _list_items(items: list[str], css_class: str = "") -> str:
    if not items:
        return '<p class="empty">None surfaced.</p>'
    cls = f' class="{css_class}"' if css_class else ""
    return f"<ul{cls}>" + "".join(f"<li>{_esc(item)}</li>" for item in items) + "</ul>"


def _panel_cards(panel: list[dict[str, str]]) -> str:
    cards = []
    for i, entry in enumerate(panel):
        label = entry.get("label") or entry.get("model", f"Model {i + 1}")
        answer = entry.get("answer", "")
        agenome_id = entry.get("agenome_id")
        badge = "Agenome" if agenome_id else "Panel"
        badge_class = "badge-agenome" if agenome_id else "badge-panel"
        sub = f'<span class="agenome-id">{_esc(str(agenome_id))}</span>' if agenome_id else ""
        cards.append(
            f"""
            <article class="panel-card" style="--delay: {i}">
              <header>
                <span class="badge {badge_class}">{badge}</span>
                <h3>{_esc(label)}</h3>
                {sub}
              </header>
              <div class="body">{_esc(answer)}</div>
            </article>
            """
        )
    return "\n".join(cards)


def _judge_section(analysis: dict[str, Any]) -> str:
    if analysis.get("parse_error"):
        raw = analysis.get("raw_output") or analysis.get("raw_judge_output", "")
        return f'<pre class="raw-json">{_esc(raw)}</pre>'

    parts: list[str] = []

    questions = analysis.get("clarifying_questions") or []
    if questions:
        parts.append(
            f"""
            <section class="judge-block highlight">
              <h4>Clarifying questions</h4>
              {_list_items(questions, "questions")}
            </section>
            """
        )

    if analysis.get("consensus"):
        parts.append(
            f"""
            <section class="judge-block">
              <h4>Consensus</h4>
              {_list_items(analysis["consensus"])}
            </section>
            """
        )

    contradictions = analysis.get("contradictions") or []
    if contradictions:
        rows = []
        for c in contradictions:
            topic = _esc(str(c.get("topic", "Disagreement")))
            views = c.get("views") or []
            view_html = "".join(f"<li>{_esc(str(v))}</li>" for v in views)
            rows.append(
                f'<div class="contradiction"><strong>{topic}</strong><ul>{view_html}</ul></div>'
            )
        parts.append(
            f"""
            <section class="judge-block warn">
              <h4>Contradictions</h4>
              {"".join(rows)}
            </section>
            """
        )

    insights = analysis.get("unique_insights") or []
    if insights:
        rows = []
        for item in insights:
            src = _esc(str(item.get("from", "Model")))
            insight = _esc(str(item.get("insight", "")))
            rows.append(f"<li><em>{src}:</em> {insight}</li>")
        parts.append(
            f"""
            <section class="judge-block">
              <h4>Unique insights</h4>
              <ul>{"".join(rows)}</ul>
            </section>
            """
        )

    if analysis.get("blind_spots"):
        parts.append(
            f"""
            <section class="judge-block">
              <h4>Blind spots</h4>
              {_list_items(analysis["blind_spots"])}
            </section>
            """
        )

    direction = analysis.get("recommended_direction")
    if direction:
        parts.append(
            f"""
            <section class="judge-block direction">
              <h4>Provisional direction</h4>
              <p>{_esc(str(direction))}</p>
            </section>
            """
        )

    if not parts:
        parts.append(f'<pre class="raw-json">{_esc(json.dumps(analysis, indent=2))}</pre>')

    return "\n".join(parts)


def _agenome_card(agenome: dict[str, Any], role: str) -> str:
    personas = agenome.get("personas") or []
    mandate = agenome.get("primary_mandate") or []
    persona_html = _list_items([str(p) for p in personas])
    mandate_html = ""
    if mandate:
        mandate_html = f"""
        <section class="genome-mandate">
          <h5>Primary mandate</h5>
          {_list_items([str(m) for m in mandate], "questions")}
        </section>
        """
    return f"""
    <article class="genome-card">
      <header>
        <span class="badge badge-genome">{_esc(role)}</span>
        <h4>{_esc(str(agenome.get("name", agenome.get("id", "Agenome"))))}</h4>
        <span class="agenome-id">{_esc(str(agenome.get("id", "")))}</span>
      </header>
      <section>
        <h5>Personas</h5>
        {persona_html}
      </section>
      {mandate_html}
    </article>
    """


def _lineage_section(lineage: dict[str, Any]) -> str:
    parents = lineage.get("parents") or []
    mandate = lineage.get("mandate") or []
    child = lineage.get("child") or {}

    parent_cards = "".join(
        f'<div class="genome-parent">{_agenome_card(parent, f"Parent {i + 1}")}</div>'
        for i, parent in enumerate(parents)
    )
    child_card = f'<div class="genome-child">{_agenome_card(child, "Child")}</div>' if child else ""

    return f"""
    <section class="step step-lineage">
      <div class="step-header">
        <span class="step-num">♦</span>
        <div>
          <h2>Sexual reproduction — blind-spot breeding</h2>
          <p class="step-desc">Two parents fuse into a child agenome mandated to hunt what both missed.</p>
        </div>
      </div>
      <section class="judge-block highlight">
        <h4>Breeding mandate</h4>
        {_list_items([str(m) for m in mandate], "questions")}
      </section>
      <div class="genome-grid">
        <div class="genome-parents">{parent_cards}</div>
        <div class="fusion-glyph">× fuse →</div>
        {child_card}
      </div>
    </section>
    """


def _critic_section(critic: dict[str, Any], passed: bool) -> str:
    if not critic:
        return '<p class="empty">No critic run.</p>'

    if critic.get("parse_error"):
        raw = critic.get("raw_output", "")
        return f'<pre class="raw-json">{_esc(raw)}</pre>'

    verdict = str(critic.get("verdict", "unknown"))
    score = critic.get("score", "?")
    status_class = "pass" if passed else "fail"
    status_label = "PASS" if passed else "NEEDS REVISION"

    parts = [
        f"""
        <div class="verdict-banner {status_class}">
          <span class="verdict-label">{status_label}</span>
          <span class="verdict-score">Score: {_esc(str(score))}/10</span>
        </div>
        """
    ]

    scores = critic.get("scores") or {}
    if scores:
        rows = "".join(
            f'<div class="score-row"><span>{_esc(k.replace("_", " "))}</span><span>{_esc(str(v))}/10</span></div>'
            for k, v in scores.items()
        )
        parts.append(f'<div class="score-grid">{rows}</div>')

    if critic.get("strengths"):
        parts.append(
            f"""
            <section class="judge-block">
              <h4>Strengths</h4>
              {_list_items(critic["strengths"])}
            </section>
            """
        )

    if critic.get("weaknesses"):
        parts.append(
            f"""
            <section class="judge-block warn">
              <h4>Weaknesses</h4>
              {_list_items(critic["weaknesses"])}
            </section>
            """
        )

    if critic.get("clarifying_questions"):
        parts.append(
            f"""
            <section class="judge-block highlight">
              <h4>Critic clarifying questions</h4>
              {_list_items(critic["clarifying_questions"])}
            </section>
            """
        )

    fix = critic.get("what_would_make_this_pass")
    if fix:
        parts.append(
            f"""
            <section class="judge-block direction">
              <h4>To pass next round</h4>
              <p>{_esc(str(fix))}</p>
            </section>
            """
        )

    return "\n".join(parts)


def _offspring_round_block(round_data: dict[str, Any], is_last: bool) -> str:
    n = round_data.get("round", 2)
    passed = round_data.get("passed", False)
    final = round_data.get("final") or ""
    critic = round_data.get("critic") or {}
    lineage = round_data.get("lineage") or {}
    offspring = round_data.get("offspring") or {}
    agenome = offspring.get("agenome") or {}

    loop_arrow = ""
    if not is_last:
        loop_arrow = '<div class="connector loop">↻ next generation</div>'

    lineage_html = _lineage_section(lineage) if lineage else ""
    genome_card = _agenome_card(agenome, "Offspring") if agenome else ""

    return f"""
    <div class="generation generation-offspring" data-round="{n}">
      <div class="gen-header">
        <span class="gen-badge">Gen {n}</span>
        <span class="gen-offspring">offspring run</span>
        {"<span class='gen-pass'>✓ passed</span>" if passed else "<span class='gen-fail'>↻ revising</span>"}
      </div>

      {lineage_html}

      <div class="connector">↓</div>

      <section class="step step-offspring">
        <div class="step-header">
          <span class="step-num">1</span>
          <div>
            <h2>Child agenome answers</h2>
            <p class="step-desc">Bred to resolve blind spots — not a prompt retry.</p>
          </div>
        </div>
        {genome_card}
        <div class="final-card">{_esc(final)}</div>
      </section>

      <div class="connector">↓</div>

      <section class="step step-critic">
        <div class="step-header">
          <span class="step-num">2</span>
          <div>
            <h2>Critic — red team</h2>
            <p class="step-desc">Does the offspring answer its mandate?</p>
          </div>
        </div>
        <div class="judge-grid">{_critic_section(critic, passed)}</div>
      </section>
    </div>
    {loop_arrow}
    """


def _round_block(round_data: dict[str, Any], is_last: bool) -> str:
    if round_data.get("mode") == "offspring":
        return _offspring_round_block(round_data, is_last)

    n = round_data.get("round", 1)
    passed = round_data.get("passed", False)
    panel = round_data.get("panel") or []
    analysis = round_data.get("analysis") or {}
    final = round_data.get("final") or ""
    critic = round_data.get("critic") or {}

    loop_arrow = ""
    if not is_last:
        loop_arrow = '<div class="connector loop">♦ breed child on blind spots →</div>'

    return f"""
    <div class="generation" data-round="{n}">
      <div class="gen-header">
        <span class="gen-badge">Gen {n}</span>
        {"<span class='gen-pass'>✓ passed</span>" if passed else "<span class='gen-fail'>↻ breed offspring</span>"}
      </div>

      <section class="step step-panel">
        <div class="step-header">
          <span class="step-num">1</span>
          <div>
            <h2>Parent agenomes — parallel answers</h2>
            <p class="step-desc">Rule-of-Cool variants, same prompt, different lenses.</p>
          </div>
        </div>
        <div class="panel-grid">{_panel_cards(panel)}</div>
      </section>

      <div class="connector">↓</div>

      <section class="step step-judge">
        <div class="step-header">
          <span class="step-num">2</span>
          <div>
            <h2>Fusion judge</h2>
            <p class="step-desc">Compare, don't merge. Surface blind spots.</p>
          </div>
        </div>
        <div class="judge-grid">{_judge_section(analysis)}</div>
      </section>

      <div class="connector">↓</div>

      <section class="step step-final">
        <div class="step-header">
          <span class="step-num">3</span>
          <div>
            <h2>Decision</h2>
          </div>
        </div>
        <div class="final-card">{_esc(final)}</div>
      </section>

      <div class="connector">↓</div>

      <section class="step step-critic">
        <div class="step-header">
          <span class="step-num">4</span>
          <div>
            <h2>Critic — red team</h2>
            <p class="step-desc">Score the answer. Ask what it glossed over.</p>
          </div>
        </div>
        <div class="judge-grid">{_critic_section(critic, passed)}</div>
      </section>
    </div>
    {loop_arrow}
    """


def _rounds_html(trace: dict[str, Any]) -> str:
    rounds = trace.get("rounds") or []
    if rounds:
        blocks = []
        for i, r in enumerate(rounds):
            blocks.append(_round_block(r, is_last=(i == len(rounds) - 1)))
        return "\n".join(blocks)

    # Legacy single-round trace
    single = {
        "round": 1,
        "panel": trace.get("panel") or [],
        "analysis": trace.get("analysis") or {},
        "final": trace.get("final") or "",
        "critic": trace.get("critic") or {},
        "passed": trace.get("passed", False),
    }
    return _round_block(single, is_last=True)


def _render(trace: dict[str, Any]) -> str:
    prompt = trace.get("prompt", "")
    official = trace.get("official")
    generated = trace.get("generated_at") or datetime.now(timezone.utc).isoformat()
    total = trace.get("total_rounds") or len(trace.get("rounds") or [1])
    passed = trace.get("passed", False)
    outcome = "Passed critic" if passed else f"{total} round(s) — best attempt"

    official_block = ""
    if official:
        official_block = f"""
        <section class="step step-official">
          <div class="step-header">
            <span class="step-num">↔</span>
            <div>
              <h2>OpenRouter Fusion (comparison)</h2>
              <p class="step-desc">Same prompt, server-side — no critic loop.</p>
            </div>
          </div>
          <div class="final-card official">{_esc(official)}</div>
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fusion Trace — Room Vitals</title>
  <style>
    :root {{
      --bg: #0c0f14;
      --surface: #141a22;
      --surface2: #1a222d;
      --border: #2a3544;
      --text: #e8edf4;
      --muted: #8b9bb0;
      --panel: #3dd68c;
      --judge: #f0b429;
      --final: #5b9dff;
      --critic: #f87171;
      --accent: #c084fc;
      --warn: #f87171;
      --highlight: #fef08a;
      --pass: #3dd68c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "SF Pro Text", "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.55;
      min-height: 100vh;
    }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    header.hero {{ text-align: center; margin-bottom: 2rem; }}
    header.hero h1 {{ font-size: 1.75rem; font-weight: 650; margin: 0 0 0.35rem; }}
    header.hero p {{ color: var(--muted); margin: 0; font-size: 0.95rem; }}
    .outcome {{
      display: inline-block;
      margin-top: 0.75rem;
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
      background: rgba(192, 132, 252, 0.15);
      color: var(--accent);
    }}
    .prompt-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      white-space: pre-wrap;
    }}
    .prompt-card label {{
      display: block;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      margin-bottom: 0.5rem;
      font-weight: 600;
    }}
    .generation {{
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.25rem;
      margin-bottom: 0.5rem;
      background: rgba(20, 26, 34, 0.6);
    }}
    .gen-header {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1rem;
    }}
    .gen-badge {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      background: rgba(192, 132, 252, 0.2);
      color: var(--accent);
    }}
    .gen-pass {{ color: var(--pass); font-size: 0.85rem; font-weight: 600; }}
    .gen-fail {{ color: var(--judge); font-size: 0.85rem; font-weight: 600; }}
    .round-prompt {{
      margin-bottom: 1rem;
      font-size: 0.85rem;
    }}
    .round-prompt summary {{ cursor: pointer; color: var(--muted); }}
    .round-prompt pre {{
      margin-top: 0.5rem;
      padding: 0.75rem;
      background: var(--surface2);
      border-radius: 8px;
      font-size: 0.78rem;
      white-space: pre-wrap;
      color: #a8b8cc;
    }}
    .connector {{
      display: flex;
      justify-content: center;
      padding: 0.35rem 0;
      color: var(--muted);
      font-size: 1.1rem;
    }}
    .connector.loop {{
      color: var(--accent);
      font-weight: 600;
      font-size: 0.9rem;
      padding: 1rem 0;
    }}
    .step {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem 1.5rem 1.5rem;
    }}
    .step-header {{
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 1.25rem;
    }}
    .step-num {{
      flex-shrink: 0;
      width: 2rem;
      height: 2rem;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
    }}
    .step-panel .step-num {{ background: rgba(61, 214, 140, 0.15); color: var(--panel); }}
    .step-judge .step-num {{ background: rgba(240, 180, 41, 0.15); color: var(--judge); }}
    .step-final .step-num {{ background: rgba(91, 157, 255, 0.15); color: var(--final); }}
    .step-critic .step-num {{ background: rgba(248, 113, 113, 0.15); color: var(--critic); }}
    .step-official .step-num {{ background: rgba(192, 132, 252, 0.15); color: var(--accent); }}
    .step-header h2 {{ margin: 0; font-size: 1.05rem; font-weight: 600; }}
    .step-desc {{ margin: 0.2rem 0 0; color: var(--muted); font-size: 0.85rem; }}
    .panel-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    @media (max-width: 720px) {{ .panel-grid {{ grid-template-columns: 1fr; }} }}
    .panel-card {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
    }}
    .panel-card header {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .panel-card h3 {{ margin: 0; font-size: 0.9rem; font-weight: 600; }}
    .panel-card .body {{
      padding: 1rem;
      font-size: 0.88rem;
      white-space: pre-wrap;
      color: #c5d0de;
    }}
    .badge {{
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-weight: 700;
    }}
    .badge-panel {{ background: rgba(61, 214, 140, 0.2); color: var(--panel); }}
    .badge-agenome {{ background: rgba(192, 132, 252, 0.2); color: var(--accent); }}
    .badge-genome {{ background: rgba(192, 132, 252, 0.25); color: var(--accent); }}
    .agenome-id {{
      font-size: 0.7rem;
      color: var(--muted);
      font-family: ui-monospace, monospace;
    }}
    .panel-card header {{ flex-wrap: wrap; }}
    .gen-offspring {{
      color: var(--accent);
      font-size: 0.85rem;
      font-weight: 600;
    }}
    .step-lineage .step-num,
    .step-offspring .step-num {{
      background: rgba(192, 132, 252, 0.15);
      color: var(--accent);
    }}
    .genome-grid {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin-top: 1rem;
    }}
    .genome-parents {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }}
    @media (max-width: 720px) {{ .genome-parents {{ grid-template-columns: 1fr; }} }}
    .fusion-glyph {{
      text-align: center;
      font-size: 1.1rem;
      color: var(--accent);
      font-weight: 700;
      padding: 0.25rem 0;
    }}
    .genome-card {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem;
    }}
    .genome-card header {{
      margin-bottom: 0.75rem;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
    }}
    .genome-card h4, .genome-card h5 {{
      margin: 0 0 0.35rem;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      width: 100%;
    }}
    .genome-card h4 {{ font-size: 0.95rem; text-transform: none; color: var(--text); letter-spacing: 0; }}
    .genome-mandate {{ margin-top: 0.75rem; }}
    .judge-grid {{ display: grid; gap: 0.85rem; }}
    .judge-block {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.85rem 1rem;
    }}
    .judge-block h4 {{
      margin: 0 0 0.5rem;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
    }}
    .judge-block ul {{ margin: 0; padding-left: 1.15rem; }}
    .judge-block li {{ margin: 0.25rem 0; font-size: 0.9rem; }}
    .judge-block.highlight {{
      border-color: rgba(254, 240, 138, 0.35);
      background: rgba(254, 240, 138, 0.06);
    }}
    .judge-block.highlight h4 {{ color: var(--highlight); }}
    .judge-block.warn {{ border-color: rgba(248, 113, 113, 0.3); }}
    .judge-block.direction p {{ margin: 0; font-size: 0.95rem; }}
    .verdict-banner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      border-radius: 10px;
      margin-bottom: 0.85rem;
      font-weight: 700;
    }}
    .verdict-banner.pass {{
      background: rgba(61, 214, 140, 0.12);
      border: 1px solid rgba(61, 214, 140, 0.35);
      color: var(--pass);
    }}
    .verdict-banner.fail {{
      background: rgba(248, 113, 113, 0.1);
      border: 1px solid rgba(248, 113, 113, 0.35);
      color: var(--critic);
    }}
    .score-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.5rem;
      margin-bottom: 0.85rem;
    }}
    .score-row {{
      display: flex;
      justify-content: space-between;
      background: var(--surface2);
      padding: 0.45rem 0.65rem;
      border-radius: 6px;
      font-size: 0.8rem;
      text-transform: capitalize;
    }}
    .empty {{ color: var(--muted); font-size: 0.85rem; margin: 0; font-style: italic; }}
    .final-card {{
      background: linear-gradient(135deg, rgba(91, 157, 255, 0.08), rgba(192, 132, 252, 0.06));
      border: 1px solid rgba(91, 157, 255, 0.35);
      border-radius: 10px;
      padding: 1.25rem 1.35rem;
      white-space: pre-wrap;
      font-size: 0.92rem;
    }}
    .final-card.official {{
      border-color: rgba(192, 132, 252, 0.35);
    }}
    .raw-json {{
      background: #0a0d11;
      border-radius: 8px;
      padding: 1rem;
      font-size: 0.8rem;
      color: #a8b8cc;
      margin: 0;
      white-space: pre-wrap;
    }}
    footer {{
      margin-top: 2.5rem;
      text-align: center;
      color: var(--muted);
      font-size: 0.75rem;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>Fusion Trace</h1>
      <p>Parent agenomes → judge → critic → breed child on blind spots</p>
      <span class="outcome">{_esc(outcome)}</span>
    </header>

    <div class="prompt-card">
      <label>Live prompt from the room</label>
      {_esc(prompt)}
    </div>

    <div class="pipeline">
      {_rounds_html(trace)}
      {official_block}
    </div>

    <footer>Generated {_esc(generated)} · OpenRouter Fusion demo</footer>
  </div>
</body>
</html>
"""
