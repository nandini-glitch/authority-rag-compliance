import os
import json
import requests
from pypdf import PdfReader
from typing import List, Dict, Any

RAW_DIR = "data/raw_pdfs"
PARSED_DIR = "data/parsed_chunks"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

DOCUMENT_SOURCES = [
    {
        "doc_id": "RBI/2022-23/111",
        "title": "RBI Guidelines on Digital Lending 2022",
        "url": "https://fidcindia.org.in/wp-content/uploads/2022/09/RBI-GUIDELINES-ON-DIGITAL-LENDING-02-09-22.pdf",
        "filename": "rbi_digital_lending_2022.pdf",
        "issuer": "Reserve Bank of India",
        "authority_tier": 1,
        "doc_type": "Guidelines",
        "date_issued": "2022-09-02",
        "status": "outdated",
        "topic": "Digital Lending",
        "is_repealed": True,
        "superseded_by": "RBI/2025-26/36"
    },
    {
        "doc_id": "RBI/2025-26/36",
        "title": "Reserve Bank of India (Digital Lending) Directions, 2025",
        "url": "https://www.axis.bank.in/docs/default-source/default-document-library/reserve-bank-of-india-digital-lending-directions2025.pdf",
        "filename": "rbi_digital_lending_2025.pdf",
        "issuer": "Reserve Bank of India",
        "authority_tier": 1,
        "doc_type": "Directions",
        "date_issued": "2025-05-08",
        "status": "current",
        "topic": "Digital Lending",
        "is_repealed": False,
        "superseded_by": ""
    },
    {
        "doc_id": "ACB/POL/DL/2024-25/04",
        "title": "Apex Commercial Bank - Internal SOP for Digital Lending 2024",
        "url": "",
        "filename": "bank_internal_digital_lending_policy_2024.txt",
        "issuer": "Apex Commercial Bank (Internal Policy)",
        "authority_tier": 3,
        "doc_type": "Internal Policy",
        "date_issued": "2024-04-15",
        "status": "internal_active",
        "topic": "Digital Lending",
        "is_repealed": False,
        "superseded_by": ""
    }
]


def download_pdfs():
    """Downloads official PDFs using proper headers, with retries and a
    clear fallback message when a source is bot-protected."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/pdf,*/*",
    }

    for item in DOCUMENT_SOURCES:
        if not item.get("url"):
            continue
        filepath = os.path.join(RAW_DIR, item["filename"])
        if os.path.exists(filepath):
            print(f"File already exists: {filepath}")
            continue

        print(f"Downloading {item['title']}...")
        try:
            res = requests.get(item["url"], headers=headers, timeout=30, allow_redirects=True)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed for {item['title']}: {e}")
            continue

        if res.content.startswith(b"%PDF"):
            with open(filepath, "wb") as f:
                f.write(res.content)
            print(f"Successfully saved: {filepath}")
        else:
            print(f"Failed: Server returned non-PDF content for {item['title']}.")
            print(f"  -> If this is an rbi.org.in URL, it's likely captcha-walled. "
                  f"Download manually from {item['url']} and place it at {filepath}.")


def extract_text_chunks(chunk_size: int = 800, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
    """Parses downloaded PDFs and text documents into metadata-enriched text chunks."""
    all_chunks = []
    step = max(50, chunk_size - chunk_overlap)

    for item in DOCUMENT_SOURCES:
        doc_path = os.path.join(RAW_DIR, item["filename"])
        if not os.path.exists(doc_path):
            print(f"Skipping {item['filename']} (file does not exist)")
            continue

        full_text = ""
        if item["filename"].endswith(".pdf"):
            reader = PdfReader(doc_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        elif item["filename"].endswith(".txt"):
            with open(doc_path, "r", encoding="utf-8") as f:
                full_text = f.read()

        if not full_text.strip():
            print(f"Warning: no extractable text in {item['filename']} "
                  f"(may be a scanned/image PDF - needs OCR)")
            continue

        chunk_idx = 0
        for i in range(0, len(full_text), step):
            chunk_text = full_text[i:i + chunk_size].strip()
            if len(chunk_text) < 100:
                continue

            chunk_id = f"{item['doc_id'].replace('/', '_').replace(' ', '_')}_chunk_{chunk_idx}"
            chunk_idx += 1

            chunk_data = {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "doc_id": item["doc_id"],
                    "issuer": item["issuer"],
                    "authority_tier": int(item["authority_tier"]),
                    "doc_type": item["doc_type"],
                    "date_issued": item["date_issued"],
                    "status": item["status"],
                    "topic": item["topic"],
                    "is_repealed": bool(item["is_repealed"]),
                    "superseded_by": item["superseded_by"] or "",
                    "filename": item["filename"]
                }
            }
            all_chunks.append(chunk_data)

    parsed_out_path = os.path.join(PARSED_DIR, "regulatory_chunks.json")
    with open(parsed_out_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Successfully processed {len(all_chunks)} chunks to {parsed_out_path}")
    return all_chunks

if __name__ == "__main__":
    download_pdfs()
    extract_text_chunks()