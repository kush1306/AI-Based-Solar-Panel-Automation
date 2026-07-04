"use client";

import { fetchDashboardPageData } from "@/services/dashboard-service";
import { useApiData } from "./use-api-data";

export function useDashboardData() {
  return useApiData(fetchDashboardPageData, []);
}
