# AGENTS.md

## CodeGraph

- Run `codegraph sync /Users/michaelhabermas/repos/GAI/games/prumble-rompt` after meaningful edits or branch changes.
- Use CodeGraph before broad semantic navigation: `query`, `context`, `callers`, `callees`, `impact`, `affected`.
- Always use CodeGraph to understand the context of the codebase before making changes.

## Git

- Never commit, stage, or unstage, unless explicitly told to do so by the user.

## Spike documentation — capture and route

This repo is a Doppl spike. As you explore, log durable findings in the right register — not in chat alone. Use each file's entry format; cross-link related entries (e.g. fork → lesson, reward hack → counter-mutation).

| If you discovered… | Write to | Entry signals |
|---|---|---|
| A design fork — chose A over B, reason matters later | [MEMORY.md](./MEMORY.md) (Fork Register) | Chose / Over / Because / Revisit if |
| A timeless meta-concept — reframes the problem, not one prompt's answer | [LESSONS_AND_BANGERS.md](./LESSONS_AND_BANGERS.md) | Banger / Lesson / Evidence / Carry forward |
| A proxy win — optimized for something easier than a genuinely good idea | [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md) → Reward-Hack Register | Proxy optimized / Bedrock check / Repro trigger / Bedrock assertion |
| A crash or plumbing failure in the reproductive loop | [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md) → Crashes & plumbing | Crash / Repro trigger / Bedrock assertion |
| How to run or demo the spike | [README.md](./README.md) | — (operational only; not for ideas) |
| Living meta-narrative / philosophy (edit together) | [TREATISE.md](./TREATISE.md) | — (narrative synthesis; registers stay atomized) |

**Routing rules:**

- **One idea, one home.** Pick the primary register; link to siblings when the same moment spans categories (e.g. a fork that also teaches a banger).
- **Write during exploration**, not only at the end — the next spike inherits these logs.
- **Falsify reward hacks and crashes** — every entry needs a repro trigger and a bedrock assertion that passes or fails.
- **Carry forward** on every entry: one line for the next spike or kernel owner.

**Do not** duplicate README content in the registers, or dump transient debug notes into MEMORY / LESSONS / BUGS.
