from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


def add_title_slide(prs: Presentation, title: str, subtitle: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle


def add_bullet_slide(prs: Presentation, title: str, bullets: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title

    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()

    for i, bullet in enumerate(bullets):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(20)


def add_image_slide(
    prs: Presentation,
    title: str,
    image_path: Path,
    caption_lines: list[str],
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.2), Inches(12.0), Inches(0.7))
    title_tf = title_box.text_frame
    title_tf.text = title
    title_tf.paragraphs[0].font.size = Pt(30)
    title_tf.paragraphs[0].font.bold = True

    if image_path.exists():
        slide.shapes.add_picture(str(image_path), Inches(0.7), Inches(1.0), width=Inches(8.8))
    else:
        missing = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.8), Inches(1.0))
        missing_tf = missing.text_frame
        missing_tf.text = f"Image not found: {image_path}"
        missing_tf.paragraphs[0].font.size = Pt(20)
        missing_tf.paragraphs[0].font.color.rgb = RGBColor(180, 0, 0)

    cap_box = slide.shapes.add_textbox(Inches(9.7), Inches(1.2), Inches(3.0), Inches(5.0))
    cap_tf = cap_box.text_frame
    cap_tf.clear()
    for i, line in enumerate(caption_lines):
        p = cap_tf.paragraphs[0] if i == 0 else cap_tf.add_paragraph()
        p.text = line
        p.font.size = Pt(18)
        p.level = 0


def build_deck(output_path: Path, repo_root: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    add_title_slide(
        prs,
        "Phase 3B: Multi-Task Neural PK-PD with Neural ODE",
        "Technical deep dive | 18-slide deck",
    )

    slide_specs = [
        (
            "Slide 2 - Agenda",
            [
                "Problem framing",
                "Theoretical basis",
                "Data and feature design",
                "Architecture and training protocol",
                "Results, risks, and next experiments",
            ],
        ),
        (
            "Slide 3 - Problem Framing",
            [
                "Need one model across efficacy and ADMET endpoints.",
                "Single-task setups miss transferable molecular signal.",
                "PK-PD workflows need mechanistic trajectory behavior.",
            ],
        ),
        (
            "Slide 4 - Why Multi-Task Learning",
            [
                "Shared encoder induces representation transfer.",
                "Hard parameter sharing reduces overfitting on small tasks.",
                "Task heads preserve specialization for task-specific patterns.",
            ],
        ),
        (
            "Slide 5 - Why Neural ODE",
            [
                "Continuous-time dynamics match PK concentration processes.",
                "Predictions available on arbitrary time grids.",
                "Supports mechanistic prior via first-order elimination form.",
            ],
        ),
        (
            "Slide 6 - Data Pipeline Overview",
            [
                "Phase 3A artifacts and bridge outputs are loaded.",
                "Task arrays converted into train/val/test DataLoaders.",
                "Task-aware scaling preserves regression/classification semantics.",
            ],
        ),
        (
            "Slide 7 - Feature Space Details",
            [
                "Input = descriptors + fingerprints + docking_quality.",
                "Unified input dimension maintained across all tasks.",
                "Bridge feature injects structure-level information into learning.",
            ],
        ),
        (
            "Slide 8 - Structure to Binding to PK Bridge",
            [
                "RapidDock geometry quality aggregated at target level.",
                "Binding task receives target-informed docking_quality values.",
                "Other ADMET tasks are zero-padded for schema consistency.",
            ],
        ),
        (
            "Slide 9 - Shared Encoder Architecture",
            [
                "Linear(input_dim, hidden_dim) + LayerNorm + ReLU + Dropout.",
                "Second hidden block mirrors first for deeper representation.",
                "Final projection maps into latent_dim with ReLU.",
                "LayerNorm stabilizes interleaved multi-task updates.",
            ],
        ),
        (
            "Slide 10 - Task Heads",
            [
                "DeepRegressionHead for binding.",
                "RegressionHead for clearance.",
                "ClassificationHead for hERG and Caco-2 with logits output.",
                "Design balances shared learning with endpoint-specific capacity.",
            ],
        ),
        (
            "Slide 11 - PKODEFunc Internals",
            [
                "Latent state maps to PK parameters [CL, V].",
                "Positivity enforced by exponentiation.",
                "k = CL / V and dynamics dC/dt = -kC.",
                "ODE integration returns concentration-time trajectories.",
            ],
        ),
        (
            "Slide 12 - Training Protocol",
            [
                "Task-wise train/val/test splits.",
                "Interleaved updates across tasks each epoch.",
                "Minimum-batch scheduling prevents over-cycling small tasks.",
                "Gradient clipping applied per update.",
            ],
        ),
        (
            "Slide 13 - Loss Design",
            [
                "Weighted multi-task objective.",
                "MSE for regression tasks.",
                "Weighted BCE-with-logits or focal logits for classification.",
                "Positive-class weighting addresses class imbalance.",
            ],
        ),
        (
            "Slide 14 - Optimization and Early Stopping",
            [
                "Optimizer: Adam with weight decay.",
                "Scheduler: ReduceLROnPlateau on validation objective.",
                "Early stopping by patience on aggregated validation loss.",
                "Best checkpoint persisted for handoff and reproducibility.",
            ],
        ),
        (
            "Slide 15 - Evaluation Protocol",
            [
                "Regression metrics: RMSE, MAE, R2.",
                "Classification metrics: AUROC, accuracy, F1.",
                "Validation threshold selected via Youden criterion.",
                "Task targets tracked consistently for go/no-go decisions.",
            ],
        ),
    ]

    for title, bullets in slide_specs:
        add_bullet_slide(prs, title, bullets)

    add_image_slide(
        prs,
        "Slide 16 - Visual: Training Dynamics",
        repo_root / "Coding" / "training_history.png",
        [
            "Loss curves show convergence and generalization.",
            "Task metric trends expose plateau regions.",
            "Signals where task-specific tuning is needed.",
        ],
    )

    add_image_slide(
        prs,
        "Slide 17 - Visual: Neural ODE PK Curves",
        repo_root / "Coding" / "pk_curves.png",
        [
            "Continuous-time ODE integration output.",
            "Monotonic decay reflects elimination dynamics.",
            "Variation reflects inferred CL and V differences.",
        ],
    )

    add_bullet_slide(
        prs,
        "Slide 18 - Summary and Next Work",
        [
            "Phase 3B provides full reproducible baseline stack.",
            "Risks: task interference, imbalance sensitivity, threshold dependence.",
            "Phase 3C: task-focused fine-tuning, loss-weight sweeps, calibration.",
        ],
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_path = repo_root / "Slides" / "Phase3B_18Slide_Deck.pptx"
    build_deck(output_path, repo_root)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
