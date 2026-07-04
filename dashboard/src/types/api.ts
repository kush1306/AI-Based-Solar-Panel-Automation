/** Backend API response types (snake_case, matching FastAPI schemas). */

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ChartDataPoint {
  timestamp: string;
  value: number;
  label?: string | null;
}

export interface DashboardOverview {
  current_power: number;
  battery_soc: number;
  temperature: number | null;
  humidity: number | null;
  optimal_tilt: number | null;
  today_energy: number;
  system_status: string;
  active_alerts: number;
  recent_logs: SystemLogResponse[];
  active_alert_items: AlertResponse[];
}

export interface DashboardCharts {
  power_generation: ChartDataPoint[];
  battery_soc: ChartDataPoint[];
  temperature: ChartDataPoint[];
  energy_consumption: ChartDataPoint[];
  telemetry: ChartDataPoint[];
  predicted_tilt: ChartDataPoint[];
}

export interface WeatherResponse {
  weather_id: number;
  recorded_at: string;
  temperature: number | null;
  humidity: number | null;
  cloud_cover: number | null;
  wind_speed: number | null;
  ghi: number | null;
  dni: number | null;
  aqi: number | null;
  city: string | null;
}

export interface SolarPanelResponse {
  panel_id: number;
  panel_name: string;
  panel_capacity: number | null;
  panel_efficiency: number | null;
  installation_date: string | null;
  current_tilt: number | null;
  status: string | null;
}

export interface SolarPredictionResponse {
  prediction_id: number;
  panel_id: number;
  weather_id: number;
  prediction_time: string;
  predicted_tilt: number;
  expected_power: number | null;
  confidence_score: number | null;
  model_version: string | null;
}

export interface EnergyConsumptionResponse {
  consumption_id: number;
  recorded_at: string;
  load_kw: number;
  temperature: number | null;
  humidity: number | null;
  hour_of_day: number | null;
  day_of_week: string | null;
  is_weekend: boolean | null;
}

export interface BatteryResponse {
  battery_id: number;
  battery_name: string;
  battery_type: string | null;
  capacity_mah: number | null;
  nominal_voltage: number | null;
  installation_date: string | null;
  health_percentage: number | null;
  status: string | null;
}

export interface BatteryStatusResponse {
  status_id: number;
  battery_id: number;
  timestamp: string;
  soc: number;
  voltage: number;
  current: number;
  temperature: number | null;
  charging_status: string;
}

export interface TelemetryResponse {
  telemetry_id: number;
  panel_id: number;
  battery_id: number;
  timestamp: string;
  voltage: number;
  current: number;
  power: number;
  lux: number | null;
  tilt_angle: number | null;
  soc: number | null;
}

export interface AlertResponse {
  alert_id: number;
  panel_id: number | null;
  battery_id: number | null;
  alert_time: string;
  alert_type: string;
  severity: string;
  message: string | null;
  status: string | null;
}

export interface SystemLogResponse {
  log_id: number;
  timestamp: string;
  module: string;
  event_type: string;
  description: string | null;
  status: string;
}

export interface SolarModelPredictResponse {
  timestamp: string;
  location: { latitude: number; longitude: number };
  azimuth_deg: number;
  elevation_deg: number;
  zenith_deg: number;
  predicted_shortwave_radiation_wm2: number;
  estimated_energy_output_watts: number;
  optimal_tilt_deg: number;
  panel_facing_direction: string;
  model_used: string;
  weather_source: string;
  weather: {
    temperature_2m: number | null;
    relative_humidity_2m: number | null;
    cloud_cover: number | null;
    wind_speed_10m: number | null;
  };
}

export interface SolarModelHealthResponse {
  status: string;
  model_loaded: boolean;
  model_name: string | null;
  timestamp: string;
}

export interface EnergyForecastPoint {
  hour: number;
  timestamp: string;
  predicted_load_kw: number;
  temperature: number | null;
  humidity: number | null;
}

export interface EnergyForecastNextResponse {
  forecast_hours: number;
  from_time: string | null;
  to_time: string | null;
  predictions: Array<{
    time: string;
    predicted_demand_kw?: number;
    [key: string]: string | number | undefined;
  }>;
  total_predicted_kwh: number | null;
  avg_demand_kw: number | null;
}

export interface EnergySummaryResponse {
  system: Record<string, unknown> | null;
  model: {
    name?: string;
    trained?: boolean;
    metrics?: {
      r2?: number;
      mape?: number;
      mae?: number;
      rmse?: number;
      [key: string]: number | undefined;
    };
  } | null;
  dataset: Record<string, unknown> | null;
  economics: Record<string, unknown> | null;
  timestamp_utc: string | null;
}

export interface EnergyOptimizeAnnualResponse {
  annual_summary: Record<string, unknown>;
  monthly_breakdown: Array<Record<string, unknown>>;
  currency: string | null;
  system: Record<string, unknown> | null;
}

export interface CombinedAiInsightsResponse {
  solar_prediction: Record<string, unknown> | null;
  energy_summary: Record<string, unknown> | null;
  energy_forecast: EnergyForecastNextResponse | Record<string, unknown> | null;
  solar_model_available: boolean;
  energy_model_available: boolean;
  errors: string[];
}

/** UI view-model types (camelCase, matching mock-data shapes). */

export interface LiveStats {
  solarGeneration: number;
  batterySoc: number;
  currentTilt: number;
  recommendedTilt: number;
  predictedConsumption: number;
  todaySavings: number;
  aqi: number;
  temperature: number;
  humidity: number;
  windSpeed: number;
  cloudCover: number;
}

export interface BatteryOverview {
  soc: number;
  health: number;
  temperature: number;
  voltage: number;
  chargeRate: string;
  dischargeRate: string;
  status: string;
}

export interface HourlyGenerationPoint {
  time: string;
  generation: number;
  consumption: number;
  [key: string]: string | number;
}

export interface AlertItem {
  id: string;
  level: "info" | "warning" | "success";
  message: string;
  time: string;
}

export interface ActivityItem {
  id: string;
  icon: string;
  message: string;
  category: string;
  time: string;
}

export interface TelemetryRow {
  label: string;
  value: string;
  time: string;
}

export interface WeatherMetric {
  label: string;
  value: string;
}

export interface AirQualityMetric {
  label: string;
  value: string;
}

export interface DeviceRow {
  id: string;
  name: string;
  type: string;
  status: "online" | "offline";
  lastUpdate: string;
  uptime: string;
  [key: string]: string;
}

export interface WeatherForecastDay {
  day: string;
  high: number;
  low: number;
  condition: string;
  aqi: number;
}

export interface HistoricalWeatherPoint {
  day: string;
  temp: number;
  aqi: number;
}

export interface AiOrientation {
  recommendedTilt: number;
  confidence: number;
  expectedGain: number;
  lastUpdated: string;
}

export interface AiConsumption {
  nextHourLoad: number;
  peakTime: string;
  accuracy: number;
  peakLoad: number;
}

export interface PredictionHistoryRow {
  id: string;
  type: string;
  prediction: string;
  actual: string;
  accuracy: number;
  date: string;
  [key: string]: string | number;
}

export interface ModelPerformanceRow {
  name: string;
  accuracy: number;
  status: string;
}

export interface ForecastPoint {
  time: string;
  value: number;
  [key: string]: string | number;
}

export interface EnergyFlowDetailed {
  generated: number;
  stored: number;
  consumed: number;
  exported: number;
}

export interface ReportSummary {
  totalGeneration: number;
  totalConsumption: number;
  netExport: number;
  savings: number;
}

export interface MonthlyReportPoint {
  month: string;
  generation: number;
  consumption: number;
  export: number;
}

export interface AnalyticsStats {
  capacityFactor: number;
  performanceRatio: number;
  peakProduction: number;
  totalToday: number;
}

export interface ChartPoint {
  [key: string]: string | number;
}

export interface DashboardPageData {
  liveStats: LiveStats;
  analyticsStats: AnalyticsStats;
  batteryOverview: BatteryOverview;
  hourlyGeneration: HourlyGenerationPoint[];
  batteryAlerts: AlertItem[];
  activityFeed: ActivityItem[];
  telemetryRows: TelemetryRow[];
  weatherMetrics: WeatherMetric[];
  devices: DeviceRow[];
  systemStatusLabel: string;
}
