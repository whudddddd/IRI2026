from __future__ import annotations

import importlib.resources as resources
import io
import logging
import os
import subprocess
from datetime import datetime
from numbers import Real

import numpy as np
import xarray
from dateutil.parser import parse

from .build import build

SIMOUT = ["ne", "Tn", "Ti", "Te", "nO+", "nH+", "nHe+", "nO2+", "nNO+", "nCI", "nN+"]


def IRI(time: str | datetime, altkmrange: list[float], glat: float, glon: float) -> xarray.Dataset:
    """Compute an IRI-2026 altitude profile and return it as an xarray dataset."""
    if isinstance(time, str):
        time = parse(time)
    if not isinstance(time, datetime):
        raise TypeError("time must be a datetime or parseable string")
    if len(altkmrange) != 3:
        raise ValueError("altitude (km) min, max, step")
    if not all(isinstance(value, Real) for value in (*altkmrange, glat, glon)):
        raise TypeError("altitude, glat, and glon must be numeric")
    if altkmrange[2] <= 0 or altkmrange[1] < altkmrange[0]:
        raise ValueError("altitude range must have max >= min and a positive step")

    exe_name = "iri2026_driver.exe" if os.name == "nt" else "iri2026_driver"
    with (
        resources.as_file(resources.files(__package__).joinpath(exe_name)) as exe,
        resources.as_file(resources.files(__package__).joinpath("data")) as data_path,
    ):
        if not exe.is_file():
            build()
        cmd = [
            str(exe), str(time.year), str(time.month), str(time.day),
            str(time.hour), str(time.minute), str(time.second),
            str(glat), str(glon), *(str(value) for value in altkmrange),
        ]
        logging.info("%s", " ".join(cmd))
        output = subprocess.check_output(cmd, text=True, cwd=data_path)

    if not output:
        raise RuntimeError("IRI failed to run correctly--gave empty text output")
    nalt = int((altkmrange[1] - altkmrange[0]) // altkmrange[2]) + 1
    profile = np.atleast_2d(np.genfromtxt(io.StringIO(output), max_rows=nalt))
    if profile.ndim != 2 or profile.shape[1] != 12:
        raise RuntimeError(f"bad text data output format, shape {profile.shape}")
    summary = np.genfromtxt(io.StringIO(output), skip_header=nalt)
    if summary.ndim != 1 or summary.size != 100:
        raise RuntimeError("bad text data output format")

    data = {name: (("alt_km",), values) for name, values in zip(SIMOUT, profile[:, 1:].T)}
    dataset = xarray.Dataset(
        data,
        coords={"time": [time], "alt_km": profile[:, 0], "glat": glat, "glon": glon},
        attrs={"f107": summary[40], "ap": summary[51]},
    )
    for index, name in enumerate(("NmF2", "hmF2", "NmF1", "hmF1", "NmE", "hmE")):
        dataset[name] = (("time",), [summary[index]])
    dataset["B0"] = (("time",), [summary[9]])
    dataset["B1"] = (("time",), [summary[34]])
    dataset["TEC"] = (("time",), [summary[36]])
    dataset["EqVertIonDrift"] = (("time",), [summary[43]])
    dataset["foF2"] = (("time",), [summary[99]])
    return dataset
