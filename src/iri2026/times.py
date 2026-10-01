from __future__ import annotations

import logging
from argparse import ArgumentParser
from datetime import timedelta

from .vprofile import timeprofile


def main(time: list[str], alt_km: list[float], glat: float, glon: float):
    return timeprofile((time[0], time[1]), timedelta(hours=float(time[2])), alt_km, glat, glon)


def cli() -> None:
    parser = ArgumentParser(description="IRI2026 time profile")
    parser.add_argument("time", nargs=3, metavar=("START", "STOP", "STEP_HOURS"))
    parser.add_argument("latlon", nargs=2, type=float, metavar=("GLAT", "GLON"))
    parser.add_argument("-alt_km", type=float, nargs=3, default=(100, 200, 20), metavar=("START", "STOP", "STEP"))
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    iono = main(args.time, args.alt_km, *args.latlon)
    try:
        from matplotlib.pyplot import show
        from .plots import timeprofile as plot_time
        plot_time(iono)
        show()
    except ImportError as exc:
        raise SystemExit(f"Skipped plotting tests {exc}")


if __name__ == "__main__":
    cli()
