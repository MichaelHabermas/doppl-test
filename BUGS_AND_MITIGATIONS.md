# Reward-Hack Register

This spike stress-tests Doppl’s evolutionary loop. The dangerous failures here aren’t mostly stack traces — they’re **proxy wins**: moments the system (or we) optimized for something easier than “a genuinely good idea.”

Log each one so the next spike inherits the counter-mutation. Every entry must be **falsifiable**: a repro trigger you can re-run and a bedrock assertion that passes or fails.

## Entry format

### [short name] — YYYY-MM-DD

- **Proxy optimized:** what we were accidentally selecting for
- **Bedrock check:** what caught it (executable test, held-out critic, human judgment, cost telemetry, etc.)
- **Symptom:** what we observed (one sentence)
- **Counter-mutation:** what we changed so it can’t recur
- **Repro trigger:** the one command, prompt, or config that reliably surfaces the proxy win again
- **Bedrock assertion:** the pass/fail check that proves the counter-mutation held
- **Carry forward:** one line for the next spike/kernel owner

### Critic-surface pass — 2026-06-16

- **Proxy optimized:** fluent, confident answer on a vague prompt
- **Bedrock check:** adversarial critic scores + forced Gen 2
- **Symptom:** Gen 1 reads well in the room but fails rubric
- **Counter-mutation:** default “Room Vitals” prompt stays vague; trace HTML makes critic failure visible
- **Repro trigger:** `./demo` (no flags — default vague prompt)
- **Bedrock assertion:** Gen 1 critic fails; `fusion_trace.html` shows breeding mandate + child genome; Gen 2 scores higher
- **Carry forward:** breed on blind spots, not on “sounds good” — see LESSONS_AND_BANGERS

## Crashes & plumbing

This spike runs a test of the reproductive loop. The reproductive loop is the core of Doppl’s evolutionary loop, and it’s the part that’s most likely to crash.

Log each one so the next spike inherits the counter-mutation. Same falsifiability contract: repro trigger + bedrock assertion.

### Entry format

#### [short name] — YYYY-MM-DD

- **Crash:** what we observed (one sentence)
- **Counter-mutation:** what we changed so it can’t recur
- **Repro trigger:** the one command or sequence that used to crash
- **Bedrock assertion:** the pass/fail check that proves the fix held (e.g. exits 0, writes trace)
- **Carry forward:** one line for the next spike/kernel owner
