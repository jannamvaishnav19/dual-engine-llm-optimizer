class ModelRouter:
    """Simple explainable routing baseline; replace with measured policy after benchmarking."""
    CODE_TERMS = ("debug", "stack trace", "algorithm", "complexity", "refactor", "code review")
    REASONING_TERMS = ("prove", "derive", "compare", "trade-off", "architecture decision")

    def choose(self, prompt: str, task_type: str = "auto") -> str:
        if task_type in {"fast", "long_context", "vision"}:
            return "gemini"
        if task_type in {"code", "reasoning"}:
            return "groq"
        text = prompt.lower()
        if len(prompt) > 7000:
            return "gemini"
        if any(term in text for term in self.CODE_TERMS + self.REASONING_TERMS):
            return "groq"
        return "gemini"
