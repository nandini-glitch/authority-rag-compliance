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
        # rbidocs.rbi.org.in is captcha-walled for automated clients -
        # use this mirror instead (verified working, plain PDF)
        "url": "https://fidcindia.org.in/wp-content/uploads/2022/09/RBI-GUIDELINES-ON-DIGITAL-LENDING-02-09-22.pdf",
        "filename": "rbi_digital_lending_2022.pdf",
        "issuer": "Reserve Bank of India",
        "authority_tier": 1,
        "doc_type": "Guidelines",
        "date_issued": "2022-09-02",
        "status": "outdated"
    },
    {
        "doc_id": "RBI/2025-26/DL_Directions",
        # Corrected: repealed by "Directions, 2025", not a 2024 Master Direction
        "title": "Reserve Bank of India (Digital Lending) Directions, 2025",
        "url": "https://www.axis.bank.in/docs/default-source/default-document-library/reserve-bank-of-india-digital-lending-directions2025.pdf",
        "filename": "rbi_digital_lending_2025.pdf",
        "issuer": "Reserve Bank of India",
        "authority_tier": 1,
        "doc_type": "Directions",
        "date_issued": "2025-05-08",
        "status": "current"
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


def extract_text_chunks(chunk_size: int = 1000) -> List[Dict[str, Any]]:
    """Parses downloaded PDFs into metadata-enriched text chunks."""
    all_chunks = []

    for item in DOCUMENT_SOURCES:
        pdf_path = os.path.join(RAW_DIR, item["filename"])
        if not os.path.exists(pdf_path):
            print(f"Skipping {item['filename']} (file does not exist)")
            continue

        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        if not full_text.strip():
            print(f"Warning: no extractable text in {item['filename']} "
                  f"(may be a scanned/image PDF - needs OCR)")
            continue

        for i in range(0, len(full_text), chunk_size - 100):
            chunk_text = full_text[i:i + chunk_size].strip()
            if len(chunk_text) < 100:
                continue

            chunk_id = f"{item['doc_id'].replace('/', '_')}_chunk_{i // chunk_size}"
            chunk_data = {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "doc_id": item["doc_id"],
                    "issuer": item["issuer"],
                    "authority_tier": item["authority_tier"],
                    "doc_type": item["doc_type"],
                    "date_issued": item["date_issued"],
                    "status": item["status"],
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