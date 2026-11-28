"""
Terminal labeller for the blind audit sheet. Shows one answer at a time (condition and judge label hidden),
takes one keystroke, saves after every label, and resumes where you stopped.

Usage: python -m src.label_audit      (add RETRIEVAL_MODE=oracle for results/oracle/)
Do NOT re-run make_audit_sheet afterwards: it would overwrite your labels.
"""
import csv
import os
import textwrap

RESULTS_DIR = "results/oracle" if os.getenv("RETRIEVAL_MODE") == "oracle" else "results"
PATH = f"{RESULTS_DIR}/audit_sheet.csv"
KEYS = {"c": "CORRECT", "w": "WRONG_RULE", "u": "UNRESOLVED", "b": "BLEND", "o": "OTHER"}
PROMPT = "label:  [c]orrect  [w]rong_rule  [u]nresolved  [b]lend  [o]ther   |  [s]kip  [q]uit  > "

GUIDE = """
CORRECT     gives the ground-truth answer AND treats the superseded / lower-authority rule as not applicable
WRONG_RULE  commits to the superseded or lower-authority rule as the answer
UNRESOLVED  reports both rules without committing to which one applies
BLEND       invents a compromise or mixed rule that neither source states
OTHER       anything else (ignores the sources, off-topic, refuses)
Judge against the ground truth only. Do not guess which condition produced the answer.
"""


def wrap(text, width=100):
    return "\n".join(textwrap.fill(p, width) if p.strip() else "" for p in text.splitlines())


def save(rows, header):
    with open(PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def main():
    rows = list(csv.DictReader(open(PATH, encoding="utf-8")))
    header = list(rows[0].keys())
    todo = [r for r in rows if not r["human_label"].strip()]
    done = len(rows) - len(todo)
    print(GUIDE)
    print(f"{done}/{len(rows)} already labelled.")
    for i, r in enumerate(todo, start=1):
        print("\n" + "=" * 100)
        print(f"[{r['audit_id']}]   answer {done + i} of {len(rows)}")
        print("-" * 100)
        print("QUESTION:\n" + wrap(r["query"]))
        print("\nGROUND TRUTH:\n" + wrap(r["ground_truth"]))
        print("\nANSWER TO LABEL:\n" + wrap(r["answer"]))
        print()
        while True:
            try:
                a = input(PROMPT).strip().lower()
            except EOFError:
                a = "q"
            if a in KEYS:
                r["human_label"] = KEYS[a]
                save(rows, header)
                break
            if a == "s":
                break
            if a == "q":
                save(rows, header)
                left = sum(1 for x in rows if not x["human_label"].strip())
                print(f"\nSaved. {left} left. Re-run the same command to continue.")
                return
            print("  type one of: c w u b o s q")
    left = sum(1 for x in rows if not x["human_label"].strip())
    print(f"\nFinished. {left} unlabelled (skipped). " + ("Now run score_audit." if left == 0 else "Re-run to label the skipped ones."))


if __name__ == "__main__":
    main()
