# Lessons and Bangers

Meta-concepts from exploring the [Doppl Capstone Proposal](./Doppl_Capstone_Proposal_volume_2.txt) in this spike.

These are not commandments — interesting ideas that surfaced while we poked at the problem and are worth bringing forward. The point is the *frame*, not a better answer to one prompt. Pair with [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md) for what we accidentally optimized.

## Entry format

### [short name] — YYYY-MM-DD

- **Banger:** the meta-concept — how we see the problem differently, what's cool about it
- **Lesson:** what that implies when we build (one line; optional if the banger stands alone)
- **Evidence:** where it showed up in this spike (demo moment, file, generation)
- **Carry forward:** one line for the next spike / Doppl proper

## Entries

### Breed on blind spots — 2026-06-16

- **Banger:** Breed the child agenome on blind spots, not on critic feedback.
- **Lesson:** The fusion judge's `blind_spots` and `clarifying_questions` are the breeding target — not "here's what you got wrong, try again."
- **Evidence:** `extract_breeding_mandate()` in `agenome.py`; Gen 2 offspring runs with `primary_mandate`, not an injected retry prompt.
- **Carry forward:** Reproduction is epistemic-gap-directed — offspring exist to see what parents couldn't.

### Chromosomalize Rule of Cool — 2026-06-16

- **Banger:** Chromosomalize Rule of Cool into a JSON agenome.
- **Lesson:** RoC isn't a chat trick — it's a serializable genome: personas, ranking rubric, output contract, mandate. Heritable. Crossover-able.
- **Evidence:** `Agenome` dataclass + seed variants in `agenome.py`; HTML trace renders parent/child genomes as first-class objects.
- **Carry forward:** Generation-0 is a genome file, not a skill invocation. Population dynamics plug into schema, not prompts.

### Genotype over transcript — 2026-06-16

- **Banger:** Put evolution in the genotype, not the transcript. When something fails scrutiny, don't patch the answer — breed a new agent. Selection pressure belongs on *who* is thinking, not *how long* they're allowed to talk.
- **Lesson:** On critic fail, `breed_child()` splices parents and mutates on `blind_spots ∪ clarifying_questions` — not on critic tone or "try harder."
- **Evidence:** Gen 1 (Transfer Hunter × Feasibility Hawk → fusion judge → critic) fails Room Vitals; offspring answers via `primary_mandate` in `agenome.py`; `fusion_trace.html` shows parent genomes, breeding mandate, and child genome.
- **Carry forward:** Default reproduction operator is genomic splice, not transcript retry. **Revisit:** crucible path as competing spawner — see [Parallel spawners, not fork resolution](./MEMORY.md#parallel-spawners-not-fork-resolution--2026-06-16).

### The fork is the prey — 2026-06-16

- **Banger:** You're not wavering on genotype vs. crucible — you're noticing that **the fork itself is the prey.** The scaffold is supposed to be under selection pressure, including *which scaffold*.
- **Lesson:** Don't prematurely resolve design forks in MEMORY; race competing loop topologies under shared bedrock and let selection pressure flow up into "what does better mean?"
- **Evidence:** Design discussion — genotype spike vs. belief-revision crucible as competing hypotheses about improvement for cheap models.
- **Carry forward:** The search for better definitions of better *is* the capstone apex bet — not a side debate to close before building.

### Loop-topology crossover — 2026-06-16

- **Banger:** **Spawning-Spawners** — not just agenome crossover, but **loop-topology crossover.** Different reproductive strategies (genotype path, crucible path, fusion-only, tournament) compete under the same environment.
- **Lesson:** Every node is spawn *and* spawner by intent: L1 spawns ideas, L2 spawns L1 configs, L3 spawns L2 runs, L4 spawns L3 instrument rounds. Life flows up (artifacts) and down (pressure + nurture).
- **Evidence:** Design discussion; maps to capstone "reproduction by Fusion" at agenome *and* output levels — extended to whole loop topologies.
- **Carry forward:** Serialize spawner genotypes: `{loop topology + judge contracts + reproduction operator + energy budget}`.

### Explore the madness, cap the combinatorics — 2026-06-16

- **Banger:** **Get crazy inside the constitution.** Explore the madness, but cap the combinatorics. Madness lives inside each stratum; restraint lives at the borders.
- **Lesson:** Hard limits make meta-level runnable: max strata (3–4 + witness), max parallel spawners, token caps, mortal projects, bedrock anchor that cannot move.
- **Evidence:** Design discussion — "beyond four levels lies madness, or money/time/intelligence we can't afford."
- **Carry forward:** Constitution before combinatorics; metabolism is the sanity rail, not a constraint to apologize for.

### Jurisdiction — 2026-06-16

- **Banger:** Cross-stratum communication is **jurisdiction**, not conversation. (Concept cluster: jurisdiction + competence boundary + payload contract — one boundary mechanism, three lenses; **jurisdiction** is the preferred handle when naming things in code.)
- **Lesson:** Each stratum struggles within its domain. L1–L2 argue about ideas and *how* to produce them; L3–L4 argue about *what we test* and *whether it passed*. Cross-stratum = typed handoffs only.
- **Evidence:** Design discussion — "level threes and fours can't talk about everything."
- **Carry forward:** Up = artifacts get abstract; down = pressure gets concrete. No free chat across strata.

### Stratified organism (L1–L4 + witness) — 2026-06-16

- **Banger:** Four strata + a **witness outside the tree** — blind ideas feeling around a **meta-phant.**
- **Lesson:**
  - **L1 Ideation** — What's the idea? (agenomes, crucible debaters)
  - **L2 Deliberation** — Should we? What does "better" mean *for doing this*? (spawner-spawners, loop topologies)
  - **L3 Instrumentation** — What are we testing? (harness, rubrics, energy accounting)
  - **L4 Adjudication** — Did it pass? Who gets energy? (bedrock, held-out, pruning)
  - **L5 Witness** — Not in the tree during the run. Watches, sifts lessons, asks "does this lesson make sense?" Registers, cron-on-repos, human + RoC reframe. Communicates *slowly* — through culture, not real-time chat with L1.
- **Evidence:** Design discussion; proto-L5 already exists as `LESSONS_AND_BANGERS.md`, `MEMORY.md`, `BUGS_AND_MITIGATIONS.md`.
- **Carry forward:** L4 judges runs; L5 judges lessons. RoC as seed-uncle passes through every level as reframing instinct, not breeding-loop participant.

### Spawn and nurture — 2026-06-16

- **Banger:** Pure spawn-without-nurture is **oviparous abandon.** Life flows in two directions: **spawn and nurture**, not spawn alone.
- **Lesson:** Two channels between every stratum: **Nurture** (budget, mandate, cool-uncle questions — friction in service of success) and **Judgment** (pass/fail, starve, prune, bedrock). Authoritative parenting, not authoritarian (L4 only) or permissive (L1 chaos).
- **Evidence:** Design discussion — snake metaphor; "if parents only judged you" vs. "if they only let you do what you want."
- **Carry forward:** Down = nurturing with intent; up = maturation signal (what did you become?).

### Uncle the shit out of it — 2026-06-16

- **Banger:** The nurturing channel is **Uncle the shit out of it** — supportive, not blindly encouraging. Ask the questions somebody should ask: "You want this job and this lifestyle — will that job get you that lifestyle?" Easy to talk to, invested, not forcing one path. Care enough to ask before it's too late.
- **Lesson:** At every level, **down = uncle** (questions, nurture, loose attachment) and **up = nephew** (ambitious, hopeful, youthful, wants to try). Different relationship going down than going up. Higher levels "uncle" lower levels into self-sufficiency — not "mommy's little boy" attachment that creates bad friction.
- **Evidence:** Design discussion; RoC skill as generation-0 cool uncle / seed reframer.
- **Carry forward:** Bake uncle-channel as first-class ops — possibly its own LLM role per stratum, distinct from judge and from ideation agents.

### Mortal projects, immortal lineage — 2026-06-16

- **Banger:** **Projects within projects** — collapsible, mortal. **Lineage log survives; the organism doesn't.** Pruning isn't failure — it's **metabolism.** Dying isn't bad; mortality is what makes all this possible.
- **Lesson:** Spike repos mayfly: proliferate, run experiments (discussion *or* code), leave trace, collapse to lessons/alleles/memes, die. Possible future: org-owned GitHub account where L4 spawns real spike projects; cron witness reads repos and kicks lessons up. You don't need to keep every repo — what's birthed is the lesson.
- **Evidence:** Design discussion — "I don't need to continue for the DNA to exist"; weak lineages go dark (capstone) extended to whole experimental lineages.
- **Carry forward:** Shared harness, mortal experiments; registers are the compressed genome that outlives any single spike folder.

### Agenome, Aphenome, extended aphenotype — 2026-06-16

- **Banger:** **Genome → Agenome. Phenome → Aphenome. Extended aphenotype.** Culture is extended phenotype — fast adaptation when genetic evolution is too slow (Dawkins / Weinstein framing).
- **Lesson:**
  - **Agenome** — heritable recipe (JSON genome, spawner topology)
  - **Aphenome** — expressed run (answers, debate, trace) — genome × environment
  - **Extended aphenotype** — outside-the-body replication tools: `fusion_trace.html`, harness, registers, spike folders, GitHub org, team process
  - **Culture / witness** — memetic layer; RoC + registers curate what replicates
  - This conversation itself may be genotype trying to express and survive
- **Evidence:** Design discussion; markdown registers as proto-extended phenotype; capstone "fitness function evolves itself" with bedrock anchor.
- **Carry forward:** Levels above agenome mutate *cultural machinery* (rubrics, harnesses, norms) — not prompt tokens alone.

### Cambrian explosion, not monoculture — 2026-06-16

- **Banger:** Explore the **Cambrian explosion of ideas** — diversity is strength. Don't always collapse to a single species. Mosquitoes and moles matter; so do apex predators (cheetah, orca, great white — stable strategies that haven't changed much for a reason). Learn from all; **sift for what's strong and interesting**, not what's loudest.
- **Lesson:** Witness sifts competing lessons across mortal spikes. Convergence is around survivability mechanics (breathing air, drinking water) — shared bedrock — not identical loop topologies. Anti-regression-to-mean: mutation, parallel mortal spikes, uncle-channel protecting risky lineages long enough to test, judgment pruning before mode collapse.
- **Evidence:** Design discussion — meta-phant / five blind ideas; many species, one ecology.
- **Carry forward:** Selection finds apex strategies per problem class; ecology preserves diversity of exploration.

### Belief-revision crucible — 2026-06-16

- **Banger:** Don't build "a discussion" — build a **belief-revision crucible** where the first-class artifact is the **delta** (revision ledger: what I held, what changed, what evidence moved me, what I still reject).
- **Lesson:** Fixed turn protocol with mandatory moves (objection, concession-or-rebuttal, steal-one-point). Judge scores final idea + revision quality + unresolved tension — not rhetorical victory. Competing L2 spawner to genotype path.
- **Evidence:** Design discussion — cheap models need structure, not open-ended chat; crucible vs. fusion-only as loop-topology fork.
- **Carry forward:** Sibling spike candidate; race under shared L3 harness + L4 bedrock — see [Parallel spawners](./MEMORY.md#parallel-spawners-not-fork-resolution--2026-06-16).
