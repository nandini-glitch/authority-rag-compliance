# Authority-Aware Contradiction Resolution in RAG for Indian Financial Compliance

Evaluating hallucination rates in RAG systems under regulatory drift across RBI/SEBI circulars and bank internal compliance documents.

## Experimental Baselines
1. **Naive RAG**: Context chunks stripped of dates and authority metadata.
2. **Recency-Aware RAG**: Context chunks prefixed with issuance dates (`YYYY-MM-DD`).
3. **Authority & Recency-Aware RAG**: Context chunks prefixed with structured authority hierarchy + dates.

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # Add your OPENAI_API_KEY