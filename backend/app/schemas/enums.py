"""MySQL ENUM values — must match the live database schema exactly."""

from typing import Literal

AlertSeverity = Literal["Low", "Medium", "High", "Critical"]
AlertStatus = Literal["Active", "Resolved"]
SystemLogStatus = Literal["Success", "Warning", "Error"]
ChargingStatus = Literal["Charging", "Discharging", "Idle"]
AssetStatus = Literal["Active", "Inactive", "Maintenance"]
