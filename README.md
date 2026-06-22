# AI-Based-Solar-Panel-Automation
AI-based solar energy optimization system for intelligent panel orientation, energy prediction, battery optimization, and real-time monitoring.

## Data Folder

This directory contains the cleaned and preprocessed datasets required for the automation process. These datasets serve as the primary data source for feature engineering and predictive modeling.

## Included Datasets

The folder consists of two primary files:

1. **`processed_consumption_dataset.csv`**
   * **Description**: Contains high-frequency energy consumption data tracking power load over time.
   * **Frequency**: 5-minute intervals.
   * **Time Interval**: From **April 1, 2023** to **January 12, 2026**.
   * **Key Metrics**: Power load (continuous).

2. **`processed_weather_dataset.csv`**
   * **Description**: Contains hourly meteorological data capturing atmospheric and solar conditions matching the localized region i.e., Delhi in our case.
   * **Frequency**: Hourly intervals.
   * **Time Interval**: From **May 1, 2016** to **March 30, 2026**.
   * **Key Metrics**: Temperature, humidity, wind speed, and solar radiation parameters.

---

## Data Schema & Features

### 1. `processed_consumption_dataset.csv`

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `timestamp` | DateTime | The date and time of the logging instance (`YYYY-MM-DD HH:MM:SS`). |
| `load_MW` | Float | The power consumption load measured in Megawatts (MW). |

### 2. `processed_weather_dataset.csv`

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `timestamp` | DateTime | The date and time of the logging instance (`YYYY-MM-DD HH:MM:SS`). |
| `temperature_2m` | Float | Air temperature at 2 meters above the ground (°C). |
| `relative_humidity_2m`| Float | Relative humidity percentage at 2 meters (%). |
| `cloud_cover` | Float | Total cloud cover percentage (%). |
| `wind_speed_10m` | Float | Wind speed measured at 10 meters above the ground (m/s). |
| `shortwave_radiation` | Float | Downward shortwave radiation ($W/m^2$). |
| `ALLSKY_SFC_SW_DWN` | Float | All-sky surface shortwave downward irradiance. |
| `CLRSKY_SFC_SW_DWN` | Float | Clear-sky surface shortwave downward irradiance. |
