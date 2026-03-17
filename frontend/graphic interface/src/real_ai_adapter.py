from __future__ import annotations

from src.model_integration import integrate_model_outputs


def enrich_with_ai_outputs(df, schema):
    return integrate_model_outputs(df)
