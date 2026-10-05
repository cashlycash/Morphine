from dataclasses import dataclass


@dataclass(frozen=True)
class ModelOption:
    model_name: str
    provider: str
    cost_per_1k_tokens: float
    quality_score: float


CATALOG = [
    ModelOption("claude-sonnet", "anthropic", 0.018, 0.95),
    ModelOption("mistral-7b", "huggingface", 0.00014, 0.78),
    ModelOption("llama3-local", "vllm", 0.0, 0.72),
]


def select_model(quality_cost_balance: float) -> ModelOption:
    target_quality = 0.70 + (quality_cost_balance * 0.25)
    eligible = [m for m in CATALOG if m.quality_score >= target_quality]
    if not eligible:
        return CATALOG[0]
    return sorted(eligible, key=lambda m: m.cost_per_1k_tokens)[0]
