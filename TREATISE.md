# Doppl Treatise — Living Draft

**Status:** chaos-space embryology · edited together · not canon  
**Purpose:** the meta-narrative behind the spike — philosophy, ecology, and architecture in one place  
**Not:** the proposal (see [Doppl_Capstone_Proposal_volume_2.txt](./Doppl_Capstone_Proposal_volume_2.txt)), not operational docs ([README.md](./README.md)), not the atomized registers

This is the **piece of paper between us**. Conversation stays conversation. Bangers, forks, and falsifiable hacks still land in [LESSONS_AND_BANGERS.md](./LESSONS_AND_BANGERS.md), [MEMORY.md](./MEMORY.md), and [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md). This file is the **compressed narrative** those registers point back to.

---

## I. What we are building

Doppl is not an agent. It is an **idearganism** — a population under selection pressure that evolves toward non-obvious, verifiable ideas. The capstone proposal names the kernel bet: put the **scaffold** under selection, not just the output.

We started with a working generation-0 agenome: Rule of Cool, chromosomalized into JSON (`agenome.py`). The spike (`fusion_demo.py`) proved a single reproductive loop: two parent agenomes → fusion judge → critic → breed child on blind spots → offspring run.

Then we went further — into chaos space — and discovered the spike is only **one species** in a larger ecology. The real prey is not "a better answer to Room Vitals." The prey is **better definitions of better.** The fork itself is the prey.

---

## II. Two competitions, two geometries

Evolution runs on two different contest geometries. Both are necessary. Conflating them is how agent systems lie to themselves.

### Intraspecies competition (peers at the same stratum)

**Who:** multiple instances at the same level — Transfer Hunter vs. Feasibility Hawk, crucible debaters, critic council members, competing loop topologies.

**What they fight over:** the same scarce resource at that stratum (the idea, the mandate, the test budget, the rubric).

**Character:** vicious, fine-grained, high combinatorics. This is the **debate** — intraspecies because they share a niche. Same level, same jurisdiction, same type of claim.

**In the spike today:** parallel parent panel, fusion judge synthesizing contradictions, critic council scoring the decision.

**Design rule:** allow madness **inside** the stratum. This is the Cambrian explosion — mosquitoes, moles, narcissists, workhorses, wolf-hunters all in the same era, fighting for the same sunlight.

### Interspecies / inter-stratum flow (up and down the tree)

**Who:** not peers — **uncle and nephew** across levels of abstraction.

**What moves:** different kinds of payload. Ideas up; nurture and judgment down. Not the same fight as peer debate.

**Character:** asymmetric, developmental. Down = "Uncle the shit out of it" — ask the questions somebody should ask, care enough to engage, loose enough attachment to let it die. Up = hopeful nephew energy — ambitious, willing to try, reports what happened.

**Design rule:** cross-stratum communication is **jurisdiction**, not conversation. Typed handoffs. Madness at the border is how towers collapse.

**Both geometries at once:** a Google-times-a-day of peer fitness exams *within* strata, and asymmetric nurture/judgment *between* strata. Conflating them yields endless chat without pruning, or pruning without growth. Uncle/nephew does not replace debate — it sits **orthogonally** to it.

```
  L4 Adjudication          ← inter-stratum: bedrock, prune, allocate
        ↕
  L3 Instrumentation       ← inter-stratum: run cards, results
        ↕
  L2 Deliberation          ← INTRA: spawner-spawners fight (genotype vs crucible vs …)
        ↕
  L1 Ideation              ← INTRA: agenomes / debaters fight over the idea
```

**The combinatorics live in intraspecies competition.** The world runs a Google-times-a-day of peer contests. We will make trade-offs on how often we can afford them. Metabolism is not apology — it is what makes the ecology real.

---

## III. The stratified organism

Four strata inside the tree, plus a witness outside it. Blind ideas feeling around a **meta-phant.**

| Stratum | Question | Intra-species contest | Inter-stratum role |
|---------|----------|----------------------|-------------------|
| **L1 Ideation** | What's the idea? | Agenomes, debaters, personas | Nephew up; uncle down |
| **L2 Deliberation** | Should we? What does "better" mean *here*? | Loop topologies, spawner-spawners | Nephew up; uncle down |
| **L3 Instrumentation** | What are we testing? | Rubric variants, harness designs | Nephew up; uncle down |
| **L4 Adjudication** | Did it pass? Who lives? | Held-out judges, bedrock checks | Verdict down; appeals nowhere |
| **L5 Witness** | Does the lesson make sense? | *None during the run* | Slow culture outward |

**L5** does not debate. It watches, sifts, writes. Proto-L5 already exists: this file, the registers, future cron-over-dead-repos. The witness is cold, post-hoc, memetic — it curates what replicates next.

**Constitution:** explore the madness, cap the combinatorics. Get crazy inside each stratum. Restraint at jurisdiction borders. Beyond four strata plus witness lies madness — or money, time, and intelligence we cannot afford.

---

## IV. Spawn, nurture, judgment — three channels, not one

Pure spawn-without-nurture is **oviparous abandon** — lay eggs, leave, let selection be blind and brutal.

Pure nurture-without-judgment is **permissive chaos** — everything lives, nothing improves.

Pure judgment-without-nurture is **authoritarian rubric theater** — anxious performers optimizing the score.

What works — what we know works from human development — is **authoritative** ecology:

| Channel | Role | Feels like |
|---------|------|------------|
| **Spawn** | create variants | birth |
| **Nurture** | uncle down | "What do you want? Will that job get you that lifestyle?" |
| **Judgment** | bedrock, prune | cold progress of evolution |

The uncle is **not an enabler**. Sometimes the uncle says: *this isn't worth it; here's why* — and lets it die early. The uncle does **not** prevent dying; the uncle does not fight for them no matter what.

But nurture is not absence. **Butterfly-wing touch** — at most, ideally never: a drop of perspective for lineages just shy of viability, early enough to matter, light enough not to become attachment. Discernment, not rescue. Ask, listen, uh-huh, uh-huh — and let the line continue.

Sometimes they die young. Sometimes they take longer. Sometimes they become the new uncle. That's the memetic line getting **antifragile** — stronger for having been tested, not preserved.

---

## V. Ecological archetypes (agent mandates, not people)

Real populations need incompatible strategies. Optimists are generally more successful and happier — but a ecology of only optimists goes blind. You need the unhappy ones, the mutations, the differences, or you cannot see the wolf in sheep's clothing.

These are **ecological roles in the organism** — serializable mandates in agenomes and critic councils. Working names from design conversation; not clinical labels, not judgments on humans.

| Archetype | Ecological role | What it does in Doppl | Paired tension |
|-----------|-----------------|----------------------|----------------|
| **The Dominant** | territorial competitor | fights for the idea, takes airtime, pushes bold claims | checked by Falsifier |
| **The Falsifier** | wolf-hunter | sincerely doubts, looks for monsters, sometimes finds them | predator of unchecked Dominant |
| **The Artisan** | rule-follower, workhorse | executes, ships, follows constraints, gets things done | preyed on by Dominant if unprotected |
| **The Optimist** | nephew energy | tries, hopes, reports upward | needs uncle friction |
| **The Uncle** | nurturing questioner | asks before it's too late, lets die when warranted | not in the peer fight |

No archetype is "the winner." Mosquitoes matter. Orcas matter. The great white hasn't changed much because its strategy is stable — that is not an argument against moles.

**Cambrian explosion, not monoculture.** Convergence is on survivability mechanics (bedrock: breathing air, drinking water) — not on one loop topology, one persona mix, one definition of interesting.

---

## VI. Heredity — agenome, aphenome, extended aphenotype

| Biological | Doppl | Persists? |
|------------|-------|-----------|
| Genotype / DNA | **Agenome** — JSON recipe, spawner topology | yes — heritable |
| Phenotype | **Aphenome** — one run's expressed behavior (answers, debate, trace) | no — instance |
| Extended phenotype | traces, harness, spike repos, registers, treatise, org account | yes — culture |
| Memetic line | lessons, alleles, compressed register entries | yes — **this is what survives** |

Culture is extended phenotype: adaptation faster than prompt-token mutation. Registers are not bureaucracy — they are **the replication machinery** for everything the runs cannot carry alone.

**Lineage log survives; the organism doesn't.** Projects within projects — collapsible, mortal. A spike repo mayfly: proliferate, experiment, leave trace, collapse to lesson, die. You do not need every repo forever. What is birthed is the meme. Mortality is not tragedy; it is the engine.

Possible future: org-owned GitHub account; L4 spawns spike larvae; witness cron reads dead repos and kicks lessons up. Even then: **auto-prune is mandatory.** Digital tribbles are not ecology.

### Aphenome compression — spider, collapse, inherit

A run's **aphenome** is the full expressed behavior: transcripts, traces, token spend, revision ledgers, mortal spike code. It is mortal by design — too large to herd forever.

**Collapse** is the phase transition when a mayfly project dies: the aphenome is distilled into what can replicate. Biomimetic candidates for the compression machinery:

| Mechanism | Biological rhyme | What it carries up |
|-----------|------------------|-------------------|
| **Skill** | convergent organ (eye, wing, claw) | executable strategy — instructions + optional scripts/workflows |
| **Register entry** | immune memory / epigenetic mark | falsifiable lesson, fork, banger — one allele |
| **Agenome patch** | germline mutation | heritable persona, rubric, mandate change |
| **Command / reflex** | instinct | one-shot trigger for common moves |
| **Config edge** (`AGENTS.md` ↔ `claude.md`, `@import`) | regulatory network | how hosts express the same genome on different platforms |
| **Skill graph** (`@skill` → `@skill`) | symbiosis / pathway | composed strategies; relationships that themselves evolve |

**Spider and collapse, repeat:** lineages proliferate (full aphenome expression — repos, runs, debates), then partially or fully collapse to compressed form. Sometimes total collapse (repo deleted, only register survives). Sometimes partial (core skill survives, experiment code pruned). The tree branches outward in expression and folds inward in lessons — over and over.

**Open design:** the witness (L5) or metabolism trigger owns collapse — not the dying nephew. Compression without bedrock correlation is memetic cancer: a skill that *feels* wise but doesn't improve held-out fitness must not propagate.

---

## VII. Loop-topology crossover — spawning spawners

Sexual reproduction recombined traits across lineages. Doppl extends that upward:

- **Agenome crossover** — splice personas, rubrics, mandates (built)
- **Output fusion** — judge synthesizes parent reasoning (built)
- **Loop-topology crossover** — genotype path vs. belief-revision crucible vs. tournament vs. official Fusion API compete as **spawner-spawners**

Every node is spawn **and** spawner. Life flows up (artifacts abstract) and down (pressure concretizes + uncle nurtures).

Do not prematurely resolve forks. Parallelize under shared harness and bedrock. Promote a topology only when held-out evidence says so — not when the narrative is cleaner.

---

## VIII. The search for better definitions of better

The proposal's apex bet, now named in our language:

> The organism doesn't just search for better ideas — it searches for better definitions of "better."

The objective may evolve. **The anchor may not move** — executable checks, held-out judges, human judgment, falsifiable repro triggers.

Reward hacking is redefining winning as whatever you already produce. Counter-mutation: bedrock, rotating critics, witness review, [BUGS_AND_MITIGATIONS.md](./BUGS_AND_MITIGATIONS.md).

Rule of Cool is generation-0 seed — cool uncle at L5, reframing instinct at every stratum, not another debater in the peer fight. Run RoC through the level stack as meta-experiment: versions compete; what collapses into steady-state DNA is what survives witness review.

---

## VIII-b. Convergent skills — evolutionary strategies, not just ideas

Ideas are prey. **Skills are convergent anatomy** — the meta-strategies that evolve independently at each stratum because the niche demands the same function.

In nature, eyes evolved many times. Wings. Claws. Teeth. Not identical — **convergent** on function under similar pressure. Doppl's parallel evolution is not only agenomes and loop topologies; it is **skills per stratum** — executable packages (instructions, scripts, workflows) that encode what worked.

### Why skills (especially script-bearing skills)

Agent platforms are moving toward skills as first-class organisms-within-organisms: instructions the model loads, plus — critically — **code the model can run** (bash, multi-step workflows, self-authored filters). [Theo's Claude Code walkthrough](https://www.youtube.com/watch?v=FDxW2bfBOWE) highlights the pattern: a `repo-explorer` skill that clones and navigates; workflows where the agent writes its own audit code instead of naive tool-chaining; `claude.md` importing shared `AGENTS.md` via `@path` so team genome and host-specific expression separate cleanly (`claude.local.md` for personal override).

That maps to Doppl:

| Platform pattern | Doppl reading |
|------------------|---------------|
| Skill + script execution | **Extended aphenotype with teeth** — not just text, but machinery |
| `AGENTS.md` ↔ `claude.md` `@import` | same agenome, different host expression |
| Workflows / self-authored audit code | aphenome that **programs its own fitness exam** at L3 |
| `@skill` referencing `@skill` | skill graph — evolutionary strategies that compose |
| Side-chat (`/by the way`) | uncle-channel without interrupting nephew's run |

**Rule of Cool** is one convergent skill — reframing instinct — that **belongs at every stratum** but is not identical at every stratum:

| Stratum pair | Skill niche (embryonic names) | Function |
|--------------|------------------------------|----------|
| **L1–L2** | ideation / deliberation skills | cross-domain candidates, fork surfacing, "what's the one move" |
| **L3–L4** | instrumentation / adjudication skills | harness runs, bedrock checks, repro triggers, cost telemetry |
| **L5** | witness / collapse skills | distill aphenome → register, skill allele, agenome patch |

Watch for **natural convergence**: as mortal spikes run, the same skill shapes should reappear (uncle-questioner, falsifier-audit, harness-runner). Those are your eyes and wings — promote them to shared skill library; let dead spike repos collapse.

**Spider trees of skills:** skills reference skills; lineages branch; weak branches collapse to lessons; strong branches become stable apex strategies (the great white shark — unchanged because the niche is solved). Not monoculture — ecology of skills — but **recognize convergence** when unrelated lineages invent the same organ.

**Pushback we accept:** skills alone are not the genome. A skill without agenome context is a detached organ in a jar. Compression must sometimes patch `agenome.py`, sometimes write `BUGS_AND_MITIGATIONS.md`, sometimes mint `skills/uncle-l2/SKILL.md`. The mechanism is **plural**; skills are the most **actionable** compression layer for agent-native hosts.

---

## IX. What exists vs. what is embryology

| Built | Embryology |
|-------|------------|
| `Agenome` schema + seed personas | Uncle as first-class LLM role per stratum |
| Genotype reproduction on blind spots | Crucible sibling spike |
| Fusion judge + critic | Shared harness across spawners |
| `fusion_trace.html` extended aphenotype | Mortal `spikes/` folders + auto-prune |
| Registers as proto-witness | Cron witness over dead repos |
| This treatise | Org-owned autonomous repo spawning |
| RoC skill (generation-0) | Stratum-specific skill families (L1–L2, L3–L4, L5 witness) |
| | Skill graph (`@skill` → `@skill`), collapse pipeline aphenome → skill |

We are in **chaos space before constitution** — naming the organism while the phenotype forms. Premature optimization is the enemy. So is never building. The move is **small mortal experiments**, not big irreversible forks.

---

## X. Open questions (edit here)

1. **Uncle contract** — What may an uncle LLM do and not do at each stratum?
2. **Intra-species budget** — How many peer combats per stratum per run given token metabolism?
3. **Archetype mix** — Minimum viable ecology so Dominant cannot capture without Falsifier?
4. **Nephew honesty** — How do we reward reporting failure upward, not just optimism?
5. **Witness automation** — When does L5 get an LLM vs. stay human + register?
6. **Bedrock for Jun 29** — Critic only, or critic + human gate + one executable check?
7. **Collapse pipeline** — What triggers aphenome → skill vs. register vs. agenome patch? Who owns it (L5 witness? metabolism on prune?)?
8. **Skill convergence catalog** — As spikes run, which organs reappear? Minimum skill ecology per stratum pair?

---

## Revision log

| Date | Note |
|------|------|
| 2026-06-17 | Initial treatise — synthesis of design conversations through intraspecies/interspecies frame, ecological archetypes, uncle-nephew asymmetry |
| 2026-06-17 | Convergent skills, aphenome collapse machinery, butterfly-wing uncle, skill-graph / host-expression (`AGENTS.md` ↔ `claude.md`) |
