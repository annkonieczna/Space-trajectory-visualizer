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




