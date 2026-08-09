"""
energy.py -- Domain calculations for solar panel energy output and geometry.

All functions are pure (no I/O, no side-effects) and unit-tested.
"""

from __future__ import annotations

# 8-point compass sectors, each covering 45 degrees.
# Centre of North is 0/360; each boundary is at multiples of 22.5 degrees.
_COMPASS_SECTORS = [
    (22.5,   "North"),
    (67.5,   "North-East"),
    (112.5,  "East"),
    (157.5,  "South-East"),
    (202.5,  "South"),
    (247.5,  "South-West"),
    (292.5,  "West"),
    (337.5,  "North-West"),
    (360.0,  "North"),   # catch-all for the upper end
]


def compute_energy_output(
    radiation_wm2: float,
    panel_area_m2: float,
    panel_efficiency: float,
) -> float:
    """
    Estimate instantaneous power output of a flat-plate solar panel.

    Formula
    -------
    energy_watts = radiation_wm2 * panel_area_m2 * panel_efficiency

    Parameters
    ----------
    radiation_wm2 : float
        Predicted shortwave irradiance incident on the panel surface (W/m2).
    panel_area_m2 : float
        Active panel area in square metres.
    panel_efficiency : float
        Panel conversion efficiency as a fraction in [0, 1].

    Returns
    -------
    float
        Estimated instantaneous power output in Watts.
    """
    return max(0.0, radiation_wm2 * panel_area_m2 * panel_efficiency)


def compute_optimal_tilt(elevation_deg: float) -> float:
    """
    Compute the optimal panel tilt angle to maximise direct irradiance.

    When the sun is at elevation E above the horizon, a panel perpendicular
    to the sun's rays has tilt = 90 - E relative to horizontal.

    Parameters
    ----------
    elevation_deg : float
        Apparent solar elevation angle in degrees.

    Returns
    -------
    float
        Recommended tilt angle in degrees, clamped to [0, 90].
        Returns 90 when the sun is at or below the horizon (elevation <= 0).
    """
    tilt = 90.0 - elevation_deg
    return float(max(0.0, min(90.0, tilt)))


def azimuth_to_compass_direction(azimuth_deg: float) -> str:
    """
    Convert a solar azimuth angle (degrees, 0/360 = North, clockwise) to an
    8-point compass label indicating the direction the panel should face.

    Parameters
    ----------
    azimuth_deg : float
        Solar azimuth in degrees [0, 360).

    Returns
    -------
    str
        One of: "North", "North-East", "East", "South-East",
                "South", "South-West", "West", "North-West".
    """
    # Normalise to [0, 360)
    azimuth_deg = azimuth_deg % 360.0

    for upper_bound, label in _COMPASS_SECTORS:
        if azimuth_deg < upper_bound:
            return label
    return "North"  # fallback (should never be reached after normalisation)
