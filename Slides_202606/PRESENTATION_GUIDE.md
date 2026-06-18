# Presentation Guide — Neural PK-PD Modeling with ODE

---

## How to Start (First 60 Seconds)

### Before the slide appears
Stand, make eye contact, and say:

> "Good [morning/afternoon]. My name is [Your Name] and today I will present my master's thesis titled *Neural PK-PD Modeling with ODE for Early Drug Discovery*."

### Opening hook (say while title slide is visible)
> "Every year, the pharmaceutical industry spends billions developing drugs that ultimately fail — not because they were ineffective in a test tube, but because we didn't predict their behaviour inside the human body early enough. My thesis addresses exactly that gap."

### One-sentence thesis summary
> "I built a complete machine learning pipeline that jointly predicts four molecular properties — binding affinity, cardiotoxicity risk, intestinal absorption, and metabolic clearance — calibrates those predictions so they can be trusted as probabilities, and feeds them into a Neural ODE pharmacokinetic-pharmacodynamic simulator to support dose selection and safety trade-off analysis."

### Transition to the overview slide
> "Let me walk you through the structure of the work."

---

## Section-by-Section Talking Points

### Slide 3 — Thesis Goal & Pipeline Flowchart
> "The core idea is to chain six components into one reproducible workflow: curated public datasets, structural fingerprint features, a multi-task neural model, probability calibration, a Neural ODE PK-PD simulator, and finally a decision layer with Pareto analysis, Monte Carlo validation, and virtual clinical trial simulation."

### Slide 10 — Data Sources
> "The dataset draws from four public sources. The most important are TDC for ADMET benchmarks and real ChEMBL SMILES for binding affinity — because ChEMBL provides actual measured activity values across eight pharmacologically diverse protein targets."

### Slide 13 — Architecture
> "A single shared encoder learns structural representations common to all four tasks simultaneously. Task-specific heads then branch from a 64-dimensional bottleneck. This lets the smaller tasks — Caco-2 has only 900 samples — borrow structural signal learned from the larger binding task."

### Slide 14 — Calibration
> "A model can rank compounds correctly but still assign wrong probability values. Since hERG and Caco-2 probabilities feed directly into downstream simulation as risk variables and absorption rates, overconfident raw outputs would bias every PK-PD prediction. Temperature scaling cut hERG ECE from 0.17 to 0.006."

### Slide 16 — ODE Mapping
> "The four model outputs map directly to ODE parameters: clearance drives the elimination rate constant, Caco-2 probability maps to oral absorption rate, binding pChEMBL gives EC50, and hERG probability acts as a cardiac safety flag."

### Slide 22 — Experimental Progression Table
> "Rather than showing you all results at once, I want you to see the progression: the baseline is near-random because we lacked real structural inputs. Each subsequent stage — real fingerprints, real ChEMBL binding, hERG refinement, calibration, GNN fusion — builds on the last."

### Slide 25 — Limitations
> "Three honest limitations: all data are from public databases with assay heterogeneity, the ODE compartment transfer constants are fixed population averages rather than per-compound predictions, and there is no prospective external validation — the virtual trial is a planning tool, not a clinical prediction."

---

## Possible Questions and Answers

### Q1: Why did you choose a multi-task approach rather than four separate models?
> "Binding affinity, hERG inhibition, Caco-2 permeability, and clearance all depend on overlapping molecular features — ring systems, functional groups, lipophilicity. A shared encoder exploits those correlations. Smaller tasks like Caco-2 (900 samples) and hERG (655 samples) benefit from structural representations jointly learned with the larger binding task (2,000 samples). Separate models would need more data per task and would miss positive transfer."

---

### Q2: Why is calibration a necessity rather than just a nice-to-have?
> "Because the hERG and Caco-2 outputs are not used just for ranking — they are passed as numeric values directly into the ODE simulation: Caco-2 probability maps to the oral absorption rate ka and hERG probability is used as a cardiac safety flag. An uncalibrated ECE of 0.17 for hERG means predicted probabilities are systematically wrong by 17 percentage points on average, which would propagate a large bias into every PK-PD trajectory and every Pareto or trial analysis downstream."

---

### Q3: How exactly does the GNN encode molecular structure?
> "RDKit extracts per-atom features: atomic number as a 10-class one-hot vector, degree, formal charge, number of hydrogens, and aromaticity flag. Per-bond features are bond type and ring membership. Three message-passing layers aggregate neighbour embeddings by mean pooling. Global mean pooling over all atom embeddings gives the graph-level representation, which is then concatenated with the MLP fingerprint latent vector before the binding regression head."

---

### Q4: Why use the fusion GNN+MLP rather than GNN alone?
> "The GNN alone achieved binding R² = 0.411 versus the MLP fingerprint baseline at 0.452 — the GNN did not immediately surpass fingerprints. The fusion model reached R² = 0.565. Graph and fingerprint representations are complementary: the GNN captures relational and local structural context while the MLP retains dense tabular fingerprint information. Combining them outperforms either branch individually."

---

### Q5: What does the Pareto analysis actually show?
> "We optimised over regimen space considering both predicted efficacy (AUC_E from PK-PD simulation) and predicted safety burden (hERG and Caco-2 risk). No tested regimen simultaneously maximised efficacy and minimised safety burden — they are in genuine conflict. The Pareto frontier exposes the geometry of that trade-off. The knee-point regimen is the most balanced solution: the point of maximum curvature on the frontier where additional efficacy gains come at disproportionately high safety cost."

---

### Q6: What does the virtual clinical trial simulation tell you?
> "It shows that the framework can translate molecular predictions all the way to trial-level operating characteristics. Simulated treatment arms show clear dose-response separation in efficacy, and statistical power under the modelled assumptions is very high. But — critically — the safety profile remains poor across all active arms, consistent with the Pareto analysis. This confirms that efficacy improvement alone does not solve the safety constraint. The trial is a planning exercise, not a clinical prediction."

---

### Q7: Why is hERG inhibition such a dominant safety constraint?
> "The hERG potassium channel is one of the most promiscuous off-targets in medicinal chemistry. Blocking it prolongs the QT interval on an electrocardiogram, which can cause potentially fatal arrhythmias. Regulatory agencies require hERG testing for all drug candidates. In our population simulation, 98.2% of compounds triggered the hERG safety flag, which reflects both the biological reality that many drug-like molecules interact with hERG and the conservative threshold we applied."

---

### Q8: What is the RapidDock prototype and why is it only exploratory?
> "It is a distance-biased transformer that predicts pairwise protein–ligand atom distances rather than scalar ADMET endpoints. The key innovation is subtracting a scaled joint distance matrix as an additive bias inside the attention softmax, so spatially distant atoms receive lower attention weight. Ligand 3D coordinates are recovered from predicted distances via L-BFGS. It is exploratory because it uses synthetic protein context points rather than real PDB structures, has no calibration or uncertainty quantification, and was trained on only ~100 small molecules. It demonstrates feasibility as a future extension."

---

### Q9: Which parameters drive PK-PD outcomes most?
> "From the tornado plot — one-at-a-time ±20% sensitivity analysis: AUC_E is most sensitive to Emax, then predicted clearance, then EC50. Cmax is dominated by dose. AUC_C1 is driven by clearance and dose. This confirms that the two most important molecular levers for translational decisions are predicted clearance and predicted binding affinity — exactly the two endpoints where data quality and model improvement matter most."

---

### Q10: What would you do differently or next?
> "Three priorities: first, external and prospective validation with held-out compounds from a different source. Second, per-compound ODE parameter prediction using PK-DB pharmacokinetic study data, replacing the fixed population-average compartment constants. Third, extending the GNN branch to all four tasks rather than only binding, and integrating the RapidDock branch with real protein structures from the PDB. Longer term, the goal is an interactive deployment as a decision-support tool for early-stage compound prioritisation."

---

## Timing Guide (20-minute defence)

| Segment | Slides | Time |
|---|---|---|
| Title + opening hook | 1 | 1 min |
| Table of Contents | 2 | 30 sec |
| Introduction + Objectives | 3–8 | 3 min |
| Data + Features + Architecture + Calibration | 9–14 | 4 min |
| PK-PD + Decision Layer | 15–18 | 3 min |
| Results | 19–25 | 4 min |
| Conclusions | 26 | 2 min |
| Thank you | — | 30 sec |
| **Q&A** | backup slides | ~10 min |

**Total presentation: ~18 min. Target finishing a minute early to allow a smooth transition to Q&A.**
