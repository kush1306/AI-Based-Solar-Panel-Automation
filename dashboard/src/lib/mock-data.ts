// Dashboard KPIs & live stats
export const liveStats = {
  solarGeneration: 7.48,
  batterySoc: 67,
  currentTilt: 32,
  recommendedTilt: 35,
  predictedConsumption: 5.21,
  todaySavings: 128.4,
  aqi: 132,
  temperature: 32,
  humidity: 58,
  windSpeed: 12,
  cloudCover: 25,
  expectedGain: 4.2,
  servoStatus: "ACTIVE" as const,
  systemEfficiency: 87,
  orientationConfidence: 94,
  consumptionConfidence: 88,
};

export const kpiCards = [
  {
    id: "generation",
    title: "Solar Generation",
    value: "7.48 kW",
    trend: "12.5% vs yesterday",
    trendUp: true,
    icon: "sun",
    bg: "bg-cream",
  },
  {
    id: "battery",
    title: "Battery SOC",
    value: "67%",
    trend: "5% vs yesterday",
    trendUp: true,
    icon: "battery",
    bg: "bg-sage",
  },
  {
    id: "tilt",
    title: "Current Tilt",
    value: "32°",
    subtext: "REC: 35°",
    icon: "tilt",
    bg: "bg-sky",
  },
  {
    id: "consumption",
    title: "Predicted Consumption",
    value: "5.21 kWh",
    trend: "8.3% vs yesterday",
    trendUp: true,
    icon: "pulse",
    bg: "bg-pink",
  },
  {
    id: "savings",
    title: "Today's Savings",
    value: "₹128.4",
    trend: "15.7% vs yesterday",
    trendUp: true,
    icon: "piggy",
    bg: "bg-butter",
  },
  {
    id: "aqi",
    title: "AQI Impact",
    value: "MODERATE",
    subtext: "AQI 132",
    icon: "leaf",
    bg: "bg-sage",
  },
];

export const hourlyGeneration = [
  { time: "6AM", generation: 0.8, consumption: 1.2 },
  { time: "9AM", generation: 4.5, consumption: 2.1 },
  { time: "12PM", generation: 7.8, consumption: 3.4 },
  { time: "3PM", generation: 6.2, consumption: 4.1 },
  { time: "6PM", generation: 2.1, consumption: 5.8 },
  { time: "9PM", generation: 0, consumption: 4.2 },
];

export const forecastData = [
  { time: "6AM", value: 3.2 },
  { time: "9AM", value: 4.1 },
  { time: "12PM", value: 5.2 },
  { time: "3PM", value: 4.8 },
  { time: "6PM", value: 3.9 },
  { time: "9PM", value: 2.8 },
  { time: "12AM", value: 1.5 },
];

export const energyFlow = [
  { id: "solar", label: "Solar Panel", icon: "☀️", value: "7.48 kW", color: "bg-butter" },
  { id: "battery", label: "Battery", icon: "🔋", value: "67% SOC", color: "bg-sage" },
  { id: "house", label: "House Load", icon: "🏠", value: "5.21 kWh", color: "bg-pink" },
  { id: "grid", label: "Grid Export", icon: "⚡", value: "1.8 kW", color: "bg-sky" },
];

export const batteryOverview = {
  soc: 67,
  health: 92,
  temperature: 31,
  chargeRate: "+1.2 kW",
  dischargeRate: "-0.4 kW",
  status: "CHARGING" as const,
};

export const batteryTrend = [
  { time: "6AM", soc: 45 },
  { time: "9AM", soc: 52 },
  { time: "12PM", soc: 61 },
  { time: "3PM", soc: 67 },
  { time: "6PM", soc: 64 },
  { time: "9PM", soc: 58 },
];

export const chargeHistory = [
  { day: "Mon", charge: 12.4, discharge: 8.2 },
  { day: "Tue", charge: 14.1, discharge: 7.5 },
  { day: "Wed", charge: 13.8, discharge: 9.1 },
  { day: "Thu", charge: 15.2, discharge: 8.8 },
  { day: "Fri", charge: 14.6, discharge: 7.9 },
  { day: "Sat", charge: 11.3, discharge: 6.4 },
  { day: "Sun", charge: 13.0, discharge: 7.1 },
];

export const batteryAlerts = [
  { id: "1", level: "info", message: "Battery entered charging mode", time: "10:05 AM" },
  { id: "2", level: "success", message: "Health check passed — 92%", time: "9:30 AM" },
  { id: "3", level: "warning", message: "Temperature slightly elevated (31°C)", time: "8:45 AM" },
];

export const activityFeed = [
  { id: "1", icon: "☀️", message: "Solar panel tilt adjusted to 32°", category: "solar", time: "10:22 AM" },
  { id: "2", icon: "🤖", message: "AI recommended tilt change to 35°", category: "ai", time: "10:18 AM" },
  { id: "3", icon: "🔋", message: "Battery entered charging mode at 65%", category: "battery", time: "10:05 AM" },
  { id: "4", icon: "🌤️", message: "Weather update: AQI rose to 132", category: "weather", time: "9:48 AM" },
  { id: "5", icon: "⚡", message: "Peak generation reached: 7.48 kW", category: "solar", time: "9:30 AM" },
  { id: "6", icon: "🔧", message: "Servo motor calibration complete", category: "system", time: "9:15 AM" },
];

// Solar Analytics
export const dailyGeneration = [
  { day: "Mon", value: 42.3 },
  { day: "Tue", value: 45.8 },
  { day: "Wed", value: 38.1 },
  { day: "Thu", value: 47.2 },
  { day: "Fri", value: 44.6 },
  { day: "Sat", value: 41.0 },
  { day: "Sun", value: 43.5 },
];

export const monthlyGeneration = [
  { month: "Jan", value: 980 },
  { month: "Feb", value: 1050 },
  { month: "Mar", value: 1180 },
  { month: "Apr", value: 1320 },
  { month: "May", value: 1410 },
  { month: "Jun", value: 1280 },
];

export const irradianceData = [
  { hour: "6", value: 120 },
  { hour: "8", value: 380 },
  { hour: "10", value: 720 },
  { hour: "12", value: 950 },
  { hour: "14", value: 880 },
  { hour: "16", value: 640 },
  { hour: "18", value: 210 },
];

export const historicalOutput = [
  { week: "W1", output: 280 },
  { week: "W2", output: 310 },
  { week: "W3", output: 295 },
  { week: "W4", output: 330 },
];

export const analyticsStats = {
  capacityFactor: 24.6,
  performanceRatio: 86.4,
  peakProduction: 8.12,
  totalToday: 43.5,
};

// AI Predictions
export const aiOrientation = {
  recommendedTilt: 35,
  confidence: 94,
  expectedGain: 4.2,
  lastUpdated: "10:18 AM",
};

export const aiConsumption = {
  nextHourLoad: 5.8,
  peakTime: "7:30 PM",
  accuracy: 88,
  peakLoad: 6.4,
};

export const predictionHistory = [
  { id: "P-1042", type: "Tilt", prediction: "35°", actual: "32°", accuracy: 91, date: "Jun 21" },
  { id: "P-1041", type: "Load", prediction: "5.4 kWh", actual: "5.2 kWh", accuracy: 96, date: "Jun 21" },
  { id: "P-1040", type: "Tilt", prediction: "34°", actual: "34°", accuracy: 100, date: "Jun 20" },
  { id: "P-1039", type: "Load", prediction: "4.8 kWh", actual: "5.1 kWh", accuracy: 87, date: "Jun 20" },
  { id: "P-1038", type: "Tilt", prediction: "33°", actual: "33°", accuracy: 98, date: "Jun 19" },
];

export const modelPerformance = [
  { name: "Orientation Model v2.1", accuracy: 94, status: "Active" },
  { name: "Consumption Model v1.8", accuracy: 88, status: "Active" },
  { name: "Weather Model v1.2", accuracy: 82, status: "Standby" },
];

// Energy Flow page
export const energyFlowDetailed = {
  generated: 43.5,
  stored: 18.2,
  consumed: 31.4,
  exported: 12.1,
};

// Weather
export const weatherForecast = [
  { day: "Today", high: 34, low: 26, condition: "Sunny", aqi: 132 },
  { day: "Mon", high: 33, low: 25, condition: "Partly Cloudy", aqi: 118 },
  { day: "Tue", high: 31, low: 24, condition: "Cloudy", aqi: 105 },
  { day: "Wed", high: 30, low: 23, condition: "Light Rain", aqi: 78 },
  { day: "Thu", high: 32, low: 24, condition: "Sunny", aqi: 95 },
];

export const historicalWeather = [
  { day: "Mon", temp: 32, aqi: 140 },
  { day: "Tue", temp: 31, aqi: 125 },
  { day: "Wed", temp: 30, aqi: 110 },
  { day: "Thu", temp: 33, aqi: 132 },
  { day: "Fri", temp: 32, aqi: 118 },
  { day: "Sat", temp: 31, aqi: 105 },
  { day: "Sun", temp: 32, aqi: 128 },
];

// Devices
export const devices = [
  { id: "INV-001", name: "Solar Inverter", type: "Inverter", status: "online", lastUpdate: "10:24 AM", uptime: "99.8%" },
  { id: "BAT-001", name: "Battery System", type: "Storage", status: "online", lastUpdate: "10:23 AM", uptime: "99.5%" },
  { id: "WS-001", name: "Weather Station", type: "Sensor", status: "online", lastUpdate: "10:20 AM", uptime: "98.9%" },
  { id: "SRV-001", name: "Tilt Motor", type: "Actuator", status: "online", lastUpdate: "10:22 AM", uptime: "99.2%" },
  { id: "SM-001", name: "Smart Meter", type: "Meter", status: "offline", lastUpdate: "9:45 AM", uptime: "97.1%" },
];

// Reports
export const reportSummary = {
  totalGeneration: 1280,
  totalConsumption: 920,
  netExport: 360,
  savings: 3840,
};

export const monthlyReports = [
  { month: "Jan", generation: 980, consumption: 720, export: 260 },
  { month: "Feb", generation: 1050, consumption: 740, export: 310 },
  { month: "Mar", generation: 1180, consumption: 810, export: 370 },
  { month: "Apr", generation: 1320, consumption: 880, export: 440 },
  { month: "May", generation: 1410, consumption: 920, export: 490 },
  { month: "Jun", generation: 1280, consumption: 890, export: 390 },
];

export const navItems = [
  { href: "/", label: "Dashboard", icon: "LayoutDashboard" },
  { href: "/solar-analytics", label: "Solar Analytics", icon: "BarChart3" },
  { href: "/ai-predictions", label: "AI Predictions", icon: "Brain" },
  { href: "/battery", label: "Battery Mgmt", icon: "Battery" },
  { href: "/energy-flow", label: "Energy Flow", icon: "Zap" },
  { href: "/weather", label: "Weather Intel", icon: "CloudSun" },
  { href: "/devices", label: "Device Monitor", icon: "Monitor" },
  { href: "/reports", label: "Reports", icon: "FileText" },
  { href: "/settings", label: "Settings", icon: "Settings" },
];

export const categoryColors: Record<string, string> = {
  solar: "bg-butter",
  battery: "bg-sage",
  ai: "bg-sky",
  weather: "bg-pink",
  system: "bg-orange",
};
