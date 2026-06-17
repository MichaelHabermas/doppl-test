"""Shared helpers for fusion demo."""

from __future__ import annotations

import json
from typing import Any


def parse_json_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw_output": raw, "parse_error": True}


def panel_to_trace(panel: list[tuple[str, str]] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    if panel and isinstance(panel[0], dict):
        return list(panel)
    return [
        {"model": model, "label": model.split("/")[-1], "answer": answer}
        for model, answer in panel  # type: ignore[misc]
    ]
