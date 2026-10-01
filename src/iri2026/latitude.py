from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .vprofile import geoprofile


def main(time: str, alt_km: float, glat: list[float], glon: float, outfn: Path | None = None):
    iono = geoprofile(latrange=glat, glon=glon, altkm=alt_km, time=time)
    if outfn:
        outfn = Path(outfn).expanduser()
        print("writing", outfn)
        iono.to_netcdf(outfn)
    return iono


def cli() -> None:
    parser = ArgumentParser(description="IRI2026 latitude profile")
    parser.add_argument("time")
    parser.add_argument("glon", type=float)
    parser.add_argument("-glat", type=float, nargs=3, default=(-60, 60, 2.0), metavar=("START", "STOP", "STEP"))
    parser.add_argument("-alt_km", type=float, default=300.0)
    parser.add_argument("-o", "--outfn")
    args = parser.parse_args()
    iono = main(args.time, args.alt_km, args.glat, args.glon, args.outfn)
    try:
        from matplotlib.pyplot import show
        from .plots import latprofile
        latprofile(iono)
        show()
    except ImportError as exc:
        raise SystemExit(f"Skipped plotting tests {exc}")


if __name__ == "__main__":
    cli()
