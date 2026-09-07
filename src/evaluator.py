import os
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

from src.pipelines import init_llm_client, call_with_retry

VALID_CLASSIFICATIONS = [
    "AUTHORITY_CORRECT_RESOLUTION",
    "FRANKENSTEIN_BLENDING",
    "PARAMETRIC_LEAKAGE",
    "OUTDATED_RULE_SELECTED"
]

class ComplianceEvaluator:
    def __init__(self, model_name: Optional[str] = None):
        self.client, self.model_name = init_llm_client(preferred_model=model_name)

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
        response = call_with_retry(
            lambda: self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": eval_prompt}],
                response_format={"type": "json_object"},
                temperature=0.0
            )
        )
        content = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
            else:
                parsed = {
                    "classification": "PARAMETRIC_LEAKAGE",
                    "reasoning": f"Failed to parse evaluator JSON response: {content}"
                }

        # Validate classification key
        classification = parsed.get("classification", "").strip()
        if classification not in VALID_CLASSIFICATIONS:
            # Fallback search for classification in text
            found = False
            for vc in VALID_CLASSIFICATIONS:
                if vc in classification:
                    parsed["classification"] = vc
                    found = True
                    break
            if not found:
                parsed["classification"] = "FRANKENSTEIN_BLENDING"

        return parsed