import { apiService, firstItem } from "@/services/api-service";
import {
  mapAlerts,
  mapBatteryOverview,
  mapBatteryTrend,
  mapChargeHistory,
} from "@/services/mappers";
import type { AlertItem, BatteryOverview } from "@/types/api";

export interface BatteryPageData {
  batteryOverview: BatteryOverview;
  batteryTrend: { time: string; soc: number }[];
  chargeHistory: { day: string; charge: number; discharge: number }[];
  batteryAlerts: AlertItem[];
}

export async function fetchBatteryPageData(): Promise<BatteryPageData> {
  const [overview, charts, batteryStatusPage, batteryPage, alertsPage] = await Promise.all([
    apiService.getDashboard(),
    apiService.getDashboardCharts(24),
    apiService.listBatteryStatus({ page_size: 200 }),
    apiService.listBattery(),
    apiService.listAlerts({ page_size: 10 }),
  ]);

  const latestStatus = firstItem(batteryStatusPage.items);
  const battery = firstItem(batteryPage.items);

  return {
    batteryOverview: mapBatteryOverview(overview, latestStatus, battery),
    batteryTrend: mapBatteryTrend(charts),
    chargeHistory: mapChargeHistory(batteryStatusPage.items),
    batteryAlerts: mapAlerts(alertsPage.items),
  };
}
