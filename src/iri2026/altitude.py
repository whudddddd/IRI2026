from __future__ import annotations

from argparse import ArgumentParser

from .base import IRI


def main(time: str, alt_km: list[float], glat: float, glon: float):
    return IRI(time, alt_km, glat, glon)


def cli() -> None:
    parser = ArgumentParser(description="IRI2026 altitude profile")
    parser.add_argument("time")
    parser.add_argument("latlon", type=float, nargs=2, metavar=("GLAT", "GLON"))
    parser.add_argument("-alt_km", type=float, nargs=3, default=(80, 1000, 10), metavar=("START", "STOP", "STEP"))
    args = parser.parse_args()
    iono = main(args.time, args.alt_km, *args.latlon)
    try:
        from matplotlib.pyplot import show
        from .plots import altprofile
        altprofile(iono)
        show()
    except ImportError:
        pass


if __name__ == "__main__":
    cli()
