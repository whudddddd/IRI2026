"""Compare the IRI2020 and IRI2026 Python interfaces.

Example::

    python compare_iri_versions.py --time 2020-01-01T12:00 \
        --lat 35 --lon 120 --alt-km 100 600 10 --plot comparison.png

Run this script with the environment that contains both packages.  The
``--iri2020-path`` option can add an existing iri2020 installation when it is
not on ``sys.path``.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np


PROFILE_VARIABLES = (
    "ne", "Tn", "Ti", "Te", "nO+", "nH+", "nHe+", "nO2+", "nNO+", "nCI", "nN+",
)
SUMMARY_VARIABLES = (
    "NmF2", "hmF2", "NmF1", "hmF1", "NmE", "hmE", "B0", "B1", "TEC",
    "EqVertIonDrift", "foF2",
)


def _load_modules(iri2020_path: str | None):
    if iri2020_path:
        sys.path.insert(0, str(Path(iri2020_path).expanduser()))
    try:
        iri2020 = importlib.import_module("iri2020")
    except ImportError as exc:
        raise SystemExit(
            "iri2020 is not importable; install it or pass --iri2020-path"
        ) from exc
    try:
        iri2026 = importlib.import_module("iri2026")
    except ImportError as exc:
        raise SystemExit("iri2026 is not importable") from exc
    return iri2020, iri2026


def _values(dataset: Any, name: str) -> np.ndarray:
    value = dataset[name]
    return np.asarray(getattr(value, "values", value), dtype=float).squeeze()


def _metrics(reference: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    reference = np.ravel(reference)
    candidate = np.ravel(candidate)
    if reference.shape != candidate.shape:
        raise ValueError(f"shape mismatch: {reference.shape} != {candidate.shape}")
    difference = candidate - reference
    scale = np.maximum(np.abs(reference), np.finfo(float).tiny)
    return {
        "max_abs": float(np.nanmax(np.abs(difference))),
        "rmse": float(np.sqrt(np.nanmean(difference**2))),
        "max_relative": float(np.nanmax(np.abs(difference) / scale)),
    }


def compare(
    time: str,
    alt_km: tuple[float, float, float],
    latitude: float,
    longitude: float,
    iri2020_path: str | None = None,
) -> tuple[dict[str, Any], Any, Any]:
    iri2020, iri2026 = _load_modules(iri2020_path)
    old = iri2020.IRI(time, alt_km, latitude, longitude)
    new = iri2026.IRI(time, alt_km, latitude, longitude)

    old_alt = np.ravel(_values(old, "alt_km"))
    new_alt = np.ravel(_values(new, "alt_km"))
    if old_alt.shape != new_alt.shape or not np.allclose(old_alt, new_alt):
        raise ValueError("IRI2020 and IRI2026 returned different altitude grids")

    result: dict[str, Any] = {
        "time": time,
        "latitude": latitude,
        "longitude": longitude,
        "alt_km": [float(alt_km[0]), float(alt_km[1]), float(alt_km[2])],
        "attributes": {
            "f107": {
                "iri2020": float(old.attrs["f107"]),
                "iri2026": float(new.attrs["f107"]),
            },
            "ap": {
                "iri2020": float(old.attrs["ap"]),
                "iri2026": float(new.attrs["ap"]),
            },
        },
        "variables": {},
    }
    for name in PROFILE_VARIABLES + SUMMARY_VARIABLES:
        if name in old and name in new:
            result["variables"][name] = _metrics(_values(old, name), _values(new, name))
    return result, old, new


def _plot(path: str, old: Any, new: Any) -> None:
    import matplotlib.pyplot as plt

    altitude = _values(new, "alt_km")
    figure, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for name, label in (("ne", "Electron density (m⁻³)"), ("Te", "Electron temperature (K)")):
        axes[0 if name == "ne" else 1].plot(_values(old, name), altitude, label="IRI2020")
        axes[0 if name == "ne" else 1].plot(_values(new, name), altitude, label="IRI2026")
        axes[0 if name == "ne" else 1].set_xlabel(label)
        axes[0 if name == "ne" else 1].set_xscale("log")
        axes[0 if name == "ne" else 1].grid(True, alpha=0.25)
        axes[0 if name == "ne" else 1].legend()
    axes[0].set_ylabel("Altitude (km)")
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time", default="2020-01-01T12:00:00")
    parser.add_argument("--lat", type=float, default=35.0)
    parser.add_argument("--lon", type=float, default=120.0)
    parser.add_argument("--alt-km", type=float, nargs=3, metavar=("MIN", "MAX", "STEP"), default=(100.0, 600.0, 10.0))
    parser.add_argument("--iri2020-path", help="directory containing the iri2020 package")
    parser.add_argument("-o", "--output", type=Path, help="write metrics as JSON")
    parser.add_argument("--plot", help="write an optional profile comparison PNG")
    args = parser.parse_args()

    result, old, new = compare(args.time, tuple(args.alt_km), args.lat, args.lon, args.iri2020_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.plot:
        _plot(args.plot, old, new)


if __name__ == "__main__":
    main()
