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

### Genotype over transcript — 2026-06-16

- **Banger:** Put evolution in the genotype, not the transcript. When something fails scrutiny, don't patch the answer — breed a new agent. Selection pressure belongs on *who* is thinking, not *how long* they're allowed to talk.
- **Lesson:** On critic fail, `breed_child()` splices parents and mutates on `blind_spots ∪ clarifying_questions` — not on critic tone or "try harder."
- **Evidence:** Gen 1 (Transfer Hunter × Feasibility Hawk → fusion judge → critic) fails Room Vitals; offspring answers via `primary_mandate` in `agenome.py`; `fusion_trace.html` shows parent genomes, breeding mandate, and child genome.
- **Carry forward:** Default reproduction operator is genomic splice, not transcript retry.
