from pathlib import Path

import matplotlib.pyplot as plt


def draw_pipeline(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.axis("off")

    labels = [
        "SMILES + target",
        "RDKit conformers",
        "PDB pocket\nretrieval",
        "Distance-biased\nTransformer",
        "D_LL / D_LP\nprediction",
        "Bridge CSV",
        "PK-PD\naugmentation",
    ]
    xs = [0.06, 0.2, 0.34, 0.5, 0.66, 0.8, 0.93]

    for x, lab in zip(xs, labels):
        ax.text(
            x,
            0.55,
            lab,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#EAF2FF", ec="#2F5DA8"),
            transform=ax.transAxes,
        )

    for i in range(len(xs) - 1):
        ax.annotate(
            "",
            xy=(xs[i + 1] - 0.045, 0.55),
            xytext=(xs[i] + 0.045, 0.55),
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", lw=1.8, color="#2F5DA8"),
        )

    ax.set_title("RapidDock End-to-End Pipeline", fontsize=14, pad=10)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def draw_architecture(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    ax.axis("off")

    blocks = [
        (0.12, 0.72, "Ligand Tokens"),
        (0.12, 0.32, "Protein Tokens"),
        (0.36, 0.52, "Type Embedding +\nProjection"),
        (0.56, 0.52, "DB-Transformer\nBlocks"),
        (0.76, 0.66, "D_LL^2 Head"),
        (0.76, 0.38, "D_LP^2 Head"),
    ]

    for x, y, text in blocks:
        ax.text(
            x,
            y,
            text,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FFF4E6", ec="#B36B00"),
            transform=ax.transAxes,
        )

    arrows = [
        ((0.18, 0.72), (0.31, 0.56)),
        ((0.18, 0.32), (0.31, 0.48)),
        ((0.42, 0.52), (0.50, 0.52)),
        ((0.62, 0.56), (0.71, 0.64)),
        ((0.62, 0.48), (0.71, 0.40)),
    ]
    for start, end in arrows:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", lw=1.8, color="#B36B00"),
        )

    ax.text(0.56, 0.8, "Distance Bias:  QK^T/sqrt(d_h) - alpha*D_joint", fontsize=10, ha="center", transform=ax.transAxes)
    ax.set_title("RapidDock Prototype Architecture", fontsize=14, pad=10)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def draw_bridge(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 3.2))
    ax.axis("off")

    labels = [
        "Predicted\nL-P distances",
        "Docking score\n(mean D_LP)",
        "docking_quality\n= -score",
        "Join with\npChEMBL",
        "Phase 3B/3C\nfeature input",
    ]
    xs = [0.09, 0.28, 0.47, 0.66, 0.86]

    for x, lab in zip(xs, labels):
        ax.text(
            x,
            0.52,
            lab,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#E9F7EF", ec="#1E8449"),
            transform=ax.transAxes,
        )

    for i in range(len(xs) - 1):
        ax.annotate(
            "",
            xy=(xs[i + 1] - 0.05, 0.52),
            xytext=(xs[i] + 0.05, 0.52),
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", lw=1.8, color="#1E8449"),
        )

    ax.set_title("Structure -> Binding -> PK-PD Bridge", fontsize=14, pad=10)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "Slides" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)

    draw_pipeline(out_dir / "rapiddock_pipeline.png")
    draw_architecture(out_dir / "rapiddock_architecture.png")
    draw_bridge(out_dir / "rapiddock_bridge.png")

    print(f"Created assets in: {out_dir}")


if __name__ == "__main__":
    main()
