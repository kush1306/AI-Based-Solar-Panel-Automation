"use client";

import { fetchDevicesPageData } from "@/services/devices-service";
import { useApiData } from "./use-api-data";

export function useDevicesData() {
  return useApiData(fetchDevicesPageData, []);
}
