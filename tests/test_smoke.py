import numpy as np

import iri2026


def test_altitude_profile_smoke():
    iono = iri2026.IRI("2026-09-28T12:00:00", (100, 200, 20), 35.0, 120.0)
    assert iono.sizes["alt_km"] == 6
    assert (iono["ne"].values > 0).any()
    assert iono["NmF2"].item() > 0
