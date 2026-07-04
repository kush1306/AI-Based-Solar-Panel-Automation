"use client";

import { fetchBatteryPageData } from "@/services/battery-service";
import { useApiData } from "./use-api-data";

export function useBatteryData() {
  return useApiData(fetchBatteryPageData, []);
}
