from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import xarray
from dateutil.parser import parse

from .base import IRI

__all__ = ["datetimerange", "timeprofile", "geoprofile"]


def datetimerange(start: datetime | str, end: datetime | str, step: timedelta) -> list[datetime]:
    if isinstance(start, str):
        start = parse(start)
    if isinstance(end, str):
        end = parse(end)
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("start and end must be datetimes or parseable strings")
    if step <= timedelta(0):
        raise ValueError("step must be positive")
    return [start + i * step for i in range((end - start) // step)]


def timeprofile(tlim: tuple, dt: timedelta, altkmrange: list[float], glat: float, glon: float) -> xarray.Dataset:
    times = datetimerange(tlim[0], tlim[1], dt)
    if not times:
        raise ValueError("time range contains no samples")
    datasets = [IRI(time, altkmrange, glat, glon) for time in times]
    iono = xarray.concat(datasets, dim="time")
    iono.attrs["f107"] = [dataset.attrs["f107"] for dataset in datasets]
    iono.attrs["ap"] = [dataset.attrs["ap"] for dataset in datasets]
    return iono


def geoprofile(latrange, glon: float, altkm: float, time: str | datetime) -> xarray.Dataset:
    glat = np.arange(*latrange)
    if glat.size == 0:
        raise ValueError("latitude range contains no samples")
    datasets = [IRI(time, [altkm] * 3, latitude, glon) for latitude in glat]
    iono = xarray.concat(datasets, dim="glat")
    iono.attrs["f107"] = [dataset.attrs["f107"] for dataset in datasets]
    iono.attrs["ap"] = [dataset.attrs["ap"] for dataset in datasets]
    return iono
