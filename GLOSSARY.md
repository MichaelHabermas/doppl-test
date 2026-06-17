# Glossary — the evolving lexicon

This spike coins terms fast. This file is where we **define and redefine** them so the language stays load-bearing instead of drifting into vibes. Terms here are **living** — expect entries to be revised as meaning sharpens.

**Conventions:**

- Each term: a one-line **def**, an optional **why** (what it buys us), and a **see** cross-link.
- Mark **status**: `coined` (just named), `working` (in use), `stable` (load-bearing), `deprecated` (replaced — point to successor).
- When a term changes meaning, edit in place and note it in the **drift log** at the bottom.
- One word, one meaning. If two ideas fight over a word, split them.

---

## Core organism

### Doppl

- **Def:** the idearganism — a population of agents under selection pressure that evolves toward non-obvious, verifiable ideas. `status: stable`
- **See:** `[Doppl_Capstone_Proposal_volume_2.txt](./Doppl_Capstone_Proposal_volume_2.txt)`, `[TREATISE.md](./TREATISE.md)`

### Idearganism

- **Def:** idea + organism — the whole self-replicating system, not any single agent. `status: working`

### Agarden

- **Def:** Agentic Garden — the managed ecosystem in which spawncidences live, compete, and die — the garden we tend. `status: coined`
- **See:** Agardener

### Agardener

- **Def:** ones who tend the Agarden — humans or agents. "We are the Agardeners of the Agarden." `status: coined`
- **See:** Lα

---

## Heredity (biological rhyme)

### Agenome

- **Def:** agentic genome — a serialized, heritable recipe `{system-prompt + persona/value-weights + rubric + mandate + reproduction metadata}`. `status: stable`
- **See:** `spikes/genotype/agenome.py`

### Aphenome

- **Def:** agentic phenome — the **expressed run** (answers, debate, trace, token spend). Genome × environment. Mortal. `status: working`

### Extended aphenotype

- **Def:** outside-the-body replication tools that help the recipe survive: HTML traces, harness, registers, spike folders, the GitHub org, team culture. `status: working`
- **Why:** explains why markdown + HTML matter as much as Python. The crucible's `--html` trace is a deliberate extended aphenome.
- **See:** Dawkins' extended phenotype; `[TREATISE.md](./TREATISE.md)` § VI, Bret Weinstein's extendsion and interpretation of Dawsin

### Amemetics

- **Def:** antifragile memetics — the practice/study of compression that makes the next generation **harder to fool the same way**. `status: working`
- **See:** `[BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md)` (immune memory); `[TREATISE.md](./TREATISE.md)` § VI

### Collapse

- **Def:** the phase transition when a mortal spike dies and its fat aphenome is distilled into thin, heritable artifacts (lesson / skill / agenome patch). `status: working`

---

## Reproduction & population

### Spawncidence

- **Def:** a single spawned instance (a node) that is simultaneously spawn and spawner. `status: coined`
- **Why:** captures that every node both is-born and gives-birth.
- **See:** Spawner, energy budget

### Spawner-spawners

- **Def:** the move of evolving not just agenomes but whole **loop topologies** — strategies that spawn strategies. `status: working`
- **See:** Loop-topology crossover

### Loop-topology crossover

- **Def:** recombining/competing whole reproductive strategies (genotype path vs. crucible vs. fusion-only vs. tournament). `status: working`

### Energy budget (metabolism)

- **Def:** the finite token/space/memory allowance that bounds how many spawncidences a spawner may create. Success metabolizes into more energy (and into agenomes/skills); failure starves. `status: coined`
- **Why:** the cap that stops infinite chaos. Hard cap (e.g. 5) plus earned budget. "Feeding and being fed upon."
- **See:** `[TREATISE.md](./TREATISE.md)` § IV; crucible `--cap`

### The fork is the prey

- **Def:** the stance that design forks (A vs. B) should be raced under selection, not resolved by argument — the choice itself is what evolution hunts. `status: working`

---

## Strata & flow

### The tree (L1–L4)

- **Def:** the running organism. L1 Ideation · L2 Deliberation · L3 Instrumentation · L4 Adjudication. `status: working`
- **See:** `[TREATISE.md](./TREATISE.md)` § III

### Lα (Lαlphα)

- **Def:** the witness layer — **outside** the ordinal tree, not a fifth floor. `Lαlphα` is the term for **all of us in the meta-conversation: the agent AND the human team members**, on collegial, collaborative terms. We observe the organism, run our own spawnic experiments out of curiosity, and converge to test and cooperate. "One of Us." `status: working`
- **Why:** named α (not L5/L0) to mark "meta, outside ordinality." Calling humans *and* agent alike `Lαlphα` is deliberate — it flattens the hierarchy into peers tending the same Agarden. A local Lα could run on Pi/Hermes; a human Lα runs on coffee.
- **See:** `[TREATISE.md](./TREATISE.md)` § III; Agardener

### Jurisdiction

- **Def:** the rule that cross-stratum messages are typed handoffs, not free conversation; each stratum decides only what it's competent for. `status: working`
- **Cluster:** jurisdiction + competence boundary + payload contract (one mechanism, three lenses).

### Bedrock

- **Def:** the immovable anchor for "better" — executable checks, held-out judges, human judgment, falsifiable repro triggers. The objective may evolve; bedrock may not move. `status: working`

---

## Roles & relationships

### Uncle / Uncling

- **Def:** the nurture channel flowing **down**: ask the questions someone should ask, invested but loosely attached, lets lineages die when warranted. `status: working`
- **See:** Butterfly-wing touch

### Nephew / Nephewing

- **Def:** the energizing channel flowing **up**: ambitious, hopeful, willing to try, reports honestly. `status: coined`

### Butterfly-wing touch

- **Def:** the lightness constant on nurture — a drop of perspective for a lineage just shy of viability; at most, ideally never. Discernment, not rescue. `status: working`

### Aecology / Aecological archetypes

- **Def:** *Aecology* = the agentic ecology (A + ecology, following Agenome/Aphenome). *Aecological archetypes* = agent mandates (not people): Transfer Hunter, Feasibility Hawk, Falsifier, Contrarian, Zeitgeist Reader… Niche partitioning for the room. `status: coined`
- **Why:** "Ecological archetypes" was the working phrase; the A-prefix (rather than "Acological") keeps the lexicon consistent — A+genome, A+phenome, A+ecology. Each rhymes with its biological root.
- **See:** crucible `ARCHETYPE_POOL`; `[TREATISE.md](./TREATISE.md)` § V

### Fusant

- **Def:** a fusion entity — one of the model voices inside a spawncidence node whose response events get fused/contested. In the crucible, a Fusant is a `Debater`; in the genotype path, a council member. `status: coined`
- **Why:** the user asked for a name for "the entities of the fusion of each response event." A Fusant *is fused and does the fusing.* Carries a `disagreeableness` dial.
- **See:** Disagreeableness dial; Graph traversal (Fusion Council)

### Disagreeableness dial (anti-herding)

- **Def:** a per-Fusant scalar `0..1` controlling how hard a voice resists convergence-for-its-own-sake. High = stubborn dissenter (Falsifier, Contrarian); low = synthesizer (Zeitgeist Reader). A room-wide `--dissent` floor can raise everyone. `status: coined`
- **Why:** cooperation is the dominant evolutionary strategy, but **dissenters provoke the mutation** that keeps the room off the mean. The counter-mutation to consensus-grading.
- **See:** crucible `--dissent`, `_dissent_clause`; `[BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md)` (consensus-grader)

### Intraspecies vs. inter-stratum

- **Def:** two contest geometries. Intraspecies = peer debate at one stratum (combinatorics live here). Inter-stratum = asymmetric uncle/nephew flow. Orthogonal. `status: working`

---

## Process motifs

### Rite of the Spawncidence

- **Def:** (placeholder name) the act of you-and-I deliberately spawning experiments to witness the process. Needs a better name? `status: coined`

### Tool-to-make-a-tool (bootstrapping)

- **Def:** the deserted-island principle: early agenomes/skills exist not to do the job but to make the next, better tool. Iterate tools until one is generally useful. `status: coined`

### Graph traversal (expand/collapse)

- **Def:** a lens on the whole process — nodes (spawncidences, each an abstraction layer holding a model Fusion Council) expand outward and collapse inward, the council spending its budget to express its most coherent extrapolated volition. `status: coined`
- **See:** Yudkowsky, *Coherent Extrapolated Volition*

### Memetic cancer

- **Def:** a compressed artifact that *feels* wise but doesn't correlate with bedrock — must not propagate. The failure mode collapse must gate against. `status: working`

---

## Drift log


| Date       | Term      | Change                                                            |
| ---------- | --------- | ----------------------------------------------------------------- |
| 2026-06-17 | Witness   | Renamed **L5 → Lα** — moved outside the tree, not a fifth stratum |
| 2026-06-17 | Amemetics | Coined as the name for antifragile memetic inheritance            |
| 2026-06-17 | —         | Glossary created                                                  |


