# Fork Register

This spike explores ideas from the [Doppl Capstone Proposal](./Doppl_Capstone_Proposal_volume_2.txt). This file is the **lineage log**: not every note, but every fork — where we chose one path over another, and why.

**Write here when:** a design choice could reasonably have gone another way, and the reason matters later.

**Write elsewhere:**

- Timeless insight → [LESSONS_AND_BANGERS.md](./LESSONS_AND_BANGERS.md)
- Proxy win / reward hack → [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md)

## Entry format

### [fork name] — YYYY-MM-DD

- **Chose:** what we committed to
- **Over:** what we set aside (be specific)
- **Because:** the constraint, observation, or bet that tipped the scale
- **Revisit if:** what would make us reopen this fork
- **Spirit note:** one line on intent — what we were protecting or optimizing for

## Entries

### Breed on blind spots, not critic feedback — 2026-06-16

- **Chose:** genomic reproduction — `breed_child()` splices parents and mutates on `blind_spots ∪ clarifying_questions`; offspring answers via `primary_mandate`
- **Over:** transcript retry — feeding critic scores or “try harder” back into the same agent’s prompt
- **Because:** critic feedback optimizes for fluency and rubric-surface pass, not coverage of what fusion actually missed; selection pressure belongs on *who* is thinking, not *how long* they talk
- **Revisit if:** offspring quality plateaus while blind-spot signal stays rich — may need a second reproduction operator or richer genotype
- **Spirit note:** evolution in the genotype, not the transcript — see [Genotype over transcript](./LESSONS_AND_BANGERS.md#genotype-over-transcript--2026-06-16)

### Parallel spawners, not fork resolution — 2026-06-16

- **Chose:** parallelize competing loop topologies (genotype spike + crucible spike + future spawners) under shared harness/bedrock — **the fork is the prey**
- **Over:** resolving genotype vs. crucible in design discussion or MEMORY before a bedrock race; premature optimization toward Jun 29 demo structure while still in chaos/exploration space
- **Because:** capstone apex bet is searching for better definitions of “better”; closing the fork early optimizes for narrative coherence, not fitness; two-week spike can explore meta-architecture without picking one topology
- **Revisit if:** one spawner consistently wins on held-out bedrock at lower cost — then promote it as default L2 topology, not before
- **Spirit note:** spawn-spawners, don't settle spawners — see [The fork is the prey](./LESSONS_AND_BANGERS.md#the-fork-is-the-prey--2026-06-16), [Loop-topology crossover](./LESSONS_AND_BANGERS.md#loop-topology-crossover--2026-06-16)

### Jurisdiction as boundary term — 2026-06-16

- **Chose:** **jurisdiction** as the preferred name for cross-stratum boundaries when something needs a variable name in code
- **Over:** treating jurisdiction / competence boundary / payload contract as three separate mechanisms
- **Because:** they're one boundary concept, three lenses (who decides / what they can know / how messages cross); chaos space is fine holding the triad until code demands a name — then jurisdiction wins
- **Revisit if:** implementation reveals distinct enforcement layers (e.g. schema validation vs. role permissions) that need separate terms
- **Spirit note:** restraint at borders, madness inside strata — see [Jurisdiction](./LESSONS_AND_BANGERS.md#jurisdiction--2026-06-16)

### Chaos space before constitution — 2026-06-16

- **Chose:** stay in unbounded exploration — naming the organism (strata, uncle/nephew, witness, extended aphenotype) before locking spike implementation or demo story
- **Over:** jumping to Jun 29 demo structure, harness specs, or `./crucible-demo` build order while still in embryology
- **Because:** premature optimization is especially toxic when the product *is* meta-improvement; documenting bangers and forks *is* L5 witness work and valid spike output
- **Revisit if:** team needs a shippable cut for showcase deadline — then apply [Explore the madness, cap the combinatorics](./LESSONS_AND_BANGERS.md#explore-the-madness-cap-the-combinatorics--2026-06-16) constitution
- **Spirit note:** meta-phant first, demo second — witness layer writing notes while phenotype forms

### Meta at root, spikes below — 2026-06-17

- **Chose:** (intent) Lα docs + registers at repo root; runnable spikes in `spikes/<name>/` as mortal sprojects
- **Over:** monolithic repo where meta treatise and genotype demo share one flat directory
- **Because:** literal mortality — delete or archive a spike folder without touching culture; mirrors "lineage log survives, organism doesn't"
- **Revisit if:** move cost outweighs benefit with only one spike and no crucible sibling yet — defer is valid
- **Spirit note:** see [TREATISE.md § XI](./TREATISE.md#xi-repo-ecology--meta-at-root-spikes-below)
