import { apiService } from "@/services/api-service";
import { mapDevices } from "@/services/mappers";
import type { DeviceRow } from "@/types/api";

export interface DevicesPageData {
  devices: DeviceRow[];
}

export async function fetchDevicesPageData(): Promise<DevicesPageData> {
  const [panelsPage, batteriesPage] = await Promise.all([
    apiService.listPanels(),
    apiService.listBattery(),
  ]);

  return {
    devices: mapDevices(panelsPage.items, batteriesPage.items),
  };
}
