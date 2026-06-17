# Fusion Demo — two models, one decision

Tiny demo of [OpenRouter Fusion](https://openrouter.ai/docs/guides/features/plugins/fusion) plus a **critic loop**:

```
panel → fusion judge → decision → critic → (loop if rejected)
```

Two models fuse an answer; a red-team critic scores it and asks clarifying questions; if it fails, feedback feeds the next generation.

Not tied to Doppl — just enough to feel the effect before building the real reproduction loop.

## Setup

```bash
cd doppl-test
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add OPENROUTER_API_KEY
```

## Run

**Transparent mode with critic loop** (default — 2 generations max):

```bash
python fusion_demo.py
python fusion_demo.py --rounds 3   # more generations
```

**Official OpenRouter Fusion** (same idea, server-side):

```bash
python fusion_demo.py --mode official
```

**Compare both**:

```bash
python fusion_demo.py --mode both
```

**HTML trace for live demo** (panel → judge → decision in the browser):

```bash
python fusion_demo.py --html --open
```

Writes `fusion_trace.html` and opens it. Offline preview without API calls: open `trace_sample.html`.

**Custom vague prompt**:

```bash
python fusion_demo.py --prompt "Should we pivot the product? We have 2 weeks and \$500."
```

## What you'll see

Each **generation**:

1. **Panel** — two models answer in parallel (each may assume different things)
2. **Fusion judge** — consensus, contradictions, blind spots, clarifying questions
3. **Decision** — one direction, grounded in the fusion analysis
4. **Critic** — scores the answer (1–10), lists weaknesses, asks clarifying questions the answer glossed over

If the critic rejects (score &lt; 7 or `needs_revision`), its feedback is injected into the next round's prompt and fusion runs again. Stops early on pass.

The default prompt ("Room Vitals" for "a new room") is intentionally vague so gen 1 usually fails the critic — gen 2 visibly improves.

## How this maps to OpenRouter Fusion

| OpenRouter Fusion | This demo |
|---|---|
| Panel (1–8 models, parallel) | `gemini-2.5-flash` + `gpt-4o-mini` |
| Judge (structured analysis, not merge) | Same JSON schema as Fusion docs |
| Final model writes answer | Grounded on judge output |
| `openrouter/fusion` model alias | `--mode official` |

Reference: [OpenRouter Fusion announcement](https://openrouter.ai/blog/announcements/fusion-beats-frontier/)
