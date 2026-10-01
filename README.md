# IRI2026 Python interface

中文说明：[README_CN.md](README_CN.md)

Python and Fortran interfaces to the International Reference Ionosphere 2026
model. The package follows the build-on-first-use layout used by
[`iri2020`](https://github.com/space-physics/iri2020): Python calls a bundled
Fortran driver and returns an `xarray.Dataset`.

## Install

Install the published wheel or a wheel built locally:

```powershell
python -m pip install iri2026
python -m pip install dist/iri2026-1.0.0-py3-none-any.whl
```

For a source checkout, install the project in editable mode:

```powershell
python -m pip install -e ".[tests]"
```

The first source build needs CMake and a Fortran compiler such as gfortran.
On Windows, the package uses the `MinGW Makefiles` CMake generator by default.

## Usage

```python
import iri2026

iono = iri2026.IRI(
    "2026-09-28T12:00:00",
    (100, 1000, 10),
    35.0,
    120.0,
)
print(iono["ne"])
print(iono["TEC"])
```

The command-line profile helpers are also installed:

```text
iri2026-altitude 2026-09-28T12:00 -11.95 -76.77
iri2026-latitude 2026-09-28T12:00 -76.77
iri2026-times 2026-09-28 2026-09-29 1 -11.95 -76.77
```

The comparison example in `examples/compare_iri_versions.py` computes metrics
between IRI2020 and IRI2026 for the same input. IRI2020 must be installed in
the active environment when that example is used.

## Data files

The `src/iri2026/data` directory contains the IRI coefficient files, IGRF
coefficients, and the `apf107.dat`/`ig_rz.dat` solar and ionospheric indices.
Update the index files periodically for dates beyond their current coverage.

## Development

```powershell
python -m pip install -e ".[tests,lint]"
python -m pytest
python -m pip wheel . --no-deps --wheel-dir dist
```

The original IRI-2026 release notes and model documentation are in
`docs/IRI2026-original-readme.txt`.
