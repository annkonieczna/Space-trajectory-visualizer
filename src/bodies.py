import numpy as np
import spiceypy as spice
from dataclasses import dataclass


@dataclass(
    frozen=True
)  # We create a dataclass that represents an ellipsoid ( it's unmutable)
class BodyEllipsoid:
    name: str
    center_km: tuple[float, float, float]  # center of the ellipsoid
    radii_km: np.ndarray  # radii of the ellipsoid


def get_body_radii(body_name: str) -> np.ndarray:
    """
    Returns triaxial body radii from SPICE kernel pool.
    """
    # bodvrd(BODYNM, ITEM, MAXN)
    # Inputs:
    # BODYNM - Body name
    # ITEM - RADII - Item for which values are desired
    # MAXN -  Maximum number of values that may be returned
    # Outputs:
    # _ - Number of values returned
    # radii -  Values

    _, radii = spice.bodvrd(body_name, "RADII", 3)
    return np.array(radii, dtype=float)

def build_body_ellipsoid(
    body_name: str, center_km: tuple[float, float, float] = (0, 0, 0)
) -> BodyEllipsoid:
    """Function responsible for cleating an ellipsoid object"""
    radii = get_body_radii(body_name)
    return BodyEllipsoid(name=body_name, center_km=center_km, radii_km=radii)


