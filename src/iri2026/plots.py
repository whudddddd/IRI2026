from __future__ import annotations

import matplotlib.pyplot as plt


def altprofile(iono):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    iono.ne.isel(time=0).plot(x="alt_km", ax=axes[0], xscale="log")
    iono.Te.isel(time=0).plot(x="alt_km", ax=axes[1])
    axes[0].set_title("Electron density")
    axes[1].set_title("Electron temperature")
    return fig


def latprofile(iono):
    fig, ax = plt.subplots(figsize=(8, 5))
    iono.NmF2.squeeze().plot(ax=ax)
    ax.set_title("NmF2 versus latitude")
    return fig


def timeprofile(iono):
    fig, ax = plt.subplots(figsize=(8, 5))
    iono.NmF2.squeeze().plot(ax=ax)
    ax.set_title("NmF2 versus time")
    return fig
