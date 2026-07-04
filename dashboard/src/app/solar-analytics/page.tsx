"use client";

import { Gauge, Sun, TrendingUp, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { KpiCard } from "@/components/cards/kpi-card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  LineTrendChart,
  AreaTrendChart,
  DualBarChart,
  EfficiencyGauge,
} from "@/components/charts/chart-widgets";
import {
  dailyGeneration,
  monthlyGeneration,
  irradianceData,
  historicalOutput,
  analyticsStats,
  hourlyGeneration,
} from "@/lib/mock-data";

export default function SolarAnalyticsPage() {
  return (
    <AppShell
      title="Solar Analytics"
      description="Generation trends, irradiance data, and system performance metrics"
    >
      <Tabs defaultValue="overview">
        <TabsList className="mb-2">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="generation">Generation</TabsTrigger>
          <TabsTrigger value="irradiance">Irradiance</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <KpiCard
                title="Total Today"
                value={`${analyticsStats.totalToday} kWh`}
                trend="8.2% vs yesterday"
                trendUp
                icon={Sun}
                accent="amber"
              />
              <KpiCard
                title="Peak Production"
                value={`${analyticsStats.peakProduction} kW`}
                icon={Zap}
                accent="sky"
              />
              <KpiCard
                title="Capacity Factor"
                value={`${analyticsStats.capacityFactor}%`}
                icon={Gauge}
                accent="emerald"
              />
            </div>
            <PanelCard title="Solar Generation Overview" description="Hourly output today">
              <LineTrendChart
                data={hourlyGeneration.map((d) => ({ time: d.time, value: d.generation }))}
                dataKey="value"
                color="#F59E0B"
                height={250}
              />
            </PanelCard>
            <PanelCard title="Historical Output" description="Weekly generation trend">
              <AreaTrendChart
                data={historicalOutput.map((d) => ({ week: d.week, output: d.output }))}
                dataKey="output"
                color="#10B981"
                height={220}
              />
            </PanelCard>
          </div>
        </TabsContent>

        <TabsContent value="generation">
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <PanelCard title="Daily Generation" description="Last 7 days">
              <LineTrendChart
                data={dailyGeneration.map((d) => ({ day: d.day, kwh: d.value }))}
                dataKey="kwh"
                color="#F59E0B"
                height={220}
              />
            </PanelCard>
            <PanelCard title="Monthly Generation" description="Year-to-date monthly totals">
              <AreaTrendChart
                data={monthlyGeneration.map((d) => ({ month: d.month, kwh: d.value }))}
                dataKey="kwh"
                color="#0EA5E9"
                height={220}
              />
            </PanelCard>
          </div>
        </TabsContent>

        <TabsContent value="irradiance">
          <PanelCard title="Irradiance Levels (W/m²)" description="Solar irradiance throughout the day">
            <AreaTrendChart
              data={irradianceData.map((d) => ({ hour: `${d.hour}h`, w: d.value }))}
              dataKey="w"
              color="#0EA5E9"
              height={280}
            />
          </PanelCard>
        </TabsContent>

        <TabsContent value="performance">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <PanelCard title="Performance Ratio" description="System efficiency score">
              <EfficiencyGauge value={analyticsStats.performanceRatio} />
            </PanelCard>
            <PanelCard title="Peak Production" description="Maximum output recorded today">
              <div className="flex flex-col items-center justify-center py-8">
                <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-accent/10 ring-1 ring-accent/20">
                  <Zap className="h-7 w-7 text-accent" />
                </div>
                <p className="mt-4 text-4xl font-semibold tracking-tight text-foreground">
                  {analyticsStats.peakProduction} kW
                </p>
                <p className="mt-1 text-sm text-muted">Recorded at 12:30 PM</p>
              </div>
            </PanelCard>
            <PanelCard title="Daily vs Monthly" description="Actual generation vs target" className="md:col-span-2">
              <DualBarChart
                data={monthlyGeneration.map((d) => ({
                  month: d.month,
                  generation: d.value,
                  target: d.value * 0.85,
                }))}
                keys={["generation", "target"]}
                height={250}
              />
            </PanelCard>
          </div>
        </TabsContent>
      </Tabs>
    </AppShell>
  );
}
