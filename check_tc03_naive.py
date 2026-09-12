import json

d = json.load(open("results/experiment_results.json"))
tc03 = [c for c in d if c["id"] == "TC-03-DLG-FLDG-CAP"][0]

naive = tc03["modes"]["naive"]
print("CLASSIFICATION:", naive["eval"]["classification"])
print("JUDGE REASONING:", naive["eval"]["reasoning"])
print()
print("RESPONSE:")
print(naive["response"])
print()
print("RETRIEVED DOC IDS:", naive["retrieved_doc_ids"])
print("Number of unique doc_ids:", len(set(naive["retrieved_doc_ids"])))
