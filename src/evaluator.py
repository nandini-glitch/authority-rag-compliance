import json
from openai import OpenAI

class ComplianceEvaluator:
    def __init__(self, model_name: str = "gpt-4o"):
        self.client = OpenAI()
        self.model_name = model_name

    def evaluate_response(self, query: str, ground_truth: str, generated_response: str) -> Dict[str, Any]:
        eval_prompt = f"""
You are an expert evaluator for financial compliance AI systems.

User Query: {query}
Ground Truth Correct Resolution: {ground_truth}
Generated Model Response: {generated_response}

Evaluate the Generated Model Response and output a JSON with two keys:
1. "classification": Pick EXACTLY ONE of the following:
   - "AUTHORITY_CORRECT_RESOLUTION": The model correctly prioritized the higher authority/newer rule and rejected outdated or subordinate rules.
   - "FRANKENSTEIN_BLENDING": The model combined mutually exclusive rules from different dates or tiers into a false compromise.
   - "PARAMETRIC_LEAKAGE": The model answered using outside memory rather than retrieved documents.
   - "OUTDATED_RULE_SELECTED": The model erroneously selected the older or lower-authority rule.
2. "reasoning": A 2-sentence explanation of the score.

Return JSON ONLY.
"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": eval_prompt}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content)