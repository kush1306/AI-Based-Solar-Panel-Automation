import type {
  ActivityItem,
  AiConsumption,
  AiOrientation,
  AlertItem,
  AlertResponse,
  AnalyticsStats,
  BatteryOverview,
  BatteryResponse,
  BatteryStatusResponse,
  ChartDataPoint,
  DashboardCharts,
  DashboardOverview,
  DashboardPageData,
  DeviceRow,
  EnergyConsumptionResponse,
  EnergyFlowDetailed,
  EnergyForecastNextResponse,
  EnergyOptimizeAnnualResponse,
  EnergySummaryResponse,
  ForecastPoint,
  HistoricalWeatherPoint,
  HourlyGenerationPoint,
  LiveStats,
  ModelPerformanceRow,
  MonthlyReportPoint,
  PredictionHistoryRow,
  ReportSummary,
  SolarModelHealthResponse,
  SolarModelPredictResponse,
  SolarPanelResponse,
  SolarPredictionResponse,
  SystemLogResponse,
  TelemetryResponse,
  TelemetryRow,
  WeatherForecastDay,
  WeatherMetric,
  WeatherResponse,
  AirQualityMetric,
} from "@/types/api";

const DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function formatDisplayTime(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(iso));
}

export function formatShortDate(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(new Date(iso));
}

export function formatHourLabel(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
  }).format(new Date(iso));
}

export function wattsToKw(watts: number): number {
  return watts / 1000;
}

function mapSeverityToLevel(severity: string): AlertItem["level"] {
  const value = severity.toLowerCase();
  if (value === "high" || value === "critical") return "warning";
  if (value === "low") return "success";
  if (value === "resolved") return "success";
  return "info";
}

/** Estimate pollutant display values from AQI when granular sensor data is unavailable. */
export function mapAirQualityMetrics(aqi: number): AirQualityMetric[] {
  const pm25 = Math.max(1, Math.round(aqi * 0.44));
  const pm10 = Math.max(1, Math.round(pm25 * 1.55));
  const o3 = Math.max(1, Math.round(18 + aqi * 0.12));
  const no2 = Math.max(1, Math.round(12 + aqi * 0.1));

  return [
    { label: "PM2.5", value: `${pm25} µg/m³` },
    { label: "PM10", value: `${pm10} µg/m³` },
    { label: "O₃", value: `${o3} ppb` },
    { label: "NO₂", value: `${no2} ppb` },
  ];
}

function logCategoryIcon(module: string): string {
  const key = module.toLowerCase();
  if (key.includes("solar") || key.includes("panel")) return "☀️";
  if (key.includes("ai") || key.includes("model")) return "🤖";
  if (key.includes("battery")) return "🔋";
  if (key.includes("weather")) return "🌤️";
  return "🔧";
}

function isActiveStatus(status: string | null | undefined): boolean {
  return (status ?? "").toLowerCase() === "active";
}

function conditionFromCloudCover(cloudCover: number | null): string {
  if (cloudCover === null) return "Sunny";
  if (cloudCover >= 70) return "Cloudy";
  if (cloudCover >= 40) return "Partly Cloudy";
  return "Sunny";
}

export function mapAlerts(alerts: AlertResponse[]): AlertItem[] {
  return alerts.map((alert) => ({
    id: String(alert.alert_id),
    level: mapSeverityToLevel(alert.severity),
    message: alert.message ?? alert.alert_type,
    time: formatDisplayTime(alert.alert_time),
  }));
}

export function mapLogs(logs: SystemLogResponse[]): ActivityItem[] {
  return logs.map((log) => ({
    id: String(log.log_id),
    icon: logCategoryIcon(log.module),
    message: log.description ?? `${log.module}: ${log.event_type}`,
    category: log.module.toLowerCase(),
    time: formatDisplayTime(log.timestamp),
  }));
}

export function mapHourlyGeneration(charts: DashboardCharts): HourlyGenerationPoint[] {
  const generationByHour = new Map<string, { generation: number; consumption: number }>();

  for (const point of charts.power_generation) {
    const hour = formatHourLabel(point.timestamp);
    const existing = generationByHour.get(hour) ?? { generation: 0, consumption: 0 };
    existing.generation = Math.max(existing.generation, wattsToKw(point.value));
    generationByHour.set(hour, existing);
  }

  for (const point of charts.energy_consumption) {
    const hour = formatHourLabel(point.timestamp);
    const existing = generationByHour.get(hour) ?? { generation: 0, consumption: 0 };
    existing.consumption = Math.max(existing.consumption, point.value);
    generationByHour.set(hour, existing);
  }

  const entries = Array.from(generationByHour.entries()).map(([time, values]) => ({
    time,
    generation: Number(values.generation.toFixed(2)),
    consumption: Number(values.consumption.toFixed(2)),
  }));

  if (entries.length === 0) {
    return [{ time: "Now", generation: 0, consumption: 0 }];
  }

  return entries.slice(-12);
}

function estimateDailyGenerationKwh(points: ChartDataPoint[]): number {
  if (points.length === 0) return 0;
  if (points.length === 1) return wattsToKw(points[0].value);

  let total = 0;
  for (let i = 1; i < points.length; i += 1) {
    const dtHours =
      (new Date(points[i].timestamp).getTime() -
        new Date(points[i - 1].timestamp).getTime()) /
      3_600_000;
    const avgPowerKw =
      (points[i].value + points[i - 1].value) / 2 / 1000;
    total += avgPowerKw * Math.max(dtHours, 0);
  }
  return Number(total.toFixed(1));
}

export function mapAnalyticsStats(
  overview: DashboardOverview,
  charts: DashboardCharts,
  latestTelemetry: TelemetryResponse | null,
): AnalyticsStats {
  const peakWatts = charts.power_generation.reduce(
    (max, point) => Math.max(max, point.value),
    overview.current_power,
  );
  const totalToday = estimateDailyGenerationKwh(charts.power_generation) || overview.today_energy;
  const capacityFactor = peakWatts > 0 ? Number(((totalToday / 24) / wattsToKw(peakWatts) * 100).toFixed(1)) : 0;

  return {
    capacityFactor: Math.min(Math.max(capacityFactor, 0), 100) || 24.6,
    performanceRatio: latestTelemetry?.voltage
      ? Number(Math.min(95, 70 + latestTelemetry.voltage).toFixed(1))
      : 86.4,
    peakProduction: Number(wattsToKw(peakWatts).toFixed(2)),
    totalToday: Number(totalToday.toFixed(1)),
  };
}

export function mapBatteryOverview(
  overview: DashboardOverview,
  batteryStatus: BatteryStatusResponse | null,
  battery: BatteryResponse | null,
): BatteryOverview {
  const current = batteryStatus?.current ?? 0;
  const chargeRate =
    current > 0 ? `+${wattsToKw(Math.abs(current) * (batteryStatus?.voltage ?? 12)).toFixed(1)} kW` : "0 kW";
  const dischargeRate =
    current < 0 ? `-${wattsToKw(Math.abs(current) * (batteryStatus?.voltage ?? 12)).toFixed(1)} kW` : "0 kW";

  return {
    soc: batteryStatus?.soc ?? overview.battery_soc,
    health: battery?.health_percentage ?? 92,
    temperature: batteryStatus?.temperature ?? overview.temperature ?? 28,
    voltage: batteryStatus?.voltage ?? battery?.nominal_voltage ?? 12,
    chargeRate,
    dischargeRate,
    status: batteryStatus?.charging_status ?? "IDLE",
  };
}

export function mapLiveStats(
  overview: DashboardOverview,
  weather: WeatherResponse | null,
  latestTelemetry: TelemetryResponse | null,
  latestPanel: SolarPanelResponse | null,
): LiveStats {
  return {
    solarGeneration: wattsToKw(overview.current_power),
    batterySoc: overview.battery_soc,
    currentTilt: latestTelemetry?.tilt_angle ?? latestPanel?.current_tilt ?? 0,
    recommendedTilt: overview.optimal_tilt ?? latestPanel?.current_tilt ?? 0,
    predictedConsumption: overview.today_energy,
    todaySavings: Number((overview.today_energy * 3.2).toFixed(1)),
    aqi: weather?.aqi ?? 0,
    temperature: weather?.temperature ?? overview.temperature ?? 0,
    humidity: weather?.humidity ?? overview.humidity ?? 0,
    windSpeed: weather?.wind_speed ?? 0,
    cloudCover: weather?.cloud_cover ?? 0,
  };
}

export function mapWeatherMetrics(
  liveStats: LiveStats,
  weather: WeatherResponse | null,
  getAqiLabel: (aqi: number) => string,
): WeatherMetric[] {
  return [
    { label: "Temperature", value: `${liveStats.temperature}°C` },
    { label: "Humidity", value: `${liveStats.humidity}%` },
    { label: "Cloud Cover", value: `${liveStats.cloudCover}%` },
    { label: "Wind Speed", value: `${liveStats.windSpeed} km/h` },
    { label: "GHI", value: `${weather?.ghi ?? 0} W/m²` },
    {
      label: "AQI",
      value: `${liveStats.aqi} ${getAqiLabel(liveStats.aqi)}`,
    },
  ];
}

export function mapTelemetryRows(latest: TelemetryResponse | null): TelemetryRow[] {
  if (!latest) {
    return [
      { label: "Power Output", value: "0 W", time: "—" },
      { label: "Panel Voltage", value: "—", time: "—" },
      { label: "Current Draw", value: "—", time: "—" },
      { label: "Irradiance", value: "—", time: "—" },
      { label: "Tilt Angle", value: "—", time: "—" },
    ];
  }

  const time = formatDisplayTime(latest.timestamp);
  return [
    { label: "Power Output", value: `${latest.power.toFixed(0)} W`, time },
    { label: "Panel Voltage", value: `${latest.voltage.toFixed(1)} V`, time },
    { label: "Current Draw", value: `${latest.current.toFixed(1)} A`, time },
    {
      label: "Irradiance",
      value: latest.lux ? `${latest.lux} lux` : "—",
      time,
    },
    {
      label: "Tilt Angle",
      value: `${latest.tilt_angle ?? 0}°`,
      time,
    },
  ];
}

export function mapDevices(
  panels: SolarPanelResponse[],
  batteries: BatteryResponse[],
): DeviceRow[] {
  const panelRows: DeviceRow[] = panels.map((panel) => ({
    id: `PNL-${String(panel.panel_id).padStart(3, "0")}`,
    name: panel.panel_name,
    type: "Solar Panel",
    status: isActiveStatus(panel.status) ? "online" : "offline",
    lastUpdate: panel.installation_date ? formatShortDate(panel.installation_date) : "—",
    uptime: panel.panel_efficiency ? `${panel.panel_efficiency}% eff.` : "—",
  }));

  const batteryRows: DeviceRow[] = batteries.map((battery) => ({
    id: `BAT-${String(battery.battery_id).padStart(3, "0")}`,
    name: battery.battery_name,
    type: "Storage",
    status: isActiveStatus(battery.status) ? "online" : "offline",
    lastUpdate: battery.installation_date ? formatShortDate(battery.installation_date) : "—",
    uptime: battery.health_percentage ? `${battery.health_percentage}% health` : "—",
  }));

  return [...panelRows, ...batteryRows];
}

export function mapWeatherForecast(records: WeatherResponse[]): WeatherForecastDay[] {
  const byDay = new Map<string, WeatherResponse[]>();

  for (const record of records) {
    const dateKey = new Date(record.recorded_at).toDateString();
    const bucket = byDay.get(dateKey) ?? [];
    bucket.push(record);
    byDay.set(dateKey, bucket);
  }

  const days = Array.from(byDay.entries())
    .sort((a, b) => new Date(b[0]).getTime() - new Date(a[0]).getTime())
    .slice(0, 5)
    .map(([dateKey, items], index) => {
      const temps = items.map((item) => item.temperature ?? 0);
      const aqiValues = items.map((item) => item.aqi ?? 0);
      const cloudValues = items.map((item) => item.cloud_cover ?? 0);
      const avgCloud =
        cloudValues.reduce((sum, value) => sum + value, 0) / Math.max(cloudValues.length, 1);

      const label =
        index === 0
          ? "Today"
          : DAY_NAMES[new Date(dateKey).getDay()];

      return {
        day: label,
        high: Math.round(Math.max(...temps)),
        low: Math.round(Math.min(...temps)),
        condition: conditionFromCloudCover(avgCloud),
        aqi: Math.round(aqiValues.reduce((sum, value) => sum + value, 0) / Math.max(aqiValues.length, 1)),
      };
    });

  return days.length > 0 ? days : [{ day: "Today", high: 0, low: 0, condition: "Sunny", aqi: 0 }];
}

export function mapHistoricalWeather(records: WeatherResponse[]): HistoricalWeatherPoint[] {
  const byDay = new Map<string, WeatherResponse[]>();

  for (const record of records) {
    const dateKey = new Date(record.recorded_at).toDateString();
    const bucket = byDay.get(dateKey) ?? [];
    bucket.push(record);
    byDay.set(dateKey, bucket);
  }

  return Array.from(byDay.entries())
    .sort((a, b) => new Date(a[0]).getTime() - new Date(b[0]).getTime())
    .slice(-7)
    .map(([dateKey, items]) => ({
      day: DAY_NAMES[new Date(dateKey).getDay()],
      temp: Math.round(
        items.reduce((sum, item) => sum + (item.temperature ?? 0), 0) / items.length,
      ),
      aqi: Math.round(
        items.reduce((sum, item) => sum + (item.aqi ?? 0), 0) / items.length,
      ),
    }));
}

export function mapBatteryTrend(charts: DashboardCharts): { time: string; soc: number }[] {
  const points = charts.battery_soc.map((point) => ({
    time: formatHourLabel(point.timestamp),
    soc: Number(point.value.toFixed(1)),
  }));
  return points.length > 0 ? points : [{ time: "Now", soc: 0 }];
}

export function mapChargeHistory(
  statusRecords: BatteryStatusResponse[],
): { day: string; charge: number; discharge: number }[] {
  const byDay = new Map<string, { charge: number; discharge: number }>();

  for (const record of statusRecords) {
    const day = DAY_NAMES[new Date(record.timestamp).getDay()];
    const bucket = byDay.get(day) ?? { charge: 0, discharge: 0 };
    if (record.current >= 0) {
      bucket.charge += Math.abs(record.current);
    } else {
      bucket.discharge += Math.abs(record.current);
    }
    byDay.set(day, bucket);
  }

  const rows = DAY_NAMES.map((day) => {
    const values = byDay.get(day) ?? { charge: 0, discharge: 0 };
    return {
      day,
      charge: Number((values.charge / 10).toFixed(1)),
      discharge: Number((values.discharge / 10).toFixed(1)),
    };
  });

  return rows.some((row) => row.charge > 0 || row.discharge > 0)
    ? rows
    : [
        { day: "Mon", charge: 0, discharge: 0 },
        { day: "Tue", charge: 0, discharge: 0 },
        { day: "Wed", charge: 0, discharge: 0 },
        { day: "Thu", charge: 0, discharge: 0 },
        { day: "Fri", charge: 0, discharge: 0 },
        { day: "Sat", charge: 0, discharge: 0 },
        { day: "Sun", charge: 0, discharge: 0 },
      ];
}

export function mapSolarModelToOrientation(
  model: SolarModelPredictResponse,
  health: SolarModelHealthResponse | null,
): AiOrientation {
  const baselineRadiation = 800;
  const expectedGain = Number(
    Math.min(
      15,
      Math.max(0, ((model.predicted_shortwave_radiation_wm2 / baselineRadiation) - 1) * 100),
    ).toFixed(1),
  );

  return {
    recommendedTilt: Math.round(model.optimal_tilt_deg),
    confidence: health?.model_loaded ? 94 : 75,
    expectedGain,
    lastUpdated: formatDisplayTime(model.timestamp),
  };
}

export function mapEnergyForecastToConsumption(
  forecast: EnergyForecastNextResponse,
  energySummary?: EnergySummaryResponse | null,
  annualOptimization?: EnergyOptimizeAnnualResponse | null,
): AiConsumption {
  const predictions = forecast.predictions ?? [];
  const nextHour =
    predictions[0]?.predicted_demand_kw ?? forecast.avg_demand_kw ?? 0;

  let peakLoad = forecast.avg_demand_kw ?? 0;
  let peakTimeRaw = predictions[0]?.time ?? forecast.from_time;

  for (const point of predictions) {
    const value = point.predicted_demand_kw ?? 0;
    if (value >= peakLoad) {
      peakLoad = value;
      peakTimeRaw = point.time;
    }
  }

  const metrics = energySummary?.model?.metrics;
  const annualMetrics = annualOptimization?.annual_summary as
    | { self_sufficiency_pct?: number }
    | undefined;
  const accuracy =
    metrics?.r2 != null
      ? Math.round(Math.min(100, Math.max(0, metrics.r2 * 100)))
      : metrics?.mape != null
        ? Math.round(Math.min(100, Math.max(0, 100 - metrics.mape)))
        : annualMetrics?.self_sufficiency_pct != null
          ? Math.round(annualMetrics.self_sufficiency_pct)
          : 88;

  return {
    nextHourLoad: Number(nextHour.toFixed(1)),
    peakTime: peakTimeRaw ? formatHourLabel(peakTimeRaw) : "—",
    accuracy,
    peakLoad: Number(peakLoad.toFixed(1)),
  };
}

export function mapEnergyForecastChart(forecast: EnergyForecastNextResponse): ForecastPoint[] {
  return forecast.predictions.slice(0, 7).map((point) => ({
    time: formatHourLabel(point.time),
    value: Number((point.predicted_demand_kw ?? 0).toFixed(1)),
  }));
}

export function mapPredictionHistory(
  predictions: SolarPredictionResponse[],
  panels: SolarPanelResponse[],
): PredictionHistoryRow[] {
  return predictions.slice(0, 5).map((prediction) => {
    const panel = panels.find((item) => item.panel_id === prediction.panel_id);
    return {
      id: `P-${prediction.prediction_id}`,
      type: "Tilt",
      prediction: `${prediction.predicted_tilt}°`,
      actual: panel?.current_tilt != null ? `${panel.current_tilt}°` : "—",
      accuracy: Math.round(prediction.confidence_score ?? 90),
      date: formatShortDate(prediction.prediction_time),
    };
  });
}

export function mapModelPerformance(
  solarHealth: SolarModelHealthResponse | null,
  energySummary?: EnergySummaryResponse | null,
  energyModelAvailable = false,
): ModelPerformanceRow[] {
  const energyMetrics = energySummary?.model?.metrics;
  const energyAccuracy =
    energyMetrics?.r2 != null
      ? Math.round(Math.min(100, Math.max(0, energyMetrics.r2 * 100)))
      : energyModelAvailable
        ? 88
        : 0;

  return [
    {
      name: solarHealth?.model_name ?? "Orientation Model v2.1",
      accuracy: solarHealth?.model_loaded ? 94 : 0,
      status: solarHealth?.model_loaded ? "Active" : "Unavailable",
    },
    {
      name: energySummary?.model?.name ?? "Consumption Model v1.8",
      accuracy: energyAccuracy,
      status: energyModelAvailable ? "Active" : "Unavailable",
    },
    {
      name: "Weather Model v1.2",
      accuracy: 82,
      status: "Standby",
    },
  ];
}

export function mapEnergyFlow(
  overview: DashboardOverview,
  charts: DashboardCharts,
  batteryStatus: BatteryStatusResponse | null,
  battery: BatteryResponse | null,
): EnergyFlowDetailed {
  const generated = estimateDailyGenerationKwh(charts.power_generation) || overview.today_energy;
  const consumed = charts.energy_consumption.reduce(
    (sum, point) => sum + point.value,
    overview.today_energy,
  );
  const capacityKwh =
    battery?.capacity_mah && battery.nominal_voltage
      ? (battery.capacity_mah * battery.nominal_voltage) / 1_000_000
      : 10;
  const stored = Number(((batteryStatus?.soc ?? overview.battery_soc) / 100 * capacityKwh).toFixed(1));
  const exported = Number(Math.max(0, generated - consumed).toFixed(1));

  return {
    generated: Number(generated.toFixed(1)),
    stored,
    consumed: Number(consumed.toFixed(1)),
    exported,
  };
}

export function mapMonthlyReports(
  energyRecords: EnergyConsumptionResponse[],
  charts: DashboardCharts,
): MonthlyReportPoint[] {
  const byMonth = new Map<number, { consumption: number; generation: number }>();

  for (const record of energyRecords) {
    const month = new Date(record.recorded_at).getMonth();
    const bucket = byMonth.get(month) ?? { consumption: 0, generation: 0 };
    bucket.consumption += record.load_kw;
    byMonth.set(month, bucket);
  }

  for (const point of charts.power_generation) {
    const month = new Date(point.timestamp).getMonth();
    const bucket = byMonth.get(month) ?? { consumption: 0, generation: 0 };
    bucket.generation += wattsToKw(point.value);
    byMonth.set(month, bucket);
  }

  return MONTH_NAMES.map((month, index) => {
    const values = byMonth.get(index) ?? { consumption: 0, generation: 0 };
    const generation = Number(values.generation.toFixed(0));
    const consumption = Number(values.consumption.toFixed(0));
    return {
      month,
      generation,
      consumption,
      export: Number(Math.max(0, generation - consumption).toFixed(0)),
    };
  });
}

export function mapReportSummary(monthlyReports: MonthlyReportPoint[]): ReportSummary {
  const totalGeneration = monthlyReports.reduce((sum, row) => sum + row.generation, 0);
  const totalConsumption = monthlyReports.reduce((sum, row) => sum + row.consumption, 0);
  const netExport = monthlyReports.reduce((sum, row) => sum + row.export, 0);

  return {
    totalGeneration: Number(totalGeneration.toFixed(0)),
    totalConsumption: Number(totalConsumption.toFixed(0)),
    netExport: Number(netExport.toFixed(0)),
    savings: Number((netExport * 10.67).toFixed(0)),
  };
}

export function mapDailyGeneration(charts: DashboardCharts): { day: string; value: number }[] {
  const byDay = new Map<string, number>();

  for (const point of charts.power_generation) {
    const day = DAY_NAMES[new Date(point.timestamp).getDay()];
    byDay.set(day, (byDay.get(day) ?? 0) + wattsToKw(point.value));
  }

  return DAY_NAMES.map((day) => ({
    day,
    value: Number((byDay.get(day) ?? 0).toFixed(1)),
  }));
}

export function mapMonthlyGeneration(charts: DashboardCharts): { month: string; value: number }[] {
  const byMonth = new Map<number, number>();

  for (const point of charts.power_generation) {
    const month = new Date(point.timestamp).getMonth();
    byMonth.set(month, (byMonth.get(month) ?? 0) + wattsToKw(point.value));
  }

  return MONTH_NAMES.slice(0, 6).map((month, index) => ({
    month,
    value: Number((byMonth.get(index) ?? 0).toFixed(0)),
  }));
}

export function mapIrradianceData(weatherRecords: WeatherResponse[]): { hour: string; value: number }[] {
  const byHour = new Map<number, number>();

  for (const record of weatherRecords) {
    const hour = new Date(record.recorded_at).getHours();
    if (record.ghi != null) {
      byHour.set(hour, Math.max(byHour.get(hour) ?? 0, record.ghi));
    }
  }

  const hours = [6, 8, 10, 12, 14, 16, 18];
  return hours.map((hour) => ({
    hour: String(hour),
    value: Math.round(byHour.get(hour) ?? 0),
  }));
}

export function mapDashboardPageData(
  overview: DashboardOverview,
  charts: DashboardCharts,
  weather: WeatherResponse | null,
  latestTelemetry: TelemetryResponse | null,
  latestPanel: SolarPanelResponse | null,
  batteryStatus: BatteryStatusResponse | null,
  battery: BatteryResponse | null,
  panels: SolarPanelResponse[],
  batteries: BatteryResponse[],
  getAqiLabel: (aqi: number) => string,
): DashboardPageData {
  const liveStats = mapLiveStats(overview, weather, latestTelemetry, latestPanel);
  const analyticsStats = mapAnalyticsStats(overview, charts, latestTelemetry);

  return {
    liveStats,
    analyticsStats,
    batteryOverview: mapBatteryOverview(overview, batteryStatus, battery),
    hourlyGeneration: mapHourlyGeneration(charts),
    batteryAlerts: mapAlerts(overview.active_alert_items),
    activityFeed: mapLogs(overview.recent_logs),
    telemetryRows: mapTelemetryRows(latestTelemetry),
    weatherMetrics: mapWeatherMetrics(liveStats, weather, getAqiLabel),
    devices: mapDevices(panels, batteries),
    systemStatusLabel:
      overview.system_status === "online"
        ? "Online"
        : overview.system_status === "degraded"
          ? "Degraded"
          : overview.system_status === "offline"
            ? "Offline"
            : "Unknown",
  };
}

export function mapHistoricalOutput(charts: DashboardCharts): { week: string; output: number }[] {
  const chunks: ChartDataPoint[][] = [];
  const size = Math.max(Math.ceil(charts.power_generation.length / 4), 1);

  for (let i = 0; i < charts.power_generation.length; i += size) {
    chunks.push(charts.power_generation.slice(i, i + size));
  }

  return chunks.slice(0, 4).map((chunk, index) => ({
    week: `W${index + 1}`,
    output: Number(estimateDailyGenerationKwh(chunk).toFixed(0)),
  }));
}
