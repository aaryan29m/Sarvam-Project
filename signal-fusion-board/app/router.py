from typing import Dict, Any
from app.config import settings

class ModelRouter:
    COMPLEXITY_KEYWORDS = {
        "reasoning": ["prove", "derive", "analyze", "architect", "step-by-step", "mathematical"],
        "coding": ["def ", "class ", "function", "async", "dockerfile", "sql", "bug"],
        "simple": ["hi", "hello", "translate", "what is", "meaning of"]
    }

    def __init__(self):
        self.fast_model = settings.DEFAULT_FAST_MODEL
        self.balanced_model = settings.DEFAULT_BALANCED_MODEL
        self.reasoning_model = settings.DEFAULT_REASONING_MODEL

    def score_complexity(self, prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower()
        length = len(prompt)

        has_code = "```" in prompt or any(k in prompt for k in self.COMPLEXITY_KEYWORDS["coding"])
        has_reasoning = any(k in p_lower for k in self.COMPLEXITY_KEYWORDS["reasoning"])
        is_simple = any(p_lower.startswith(k) for k in self.COMPLEXITY_KEYWORDS["simple"]) and length < 100

        if is_simple and not has_code:
            tier = "fast"
            selected_model = self.fast_model
        elif has_reasoning or (has_code and length > 600):
            tier = "reasoning"
            selected_model = self.reasoning_model
        else:
            tier = "balanced"
            selected_model = self.balanced_model

        return {"tier": tier, "selected_model": selected_model}
