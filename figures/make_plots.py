"""
Builds the paper figures from the two finished runs.

  results/experiment_results.json         standard retrieval (top_k=15)
  results/oracle/experiment_results.json  oracle context (gold evidence chunks)

Run from the repo root:   python figures/make_plots.py
Writes PNG (300 dpi) + PDF (vector) to figures/out/ and a numbers summary to figures/out/summary.txt.
Only the three core conditions are plotted.
"""
import json
import math
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures" / "out"
OUT.mkdir(parents=True, exist_ok=True)

MODES = ["naive", "recency_only", "full"]
MODE_LABEL = {"naive": "Naive", "recency_only": "Recency-only", "full": "Full\n(authority+recency)"}
MODE_COLOR = {"naive": "#9e9e9e", "recency_only": "#e69f00", "full": "#0072b2"}
MODE_HATCH = {"naive": "", "recency_only": "///", "full": "xx"}
RUNS = {"Standard retrieval (top-$k$=15)": ROOT / "results" / "experiment_results.json",
        "Oracle context (gold chunks)": ROOT / "results" / "oracle" / "experiment_results.json"}
CASE_TYPES = ["temporal", "authority", "control"]
OK = "AUTHORITY_CORRECT_RESOLUTION"
CATS = ["AUTHORITY_CORRECT_RESOLUTION", "FRANKENSTEIN_BLENDING", "OUTDATED_RULE_SELECTED", "PARAMETRIC_LEAKAGE"]
CAT_LABEL = {CATS[0]: "Correct", CATS[1]: "Blended (judge label)", CATS[2]: "Wrong rule selected", CATS[3]: "Parametric"}
CAT_COLOR = {CATS[0]: "#2a9d5c", CATS[1]: "#f4a261", CATS[2]: "#d1495b", CATS[3]: "#7b6fb0"}
CAT_HATCH = {CATS[0]: "", CATS[1]: "..", CATS[2]: "//", CATS[3]: "\\\\"}

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5, "legend.fontsize": 7,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 42,
})
COL, DBL = 3.5, 7.16   # IEEE single / double column width (inches)


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def load():
    runs = {}
    for name, path in RUNS.items():
        if path.exists():
            runs[name] = json.load(open(path, encoding="utf-8"))
        else:
            print(f"[skip] {path} not found")
    if not runs:
        raise SystemExit("No results found. Run from the repo root after the experiments finished.")
    return runs


def cls(rec, m):
    return rec["modes"][m]["eval"]["classification"] if m in rec["modes"] else None


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}")
    plt.close(fig)
    print(f"saved figures/out/{name}.png/.pdf")


def fig_accuracy(runs, log):
    fig, ax = plt.subplots(figsize=(COL, 2.7))
    names = list(runs)
    w = 0.8 / len(names)
    shades = [1.0, 0.55]
    for j, name in enumerate(names):
        for i, m in enumerate(MODES):
            recs = runs[name]
            n = len(recs)
            k = sum(cls(r, m) == OK for r in recs)
            p = k / n * 100
            lo, hi = wilson(k, n)
            x = i + (j - (len(names) - 1) / 2) * w
            ax.bar(x, p, w * 0.92, color=MODE_COLOR[m], alpha=shades[j % 2], hatch=MODE_HATCH[m],
                   edgecolor="black", linewidth=0.5)
            ax.errorbar(x, p, yerr=[[p - lo * 100], [hi * 100 - p]], color="black", capsize=2, lw=0.7)
            ax.text(x, hi * 100 + 2, f"{k}/{n}", ha="center", va="bottom", fontsize=6.5)
            log.append(f"accuracy | {name} | {m}: {k}/{n} = {p:.1f}%  (Wilson 95% CI {lo*100:.1f}-{hi*100:.1f})")
    ax.set_xticks(range(len(MODES)))
    ax.set_xticklabels([MODE_LABEL[m] for m in MODES])
    ax.set_ylabel("Correct resolution (%)")
    ax.set_ylim(0, 118)
    ax.set_yticks(range(0, 101, 20))
    handles = [plt.Rectangle((0, 0), 1, 1, fc="#444", alpha=shades[j % 2], ec="black", lw=0.5) for j in range(len(names))]
    ax.legend(handles, names, loc="upper left", frameon=False, ncol=1)
    save(fig, "fig1_accuracy_by_condition")


def fig_by_type(runs, log):
    names = list(runs)
    fig, axes = plt.subplots(1, len(names), figsize=(DBL if len(names) > 1 else COL * 1.4, 2.6), sharey=True, squeeze=False)
    for ax, name in zip(axes[0], names):
        recs = runs[name]
        w = 0.26
        for i, m in enumerate(MODES):
            for t_i, t in enumerate(CASE_TYPES):
                sub = [r for r in recs if r.get("case_type") == t]
                n = len(sub)
                if not n:
                    continue
                k = sum(cls(r, m) == OK for r in sub)
                x = t_i + (i - 1) * w
                ax.bar(x, k / n * 100, w * 0.92, color=MODE_COLOR[m], hatch=MODE_HATCH[m], edgecolor="black", linewidth=0.5,
                       label=MODE_LABEL[m].replace("\n", " ") if t_i == 0 else None)
                ax.text(x, k / n * 100 + 2, f"{k}/{n}", ha="center", va="bottom", fontsize=6.5)
                log.append(f"by type | {name} | {t} | {m}: {k}/{n}")
        ax.set_xticks(range(len(CASE_TYPES)))
        ax.set_xticklabels([f"{t.capitalize()}\n(n={sum(r.get('case_type') == t for r in recs)})" for t in CASE_TYPES])
        ax.set_title(name)
        ax.set_ylim(0, 118)
        ax.set_yticks(range(0, 101, 20))
    axes[0][0].set_ylabel("Correct resolution (%)")
    handles = [plt.Rectangle((0, 0), 1, 1, fc=MODE_COLOR[m], hatch=MODE_HATCH[m], ec="black", lw=0.5) for m in MODES]
    fig.legend(handles, [MODE_LABEL[m].replace("\n", " ") for m in MODES], loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save(fig, "fig2_accuracy_by_case_type")


def fig_failures(runs, log):
    names = list(runs)
    fig, axes = plt.subplots(1, len(names), figsize=(DBL if len(names) > 1 else COL * 1.4, 2.6), sharey=True, squeeze=False)
    for ax, name in zip(axes[0], names):
        recs = runs[name]
        bottom = np.zeros(len(MODES))
        for c in CATS:
            vals = np.array([sum(cls(r, m) == c for r in recs) for m in MODES])
            ax.bar(range(len(MODES)), vals, 0.6, bottom=bottom, color=CAT_COLOR[c], hatch=CAT_HATCH[c], edgecolor="black",
                   linewidth=0.5, label=CAT_LABEL[c])
            for x, (v, b) in enumerate(zip(vals, bottom)):
                if v:
                    ax.text(x, b + v / 2, str(v), ha="center", va="center", fontsize=7, color="black",
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
            for m, v in zip(MODES, vals):
                log.append(f"outcomes | {name} | {m} | {CAT_LABEL[c]}: {v}")
            bottom += vals
        ax.set_xticks(range(len(MODES)))
        ax.set_xticklabels([MODE_LABEL[m] for m in MODES])
        ax.set_title(name)
        ax.set_ylim(0, len(recs) + 1)
        ax.set_yticks(range(0, len(recs) + 1, 4))
    axes[0][0].set_ylabel("Number of test cases")
    axes[0][-1].legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    fig.tight_layout()
    save(fig, "fig3_outcome_breakdown")


def fig_heatmap(runs, log):
    names = list(runs)
    n_cases = max(len(r) for r in runs.values())
    fig, axes = plt.subplots(1, len(names), figsize=(DBL if len(names) > 1 else COL * 1.4, 0.19 * n_cases + 1.1), sharey=True, squeeze=False)
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap([CAT_COLOR[c] for c in CATS])
    symbol = {CATS[0]: "C", CATS[1]: "B", CATS[2]: "W", CATS[3]: "P"}
    for ax, name in zip(axes[0], names):
        recs = runs[name]
        grid = np.array([[CATS.index(cls(r, m)) if cls(r, m) in CATS else 0 for m in MODES] for r in recs])
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=len(CATS) - 1, aspect="auto")
        for i, r in enumerate(recs):
            for j, m in enumerate(MODES):
                ax.text(j, i, symbol.get(cls(r, m), "?"), ha="center", va="center", fontsize=7, color="white", fontweight="bold")
        ax.set_xticks(range(len(MODES)))
        ax.set_xticklabels([MODE_LABEL[m].replace("\n", " ") for m in MODES], rotation=20, ha="right")
        ax.set_yticks(range(len(recs)))
        ax.set_yticklabels([r["id"].split("-")[0] for r in recs])
        ax.set_title(name)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
    handles = [plt.Rectangle((0, 0), 1, 1, fc=CAT_COLOR[c]) for c in CATS]
    fig.legend(handles, [f"{symbol[c]} {CAT_LABEL[c]}" for c in CATS], loc="lower center", ncol=4, frameon=False, fontsize=7)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "fig4_case_heatmap")


def main():
    runs = load()
    log = []
    fig_accuracy(runs, log)
    fig_by_type(runs, log)
    fig_failures(runs, log)
    fig_heatmap(runs, log)
    (OUT / "summary.txt").write_text("\n".join(log), encoding="utf-8")
    print("numbers used in the figures: figures/out/summary.txt")


if __name__ == "__main__":
    main()
