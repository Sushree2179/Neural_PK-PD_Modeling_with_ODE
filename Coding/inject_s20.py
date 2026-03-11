"""Inject Section 20 cells into phase3_neural_ode_model.ipynb"""
import json, uuid, pathlib

NB_PATH = pathlib.Path(__file__).parent / "phase3_neural_ode_model.ipynb"

with open(NB_PATH) as f:
    nb = json.load(f)

def make_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": str(uuid.uuid4())[:8],
        "metadata": {},
        "outputs": [],
        "source": source_lines,
    }

# ── S20-A: IIV sampling ──────────────────────────────────────────────────────
s20a_src = """\
# ====================================================================
# SECTION 20 - CELL A: Population PK-PD Setup + IIV Sampling
# Objective: 500 virtual patients, 30% log-normal IIV on CL,V1,V2,Q,EC50
# ====================================================================
import numpy as np, pathlib as _path20

_ts("Cell S20-A — Population setup + IIV sampling")

# Population parameters (typical values)
POP_DOSE  = 100.0   # mg  IV bolus
POP_CL    = 5.0     # L/h clearance
POP_V1    = 10.0    # L   central volume
POP_V2    = 20.0    # L   peripheral volume
POP_Q     = 3.0     # L/h inter-compartmental CL
POP_EMAX  = 1.0     # fractional Emax
POP_EC50  = 0.5     # mg/L EC50
POP_GAMMA = 1.5     # Hill coefficient
POP_KE0   = 0.3     # h-1 effect-site equilibration rate

N_POP  = 500          # virtual patients
CV_IIV = 0.30         # 30% IIV (log-normal CV)
OMEGA  = np.sqrt(np.log(1 + CV_IIV**2))  # log-normal SD

rng20 = np.random.default_rng(SEED)

def _lognorm(pop_val, n, rng):
    return pop_val * np.exp(rng.normal(0, OMEGA, n))

CL_i   = _lognorm(POP_CL,   N_POP, rng20)
V1_i   = _lognorm(POP_V1,   N_POP, rng20)
V2_i   = _lognorm(POP_V2,   N_POP, rng20)
Q_i    = _lognorm(POP_Q,    N_POP, rng20)
EC50_i = _lognorm(POP_EC50, N_POP, rng20)

k10_i = CL_i / V1_i   # elimination from central
k12_i = Q_i  / V1_i   # central -> peripheral
k21_i = Q_i  / V2_i   # peripheral -> central

print(f"  N_POP={N_POP}  CV_IIV={CV_IIV*100:.0f}%  OMEGA={OMEGA:.4f}")
print(f"  CL    median={np.median(CL_i):.2f} L/h   "
      f"[5-95th: {np.percentile(CL_i,5):.2f}-{np.percentile(CL_i,95):.2f}]")
print(f"  V1    median={np.median(V1_i):.2f} L      "
      f"[5-95th: {np.percentile(V1_i,5):.2f}-{np.percentile(V1_i,95):.2f}]")
print(f"  EC50  median={np.median(EC50_i):.3f} mg/L "
      f"[5-95th: {np.percentile(EC50_i,5):.3f}-{np.percentile(EC50_i,95):.3f}]")
log_elapsed("S20-A done")
"""

# ── S20-B: Monte Carlo PK ODE ────────────────────────────────────────────────
s20b_src = """\
# ====================================================================
# SECTION 20 - CELL B: Monte Carlo 2-cpt PK ODE (N=500 patients)
# 2-compartment IV-bolus:
#   c1' = -(k10+k12)*c1 + k21*(V2/V1)*c2
#   c2' = k12*(V1/V2)*c1 - k21*c2
#   ce' = ke0*(c1 - ce)
# ====================================================================
from scipy.integrate import solve_ivp

_ts("Cell S20-B — Monte Carlo PK ODE (2-cpt + effect-site)")

T_SIM = 48.0
N_T   = 200
t_sim = np.linspace(0, T_SIM, N_T)

C1_pop = np.zeros((N_POP, N_T))
C2_pop = np.zeros((N_POP, N_T))
Ce_pop = np.zeros((N_POP, N_T))

def pk_ode(t, y, k10, k12, k21, v_ratio, ke0):
    c1, c2, ce = y
    dc1 = -(k10 + k12)*c1 + k21*v_ratio*c2
    dc2 = (k12/v_ratio)*c1 - k21*c2
    dce = ke0*(c1 - ce)
    return [dc1, dc2, dce]

for p in range(N_POP):
    C0  = POP_DOSE / V1_i[p]
    y0  = [C0, 0.0, C0]
    rat = V2_i[p] / V1_i[p]
    sol = solve_ivp(
        pk_ode, [0, T_SIM], y0, t_eval=t_sim,
        args=(k10_i[p], k12_i[p], k21_i[p], rat, POP_KE0),
        method="RK45", rtol=1e-5, atol=1e-8, dense_output=False
    )
    C1_pop[p] = np.clip(sol.y[0], 0, None)
    C2_pop[p] = np.clip(sol.y[1], 0, None)
    Ce_pop[p] = np.clip(sol.y[2], 0, None)

def pct(arr, q): return np.percentile(arr, q, axis=0)

C1_p5,  C1_p50,  C1_p95 = pct(C1_pop, 5),  pct(C1_pop, 50),  pct(C1_pop, 95)
Ce_p5,  Ce_p50,  Ce_p95 = pct(Ce_pop, 5),  pct(Ce_pop, 50),  pct(Ce_pop, 95)

Cmax_all = C1_pop.max(axis=1)
print(f"  PK simulation complete: C1_pop shape = {C1_pop.shape}")
print(f"  Cmax median = {np.median(Cmax_all):.2f} mg/L  "
      f"[5-95th: {np.percentile(Cmax_all,5):.2f}-{np.percentile(Cmax_all,95):.2f}]")
idx_4h = np.argmin(np.abs(t_sim - 4.0))
print(f"  Ce at 4h   median = {np.median(Ce_pop[:,idx_4h]):.4f} mg/L")
log_elapsed("S20-B done")
"""

# ── S20-C: PD + safety + 4-panel plot ───────────────────────────────────────
s20c_src = """\
# ====================================================================
# SECTION 20 - CELL C: Emax PD + safety integration + 4-panel plot
# E(t) = Emax * Ce^gamma / (EC50_i^gamma + Ce^gamma)
# Safety: Platt-scaled hERG and Temp-scaled Caco-2 (S18 params)
# ====================================================================
%matplotlib inline
import matplotlib.pyplot as plt
from IPython.display import display as ipy_display
import pathlib as _pl20

_ts("Cell S20-C — PD simulation + safety overlay + uncertainty plot")

# ── Emax PD model ─────────────────────────────────────────────────
E_pop = np.zeros((N_POP, N_T))
for p in range(N_POP):
    ce    = np.clip(Ce_pop[p], 0, None)
    ec50g = EC50_i[p] ** POP_GAMMA
    E_pop[p] = POP_EMAX * ce**POP_GAMMA / (ec50g + ce**POP_GAMMA + 1e-12)

E_p5,  E_p50,  E_p95 = pct(E_pop, 5),  pct(E_pop, 50),  pct(E_pop, 95)
E_p25, E_p75          = pct(E_pop, 25), pct(E_pop, 75)

AUC_E_pop  = np.trapezoid(E_pop,  t_sim, axis=1)
AUC_C1_pop = np.trapezoid(C1_pop, t_sim, axis=1)
print(f"  AUC(0-48h) effect  median={np.median(AUC_E_pop):.3f}  "
      f"[5th={np.percentile(AUC_E_pop,5):.3f}, 95th={np.percentile(AUC_E_pop,95):.3f}]")

# ── Safety: calibration_18 hard-coded params ──────────────────────
# hERG  Platt: a=1.0, b=-1.7372
# Caco-2 Temp: T=0.4504
A_HERG, B_HERG = 1.0, -1.7372
T_CACO         = 0.4504
HERG_THR       = 0.30
CACO_THR       = 0.50

# Per-patient logit from Cmax-based proxy + random noise
rng_s     = np.random.default_rng(SEED + 1)
Cmax_pop  = C1_pop.max(axis=1)
raw_herg  = np.log(Cmax_pop / POP_EC50 + 1e-6) + rng_s.normal(0, 0.8, N_POP)
raw_caco  = -np.log(Cmax_pop / (2*POP_EC50) + 1e-6) + rng_s.normal(0, 0.8, N_POP)

herg_probs_pop = 1.0 / (1.0 + np.exp(-(A_HERG * raw_herg + B_HERG)))
caco_probs_pop = 1.0 / (1.0 + np.exp(-raw_caco / T_CACO))

herg_flag_pop = herg_probs_pop > HERG_THR
caco_flag_pop = caco_probs_pop < CACO_THR
dual_flag_pop = herg_flag_pop & caco_flag_pop

print(f"  hERG P(block)>{HERG_THR*100:.0f}%:  "
      f"{herg_flag_pop.sum()}/{N_POP} ({100*herg_flag_pop.mean():.1f}%)")
print(f"  Caco-2 P(perm)<{CACO_THR*100:.0f}%: "
      f"{caco_flag_pop.sum()}/{N_POP} ({100*caco_flag_pop.mean():.1f}%)")
print(f"  Dual flag (both):       "
      f"{dual_flag_pop.sum()}/{N_POP} ({100*dual_flag_pop.mean():.1f}%)")

# ── 4-panel figure ────────────────────────────────────────────────
fig20, axes20 = plt.subplots(2, 2, figsize=(14, 9))
fig20.suptitle(
    "Section 20 — Population PK-PD Simulation (N=500, IIV=30%)",
    fontsize=13, fontweight="bold"
)

# Panel 1: PK uncertainty bands
ax = axes20[0, 0]
ax.fill_between(t_sim, C1_p5, C1_p95, alpha=0.25, color="steelblue", label="5-95th pct")
ax.fill_between(t_sim, pct(C1_pop,25), pct(C1_pop,75), alpha=0.40, color="steelblue", label="25-75th pct")
ax.plot(t_sim, C1_p50, color="steelblue", lw=2, label="Median")
ax.set_xlabel("Time (h)"); ax.set_ylabel("C1 (mg/L)")
ax.set_title("Central Compartment PK (2-cpt)"); ax.legend(fontsize=8); ax.set_xlim(0, T_SIM)

# Panel 2: Emax PD effect
ax = axes20[0, 1]
ax.fill_between(t_sim, E_p5,  E_p95,  alpha=0.25, color="tomato", label="5-95th pct")
ax.fill_between(t_sim, E_p25, E_p75,  alpha=0.40, color="tomato", label="25-75th pct")
ax.plot(t_sim, E_p50, color="tomato", lw=2, label="Median")
ax.axhline(0.5, ls="--", lw=0.8, color="gray", alpha=0.7, label="E=0.5")
ax.set_xlabel("Time (h)"); ax.set_ylabel("Effect (0-1)")
ax.set_title("Emax PD Effect (effect-site)"); ax.legend(fontsize=8)
ax.set_xlim(0, T_SIM); ax.set_ylim(0, 1.05)

# Panel 3: Efficacy vs hERG safety scatter
ax = axes20[1, 0]
safe = ~herg_flag_pop
ax.scatter(AUC_E_pop[safe],  herg_probs_pop[safe],  alpha=0.5, s=12,
           color="steelblue", label="Safe", edgecolors="none")
ax.scatter(AUC_E_pop[~safe], herg_probs_pop[~safe], alpha=0.7, s=18,
           color="crimson",   label="hERG flag", edgecolors="none", marker="^")
ax.axhline(HERG_THR, ls="--", lw=0.9, color="crimson", label=f"Threshold={HERG_THR}")
ax.set_xlabel("AUC(0-48h) Effect"); ax.set_ylabel("P(hERG block)")
ax.set_title("Efficacy vs hERG Safety"); ax.legend(fontsize=8)

# Panel 4: Safety pie chart
ax = axes20[1, 1]
n_safe = int((~herg_flag_pop & ~caco_flag_pop).sum())
n_herg = int((herg_flag_pop & ~caco_flag_pop).sum())
n_caco = int((~herg_flag_pop & caco_flag_pop).sum())
n_dual = int(dual_flag_pop.sum())
wedges  = [n_safe, n_herg, n_caco, n_dual]
wlabels = [f"Safe\\n({n_safe})", f"hERG only\\n({n_herg})",
           f"Caco-2 only\\n({n_caco})", f"Both\\n({n_dual})"]
wcolors = ["#70ad47", "#ff9900", "#5b9bd5", "#c00000"]
ax.pie(wedges, labels=wlabels, colors=wcolors,
       autopct="%1.1f%%", startangle=90, textprops={"fontsize": 9})
ax.set_title("Safety Flag Distribution")

plt.tight_layout()
_s20_data_dir = globals().get("DATA_DIR", "data/raw")
_pl20.Path(_s20_data_dir).mkdir(parents=True, exist_ok=True)
out_path_20 = _pl20.Path(_s20_data_dir) / "popPKPD_s20.png"
fig20.savefig(out_path_20, dpi=120, bbox_inches="tight")
ipy_display(fig20)
plt.close(fig20)
print(f"  Figure saved -> {out_path_20.resolve()}")
log_elapsed("S20-C done")
"""

# ── S20-D: Summary table + kernel snapshot ───────────────────────────────────
s20d_src = """\
# ====================================================================
# SECTION 20 - CELL D: Summary statistics + kernel snapshot
# ====================================================================
import pandas as pd
from IPython.display import display as ipy_display

_ts("Cell S20-D — Summary table + kernel snapshot")

Emax_obs_pop = E_pop.max(axis=1)
t_half_pk    = np.log(2) / np.mean(k10_i)

summary_rows = [
    ("PK - Cmax (mg/L)",        C1_pop.max(axis=1)),
    ("PK - AUC0-48 (mg*h/L)",   AUC_C1_pop),
    ("PD - Peak Effect",        Emax_obs_pop),
    ("PD - AUC0-48 Effect",     AUC_E_pop),
    ("Safety - P(hERG block)",   herg_probs_pop),
    ("Safety - P(Caco-2 perm)", caco_probs_pop),
]

tbl20 = pd.DataFrame([
    {"Metric": lbl,
     "5th pct":  f"{np.percentile(arr,  5):.3f}",
     "Median":   f"{np.median(arr):.3f}",
     "Mean":     f"{np.mean(arr):.3f}",
     "95th pct": f"{np.percentile(arr, 95):.3f}"}
    for lbl, arr in summary_rows
])

print("=" * 62)
print("  SECTION 20 SUMMARY — Population PK-PD (N=500)")
print("=" * 62)
ipy_display(tbl20)

print(f"  Population mean t1/2 (elimination): {t_half_pk:.2f} h")
print(f"  hERG flag rate (>{HERG_THR*100:.0f}%):  {100*herg_flag_pop.mean():.1f}%")
print(f"  Caco-2 flag rate (<{CACO_THR*100:.0f}%): {100*caco_flag_pop.mean():.1f}%")

calibration_20 = {
    "section":         20,
    "N_POP":           N_POP,
    "T_SIM":           T_SIM,
    "C1_pop":          C1_pop,
    "Ce_pop":          Ce_pop,
    "E_pop":           E_pop,
    "AUC_E_pop":       AUC_E_pop,
    "AUC_C1_pop":      AUC_C1_pop,
    "herg_probs_pop":  herg_probs_pop,
    "caco_probs_pop":  caco_probs_pop,
    "herg_flag_pop":   herg_flag_pop,
    "caco_flag_pop":   caco_flag_pop,
    "summary_df":      tbl20,
    "fig_path":        str(out_path_20) if "out_path_20" in dir() else "data/raw/popPKPD_s20.png",
}

print()
print("=" * 62)
print("  SECTION 20 COMPLETE — Population PK-PD Simulation")
print("=" * 62)
print(f"  S19 Joint GNN+MLP: R2=0.5650, RMSE=0.7216")
print(f"  Pop PK N={N_POP}, IIV={CV_IIV*100:.0f}%: t1/2={t_half_pk:.2f}h")
print(f"  Median peak PD effect: {np.median(Emax_obs_pop):.3f}")
print(f"  hERG flag rate:        {100*herg_flag_pop.mean():.1f}%")
print(f"  Plot -> {out_path_20}")
print("  calibration_20 dict saved to kernel")
log_elapsed("S20-D done -- Section 20 complete")
"""

cells_to_add = [
    (s20a_src, "S20-A"),
    (s20b_src, "S20-B"),
    (s20c_src, "S20-C"),
    (s20d_src, "S20-D"),
]

for src, name in cells_to_add:
    cell = make_cell(src)
    nb["cells"].append(cell)
    print(f"Added {name}: id={cell['id']}")

print(f"Total cells: {len(nb['cells'])}")

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook saved successfully.")
