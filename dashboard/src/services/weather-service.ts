import { getAqiLabel } from "@/lib/utils";
import { apiService, firstItem } from "@/services/api-service";
import {
  mapHistoricalWeather,
  mapLiveStats,
  mapWeatherForecast,
  mapWeatherMetrics,
  mapAirQualityMetrics,
} from "@/services/mappers";
import type {
  AirQualityMetric,
  HistoricalWeatherPoint,
  LiveStats,
  WeatherForecastDay,
  WeatherMetric,
} from "@/types/api";

export interface WeatherPageData {
  liveStats: LiveStats;
  weatherMetrics: WeatherMetric[];
  weatherForecast: WeatherForecastDay[];
  historicalWeather: HistoricalWeatherPoint[];
  airQualityMetrics: AirQualityMetric[];
}

export async function fetchWeatherPageData(): Promise<WeatherPageData> {
  const [overview, weatherPage] = await Promise.all([
    apiService.getDashboard(),
    apiService.listWeather({ page_size: 100, sort_order: "desc" }),
  ]);

  const latestWeather = firstItem(weatherPage.items);
  const liveStats = mapLiveStats(overview, latestWeather, null, null);

  return {
    liveStats,
    weatherMetrics: mapWeatherMetrics(liveStats, latestWeather, getAqiLabel),
    weatherForecast: mapWeatherForecast(weatherPage.items),
    historicalWeather: mapHistoricalWeather(weatherPage.items),
    airQualityMetrics: mapAirQualityMetrics(liveStats.aqi),
  };
}
