"use client";

import { motion } from "framer-motion";
import { Brain, Clock, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { KpiCard } from "@/components/cards/kpi-card";
import { ForecastBarChart } from "@/components/charts/chart-widgets";
import { DataTable } from "@/components/tables/data-table";
import { Badge } from "@/components/ui/badge";
import { PageState } from "@/components/ui/page-state";
import { useAiPredictionsData } from "@/hooks/use-ai-predictions-data";

export default function AIPredictionsPage() {
  const { data, loading, error, retry } = useAiPredictionsData();

  return (
    <AppShell
      title="AI Predictions"
      description="Machine learning forecasts for orientation, consumption, and system optimization"
    >
      <PageState loading={loading} error={error} onRetry={retry}>
        {data ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              <PanelCard title="Solar Orientation AI" description="Optimal panel tilt recommendations">
                <div className="space-y-4">
                  <div className="flex justify-center">
                    <svg viewBox="0 0 100 70" className="h-24 w-36 rounded-lg border border-border bg-surface-elevated/50">
                      <g transform="rotate(-20 50 40)">
                        <rect x="20" y="20" width="60" height="30" fill="#0EA5E9" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                        <rect x="47" y="50" width="6" height="12" fill="#71717A" />
                      </g>
                    </svg>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="rounded-lg border border-border/50 bg-background/40 p-3 text-center">
                      <p className="text-xs text-muted">Recommended Tilt</p>
                      <p className="mt-1 text-3xl font-semibold text-accent">{data.aiOrientation.recommendedTilt}°</p>
                    </div>
                    <div className="rounded-lg border border-border/50 bg-background/40 p-3 text-center">
                      <p className="text-xs text-muted">Expected Gain</p>
                      <p className="mt-1 text-3xl font-semibold text-success">+{data.aiOrientation.expectedGain}%</p>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted">Confidence</span>
                      <span className="font-medium text-foreground">{data.aiOrientation.confidence}%</span>
                    </div>
                    <div className="mt-2 h-2 overflow-hidden rounded-full bg-surface-elevated">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${data.aiOrientation.confidence}%` }}
                        className="h-full rounded-full bg-success"
                      />
                    </div>
                  </div>
                </div>
              </PanelCard>

              <PanelCard title="Consumption Forecast AI" description="Load prediction and accuracy metrics">
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <KpiCard
                      title="Next Hour Load"
                      value={`${data.aiConsumption.nextHourLoad} kWh`}
                      icon={Zap}
                      accent="orange"
                    />
                    <KpiCard title="Peak Time" value={data.aiConsumption.peakTime} icon={Clock} accent="amber" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted">Accuracy Score</span>
                      <span className="font-medium text-foreground">{data.aiConsumption.accuracy}%</span>
                    </div>
                    <div className="mt-2 h-2 overflow-hidden rounded-full bg-surface-elevated">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${data.aiConsumption.accuracy}%` }}
                        className="h-full rounded-full bg-info"
                      />
                    </div>
                  </div>
                  <ForecastBarChart data={data.forecastData} height={140} />
                </div>
              </PanelCard>
            </div>

            <PanelCard title="Prediction History" description="Recent AI forecast results">
              <DataTable
                columns={[
                  { key: "id", header: "ID" },
                  {
                    key: "type",
                    header: "Type",
                    render: (row) => (
                      <Badge variant={row.type === "Tilt" ? "info" : "default"}>{String(row.type)}</Badge>
                    ),
                  },
                  { key: "prediction", header: "Prediction" },
                  { key: "actual", header: "Actual" },
                  {
                    key: "accuracy",
                    header: "Accuracy",
                    render: (row) => (
                      <span className="font-semibold text-success">{String(row.accuracy)}%</span>
                    ),
                  },
                  { key: "date", header: "Date" },
                ]}
                data={data.predictionHistory}
              />
            </PanelCard>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {data.modelPerformance.map((model) => (
                <PanelCard key={model.name} title={model.name} description="Model accuracy">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-3xl font-semibold text-foreground">{model.accuracy}%</p>
                      <p className="mt-1 text-sm text-muted">Accuracy</p>
                      <Badge variant="success" className="mt-3">
                        {model.status}
                      </Badge>
                    </div>
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-400/10 ring-1 ring-purple-400/20">
                      <Brain className="h-5 w-5 text-purple-400" />
                    </div>
                  </div>
                </PanelCard>
              ))}
            </div>
          </div>
        ) : null}
      </PageState>
    </AppShell>
  );
}
