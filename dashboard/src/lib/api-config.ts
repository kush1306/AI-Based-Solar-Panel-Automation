/**
 * Backend API configuration for the Next.js dashboard.
 * Set NEXT_PUBLIC_API_URL in dashboard/.env.local (local) or at build time (production).
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
  logs: `${API_BASE_URL}/api/logs`,
  dashboard: `${API_BASE_URL}/api/dashboard`,
  dashboardCharts: `${API_BASE_URL}/api/dashboard/charts`,
} as const;

export async function fetchApi<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      (error as { error?: string }).error ??
        `API request failed (${response.status})`,
    );
  }
  return response.json() as Promise<T>;
}
