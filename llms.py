from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class ModelConfig:
    name: int 
    input_cost: float
    output_cost: float
    context_window: int 
    reasoning: str
    verbosity: str
    tool_choice: str

GPT_5_MINI = ModelConfig(
    name = "gpt-5-mini",
    input_cost = 0.25,
    output_cost = 2.00,
    context_window = 400000,
    reasoning = "high",
    verbosity = "low",
    tool_choice = "auto" 
)

GPT_5_NANO = ModelConfig(
    name = "gpt-5-nano",
    input_cost = 0.05,
    output_cost = 0.40,
    context_window = 400000,
    reasoning = "high",
    verbosity = "low",
    tool_choice = "auto" 
)