#!/usr/bin/env python3
"""Build a root-level index.html — the single, findable entry point into every
run that currently exists across all Agardens and spawncidences.

It scans `spikes/*/` for trace HTML files, enriches each with its sibling
`*.trace.json` when present (prompt, judge score/verdict, roster), and writes a
navigable hub with a reusable side menu. Mortal traces come and go; this index is
regenerated on demand:

    python build_index.py            # write index.html
    python build_index.py --open     # write + open in browser

Run it after a spike emits a new HTML trace (or wire it into a spike's demo).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import webbrowser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SPIKES_DIR = ROOT / "spikes"
INDEX_PATH = ROOT / "index.html"

_CSS = """
:root{--bg:#0b0e13;--surface:#141a22;--surface2:#1b232e;--border:#2a3544;
--text:#e8edf4;--muted:#8b9bb0;--accent:#c084fc;--green:#3dd68c;--yellow:#f5c451;--red:#fb7185;}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);line-height:1.55;
font-family:"SF Pro Text","Segoe UI",system-ui,sans-serif;}
.layout{display:grid;grid-template-columns:240px 1fr;min-height:100vh;}
aside{background:var(--surface);border-right:1px solid var(--border);padding:1.5rem 1rem;
position:sticky;top:0;height:100vh;overflow:auto;}
aside h2{font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;color:var(--accent);margin:0 0 .8rem;}
aside .spike{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
margin:1rem 0 .35rem;}
aside a{display:block;color:var(--text);text-decoration:none;font-size:.85rem;padding:.25rem .4rem;
border-radius:6px;}
aside a:hover{background:var(--surface2);color:var(--accent);}
main{padding:2.5rem 2rem 5rem;max-width:900px;}
h1{font-size:1.7rem;margin:0 0 .3rem;}
.sub{color:var(--muted);margin:0 0 2rem;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;
padding:1.1rem 1.25rem;margin-bottom:1rem;}
.card a.title{color:var(--text);text-decoration:none;font-weight:650;font-size:1.05rem;}
.card a.title:hover{color:var(--accent);}
.row{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.4rem 0;}
.pill{font-size:.72rem;padding:.18rem .55rem;border-radius:999px;background:var(--surface2);
border:1px solid var(--border);color:var(--muted);}
.pill.pass{color:var(--green);border-color:#1f5b3a;}
.pill.fail{color:var(--yellow);border-color:#5b4a1f;}
.pill.herded{color:var(--red);border-color:#5b1f28;}
.prompt{color:var(--muted);font-size:.88rem;margin:.4rem 0 0;}
.meta{color:var(--muted);font-size:.76rem;margin-top:.5rem;}
.empty{color:var(--muted);font-style:italic;}
"""


def _now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def _find_sibling_json(html_path: Path) -> Path | None:
    """Best-effort pairing of a trace HTML with its JSON record."""
    stem = html_path.stem  # e.g. crucible_trace_rerun
    candidates = [
        html_path.with_suffix(".json"),
        html_path.with_suffix(".trace.json"),
    ]
    for marker in ("crucible_trace_", "fusion_trace_", "trace_", "_trace"):
        if marker in stem:
            tag = stem.replace("crucible_trace_", "").replace("fusion_trace_", "")
            tag = tag.replace("trace_", "").replace("_trace", "").strip("_-")
            if tag:
                candidates.append(html_path.with_name(f"{tag}.trace.json"))
                candidates.append(html_path.with_name(f"{tag}.json"))
    for c in candidates:
        if c.exists():
            return c
    return None


def _load_record(json_path: Path | None) -> dict[str, Any]:
    if not json_path:
        return {}
    try:
        with open(json_path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _esc(value: Any) -> str:
    import html as _html

    return _html.escape(str(value if value is not None else ""))


def _card(html_path: Path, record: dict[str, Any]) -> str:
    rel = html_path.relative_to(ROOT).as_posix()
    anchor = rel.replace("/", "__")
    mtime = dt.datetime.fromtimestamp(html_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    judge = record.get("judge", {}) or {}
    prompt = str(record.get("prompt", "")).strip().replace("\n", " ")
    if len(prompt) > 200:
        prompt = prompt[:200] + "…"

    pills = []
    score = judge.get("score")
    verdict = str(judge.get("verdict", ""))
    if score is not None:
        klass = "pass" if verdict.startswith("pass") else "fail"
        pills.append(f'<span class="pill {klass}">{_esc(score)}/10 · {_esc(verdict or "?")}</span>')
    consensus = str(judge.get("consensus_quality", ""))
    if consensus:
        cclass = "herded" if consensus == "herded" else ""
        pills.append(f'<span class="pill {cclass}">consensus: {_esc(consensus)}</span>')
    debaters = record.get("debaters", []) or []
    if debaters:
        names = ", ".join(str(d.get("name", "")) for d in debaters)
        pills.append(f'<span class="pill">{_esc(len(debaters))} fusants: {_esc(names)}</span>')

    prompt_html = f'<p class="prompt">{_esc(prompt)}</p>' if prompt else ""
    return (
        f'<div class="card" id="{anchor}">'
        f'<a class="title" href="{rel}">{_esc(html_path.name)}</a>'
        f'<div class="row">{"".join(pills)}</div>'
        f"{prompt_html}"
        f'<p class="meta">{rel} · updated {mtime}</p>'
        "</div>"
    )


def collect() -> dict[str, list[tuple[Path, dict[str, Any]]]]:
    by_spike: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    if not SPIKES_DIR.exists():
        return by_spike
    for spike_dir in sorted(p for p in SPIKES_DIR.iterdir() if p.is_dir()):
        traces = sorted(
            (p for p in spike_dir.glob("*.html") if "trace" in p.name.lower()),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not traces:
            continue
        rows = [(t, _load_record(_find_sibling_json(t))) for t in traces]
        by_spike[spike_dir.name] = rows
    return by_spike


def render(by_spike: dict[str, list[tuple[Path, dict[str, Any]]]]) -> str:
    side, body = [], []
    total = 0
    for spike, rows in by_spike.items():
        side.append(f'<div class="spike">{_esc(spike)}</div>')
        body.append(f'<h2 style="margin-top:2rem">{_esc(spike)}</h2>')
        for html_path, record in rows:
            anchor = html_path.relative_to(ROOT).as_posix().replace("/", "__")
            side.append(f'<a href="#{anchor}">{_esc(html_path.name)}</a>')
            body.append(_card(html_path, record))
            total += 1

    if not by_spike:
        body.append(
            '<p class="empty">No trace HTML found yet. Run a spike with <code>--html</code> '
            "(e.g. <code>cd spikes/crucible && ./demo --html</code>), then rebuild this index.</p>"
        )

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Doppl Agarden — run index</title><style>{_CSS}</style></head>
<body><div class="layout">
<aside><h2>Agarden</h2><a href="#">All runs ({total})</a>{"".join(side)}
<div class="spike">docs</div>
<a href="TREATISE.md">TREATISE.md</a><a href="GLOSSARY.md">GLOSSARY.md</a>
</aside>
<main><h1>Doppl Agarden — run index</h1>
<p class="sub">Every trace that currently exists across spawncidences. Mortal artifacts;
regenerate with <code>python build_index.py</code>. Generated {_now()}.</p>
{"".join(body)}
</main></div></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Agarden run index")
    parser.add_argument("--open", action="store_true", help="Open index.html after writing")
    args = parser.parse_args()

    by_spike = collect()
    INDEX_PATH.write_text(render(by_spike), encoding="utf-8")
    count = sum(len(v) for v in by_spike.values())
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)} — {count} run(s) across {len(by_spike)} spike(s).")
    if args.open:
        webbrowser.open(INDEX_PATH.resolve().as_uri())


if __name__ == "__main__":
    main()
