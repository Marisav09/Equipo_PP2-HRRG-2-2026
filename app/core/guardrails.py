from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str | None = None


def require_equipment_scope(equipment_name: str | None) -> GuardrailDecision:
    if not equipment_name:
        return GuardrailDecision(
            allowed=False,
            reason="Debe seleccionarse un equipo exacto antes de consultar manuales.",
        )
    return GuardrailDecision(allowed=True)
