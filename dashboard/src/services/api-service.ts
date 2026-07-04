import { fetchApi, fetchList } from "@/lib/api/client";
import { API_ROUTES } from "@/lib/api/routes";
import type {
  AlertResponse,
  BatteryResponse,
  BatteryStatusResponse,
  DashboardCharts,
  DashboardOverview,
  EnergyConsumptionResponse,
  MockEnergyForecastResponse,
  SolarModelHealthResponse,
  SolarModelPredictResponse,
  SolarPanelResponse,
  SolarPredictionResponse,
  TelemetryResponse,
  WeatherResponse,
} from "@/types/api";

export const apiService = {
  getDashboard(): Promise<DashboardOverview> {
    return fetchApi(API_ROUTES.dashboard);
  },

  getDashboardCharts(hours = 24): Promise<DashboardCharts> {
    return fetchApi(`${API_ROUTES.dashboardCharts}?hours=${hours}`);
  },

  listWeather(params?: { page_size?: number; sort_by?: string; sort_order?: "asc" | "desc" }) {
    return fetchList<WeatherResponse>(API_ROUTES.weather, {
      page: 1,
      page_size: params?.page_size ?? 100,
      sort_by: params?.sort_by ?? "recorded_at",
      sort_order: params?.sort_order ?? "desc",
    });
  },

  listPanels(params?: { page_size?: number }) {
    return fetchList<SolarPanelResponse>(API_ROUTES.panels, {
      page: 1,
      page_size: params?.page_size ?? 100,
    });
  },

  listPredictions(params?: { page_size?: number }) {
    return fetchList<SolarPredictionResponse>(API_ROUTES.predictions, {
      page: 1,
      page_size: params?.page_size ?? 20,
      sort_by: "prediction_time",
      sort_order: "desc",
    });
  },

  listEnergy(params?: { page_size?: number }) {
    return fetchList<EnergyConsumptionResponse>(API_ROUTES.energy, {
      page: 1,
      page_size: params?.page_size ?? 500,
      sort_by: "recorded_at",
      sort_order: "desc",
    });
  },

  listBattery(params?: { page_size?: number }) {
    return fetchList<BatteryResponse>(API_ROUTES.battery, {
      page: 1,
      page_size: params?.page_size ?? 20,
    });
  },

  listBatteryStatus(params?: { page_size?: number; sort_order?: "asc" | "desc" }) {
    return fetchList<BatteryStatusResponse>(API_ROUTES.batteryStatus, {
      page: 1,
      page_size: params?.page_size ?? 200,
      sort_by: "timestamp",
      sort_order: params?.sort_order ?? "desc",
    });
  },

  listTelemetry(params?: { page_size?: number; sort_order?: "asc" | "desc" }) {
    return fetchList<TelemetryResponse>(API_ROUTES.telemetry, {
      page: 1,
      page_size: params?.page_size ?? 20,
      sort_by: "timestamp",
      sort_order: params?.sort_order ?? "desc",
    });
  },

  listAlerts(params?: { page_size?: number }) {
    return fetchList<AlertResponse>(API_ROUTES.alerts, {
      page: 1,
      page_size: params?.page_size ?? 20,
      sort_by: "alert_time",
      sort_order: "desc",
    });
  },

  listActiveAlerts(): Promise<AlertResponse[]> {
    return fetchApi(API_ROUTES.alertsActive);
  },

  getSolarPrediction(): Promise<SolarModelPredictResponse> {
    return fetchApi(API_ROUTES.aiSolarPrediction);
  },

  getSolarPredictionHealth(): Promise<SolarModelHealthResponse> {
    return fetchApi(API_ROUTES.aiSolarPredictionHealth);
  },

  getMockEnergyForecast(horizonHours = 24): Promise<MockEnergyForecastResponse> {
    return fetchApi(`${API_ROUTES.mockEnergy}?horizon_hours=${horizonHours}`);
  },
};

export function firstItem<T>(items: T[]): T | null {
  return items.length > 0 ? items[0] : null;
}
