import { apiService } from "@/services/api-service";
import {
  mapMockEnergyForecastChart,
  mapMockEnergyToConsumption,
  mapModelPerformance,
  mapPredictionHistory,
  mapSolarModelToOrientation,
} from "@/services/mappers";
import type {
  AiConsumption,
  AiOrientation,
  ForecastPoint,
  ModelPerformanceRow,
  PredictionHistoryRow,
} from "@/types/api";

export interface AiPredictionsPageData {
  aiOrientation: AiOrientation;
  aiConsumption: AiConsumption;
  predictionHistory: PredictionHistoryRow[];
  modelPerformance: ModelPerformanceRow[];
  forecastData: ForecastPoint[];
  solarModelAvailable: boolean;
}

export async function fetchAiPredictionsPageData(): Promise<AiPredictionsPageData> {
  const [predictionsPage, panelsPage, mockEnergy] = await Promise.all([
    apiService.listPredictions({ page_size: 10 }),
    apiService.listPanels(),
    apiService.getMockEnergyForecast(24),
  ]);

  let aiOrientation: AiOrientation = {
    recommendedTilt: 0,
    confidence: 0,
    expectedGain: 0,
    lastUpdated: "—",
  };
  let modelPerformance: ModelPerformanceRow[] = mapModelPerformance(null);
  let solarModelAvailable = false;

  try {
    const [solarPrediction, solarHealth] = await Promise.all([
      apiService.getSolarPrediction(),
      apiService.getSolarPredictionHealth(),
    ]);
    aiOrientation = mapSolarModelToOrientation(solarPrediction, solarHealth);
    modelPerformance = mapModelPerformance(solarHealth);
    solarModelAvailable = solarHealth.model_loaded;
  } catch {
    solarModelAvailable = false;
  }

  return {
    aiOrientation,
    aiConsumption: mapMockEnergyToConsumption(mockEnergy),
    predictionHistory: mapPredictionHistory(predictionsPage.items, panelsPage.items),
    modelPerformance,
    forecastData: mapMockEnergyForecastChart(mockEnergy),
    solarModelAvailable,
  };
}
