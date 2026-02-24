# Neural PK-PD Project: Troubleshooting Guide

**Quick Reference for Issues & Solutions**

---

## 📚 Navigation

- **[← Master Index](../MASTER_INDEX.md)** - All documentation organized by date
- **[Quick Summary →](EXECUTIVE_SUMMARY.md)** - One-page overview
- **[Complete Docs →](PROJECT_SUMMARY.md)** - Full project documentation
- **[Notebook (EDA) →](phase1_2_data_exploration.ipynb)** - Phase 1–2 working code
- **[Notebook (Neural ODE) →](phase3_neural_ode_model.ipynb)** - Phase 3 model code

---

## 🐛 Common Issues & Quick Fixes

### Issue 1: RDKit Not Available After Installation

**Symptoms:**
```
⚠️ Descriptor extraction failed (RDKit may not be available)
```

**Quick Fix:**
1. Restart Jupyter kernel: `Kernel → Restart Kernel`
2. Re-run import cell (Cell 2)
3. Re-run RDKit import cell (Cell 18)

**Why:** Jupyter kernel doesn't recognize newly installed packages until restart.

---

### Issue 2: AttributeError - FractionCsp3

**Error:**
```python
AttributeError: module 'rdkit.Chem.Descriptors' has no attribute 'FractionCsp3'
```

**Solution:**
Replace `FractionCsp3` descriptor with alternative:
```python
# Instead of:
'FractionCSP3': Descriptors.FractionCsp3(mol)

# Use:
'NumRings': Descriptors.RingCount(mol)
```

**Why:** `FractionCsp3` not available in all RDKit versions.

---

### Issue 3: KeyError - Columns Not in Index

**Error:**
```python
KeyError: "['HBA', 'HBD'] not in index"
```

**Solution:**
Check column availability before accessing:
```python
# Instead of:
df[['MW', 'LogP', 'HBA', 'HBD']]

# Use:
available_cols = [col for col in ['MW', 'LogP', 'HBA', 'HBD'] if col in df.columns]
df[available_cols]
```

**Why:** Different datasets have different descriptor columns.

---

### Issue 4: Kernel Shows Wrong Environment

**Symptoms:**
- Kernel shows "test_env" instead of "venv_pkpd"
- Packages not found despite installation

**Solution:**
1. Check kernel metadata in notebook
2. Update kernel selection: `Kernel → Change Kernel → venv_pkpd`
3. Verify with: `import sys; print(sys.executable)`

---

### Issue 5: Cannot Merge Datasets on SMILES

**Problem:**
SMILES are anonymized IDs ("SMILES_0"), not actual chemical structures.

**Solution:**
Use multi-task learning instead of merging:
```python
# Concatenate datasets with task labels
unified_features = pd.concat([
    chembl_data,
    tdc_data_herg,
    tdc_data_caco2,
    tdc_data_clearance
])
```

**Advantage:** 13,030 samples vs ~2,000 from single dataset.

---

### Issue 6: Cells Show Errors After Kernel Restart

**Symptoms:**
Previous cell outputs show errors, but notebook worked before.

**Solution:**
1. Old execution outputs are stale
2. Clear all outputs: `Edit → Clear All Outputs`
3. Run all cells sequentially: `Run → Run All Cells`

**Why:** Cell execution counts and outputs persist until cleared.

---

## 🔧 Environment Setup Issues

### Issue: pip install fails

**Solution:**
```bash
# Ensure virtual environment is activated
source Coding/venv_pkpd/bin/activate  # macOS/Linux
Coding\venv_pkpd\Scripts\activate     # Windows

# Upgrade pip first
pip install --upgrade pip

# Then install packages
pip install rdkit
```

---

### Issue: Import errors despite installation

**Check installation:**
```python
import sys
print(sys.executable)  # Should show venv_pkpd path

import rdkit
print(rdkit.__file__)  # Should show venv_pkpd path
```

**If paths differ:**
- Wrong kernel selected
- Multiple Python installations conflicting
- Restart kernel and verify

---

## 📊 Data Loading Issues

### Issue: File not found errors

**Solution:**
```python
from pathlib import Path

# Use Path objects for cross-platform compatibility
DATA_DIR = Path('data/raw')

# Check if file exists before loading
file_path = DATA_DIR / 'chembl/chembl_binding_affinity.csv'
if file_path.exists():
    df = pd.read_csv(file_path)
else:
    print(f"File not found: {file_path}")
```

---

### Issue: Encoding errors when reading CSV

**Solution:**
```python
# Try different encodings
df = pd.read_csv(file_path, encoding='utf-8')
# or
df = pd.read_csv(file_path, encoding='latin-1')
```

---

## 🧮 Data Processing Issues

### Issue: SettingWithCopyWarning

**Warning:**
```
SettingWithCopyWarning: A value is trying to be set on a copy of a slice
```

**Solution:**
```python
# Instead of:
df_subset = df[df['column'] > 0]
df_subset['new_col'] = values  # Warning!

# Use .copy():
df_subset = df[df['column'] > 0].copy()
df_subset['new_col'] = values  # No warning
```

---

### Issue: Missing values causing errors

**Solution:**
```python
# Check for missing values
df.isnull().sum()

# Handle missing values
df = df.dropna(subset=['important_column'])  # Drop rows
df['column'].fillna(df['column'].median())   # Impute
```

---

### Issue: Data types incorrect

**Solution:**
```python
# Check data types
print(df.dtypes)

# Convert types
df['column'] = df['column'].astype(float)
df['category'] = df['category'].astype('category')
```

---

## 🎨 Visualization Issues

### Issue: Plots not showing

**Solution:**
```python
import matplotlib.pyplot as plt

# For Jupyter notebooks
%matplotlib inline

# After plotting
plt.show()  # Explicit display
```

---

### Issue: Figure size too small

**Solution:**
```python
# Set default figure size
plt.rcParams['figure.figsize'] = (12, 6)

# Or per-plot
fig, ax = plt.subplots(figsize=(14, 8))
```

---

## 🤖 Machine Learning Issues

### Issue: Features not normalized

**Check:**
```python
print(f"Mean: {X.mean().mean()}")  # Should be ~0
print(f"Std: {X.std().mean()}")    # Should be ~1
```

**Solution:**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

---

### Issue: Class imbalance in binary tasks

**Check:**
```python
print(y.value_counts(normalize=True))
```

**Solution:**
```python
# Use stratified split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2
)

# Or use weighted loss
from sklearn.utils.class_weight import compute_class_weight
weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
```

---

## 🧠 Phase 3: Neural ODE Model Issues (February 24, 2026)

> These issues were encountered while building `phase3_neural_ode_model.ipynb`.

---

### Issue P3-1: FileNotFoundError — TDC CSV files not found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/tdc/tdc_caco2.csv'
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/tdc/tdc_clearance_hepatocyte.csv'
```

**Cause:** TDC downloads save files with the variant name appended.

**Fix:**
```python
# Wrong:
caco2_df   = pd.read_csv(DATA_DIR / 'tdc/tdc_caco2.csv')
clear_df   = pd.read_csv(DATA_DIR / 'tdc/tdc_clearance_hepatocyte.csv')

# Correct:
caco2_df   = pd.read_csv(DATA_DIR / 'tdc/tdc_caco2_wang.csv')
clear_df   = pd.read_csv(DATA_DIR / 'tdc/tdc_clearance_hepatocyte_az.csv')
```

**Check actual filenames first:**
```python
import os
print(sorted(os.listdir('data/raw/tdc/')))
```

---

### Issue P3-2: ReduceLROnPlateau `verbose` deprecated in PyTorch 2.10

**Warning / Error:**
```
DeprecationWarning: The `verbose` parameter is deprecated.
```

**Fix:**
```python
# Remove verbose=True:
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=10  # no verbose
)
```

---

### Issue P3-3: `torch.load` security warning — missing `weights_only`

**Warning:**
```
FutureWarning: You are using `torch.load` without specifying the `weights_only` parameter...
```

**Fix:**
```python
# Always specify weights_only in PyTorch 2.x:
checkpoint = torch.load('model_checkpoint.pt', weights_only=True)
```

---

### Issue P3-4: BatchNorm corrupts multi-task training

**Symptom:** Loss spikes or diverges when switching tasks mid-epoch; training unstable.

**Cause:** `BatchNorm1d` maintains running mean/variance across the whole batch.
When batches alternate between tasks of very different sizes (e.g. hERG 7,997 vs
Caco-2 637), the running stats are dominated by the large task and corrupt the
normalization for smaller tasks.

**Fix:** Replace all `BatchNorm1d` with `LayerNorm` in your encoder:
```python
# Instead of:
nn.BatchNorm1d(hidden_dim)

# Use:
nn.LayerNorm(hidden_dim)
```

`LayerNorm` normalizes per sample, independent of batch composition.

---

### Issue P3-5: Large task dominates training (task imbalance)

**Symptom:** hERG metrics improve but Caco-2 / clearance stay near baseline;
training steps heavily skewed toward the largest dataset.

**Cause:** If interleaving iterates to the largest loader's length, small-dataset
tasks run once while large-dataset tasks run many more times.

**Fix:** Use min-step interleaving — cap all tasks to the smallest loader:
```python
n_steps = min(len(loader) for loader in train_loaders.values())
loops   = [iter(loader) for loader in train_loaders.values()]

for step in range(n_steps):
    for task_iter in loops:
        X_batch, y_batch = next(task_iter)
        # ... forward pass for this task
```

---

### Issue P3-6: Regression loss explodes — targets not normalized

**Symptom:** Training loss suddenly jumps to NaN or very large values;
MSE for clearance (~10⁴) overwhelms MSE for binding (~0.01).

**Cause:** Different regression targets live on very different scales
(pChEMBL binding: 4–11; hepatocyte clearance: 0.01–500).

**Fix:** Normalize each regression target independently before training:
```python
from sklearn.preprocessing import StandardScaler

target_scalers = {}
for task, y_train in regression_targets.items():
    sc = StandardScaler()
    y_train_scaled = sc.fit_transform(y_train.reshape(-1, 1)).ravel()
    target_scalers[task] = sc
    # store y_train_scaled for DataLoader

# At inference time, inverse-transform to get real units:
y_pred_real = target_scalers[task].inverse_transform(y_pred_scaled)
```

---

### Issue P3-7: Caco-2 set up as classification instead of regression

**Symptom:** Caco-2 R² stuck at −0.1; loss shows binary cross-entropy behaviour
on continuous permeability values.

**Cause:** Caco-2 permeability is a continuous real-valued measurement, not a
binary label — using `ClassificationHead` + BCE is incorrect.

**Fix:** Use `RegressionHead` + MSE for Caco-2:
```python
# In MultiTaskPKPDModel:
self.caco2_head = RegressionHead(latent_dim)   # NOT ClassificationHead

# In MultiTaskLoss:
def forward(self, preds, targets):
    loss_caco2 = F.mse_loss(preds['caco2'], targets['caco2'])  # NOT BCE
```

---

### Issue P3-8: All ADMET tasks stuck near mean-prediction (open)

**Symptom:** All regression tasks have R² ≈ 0; hERG AUROC ≈ 0.5;
training loss decreases but validation metrics don't improve.

**Diagnosis:** With only 64-bit Morgan fingerprints, bit collision is severe —
structurally different molecules map to identical fingerprint vectors, making
structure–activity discrimination impossible for the model.

**Fix (in progress):** Increase fingerprint bit width:
```python
# In Cell 11 of phase3_neural_ode_model.ipynb:
N_BITS = 1024   # was 64 — dramatically reduces collisions

# In Cell 5 (config):
config['input_dim'] = 1028   # 4 physico + 1024 Morgan  (was 68)
```
Then re-run cells 11 → 12 → 13 → 35.

**Status:** Open — 1024-bit retraining not yet done.

**Longer-term fix:** Replace static fingerprints with a GNN molecular encoder
(PyTorch Geometric) for richer structural representations.

---

## 🔍 Debugging Tips

### General Debugging Strategy

1. **Isolate the problem**
   ```python
   # Test small subset first
   df_test = df.head(10)
   result = process_function(df_test)
   ```

2. **Add print statements**
   ```python
   print(f"Shape: {df.shape}")
   print(f"Columns: {df.columns.tolist()}")
   print(f"Data types: {df.dtypes}")
   ```

3. **Check intermediate results**
   ```python
   display(df.head())
   print(df.describe())
   ```

4. **Use try-except for graceful errors**
   ```python
   try:
       result = risky_operation()
   except Exception as e:
       print(f"Error: {type(e).__name__}: {e}")
       result = None
   ```

---

## 📝 Best Practices

### 1. Always Use Virtual Environments
```bash
python -m venv venv_pkpd
source venv_pkpd/bin/activate
pip install -r requirements.txt
```

### 2. Save Preprocessing Objects
```python
import pickle

# Save scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Load scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

### 3. Document Your Code
```python
# =============================================================================
# CELL: Cell Purpose
# PURPOSE: What this cell does
# INPUTS: What data it needs
# OUTPUTS: What it produces
# =============================================================================
```

### 4. Version Control Friendly
- Clear all outputs before committing: `Edit → Clear All Outputs`
- Use relative paths, not absolute
- Don't hardcode file paths

---

## 🆘 When All Else Fails

### Nuclear Option: Fresh Start

```bash
# 1. Save your data
cp -r data/ data_backup/

# 2. Delete virtual environment
rm -rf venv_pkpd/

# 3. Recreate environment
python3 -m venv venv_pkpd
source venv_pkpd/bin/activate

# 4. Reinstall packages
pip install --upgrade pip
pip install -r requirements.txt

# 5. Register Jupyter kernel
python -m ipykernel install --user --name=venv_pkpd --display-name="venv_pkpd (Python 3.14)"

# 6. Restart Jupyter
# Kill Jupyter server and start fresh

# 7. Restart kernel in notebook
# Kernel → Restart Kernel & Clear Output

# 8. Run All Cells
# Cell → Run All
```

---

## 📞 Getting Help

### Before Asking for Help

1. ✅ Read error message completely
2. ✅ Check this troubleshooting guide
3. ✅ Google the exact error message
4. ✅ Check package documentation
5. ✅ Try on a minimal example

### What to Include When Reporting Issues

```markdown
**Environment:**
- Python version: 3.14.2
- OS: macOS
- Virtual env: venv_pkpd

**Error:**
[Full error traceback]

**Code:**
[Minimal code that reproduces issue]

**What I've tried:**
1. Restarted kernel
2. Checked column names
3. ...
```

---

**Last Updated**: February 24, 2026 (Phase 3 issues added)

---
