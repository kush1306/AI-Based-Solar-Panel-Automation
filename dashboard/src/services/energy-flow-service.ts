import { apiService, firstItem } from "@/services/api-service";
import { mapEnergyFlow } from "@/services/mappers";
import type { EnergyFlowDetailed } from "@/types/api";

export interface EnergyFlowPageData {
  energyFlowDetailed: EnergyFlowDetailed;
}

export async function fetchEnergyFlowPageData(): Promise<EnergyFlowPageData> {
  const [overview, charts, batteryStatusPage, batteryPage] = await Promise.all([
    apiService.getDashboard(),
    apiService.getDashboardCharts(24),
    apiService.listBatteryStatus({ page_size: 1 }),
    apiService.listBattery(),
  ]);

  return {
    energyFlowDetailed: mapEnergyFlow(
      overview,
      charts,
      firstItem(batteryStatusPage.items),
      firstItem(batteryPage.items),
    ),
  };
}
