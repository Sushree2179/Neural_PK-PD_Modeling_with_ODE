"""
Generate all thesis figures and save to:
  Thesis_Latex/2. thesis/figures/

Run from the Coding/ directory with venv_pkpd active.
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE, "data", "raw")
OUT_DIR = os.path.join(BASE, "..", "Thesis_Latex", "2. thesis", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ── style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.fontsize": 10,
    "figure.constrained_layout.use": True,
})

# ══════════════════════════════════════════════════════════════════════════════
# Figure 5.1 – ChEMBL Binding Affinity Overview
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 5.1 – ChEMBL binding affinity …")
df_chem = pd.read_csv(os.path.join(DATA_RAW, "chembl", "chembl_binding_affinity.csv"))

# Identify pIC50-like column
pic50_col = next(
    (c for c in df_chem.columns if "pic50" in c.lower() or "pchembl" in c.lower() or "value" in c.lower()),
    None,
)
target_col = next(
    (c for c in df_chem.columns if "target" in c.lower() or "gene" in c.lower() or "protein" in c.lower()),
    None,
)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Left: pIC50 histogram
if pic50_col:
    raw = pd.to_numeric(df_chem[pic50_col], errors="coerce").dropna()
    # Convert nM IC50 → pIC50 if values look like nM (> 100 suggests concentration not log)
    if raw.median() > 100:
        vals = 9 - np.log10(raw.clip(lower=1e-6))  # IC50 in nM → pIC50
        xlabel = "pIC50 (converted from IC50 [nM])"
    else:
        vals = raw
        xlabel = "pIC50 (–log₁₀ IC50 [M])"
    ax = axes[0]
    ax.hist(vals, bins=40, color="#3B82F6", edgecolor="white", linewidth=0.4)
    ax.axvline(vals.mean(), color="#EF4444", linestyle="--", linewidth=1.2,
               label=f"Mean = {vals.mean():.2f}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of compounds")
    ax.set_title("Binding Affinity Distribution")
    ax.legend()
    print(f"  {pic50_col}: {len(vals):,} values, mean pIC50={vals.mean():.2f}")
else:
    axes[0].text(0.5, 0.5, "pIC50 column not found", ha="center", va="center")
    axes[0].set_title("Binding Affinity Distribution")

# Right: top-10 targets by compound count
if target_col:
    top = df_chem[target_col].value_counts().head(10)
    # shorten long names
    labels = [str(t)[:30] for t in top.index]
    ax2 = axes[1]
    bars = ax2.barh(range(len(top)), top.values, color="#6366F1", edgecolor="white", linewidth=0.3)
    ax2.set_yticks(range(len(top)))
    ax2.set_yticklabels(labels, fontsize=9)
    ax2.invert_yaxis()
    ax2.set_xlabel("Number of compounds")
    ax2.set_title("Top 10 Protein Targets")
    for bar, v in zip(bars, top.values):
        ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                 str(v), va="center", fontsize=8)
else:
    axes[1].text(0.5, 0.5, "Target column not found", ha="center", va="center")
    axes[1].set_title("Top Protein Targets")

fig.suptitle("Figure 5.1: ChEMBL Binding Affinity Dataset Overview", fontsize=12, y=1.01)
out = os.path.join(OUT_DIR, "fig5_1_chembl_binding.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 5.2 – ToxCast Toxicity Stratification
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 5.2 – ToxCast toxicity …")

frames = []
labels_map = {"critical": "Critical", "high": "High", "representative": "Representative"}
for key in labels_map:
    path = os.path.join(DATA_RAW, "toxcast", f"toxcast_{key}_priority.csv")
    if os.path.exists(path):
        tmp = pd.read_csv(path)
        tmp["risk_tier"] = labels_map[key]
        frames.append(tmp)

if frames:
    df_tox = pd.concat(frames, ignore_index=True)
    print(f"  ToxCast rows: {len(df_tox):,}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # Left: risk-tier bar chart
    tier_counts = df_tox["risk_tier"].value_counts().reindex(
        ["Critical", "High", "Representative"], fill_value=0
    )
    colors = ["#EF4444", "#F97316", "#22C55E"]
    ax = axes[0]
    bars = ax.bar(tier_counts.index, tier_counts.values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_ylabel("Number of compounds")
    ax.set_title("Compounds by Risk Tier")
    for bar, v in zip(bars, tier_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(v), ha="center", va="bottom", fontsize=10)

    # Right: toxicity endpoint availability heatmap / category bar
    tox_cols = [c for c in df_tox.columns
                if c not in ("SMILES", "smiles", "risk_tier") and df_tox[c].dtype in (float, int)]
    if len(tox_cols) >= 2:
        active_frac = df_tox[tox_cols[:10]].apply(
            lambda c: (pd.to_numeric(c, errors="coerce") == 1).mean()
        )
        ax2 = axes[1]
        ax2.barh(active_frac.index, active_frac.values * 100, color="#A78BFA", edgecolor="white", linewidth=0.3)
        ax2.set_xlabel("% active compounds")
        ax2.set_title("Endpoint Activity Rates (top 10 assays)")
        ax2.set_xlim(0, 100)
    else:
        # Fallback: total compounds per tier as pie
        ax2 = axes[1]
        ax2.pie(tier_counts.values, labels=tier_counts.index, colors=colors, autopct="%1.0f%%",
                startangle=90)
        ax2.set_title("Risk Tier Proportions")

    fig.suptitle("Figure 5.2: ToxCast Toxicity Dataset Stratification", fontsize=12, y=1.01)
else:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, "ToxCast data not found", ha="center", va="center")
    fig.suptitle("Figure 5.2: ToxCast (data unavailable)")

out = os.path.join(OUT_DIR, "fig5_2_toxcast_risk.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 5.3 – TDC ADMET Dataset Overview
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 5.3 – TDC ADMET …")

fig = plt.figure(figsize=(13, 4))
gs = GridSpec(1, 3, figure=fig, wspace=0.35)

# hERG – binary
ax1 = fig.add_subplot(gs[0])
herg_path = os.path.join(DATA_RAW, "tdc", "tdc_herg.csv")
if os.path.exists(herg_path):
    df_herg = pd.read_csv(herg_path)
    label_col = next((c for c in df_herg.columns if "label" in c.lower() or "y" == c.lower()), None)
    if label_col:
        vc = df_herg[label_col].value_counts().sort_index()
        ax1.bar(["hERG-safe\n(0)", "hERG-blocker\n(1)"],
                [vc.get(0, 0), vc.get(1, 0)],
                color=["#22C55E", "#EF4444"], edgecolor="white", linewidth=0.5)
        ax1.set_ylabel("Number of compounds")
        total = vc.sum()
        pos_rate = vc.get(1, 0) / total * 100
        ax1.set_title(f"hERG Cardiotoxicity\n({total:,} compounds, {pos_rate:.0f}% blockers)")
        print(f"  hERG: {total:,} compounds, {pos_rate:.0f}% positive")
    else:
        ax1.text(0.5, 0.5, "label col not found", ha="center", va="center")
        ax1.set_title("hERG Cardiotoxicity")
else:
    ax1.text(0.5, 0.5, "File not found", ha="center", va="center")
    ax1.set_title("hERG Cardiotoxicity")

# Caco-2 – continuous
ax2 = fig.add_subplot(gs[1])
caco_path = os.path.join(DATA_RAW, "tdc", "tdc_caco2_wang.csv")
if os.path.exists(caco_path):
    df_caco = pd.read_csv(caco_path)
    val_col = next((c for c in df_caco.columns if "y" in c.lower() and df_caco[c].dtype in (float, int)), None)
    if val_col is None:
        numeric_cols = df_caco.select_dtypes(include=[float, int]).columns
        val_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    if val_col:
        vals = pd.to_numeric(df_caco[val_col], errors="coerce").dropna()
        ax2.hist(vals, bins=35, color="#3B82F6", edgecolor="white", linewidth=0.4)
        ax2.axvline(vals.median(), color="#EF4444", linestyle="--", linewidth=1.2,
                    label=f"Median = {vals.median():.2f}")
        ax2.set_xlabel("log₁₀ Papp (cm/s)")
        ax2.set_ylabel("Count")
        ax2.set_title(f"Caco-2 Permeability\n({len(vals):,} compounds)")
        ax2.legend()
        print(f"  Caco-2: {len(vals):,} compounds, median={vals.median():.2f}")
    else:
        ax2.text(0.5, 0.5, "Value col not found", ha="center", va="center")
        ax2.set_title("Caco-2 Permeability")
else:
    ax2.text(0.5, 0.5, "File not found", ha="center", va="center")
    ax2.set_title("Caco-2 Permeability")

# Clearance – continuous
ax3 = fig.add_subplot(gs[2])
clr_path = os.path.join(DATA_RAW, "tdc", "tdc_clearance_hepatocyte_az.csv")
if os.path.exists(clr_path):
    df_clr = pd.read_csv(clr_path)
    val_col = next((c for c in df_clr.columns if "y" in c.lower() and df_clr[c].dtype in (float, int)), None)
    if val_col is None:
        numeric_cols = df_clr.select_dtypes(include=[float, int]).columns
        val_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    if val_col:
        vals = pd.to_numeric(df_clr[val_col], errors="coerce").dropna()
        # log transform for readability if wide range
        if vals.max() / (vals.min() + 1e-9) > 100:
            ax3.hist(np.log10(vals + 1e-6), bins=35, color="#A78BFA", edgecolor="white", linewidth=0.4)
            ax3.set_xlabel("log₁₀ Hepatic Clearance (mL/min/kg)")
        else:
            ax3.hist(vals, bins=35, color="#A78BFA", edgecolor="white", linewidth=0.4)
            ax3.set_xlabel("Hepatic Clearance (mL/min/kg)")
        ax3.set_ylabel("Count")
        ax3.set_title(f"Hepatic Clearance\n({len(vals):,} compounds)")
        print(f"  Clearance: {len(vals):,} compounds")
    else:
        ax3.text(0.5, 0.5, "Value col not found", ha="center", va="center")
        ax3.set_title("Hepatic Clearance")
else:
    ax3.text(0.5, 0.5, "File not found", ha="center", va="center")
    ax3.set_title("Hepatic Clearance")

fig.suptitle("Figure 5.3: TDC ADMET Dataset Overview", fontsize=12, y=1.02)
out = os.path.join(OUT_DIR, "fig5_3_tdc_admet.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 8.1 – Training History (already generated; copy it)
# ══════════════════════════════════════════════════════════════════════════════
print("Processing training_history.png …")
src = os.path.join(BASE, "training_history.png")
if os.path.exists(src):
    shutil.copy2(src, os.path.join(OUT_DIR, "fig8_1_training_history.png"))
    print(f"  Copied → fig8_1_training_history.png")
else:
    print("  training_history.png not found – skipping")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 8.2 – PK Curves (already generated; copy it)
# ══════════════════════════════════════════════════════════════════════════════
print("Processing pk_curves.png …")
src = os.path.join(BASE, "pk_curves.png")
if os.path.exists(src):
    shutil.copy2(src, os.path.join(OUT_DIR, "fig8_2_pk_curves.png"))
    print(f"  Copied → fig8_2_pk_curves.png")
else:
    print("  pk_curves.png not found – skipping")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 8.3 – Model Performance Summary (bar chart from known metrics)
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 8.3 – performance summary …")
metrics = {
    "hERG\nAUROC": (0.8206, 0.80),
    "Caco-2\nAUROC": (0.8635, 0.75),
    "Clearance\nR²": (0.3478, 0.20),
    "Binding\nR²": (0.5502, 0.40),
}
names = list(metrics.keys())
achieved = [v[0] for v in metrics.values()]
targets  = [v[1] for v in metrics.values()]

fig, ax = plt.subplots(figsize=(9, 4.5))
x = np.arange(len(names))
w = 0.35
bars1 = ax.bar(x - w/2, achieved, w, label="Achieved", color="#3B82F6", edgecolor="white")
bars2 = ax.bar(x + w/2, targets,  w, label="Target",   color="#D1D5DB", edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=11)
ax.set_ylim(0, 1.0)
ax.set_ylabel("Score")
ax.set_title("Final Model Performance vs. Research Targets")
ax.legend()
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
            f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=9, color="#1D4ED8")
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
            f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9, color="#6B7280")
fig.suptitle("Figure 8.3: Model Performance Summary", fontsize=12)
out = os.path.join(OUT_DIR, "fig8_3_performance_summary.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 8.4 – Calibration Before / After (ECE bar chart)
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 8.4 – calibration ECE …")
tasks   = ["hERG", "Caco-2"]
before  = [0.1727, 0.3583]
after   = [0.0058, 0.0448]

fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(len(tasks))
w = 0.3
ax.bar(x - w/2, before, w, label="Before calibration", color="#F97316", edgecolor="white")
ax.bar(x + w/2, after,  w, label="After temperature scaling", color="#22C55E", edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(tasks)
ax.set_ylabel("Expected Calibration Error (ECE)")
ax.set_title("Probability Calibration: ECE Before vs. After Temperature Scaling")
ax.legend()
for vals, offset in [(before, -w/2), (after, w/2)]:
    for xi, v in zip(x, vals):
        ax.text(xi + offset, v + 0.003, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
fig.suptitle("Figure 8.4: Calibration Results", fontsize=12)
out = os.path.join(OUT_DIR, "fig8_4_calibration_ece.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 8.5 – Experiment Progression
# ══════════════════════════════════════════════════════════════════════════════
print("Generating Figure 8.5 – experiment progression …")
exps = [
    "Baseline\n(256-bit, syn.)",
    "Real SMILES\n2048-bit",
    "Real Binding\nSMILES",
    "hERG Push\n(model_15)",
    "GNN\nEncoder",
    "Joint Fusion\nGNN+MLP",
]
herg   = [0.4836, 0.6989, 0.7738, 0.8206, None, None]
caco2  = [0.4719, 0.8550, 0.8713, 0.8635, None, None]
clr_r2 = [0.0037, 0.2115, 0.3013, 0.3478, None, None]
bind   = [None, None, 0.4306, 0.4521, 0.4115, 0.5502]

def clean(lst):
    return [v if v is not None else np.nan for v in lst]

xi = np.arange(len(exps))
fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharex=True)
specs = [
    (axes[0, 0], clean(herg),   "#3B82F6", "hERG AUROC",       0.80, "Target ≥ 0.80"),
    (axes[0, 1], clean(caco2),  "#6366F1", "Caco-2 AUROC",     0.75, "Target ≥ 0.75"),
    (axes[1, 0], clean(clr_r2), "#22C55E", "Clearance R²",     0.20, "Target ≥ 0.20"),
    (axes[1, 1], clean(bind),   "#F97316", "Binding R²",       0.40, "Target ≥ 0.40"),
]
for ax, vals, color, title, tgt, tgt_label in specs:
    ax.plot(xi, vals, "o-", color=color, linewidth=2, markersize=7, clip_on=False)
    ax.axhline(tgt, color="#EF4444", linestyle="--", linewidth=1, label=tgt_label)
    ax.set_xticks(xi)
    ax.set_xticklabels(exps, fontsize=8, rotation=10)
    ax.set_title(title)
    ax.legend(fontsize=8)
fig.suptitle("Figure 8.5: Metric Progression Across All Experiments", fontsize=12)
out = os.path.join(OUT_DIR, "fig8_5_experiment_progression.pdf")
fig.savefig(out, bbox_inches="tight")
plt.close(fig)
print(f"  Saved → {out}")

# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════
print("\n✓ All figures generated in:", OUT_DIR)
for f in sorted(os.listdir(OUT_DIR)):
    size = os.path.getsize(os.path.join(OUT_DIR, f))
    print(f"  {f}  ({size//1024} KB)")
