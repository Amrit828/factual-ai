import re
import logging
from typing import List, Dict, Any
from llm.client import LLMClient
from retrieval.faiss_index import DocumentRetriever

logger = logging.getLogger(__name__)

class VerificationPipeline:
    def __init__(self):
        logger.info("Initializing VerificationPipeline...")
        self.llm = LLMClient()
        self.retriever = DocumentRetriever()
        
    def segment_text(self, text: str) -> List[str]:
        """Segments raw text into individual sentences."""
        # Simple regex segmentation for demonstration
        # Matches punctuation followed by space and capital letter
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if len(s.strip()) > 5]
        
    async def process_article(self, text: str) -> Dict[str, Any]:
        """Processes an entire article: splits, filters claims, and verifies them."""
        # 1. Segment article
        sentences = self.segment_text(text)
        logger.info(f"Segmented article into {len(sentences)} sentences.")
        
        # 2. Extract verifiable claims using LLM
        claims = self.llm.filter_claims(sentences)
        logger.info(f"Extracted {len(claims)} verifiable claims.")
        
        # 3. Process each claim
        verified_claims = []
        for claim in claims:
            # Retrieve evidence
            results = self.retriever.retrieve(claim, k=3)
            evidence_texts = [r['text'] for r in results] if results else []
            
            # Analyze claim with LLM based on evidence
            if not evidence_texts:
                analysis = {
                    "verdict": "Unverifiable",
                    "reasoning": "No relevant evidence found in the knowledge base.",
                    "confidence": 0.0
                }
            else:
                analysis = self.llm.analyze_claim(claim, evidence_texts)
                
            verified_claims.append({
                "claim": claim,
                "verdict": analysis.get("verdict", "Unverifiable"),
                "confidence": analysis.get("confidence", 0.0),
                "reasoning": analysis.get("reasoning", "No reasoning provided."),
                "evidence": results
            })
            
        return {
            "status": "success",
            "total_sentences": len(sentences),
            "claims_extracted": len(claims),
            "claims": verified_claims
        }
        
    async def process_single_claim(self, claim: str) -> Dict[str, Any]:
        """Processes a single claim directly."""
        # Retrieve evidence
        results = self.retriever.retrieve(claim, k=3)
        evidence_texts = [r['text'] for r in results] if results else []
        
        # Analyze claim with LLM based on evidence
        if not evidence_texts:
            analysis = {
                "verdict": "Unverifiable",
                "reasoning": "No relevant evidence found in the knowledge base.",
                "confidence": 0.0
            }
        else:
            analysis = self.llm.analyze_claim(claim, evidence_texts)
            
        return {
            "claim": claim,
            "verdict": analysis.get("verdict", "Unverifiable"),
            "confidence": analysis.get("confidence", 0.0),
            "reasoning": analysis.get("reasoning", "No reasoning provided."),
            "evidence": results
        }
