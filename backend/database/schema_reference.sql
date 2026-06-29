# Reference schema — OUTDATED TEMPLATE. Do NOT run against production.
# Authoritative schema mapping: backend/app/models/entities.py
# Database name: solar_panel_automation
# Align models with your existing MySQL tables. Contact the data team if columns differ.

CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at DATETIME NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    cloud_cover DECIMAL(5,2),
    wind_speed DECIMAL(6,2),
    ghi DECIMAL(8,2),
    aqi INT,
    location VARCHAR(100) DEFAULT 'Delhi',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_weather_recorded_at (recorded_at)
);

CREATE TABLE IF NOT EXISTS solar_panel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    panel_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    capacity_kw DECIMAL(8,2),
    current_tilt DECIMAL(5,2),
    optimal_tilt DECIMAL(5,2),
    power_output_w DECIMAL(10,2),
    voltage DECIMAL(8,2),
    current_amp DECIMAL(8,2),
    status VARCHAR(50) DEFAULT 'online',
    last_updated DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS solar_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_type VARCHAR(50) NOT NULL,
    predicted_value DECIMAL(12,4),
    actual_value DECIMAL(12,4),
    unit VARCHAR(20),
    confidence DECIMAL(5,2),
    model_version VARCHAR(50),
    recorded_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prediction_type (prediction_type),
    INDEX idx_prediction_recorded_at (recorded_at)
);

CREATE TABLE IF NOT EXISTS energy_consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at DATETIME NOT NULL,
    consumption_kwh DECIMAL(10,4),
    load_kw DECIMAL(10,4),
    peak_load_kw DECIMAL(10,4),
    source VARCHAR(50) DEFAULT 'meter',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_energy_recorded_at (recorded_at)
);

CREATE TABLE IF NOT EXISTS battery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    battery_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    capacity_kwh DECIMAL(8,2),
    chemistry VARCHAR(50),
    health_score DECIMAL(5,2),
    status VARCHAR(50) DEFAULT 'active',
    installed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS battery_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    battery_id INT NOT NULL,
    soc DECIMAL(5,2) NOT NULL,
    voltage DECIMAL(8,2),
    current_amp DECIMAL(8,2),
    temperature DECIMAL(5,2),
    health_score DECIMAL(5,2),
    status VARCHAR(50) DEFAULT 'idle',
    recorded_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_battery_status_battery_id (battery_id),
    INDEX idx_battery_status_recorded_at (recorded_at),
    FOREIGN KEY (battery_id) REFERENCES battery(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS telemetry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(12,4) NOT NULL,
    unit VARCHAR(20),
    sensor_type VARCHAR(50),
    recorded_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_telemetry_device_id (device_id),
    INDEX idx_telemetry_metric_name (metric_name),
    INDEX idx_telemetry_recorded_at (recorded_at)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    priority VARCHAR(20) DEFAULT 'info',
    status VARCHAR(20) DEFAULT 'active',
    category VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME NULL,
    INDEX idx_alerts_status (status),
    INDEX idx_alerts_created_at (created_at)
);

CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20) DEFAULT 'info',
    message TEXT NOT NULL,
    source VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_system_logs_created_at (created_at)
);
