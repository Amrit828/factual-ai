from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pipeline.verifier import VerificationPipeline

router = APIRouter()

# Initialize the pipeline
pipeline = VerificationPipeline()

class ArticleRequest(BaseModel):
    text: str

class ClaimRequest(BaseModel):
    claim_text: str

@router.post("/verify_article")
async def verify_article(request: ArticleRequest):
    result = await pipeline.process_article(request.text)
    return result

@router.post("/verify_claim")
async def verify_claim(request: ClaimRequest):
    result = await pipeline.process_single_claim(request.claim_text)
    return result
