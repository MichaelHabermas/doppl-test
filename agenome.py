"""Rule-of-Cool agenomes: serializable genomes that breed on blind spots."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

ROC_OUTPUT_CONTRACT = """Emit exactly ONE recommendation — the single best surviving idea.
Structure:
1. **Decision** — one clear direction (confidence: low/medium/high)
2. **Why** — 2-3 bullets
3. **Assumptions** — what you're assuming about the underspecified prompt
4. **Next step** — one concrete action for this week

Keep it under 250 words. State assumptions explicitly when the prompt is vague."""

ROC_RANKING_RUBRIC = """Silently consider 3-5 candidates from different angles, then emit only the winner.
Filter for: genuinely non-obvious, practical, accretive to what's asked, surprising-in-retrospect.
Reject: safe consensus, scope creep, overconfidence on ambiguous prompts."""


@dataclass
class Agenome:
    """Serialized agent genome — prompt + persona + reproduction metadata."""

    id: str
    name: str
    model: str
    personas: list[str]
    ranking_rubric: str
    output_contract: str
    primary_mandate: list[str] = field(default_factory=list)
    parent_ids: list[str] = field(default_factory=list)
    generation: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Agenome:
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            model=str(data["model"]),
            personas=list(data.get("personas") or []),
            ranking_rubric=str(data.get("ranking_rubric", ROC_RANKING_RUBRIC)),
            output_contract=str(data.get("output_contract", ROC_OUTPUT_CONTRACT)),
            primary_mandate=list(data.get("primary_mandate") or []),
            parent_ids=list(data.get("parent_ids") or []),
            generation=int(data.get("generation", 0)),
        )


SEED_AGENOMES: dict[str, Agenome] = {
    "transfer-hunter": Agenome(
        id="transfer-hunter",
        name="Transfer Hunter",
        model="google/gemini-2.5-flash",
        personas=[
            "veteran engineer hunting cross-domain analogies",
            "researcher who spots techniques from field A that crack field B",
        ],
        ranking_rubric=ROC_RANKING_RUBRIC,
        output_contract=ROC_OUTPUT_CONTRACT,
    ),
    "feasibility-hawk": Agenome(
        id="feasibility-hawk",
        name="Feasibility Hawk",
        model="openai/gpt-4o-mini",
        personas=[
            "startup CTO obsessed with 2-week shippability",
            "operator who kills fantasy scope and names real constraints",
        ],
        ranking_rubric=ROC_RANKING_RUBRIC,
        output_contract=ROC_OUTPUT_CONTRACT,
    ),
    "contrarian": Agenome(
        id="contrarian",
        name="Contrarian",
        model="openai/gpt-4o-mini",
        personas=[
            "skeptical product designer who rejects the obvious direction",
            "red-team thinker who asks what everyone is assuming wrong",
        ],
        ranking_rubric=ROC_RANKING_RUBRIC,
        output_contract=ROC_OUTPUT_CONTRACT,
    ),
    "zeitgeist-reader": Agenome(
        id="zeitgeist-reader",
        name="Zeitgeist Reader",
        model="google/gemini-2.5-flash",
        personas=[
            "growth strategist reading what the moment rewards",
            "novelist sensing the narrative the room wants but hasn't said",
        ],
        ranking_rubric=ROC_RANKING_RUBRIC,
        output_contract=ROC_OUTPUT_CONTRACT,
    ),
}

DEFAULT_PARENT_IDS = ("transfer-hunter", "feasibility-hawk")


def default_parent_pair() -> tuple[Agenome, Agenome]:
    a_id, b_id = DEFAULT_PARENT_IDS
    return SEED_AGENOMES[a_id], SEED_AGENOMES[b_id]


def build_system_prompt(agenome: Agenome) -> str:
    persona_block = "\n".join(f"- {p}" for p in agenome.personas)
    mandate_block = ""
    if agenome.primary_mandate:
        items = "\n".join(f"- {m}" for m in agenome.primary_mandate)
        mandate_block = f"""
PRIMARY MANDATE — you exist to resolve these gaps the parents missed:
{items}

Every section of your answer must visibly address at least one mandate item."""

    return f"""You are a Rule-of-Cool agenome: {agenome.name}.

Persona lenses (think through all, answer as one voice):
{persona_block}

Ranking rubric:
{agenome.ranking_rubric}
{mandate_block}

Output contract:
{agenome.output_contract}"""


def extract_breeding_mandate(analysis: dict[str, Any], critic: dict[str, Any]) -> list[str]:
    """Union of fusion judge blind spots and critic gaps — the child's reason to exist."""
    seen: set[str] = set()
    mandate: list[str] = []

    for source in (
        analysis.get("blind_spots") or [],
        analysis.get("clarifying_questions") or [],
        critic.get("weaknesses") or [],
        critic.get("clarifying_questions") or [],
    ):
        for item in source:
            text = str(item).strip()
            if text and text.lower() not in seen:
                seen.add(text.lower())
                mandate.append(text)

    fix = critic.get("what_would_make_this_pass")
    if fix:
        text = str(fix).strip()
        if text and text.lower() not in seen:
            mandate.append(text)

    return mandate


def crossover(
    parent_a: Agenome,
    parent_b: Agenome,
    mandate: list[str],
    *,
    child_generation: int,
) -> Agenome:
    """Splice parent traits, mutate with blind-spot mandate."""
    child_id = f"child-g{child_generation}-{parent_a.id[:4]}-{parent_b.id[:4]}"
    merged_personas = list(dict.fromkeys(parent_a.personas + parent_b.personas))

    return Agenome(
        id=child_id,
        name=f"Offspring ({parent_a.name} × {parent_b.name})",
        model=parent_a.model,
        personas=merged_personas,
        ranking_rubric=parent_a.ranking_rubric,
        output_contract=parent_b.output_contract,
        primary_mandate=mandate,
        parent_ids=[parent_a.id, parent_b.id],
        generation=child_generation,
    )


def breed_child(
    parent_a: Agenome,
    parent_b: Agenome,
    analysis: dict[str, Any],
    critic: dict[str, Any],
    *,
    child_generation: int,
) -> tuple[Agenome, list[str]]:
    mandate = extract_breeding_mandate(analysis, critic)
    child = crossover(parent_a, parent_b, mandate, child_generation=child_generation)
    return child, mandate


def run_agenome(
    chat: Callable[..., str],
    client: Any,
    agenome: Agenome,
    prompt: str,
    *,
    temperature: float = 0.4,
) -> str:
    return chat(
        client,
        model=agenome.model,
        messages=[
            {"role": "system", "content": build_system_prompt(agenome)},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )


def agenome_panel_entry(agenome: Agenome, answer: str) -> dict[str, Any]:
    return {
        "model": agenome.model,
        "label": agenome.name,
        "agenome_id": agenome.id,
        "answer": answer,
        "agenome": agenome.to_dict(),
    }


def lineage_record(
    parent_a: Agenome,
    parent_b: Agenome,
    child: Agenome,
    mandate: list[str],
) -> dict[str, Any]:
    return {
        "parents": [parent_a.to_dict(), parent_b.to_dict()],
        "mandate": mandate,
        "child": child.to_dict(),
    }


def format_lineage_json(lineage: dict[str, Any]) -> str:
    return json.dumps(lineage, indent=2)
