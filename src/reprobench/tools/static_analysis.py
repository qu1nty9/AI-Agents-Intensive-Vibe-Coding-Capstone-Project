"""Static analysis checks for experiment artifacts."""

from __future__ import annotations

from pathlib import Path

from reprobench.models import AuditFinding

RANDOMNESS_MARKERS = (
    "random.",
    "from random import",
    "numpy.random",
    "np.random",
)

SEED_MARKERS = (
    "random.seed",
    "numpy.random.seed",
    "np.random.seed",
    "default_rng(",
    "RandomState(",
)


def detect_missing_seed(script_path: Path) -> tuple[AuditFinding, ...]:
    """Detect obvious use of randomness without seed control."""

    text = Path(script_path).read_text(encoding="utf-8", errors="ignore")
    uses_randomness = any(marker in text for marker in RANDOMNESS_MARKERS)
    has_seed_control = any(marker in text for marker in SEED_MARKERS)
    if uses_randomness and not has_seed_control:
        return (
            AuditFinding(
                severity="warning",
                title="Missing seed control",
                detail="The artifact uses randomness but no obvious seed control was found.",
            ),
        )
    return ()

