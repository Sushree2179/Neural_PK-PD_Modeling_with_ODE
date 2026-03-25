# Phase 3B Presentation Material (18 Slides, Technical Deep Dive)

## Slide 1 - Title
Phase 3B: Multi-Task Neural PK-PD Model with Neural ODE
- Focus: architecture, theory, training protocol, and baseline behavior.

## Slide 2 - Agenda
- Problem framing
- Theoretical basis
- Data and features
- Detailed architecture
- Training and evaluation protocol
- Results, risks, and next experiments

## Slide 3 - Problem Framing
- Need a single model for efficacy and ADMET endpoints.
- Separate models ignore shared molecular signal.
- PK-PD workflows also require mechanistic trajectory behavior, not only endpoint prediction.

## Slide 4 - Why Multi-Task Learning
- Shared encoder acts as inductive transfer across related tasks.
- Hard parameter sharing lowers overfitting risk on smaller tasks.
- Task-specific heads preserve specialization where task distributions differ.

## Slide 5 - Why Neural ODE for PK
- Continuous-time latent dynamics are natural for concentration-time curves.
- ODE solver enables trajectory prediction at arbitrary time grids.
- Mechanistic prior: first-order elimination behavior can be encoded in the dynamics form.

## Slide 6 - Data Pipeline Overview
- Source features from Phase 3A artifacts and bridge outputs.
- Per-task arrays rebuilt into train/val/test DataLoaders.
- Task-wise preprocessing preserves target semantics for regression vs classification.

## Slide 7 - Feature Space Details
- Input vector combines:
	- physicochemical descriptors
	- Morgan fingerprint bits
	- docking_quality bridge feature
- Unified input dimension across all four tasks.

## Slide 8 - Structure to Binding to PK Bridge
- RapidDock geometry quality aggregated per target.
- Target-level docking_quality injected into binding samples.
- Non-target ADMET tasks receive zero-padding for same feature schema.

## Slide 9 - Shared Encoder Architecture
- Block 1: Linear(input_dim, hidden_dim) + LayerNorm + ReLU + Dropout
- Block 2: Linear(hidden_dim, hidden_dim) + LayerNorm + ReLU + Dropout
- Projection: Linear(hidden_dim, latent_dim) + ReLU
- LayerNorm chosen for stability in interleaved multi-task batches.

## Slide 10 - Task Head Design
- DeepRegressionHead for binding (harder regression landscape).
- RegressionHead for clearance.
- ClassificationHead for hERG and Caco-2, outputting logits.
- Design intent: low coupling at head level, high sharing at encoder level.

## Slide 11 - PKODEFunc Internals
- Latent vector maps to PK parameters [CL, V].
- Positivity enforced via exponentiation.
- Elimination rate k = CL / V.
- ODE definition: dC/dt = -kC.

## Slide 12 - Training Protocol
- Per-task splits: train/validation/test.
- Interleaved training over tasks per epoch.
- Minimum-batch scheduling avoids excessive cycling of small tasks.
- Gradient clipping used each update step.

## Slide 13 - Loss Function Design
- Weighted multi-task loss with task coefficients.
- Regression losses: MSE for binding and clearance.
- Classification losses: weighted BCE-with-logits or focal logits loss.
- Imbalance handled using positive-class weighting.

## Slide 14 - Optimization and Early Stopping
- Optimizer: Adam with weight decay.
- Scheduler: ReduceLROnPlateau on aggregated validation loss.
- Early stopping via patience counter on validation objective.
- Best checkpoint persisted for evaluation and handoff.

## Slide 15 - Evaluation Protocol
- Regression metrics: RMSE, MAE, R2.
- Classification metrics: AUROC, accuracy, F1.
- Threshold selected on validation set using Youden criterion.
- Final evaluation aligns with fixed task-specific metric targets.

## Slide 16 - Visual: Training Dynamics
![Training History](../Coding/training_history.png)

Technical readout:
- Loss curves show convergence and generalization trend.
- Metric traces reveal relative task learning speed and plateau points.
- Divergence signals where task-specific tuning is likely required.

## Slide 17 - Visual: Neural ODE PK Curves
![PK Curves](../Coding/pk_curves.png)

Technical readout:
- Curves are continuous-time ODE integrations from shared latent states.
- Expected monotonic concentration decay is preserved.
- Curve diversity indicates compound-level variation in inferred CL and V.

## Slide 18 - Summary, Risks, Next Work
- Phase 3B produced a complete reproducible baseline stack.
- Key risks: task interference, class imbalance sensitivity, threshold dependence.
- Phase 3C plan: targeted fine-tuning, loss-weight sweeps, calibration, robustness checks.
