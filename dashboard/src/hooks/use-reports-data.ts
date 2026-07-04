"use client";

import { fetchReportsPageData } from "@/services/reports-service";
import { useApiData } from "./use-api-data";

export function useReportsData() {
  return useApiData(fetchReportsPageData, []);
}
