from dataclasses import dataclass

import numpy as np
import spiceypy as spice


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


def create_ellipsoid_mesh(
    ellipsoid: BodyEllipsoid, number_of_points: int = 100, scale: float = 1.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Function responsible for scaling the radius of the planet and
    creating  x, y, z mesh arrays for plotting a triaxial ellipsoid."""
    rx, ry, rz = ellipsoid.radii_km * scale  # radious points
    cx, cy, cz = ellipsoid.center_km  # center points
    u = np.linspace(
        0, 2 * np.pi, number_of_points
    )  # angle of rotation around the Z axis
    v = np.linspace(
        0, np.pi, number_of_points
    )  # transition angle from the North Pole to the South Pole
    x = cx + rx * (np.outer(np.cos(u), np.sin(v)))  # spherical coordinates
    y = cy + ry * (np.outer(np.sin(u), np.sin(v)))
    z = cz + rz * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z
