import json

d = json.load(open("results/experiment_results.json"))
tc03 = [c for c in d if c["id"] == "TC-03-DLG-FLDG-CAP"][0]

print("CLASSIFICATION:", tc03["modes"]["full"]["eval"]["classification"])
print("JUDGE REASONING:", tc03["modes"]["full"]["eval"]["reasoning"])
print()
print("FULL RESPONSE:")
print(tc03["modes"]["full"]["response"])
print()
print("RETRIEVED DOC IDS:", tc03["modes"]["full"]["retrieved_doc_ids"])
