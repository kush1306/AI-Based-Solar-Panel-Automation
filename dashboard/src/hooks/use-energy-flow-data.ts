"use client";

import { fetchEnergyFlowPageData } from "@/services/energy-flow-service";
import { useApiData } from "./use-api-data";

export function useEnergyFlowData() {
  return useApiData(fetchEnergyFlowPageData, []);
}
