#!/usr/bin/env python3
"""
Export thesis figures from notebook to PDF format.
Generates Figures 5.1, 5.2, 5.3 for inclusion in LaTeX document.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
NOTEBOOK_DIR = Path("/Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Coding")
DATA_DIR = NOTEBOOK_DIR / "data" / "raw"
FIGURE_DIR = Path("/Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Thesis_Latex/figures")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Style configuration
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

print("Loading data...")
# Load ChEMBL
try:
    chembl_df = pd.read_csv(DATA_DIR / "s1_chembl.csv")
    print(f"✓ ChEMBL: {len(chembl_df)} records")
except Exception as e:
    print(f"✗ ChEMBL loading failed: {e}")
    chembl_df = None

# Load ToxCast
try:
    toxcast_df = pd.read_csv(DATA_DIR / "s2_toxcast.csv")
    print(f"✓ ToxCast: {len(toxcast_df)} records")
except Exception as e:
    print(f"✗ ToxCast loading failed: {e}")
    toxcast_df = None

# Load TDC data
try:
    tdc_herg = pd.read_csv(DATA_DIR / "s3a_tdc_herg.csv")
    tdc_caco2 = pd.read_csv(DATA_DIR / "s3b_tdc_caco2.csv")
    tdc_clearance = pd.read_csv(DATA_DIR / "s3c_tdc_clearance.csv")
    print(f"✓ TDC hERG: {len(tdc_herg)} records")
    print(f"✓ TDC Caco-2: {len(tdc_caco2)} records")
    print(f"✓ TDC Clearance: {len(tdc_clearance)} records")
except Exception as e:
    print(f"✗ TDC loading failed: {e}")
    tdc_herg = tdc_caco2 = tdc_clearance = None

# ============================================================================
# FIGURE 5.1: ChEMBL Binding Affinity & Targets
# ============================================================================
print("\nGenerating Figure 5.1 (ChEMBL)...")
if chembl_df is not None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: pIC50 distribution
    pic50_values = chembl_df['Y'].dropna()
    axes[0].hist(pic50_values, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(pic50_values.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {pic50_values.mean():.2f}')
    axes[0].set_xlabel('pIC50 (Binding Affinity)', fontsize=11)
    axes[0].set_ylabel('Frequency', fontsize=11)
    axes[0].set_title('ChEMBL Binding Affinity Distribution', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Panel B: Top 10 targets
    target_counts = chembl_df['Target'].value_counts().head(10)
    axes[1].barh(range(len(target_counts)), target_counts.values, color='skyblue', edgecolor='black')
    axes[1].set_yticks(range(len(target_counts)))
    axes[1].set_yticklabels(target_counts.index, fontsize=9)
    axes[1].set_xlabel('Number of Compounds', fontsize=11)
    axes[1].set_title('Top 10 Targets in ChEMBL Data', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    fig_path = FIGURE_DIR / "fig5_1_chembl_binding.pdf"
    plt.savefig(fig_path, format='pdf', bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {fig_path}")
    plt.close()

# ============================================================================
# FIGURE 5.2: ToxCast Risk Levels & Categories
# ============================================================================
print("Generating Figure 5.2 (ToxCast)...")
if toxcast_df is not None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: Risk level distribution
    risk_mapping = {'CRITICAL': 1, 'HIGH': 2, 'MEDIUM': 3, 'LOW': 4}
    toxcast_df['risk_level'] = toxcast_df['Risk Level'].map(risk_mapping)
    risk_counts = toxcast_df['Risk Level'].value_counts()
    
    colors = {'CRITICAL': 'red', 'HIGH': 'yellow', 'MEDIUM': 'orange', 'LOW': 'lightblue'}
    risk_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    risk_counts = risk_counts.reindex([r for r in risk_order if r in risk_counts.index])
    risk_colors = [colors.get(r, 'gray') for r in risk_counts.index]
    
    axes[0].bar(range(len(risk_counts)), risk_counts.values, color=risk_colors, edgecolor='black')
    axes[0].set_xticks(range(len(risk_counts)))
    axes[0].set_xticklabels(risk_counts.index, fontsize=10)
    axes[0].set_ylabel('Count', fontsize=11)
    axes[0].set_title('ToxCast Risk Level Distribution', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Panel B: Toxicity categories
    if 'Toxicity Category' in toxcast_df.columns:
        cat_counts = toxcast_df['Toxicity Category'].value_counts()
        axes[1].bar(range(len(cat_counts)), cat_counts.values, color='steelblue', edgecolor='black')
        axes[1].set_xticks(range(len(cat_counts)))
        axes[1].set_xticklabels(cat_counts.index, rotation=45, ha='right', fontsize=9)
        axes[1].set_ylabel('Count', fontsize=11)
        axes[1].set_title('Toxicity Categories', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig_path = FIGURE_DIR / "fig5_2_toxcast_risk.pdf"
    plt.savefig(fig_path, format='pdf', bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {fig_path}")
    plt.close()

# ============================================================================
# FIGURE 5.3: TDC ADMET Properties
# ============================================================================
print("Generating Figure 5.3 (TDC ADMET)...")
if tdc_herg is not None and tdc_caco2 is not None and tdc_clearance is not None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Panel A: hERG binary classification
    if 'Y' in tdc_herg.columns:
        herg_counts = tdc_herg['Y'].value_counts()
        herg_labels = ['Non-inhibitor', 'Inhibitor'] if 0 in herg_counts.index else ['Inhibitor', 'Non-inhibitor']
        herg_values = [herg_counts.get(0, 0), herg_counts.get(1, 0)]
        colors_herg = ['green', 'red']
        axes[0].bar(herg_labels, herg_values, color=colors_herg, edgecolor='black', alpha=0.8)
        axes[0].set_ylabel('Count', fontsize=11)
        axes[0].set_title('TDC hERG Inhibition', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
    
    # Panel B: Caco-2 permeability
    if 'Y' in tdc_caco2.columns:
        caco2_values = pd.to_numeric(tdc_caco2['Y'], errors='coerce').dropna()
        axes[1].hist(caco2_values, bins=40, color='steelblue', edgecolor='black', alpha=0.7)
        axes[1].axvline(caco2_values.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {caco2_values.mean():.2f}')
        axes[1].set_xlabel('Caco-2 Permeability (log unit)', fontsize=11)
        axes[1].set_ylabel('Frequency', fontsize=11)
        axes[1].set_title('TDC Caco-2 Permeability', fontsize=12, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    
    # Panel C: Hepatocyte clearance
    if 'Y' in tdc_clearance.columns:
        clearance_values = pd.to_numeric(tdc_clearance['Y'], errors='coerce').dropna()
        axes[2].hist(clearance_values, bins=40, color='orange', edgecolor='black', alpha=0.7)
        axes[2].axvline(clearance_values.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {clearance_values.mean():.2f}')
        axes[2].set_xlabel('Clearance (mL/min/kg)', fontsize=11)
        axes[2].set_ylabel('Frequency', fontsize=11)
        axes[2].set_title('TDC Hepatocyte Clearance', fontsize=12, fontweight='bold')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig_path = FIGURE_DIR / "fig5_3_tdc_admet.pdf"
    plt.savefig(fig_path, format='pdf', bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {fig_path}")
    plt.close()

print("\n" + "="*60)
print("✓ All figures exported successfully!")
print(f"  Location: {FIGURE_DIR}")
print("="*60)
