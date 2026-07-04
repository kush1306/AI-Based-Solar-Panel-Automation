/**
 * Centralized API route definitions.
 * Base URL comes from NEXT_PUBLIC_API_URL — never hardcode hostnames in pages.
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const API_ROUTES = {
  health: `${API_BASE_URL}/health`,
  healthReady: `${API_BASE_URL}/health/ready`,
  docs: `${API_BASE_URL}/docs`,
  weather: `${API_BASE_URL}/api/weather`,
  panels: `${API_BASE_URL}/api/panels`,
  predictions: `${API_BASE_URL}/api/predictions`,
  energy: `${API_BASE_URL}/api/energy`,
  battery: `${API_BASE_URL}/api/battery`,
  batteryStatus: `${API_BASE_URL}/api/battery-status`,
  telemetry: `${API_BASE_URL}/api/telemetry`,
  alerts: `${API_BASE_URL}/api/alerts`,
  alertsActive: `${API_BASE_URL}/api/alerts/active`,
  alertsHistory: `${API_BASE_URL}/api/alerts/history`,
  logs: `${API_BASE_URL}/api/logs`,
  dashboard: `${API_BASE_URL}/api/dashboard`,
  dashboardCharts: `${API_BASE_URL}/api/dashboard/charts`,
  aiSolarPrediction: `${API_BASE_URL}/api/ai/solar-prediction`,
  aiSolarPredictionHealth: `${API_BASE_URL}/api/ai/solar-prediction/health`,
  mockEnergy: `${API_BASE_URL}/api/mock/energy`,
  mockSolarPrediction: `${API_BASE_URL}/api/mock/solar-prediction`,
} as const;
