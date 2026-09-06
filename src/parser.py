import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class RegulatoryMetadata(BaseModel):
    doc_id: str = Field(description="Official circular number e.g., RBI/2025-26/53")
    issuer: str = Field(description="e.g., Reserve Bank of India, HDFC Bank")
    authority_tier: int = Field(description="1: Regulator (RBI/SEBI), 2: SRO/Association, 3: Internal Bank Policy")
    doc_type: str = Field(description="Master Direction, Circular, Policy Document, FAQ")
    date_issued: str = Field(description="YYYY-MM-DD")
    topic: str = Field(description="e.g., KYC, Digital Lending, Credit Cards")
    is_repealed: bool = Field(default=False)
    superseded_by: Optional[str] = Field(default=None)

class ComplianceChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: RegulatoryMetadata

def format_authority_header(metadata: RegulatoryMetadata, mode: str = "full") -> str:
    """
    Constructs the contextual prefix injected into the LLM prompt.
    """
    if mode == "naive":
        return ""
    elif mode == "recency_only":
        return f"[DATE ISSUED: {metadata.date_issued}]\n"
    elif mode == "full":
        return (
            f"[METADATA | Issuer: {metadata.issuer} | "
            f"Authority Tier: {metadata.authority_tier} | "
            f"Doc Type: {metadata.doc_type} | "
            f"Date Issued: {metadata.date_issued} | "
            f"Doc ID: {metadata.doc_id}]\n"
        )
    else:
        raise ValueError(f"Unknown metadata mode: {mode}")