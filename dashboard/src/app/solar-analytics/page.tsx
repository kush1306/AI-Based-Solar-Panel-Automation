"use client";

import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { KPIWidget } from "@/components/KPIWidget";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  LineTrendChart,
  AreaTrendChart,
  DualBarChart,
  EfficiencyGauge,
} from "@/components/ChartWidgets";
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
    <AppShell title="Solar Analytics">
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="generation">Generation</TabsTrigger>
          <TabsTrigger value="irradiance">Irradiance</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <KPIWidget title="Total Today" value={`${analyticsStats.totalToday} kWh`} icon="sun" bg="bg-butter" trend="8.2% vs yesterday" trendUp />
              <KPIWidget title="Peak Production" value={`${analyticsStats.peakProduction} kW`} icon="pulse" bg="bg-sky" />
              <KPIWidget title="Capacity Factor" value={`${analyticsStats.capacityFactor}%`} icon="tilt" bg="bg-sage" />
            </div>
            <WindowCard title="Solar Generation Overview">
              <LineTrendChart data={hourlyGeneration.map((d) => ({ time: d.time, value: d.generation }))} dataKey="value" color="#FFD84D" height={250} />
            </WindowCard>
            <WindowCard title="Historical Output" headerColor="bg-sage">
              <AreaTrendChart data={historicalOutput.map((d) => ({ week: d.week, output: d.output }))} dataKey="output" color="#A8D5BA" height={220} />
            </WindowCard>
          </div>
        </TabsContent>

        <TabsContent value="generation">
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <WindowCard title="Daily Generation">
              <LineTrendChart data={dailyGeneration.map((d) => ({ day: d.day, kwh: d.value }))} dataKey="kwh" color="#FFD84D" height={220} />
            </WindowCard>
            <WindowCard title="Monthly Generation" headerColor="bg-butter">
              <AreaTrendChart data={monthlyGeneration.map((d) => ({ month: d.month, kwh: d.value }))} dataKey="kwh" color="#FF9F45" height={220} />
            </WindowCard>
          </div>
        </TabsContent>

        <TabsContent value="irradiance">
          <WindowCard title="Irradiance Levels (W/m²)">
            <AreaTrendChart data={irradianceData.map((d) => ({ hour: `${d.hour}h`, w: d.value }))} dataKey="w" color="#8FD3FF" height={280} />
          </WindowCard>
        </TabsContent>

        <TabsContent value="performance">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <WindowCard title="Performance Ratio">
              <EfficiencyGauge value={analyticsStats.performanceRatio} />
            </WindowCard>
            <WindowCard title="Peak Production" headerColor="bg-orange">
              <div className="flex flex-col items-center justify-center py-8">
                <span className="text-5xl">⚡</span>
                <p className="mt-4 font-retro text-4xl font-bold">{analyticsStats.peakProduction} kW</p>
                <p className="font-retro text-lg opacity-70">Recorded at 12:30 PM</p>
              </div>
            </WindowCard>
            <WindowCard title="Daily vs Monthly" className="md:col-span-2">
              <DualBarChart data={monthlyGeneration.map((d) => ({ month: d.month, generation: d.value, target: d.value * 0.85 }))} keys={["generation", "target"]} height={250} />
            </WindowCard>
          </div>
        </TabsContent>
      </Tabs>
    </AppShell>
  );
}
