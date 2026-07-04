"use client";

import { fetchWeatherPageData } from "@/services/weather-service";
import { useApiData } from "./use-api-data";

export function useWeatherData() {
  return useApiData(fetchWeatherPageData, []);
}
