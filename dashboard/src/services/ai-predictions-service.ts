import { apiService } from "@/services/api-service";
import {
  mapEnergyForecastChart,
  mapEnergyForecastToConsumption,
  mapModelPerformance,
  mapPredictionHistory,
  mapSolarModelToOrientation,
} from "@/services/mappers";
import type {
  AiConsumption,
  AiOrientation,
  CombinedAiInsightsResponse,
  EnergyForecastNextResponse,
  EnergyOptimizeAnnualResponse,
  EnergySummaryResponse,
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
  energyModelAvailable: boolean;
  energySummary: EnergySummaryResponse | null;
  annualOptimization: EnergyOptimizeAnnualResponse | null;
  aiInsights: CombinedAiInsightsResponse | null;
}

function asEnergySummary(
  value: Record<string, unknown> | EnergySummaryResponse | null | undefined,
): EnergySummaryResponse | null {
  if (!value || typeof value !== "object") {
    return null;
  }

  if ("economics" in value || "model" in value) {
    return value as EnergySummaryResponse;
  }

  return null;
}

function asEnergyForecast(
  value: EnergyForecastNextResponse | Record<string, unknown> | null | undefined,
): EnergyForecastNextResponse | null {
  if (!value || typeof value !== "object") {
    return null;
  }

  if ("predictions" in value && Array.isArray(value.predictions)) {
    return value as EnergyForecastNextResponse;
  }

  return null;
}

function emptyConsumption(): AiConsumption {
  return {
    nextHourLoad: 0,
    peakTime: "—",
    accuracy: 0,
    peakLoad: 0,
  };
}

async function fetchEnergyAiData(): Promise<{
  energyForecast: EnergyForecastNextResponse | null;
  energySummary: EnergySummaryResponse | null;
  annualOptimization: EnergyOptimizeAnnualResponse | null;
  aiInsights: CombinedAiInsightsResponse | null;
}> {
  const [forecastResult, summaryResult, optimizationResult, insightsResult] =
    await Promise.allSettled([
      apiService.getEnergyForecast(24),
      apiService.getEnergySummary(),
      apiService.getAnnualOptimization(),
      apiService.getAIInsights(24),
    ]);

  const energyForecast =
    forecastResult.status === "fulfilled" ? forecastResult.value : null;
  const energySummary =
    summaryResult.status === "fulfilled" ? summaryResult.value : null;
  const annualOptimization =
    optimizationResult.status === "fulfilled" ? optimizationResult.value : null;
  const aiInsights =
    insightsResult.status === "fulfilled" ? insightsResult.value : null;

  return { energyForecast, energySummary, annualOptimization, aiInsights };
}

export async function fetchAiPredictionsPageData(): Promise<AiPredictionsPageData> {
  const [predictionsPage, panelsPage, energyAi] = await Promise.all([
    apiService.listPredictions({ page_size: 10 }),
    apiService.listPanels(),
    fetchEnergyAiData(),
  ]);

  const { energyForecast, energySummary, annualOptimization, aiInsights } = energyAi;

  let aiOrientation: AiOrientation = {
    recommendedTilt: 0,
    confidence: 0,
    expectedGain: 0,
    lastUpdated: "—",
  };
  let solarHealth = null;
  let solarModelAvailable = false;

  try {
    const [solarPrediction, health] = await Promise.all([
      apiService.getSolarPrediction(),
      apiService.getSolarPredictionHealth(),
    ]);
    solarHealth = health;
    aiOrientation = mapSolarModelToOrientation(solarPrediction, health);
    solarModelAvailable = health.model_loaded;
  } catch {
    solarModelAvailable = false;
  }

  const resolvedForecast =
    energyForecast ?? asEnergyForecast(aiInsights?.energy_forecast ?? null);
  const resolvedSummary = energySummary ?? asEnergySummary(aiInsights?.energy_summary ?? null);
  const energyModelAvailable =
    aiInsights?.energy_model_available ??
    Boolean(resolvedForecast || resolvedSummary || annualOptimization);

  return {
    aiOrientation,
    aiConsumption: resolvedForecast
      ? mapEnergyForecastToConsumption(resolvedForecast, resolvedSummary, annualOptimization)
      : emptyConsumption(),
    predictionHistory: mapPredictionHistory(predictionsPage.items, panelsPage.items),
    modelPerformance: mapModelPerformance(
      solarHealth,
      resolvedSummary,
      energyModelAvailable,
    ),
    forecastData: resolvedForecast ? mapEnergyForecastChart(resolvedForecast) : [],
    solarModelAvailable,
    energyModelAvailable,
    energySummary: resolvedSummary,
    annualOptimization,
    aiInsights,
  };
}
