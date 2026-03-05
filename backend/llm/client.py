import json
from typing import List, Dict, Any
from ollama import Client as OllamaClient
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model_name: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.client = OllamaClient(host=base_url)
        self.model_name = model_name
        logger.info(f"Initialized LLMClient with model: {model_name} at {base_url}")
        
    def filter_claims(self, sentences: List[str]) -> List[str]:
        """Filters a list of sentences to keep only verifiable factual claims."""
        if not sentences:
            return []
            
        prompt = f"""
You are an expert fact-checker assistant. Your task is to identify which sentences contain verifiable factual claims.
A verifiable factual claim is a statement that can be proven true or false using objective evidence (e.g., historical events, scientific facts, statistics).
Do not include opinions, questions, or subjective statements.

Return ONLY a JSON object with a single key "claims" containing an array of strings representing the verifiable claims.

Sentences:
{json.dumps(sentences)}
"""
        try:
            response = self.client.generate(model=self.model_name, prompt=prompt, format="json")
            if "response" in response:
                result = json.loads(response["response"])
                if isinstance(result, dict) and "claims" in result:
                    return result["claims"]
                elif isinstance(result, list):
                    return result
            return []
        except Exception as e:
            logger.error(f"Error filtering claims: {e}")
            return []
            
    def analyze_claim(self, claim: str, evidence: List[str]) -> Dict[str, Any]:
        """Analyzes a claim against retrieved evidence."""
        evidence_text = "\n".join([f"- {e}" for e in evidence])
        prompt = f"""
You are an expert fact-checker. Determine if the following claim is Supported, Refuted, or Unverifiable based ONLY on the provided evidence.

Claim: "{claim}"

Evidence:
{evidence_text}

Instructions:
1. Verify the claim using the evidence.
2. If the evidence confirms the claim, the verdict is "Supported".
3. If the evidence contradicts the claim, the verdict is "Refuted".
4. If there is not enough evidence to verify the claim, the verdict is "Unverifiable".
5. Provide a brief reasoning for your decision (1-2 sentences).
6. Provide a confidence score between 0.0 and 1.0.

Respond ONLY with a JSON object in the following format:
{{
    "verdict": "Supported" | "Refuted" | "Unverifiable",
    "reasoning": "Your explanation here.",
    "confidence": 0.95
}}
"""
        try:
            response = self.client.generate(model=self.model_name, prompt=prompt, format="json")
            if "response" in response:
                return json.loads(response["response"])
            
            return {
                "verdict": "Unverifiable",
                "reasoning": "Failed to generate a valid response.",
                "confidence": 0.0
            }
        except Exception as e:
            logger.error(f"Error analyzing claim: {e}")
            return {
                "verdict": "Unverifiable",
                "reasoning": f"Error during analysis: {str(e)}",
                "confidence": 0.0
            }
