"use client";

import { fetchAiPredictionsPageData } from "@/services/ai-predictions-service";
import { useApiData } from "./use-api-data";

export function useAiPredictionsData() {
  return useApiData(fetchAiPredictionsPageData, []);
}
