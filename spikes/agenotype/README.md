# Agenotype Spike — Fusion Demo

Parent agenomes → fusion judge → decision → critic → **breed child on blind spots** → offspring run. Then opens the trace in your browser.

> One mortal spike in the Doppl ecology. Meta-narrative + lineage logs live at the repo root (`../../`). See [`../../TREATISE.md`](../../TREATISE.md).

## First time only

```bash
cd spikes/agenotype
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add OPENROUTER_API_KEY
chmod +x demo
```

The `demo` runner also falls back to a shared repo-root `.venv` (`../../.venv`) if no spike-local venv exists.

## Run the demo (one command)

```bash
./demo
```

That's it. Runs 2 generations (parents + offspring), writes `fusion_trace.html`, opens it.

Custom prompt:

```bash
./demo --prompt "Your vague question here"
```

Terminal only, no browser:

```bash
./demo --no-open
```

## What happens

1. **Parent agenomes** — two Rule-of-Cool variants answer in parallel (Transfer Hunter × Feasibility Hawk)
2. **Fusion judge** — consensus, contradictions, clarifying questions, **blind spots**
3. **Decision** — grounded answer
4. **Critic** — scores it, asks what it glossed over
5. If critic fails → **breed a child agenome** on blind spots (not a prompt retry)
6. **Gen 2 offspring** — child answers with a primary mandate, critic again
7. **HTML opens** — full lineage + trace for the room / projector

Default prompt ("Room Vitals" for "a new room") is vague on purpose so Gen 1 usually fails and the bred offspring improves.

## Power-user flags

| Flag | Effect |
|------|--------|
| `--rounds 3` | More generations (offspring only breeds once in this spike) |
| `--no-html` | Skip HTML file |
| `--no-open` | Write HTML but don't open browser |
| `--mode official` | Also call OpenRouter's built-in Fusion API |

Reference: [OpenRouter Fusion](https://openrouter.ai/docs/guides/features/plugins/fusion)
