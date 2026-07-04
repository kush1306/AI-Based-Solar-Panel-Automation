"use client";

import { fetchSolarAnalyticsPageData } from "@/services/solar-analytics-service";
import { useApiData } from "./use-api-data";

export function useSolarAnalyticsData() {
  return useApiData(fetchSolarAnalyticsPageData, []);
}
