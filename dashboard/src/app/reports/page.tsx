"use client";

import { DollarSign, FileDown, FileSpreadsheet, Leaf, Sun, Zap } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { KpiCard } from "@/components/cards/kpi-card";
import { DualBarChart, AreaTrendChart } from "@/components/charts/chart-widgets";
import { Button } from "@/components/ui/button";
import { monthlyReports, reportSummary } from "@/lib/mock-data";

export default function ReportsPage() {
  return (
    <AppShell
      title="Reports"
      description="Energy generation, consumption, and savings analytics"
    >
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <KpiCard
            title="Total Generation"
            value={`${reportSummary.totalGeneration} kWh`}
            trend="12% vs last month"
            trendUp
            icon={Sun}
            accent="amber"
          />
          <KpiCard
            title="Total Consumption"
            value={`${reportSummary.totalConsumption} kWh`}
            icon={Zap}
            accent="orange"
          />
          <KpiCard
            title="Net Export"
            value={`${reportSummary.netExport} kWh`}
            trend="8% vs last month"
            trendUp
            icon={Leaf}
            accent="sky"
          />
          <KpiCard
            title="Savings"
            value={`₹${reportSummary.savings}`}
            trend="15% vs last month"
            trendUp
            icon={DollarSign}
            accent="emerald"
          />
        </div>

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <PanelCard title="Monthly Reports" description="Generation vs consumption by month">
            <DualBarChart
              data={monthlyReports.map((d) => ({
                month: d.month,
                generation: d.generation,
                consumption: d.consumption,
              }))}
              keys={["generation", "consumption"]}
              height={240}
            />
          </PanelCard>
          <PanelCard title="Export Reports" description="Grid export volume over time">
            <AreaTrendChart
              data={monthlyReports.map((d) => ({ month: d.month, export: d.export }))}
              dataKey="export"
              color="#0EA5E9"
              height={240}
            />
          </PanelCard>
        </div>

        <PanelCard title="Usage Reports" description="Monthly consumption trend">
          <AreaTrendChart
            data={monthlyReports.map((d) => ({ month: d.month, usage: d.consumption }))}
            dataKey="usage"
            color="#F59E0B"
            height={220}
          />
        </PanelCard>

        <div className="flex flex-wrap gap-3">
          <Button>
            <FileDown className="h-4 w-4" /> Export PDF
          </Button>
          <Button variant="outline">
            <FileSpreadsheet className="h-4 w-4" /> Export CSV
          </Button>
        </div>
      </div>
    </AppShell>
  );
}
