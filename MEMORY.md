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
