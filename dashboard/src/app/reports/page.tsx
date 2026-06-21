"use client";

import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { KPIWidget } from "@/components/KPIWidget";
import { DualBarChart, AreaTrendChart } from "@/components/ChartWidgets";
import { Button } from "@/components/ui/button";
import { monthlyReports, reportSummary } from "@/lib/mock-data";
import { FileDown, FileSpreadsheet } from "lucide-react";

export default function ReportsPage() {
  return (
    <AppShell title="Reports">
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <KPIWidget title="Total Generation" value={`${reportSummary.totalGeneration} kWh`} icon="sun" bg="bg-butter" trend="12% vs last month" trendUp />
          <KPIWidget title="Total Consumption" value={`${reportSummary.totalConsumption} kWh`} icon="pulse" bg="bg-pink" />
          <KPIWidget title="Net Export" value={`${reportSummary.netExport} kWh`} icon="leaf" bg="bg-sky" trend="8% vs last month" trendUp />
          <KPIWidget title="Savings" value={`₹${reportSummary.savings}`} icon="piggy" bg="bg-sage" trend="15% vs last month" trendUp />
        </div>

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <WindowCard title="Monthly Reports">
            <DualBarChart data={monthlyReports.map((d) => ({ month: d.month, generation: d.generation, consumption: d.consumption }))} keys={["generation", "consumption"]} height={240} />
          </WindowCard>
          <WindowCard title="Export Reports" headerColor="bg-sky">
            <AreaTrendChart data={monthlyReports.map((d) => ({ month: d.month, export: d.export }))} dataKey="export" color="#8FD3FF" height={240} />
          </WindowCard>
        </div>

        <WindowCard title="Usage Reports" headerColor="bg-pink">
          <AreaTrendChart data={monthlyReports.map((d) => ({ month: d.month, usage: d.consumption }))} dataKey="usage" color="#FFB6D5" height={220} />
        </WindowCard>

        <div className="flex flex-wrap gap-3">
          <Button><FileDown className="h-4 w-4" /> Export PDF</Button>
          <Button variant="secondary"><FileSpreadsheet className="h-4 w-4" /> Export CSV</Button>
        </div>
      </div>
    </AppShell>
  );
}
