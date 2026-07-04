import { apiService, firstItem } from "@/services/api-service";
import {
  mapAnalyticsStats,
  mapDailyGeneration,
  mapHistoricalOutput,
  mapHourlyGeneration,
  mapIrradianceData,
  mapMonthlyGeneration,
} from "@/services/mappers";
import type { AnalyticsStats, HourlyGenerationPoint } from "@/types/api";

export interface SolarAnalyticsPageData {
  analyticsStats: AnalyticsStats;
  hourlyGeneration: HourlyGenerationPoint[];
  dailyGeneration: { day: string; value: number }[];
  monthlyGeneration: { month: string; value: number }[];
  irradianceData: { hour: string; value: number }[];
  historicalOutput: { week: string; output: number }[];
}

export async function fetchSolarAnalyticsPageData(): Promise<SolarAnalyticsPageData> {
  const [overview, charts, telemetryPage, weatherPage] = await Promise.all([
    apiService.getDashboard(),
    apiService.getDashboardCharts(24 * 7),
    apiService.listTelemetry({ page_size: 1 }),
    apiService.listWeather({ page_size: 200 }),
  ]);

  const latestTelemetry = firstItem(telemetryPage.items);

  return {
    analyticsStats: mapAnalyticsStats(overview, charts, latestTelemetry),
    hourlyGeneration: mapHourlyGeneration(charts),
    dailyGeneration: mapDailyGeneration(charts),
    monthlyGeneration: mapMonthlyGeneration(charts),
    irradianceData: mapIrradianceData(weatherPage.items),
    historicalOutput: mapHistoricalOutput(charts),
  };
}
