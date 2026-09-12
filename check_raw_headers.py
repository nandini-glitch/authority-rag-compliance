import json

d = json.load(open("data/parsed_chunks/regulatory_chunks.json"))

for cid in ["RBI_2025-26_36_chunk_0", "ACB_POL_DL_2024-25_04_chunk_0"]:
    match = [c for c in d if c["chunk_id"] == cid]
    if match:
        print(f"--- {cid} ---")
        print(match[0]["text"][:400])
        print()
