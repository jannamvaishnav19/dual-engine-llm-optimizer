import json
from app.providers.factory import ProviderFactory

class JudgeService:
    async def evaluate(self, prompt, answer, provider_name, settings):
        try:
            return await self.evaluate_now(prompt, answer, provider_name, settings)
        except Exception:
            return None

    async def evaluate_now(self, prompt, answer, provider_name, settings):
        # Cross-evaluate with the other engine instead of asking the generator to grade itself.
        judge_name = "groq" if provider_name == "gemini" else "gemini"
        judge = ProviderFactory.create(judge_name, settings)
        rubric = (
            "You are an impartial response evaluator. Score correctness, relevance, clarity, and completeness. "
            "Return ONLY valid JSON with keys score (0-10), verdict (short label), rationale (one paragraph)."
        )
        evaluation_prompt = (
            f"USER PROMPT:\\n{prompt[:6000]}\\n\\nMODEL ({provider_name}) ANSWER:\\n{answer[:8000]}\\n\\n"
            "Score the answer using the rubric."
        )
        result = await judge.generate(evaluation_prompt, rubric, 0.0, 300)
        raw = result.text.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            data = json.loads(raw)
            score = max(0.0, min(10.0, float(data["score"])))
            return {"score": score, "verdict": str(data["verdict"])[:80],
                    "rationale": str(data["rationale"])[:1500], "judge_provider": judge_name}
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return {"score": 0.0, "verdict": "unparseable",
                    "rationale": "Judge response was not valid JSON; inspect provider output.",
                    "judge_provider": judge_name}
