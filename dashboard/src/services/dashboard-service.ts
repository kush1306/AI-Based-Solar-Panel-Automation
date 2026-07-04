import { getAqiLabel } from "@/lib/utils";
import { apiService, firstItem } from "@/services/api-service";
import { mapDashboardPageData } from "@/services/mappers";
import type { DashboardPageData } from "@/types/api";

export async function fetchDashboardPageData(): Promise<DashboardPageData> {
  const [overview, charts, weatherPage, telemetryPage, panelsPage, batteriesPage, batteryStatusPage] =
    await Promise.all([
      apiService.getDashboard(),
      apiService.getDashboardCharts(24),
      apiService.listWeather({ page_size: 1 }),
      apiService.listTelemetry({ page_size: 1 }),
      apiService.listPanels(),
      apiService.listBattery(),
      apiService.listBatteryStatus({ page_size: 1 }),
    ]);

  const weather = firstItem(weatherPage.items);
  const latestTelemetry = firstItem(telemetryPage.items);
  const latestPanel = firstItem(panelsPage.items);
  const battery = firstItem(batteriesPage.items);
  const batteryStatus = firstItem(batteryStatusPage.items);

  return mapDashboardPageData(
    overview,
    charts,
    weather,
    latestTelemetry,
    latestPanel,
    batteryStatus,
    battery,
    panelsPage.items,
    batteriesPage.items,
    getAqiLabel,
  );
}
