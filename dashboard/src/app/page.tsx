"use client";

import {
  Activity,
  AlertTriangle,
  Battery,
  CloudSun,
  Gauge,
  Sun,
  Zap,
} from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { KpiCard } from "@/components/cards/kpi-card";
import { PanelCard } from "@/components/cards/panel-card";
import { PowerGenerationChart, BatteryGauge } from "@/components/charts/chart-widgets";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  activityFeed,
  analyticsStats,
  batteryAlerts,
  batteryOverview,
  devices,
  hourlyGeneration,
  liveStats,
} from "@/lib/mock-data";
import { getAqiLabel } from "@/lib/utils";

const telemetryRows = [
  { label: "Power Output", value: `${liveStats.solarGeneration} kW`, time: "Just now" },
  { label: "Panel Voltage", value: "24.6 V", time: "Just now" },
  { label: "Current Draw", value: "11.5 A", time: "Just now" },
  { label: "Irradiance", value: "785 W/m²", time: "Just now" },
  { label: "Tilt Angle", value: `${liveStats.currentTilt}°`, time: "Just now" },
];

const weatherMetrics = [
  { label: "Temperature", value: `${liveStats.temperature}°C` },
  { label: "Humidity", value: `${liveStats.humidity}%` },
  { label: "Cloud Cover", value: `${liveStats.cloudCover}%` },
  { label: "Wind Speed", value: `${liveStats.windSpeed} km/h` },
  { label: "GHI", value: "785 W/m²" },
  { label: "AQI", value: `${liveStats.aqi} ${getAqiLabel(liveStats.aqi)}` },
];

export default function DashboardPage() {
  const onlineDevices = devices.filter((d) => d.status === "online").length;

  return (
    <AppShell
      title="Dashboard"
      description="Real-time overview of your solar power system"
    >
      {/* Row 1 — KPIs */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-6">
        <KpiCard
          title="Current Power"
          value={`${(liveStats.solarGeneration * 1000).toFixed(0)} W`}
          trend="12.5% vs yesterday"
          trendUp
          icon={Zap}
          accent="sky"
        />
        <KpiCard
          title="Today's Energy"
          value={`${analyticsStats.totalToday} kWh`}
          trend="8.3% vs yesterday"
          trendUp
          icon={Sun}
          accent="amber"
        />
        <KpiCard
          title="Battery SOC"
          value={`${liveStats.batterySoc}%`}
          subtitle={batteryOverview.status}
          trend="5% vs yesterday"
          trendUp
          icon={Battery}
          accent="emerald"
        />
        <KpiCard
          title="Optimal Tilt"
          value={`${liveStats.recommendedTilt}°`}
          subtitle="AI Recommended"
          icon={Gauge}
          accent="purple"
        />
        <KpiCard
          title="Weather"
          value={`${liveStats.temperature}°C`}
          subtitle={`AQI ${liveStats.aqi} · ${getAqiLabel(liveStats.aqi)}`}
          icon={CloudSun}
          accent="orange"
        />
        <KpiCard
          title="System Status"
          value="Online"
          subtitle={`${onlineDevices}/${devices.length} devices active`}
          icon={Activity}
          accent="emerald"
        />
      </div>

      {/* Row 2 — Charts */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <PanelCard
            title="Power Generation (Today)"
            description="Actual vs predicted output"
            action={<Button variant="outline" size="sm">Today</Button>}
          >
            <PowerGenerationChart data={hourlyGeneration} />
          </PanelCard>
        </div>

        <div className="lg:col-span-2">
          <PanelCard title="Battery Status" description="Real-time SOC">
            <BatteryGauge value={batteryOverview.soc} />
            <div className="mt-4 space-y-2 border-t border-border pt-4">
              {[
                { label: "Voltage", value: "12.48 V" },
                { label: "Current", value: batteryOverview.chargeRate },
                { label: "Temp", value: `${batteryOverview.temperature}°C` },
              ].map((item) => (
                <div key={item.label} className="flex justify-between text-xs">
                  <span className="text-muted">{item.label}</span>
                  <span className="font-medium text-foreground">{item.value}</span>
                </div>
              ))}
              <div className="flex items-center gap-2 pt-1">
                <span className="h-2 w-2 rounded-full bg-success" />
                <span className="text-xs font-medium text-success">{batteryOverview.status}</span>
                <span className="text-xs text-muted">· Health {batteryOverview.health}%</span>
              </div>
            </div>
          </PanelCard>
        </div>

        <div className="lg:col-span-3">
          <PanelCard title="Weather Overview" description="Delhi, India">
            <div className="space-y-3">
              {weatherMetrics.map((m) => (
                <div key={m.label} className="flex items-center justify-between rounded-lg border border-border/50 bg-background/40 px-3 py-2">
                  <span className="text-xs text-muted">{m.label}</span>
                  <span className="text-sm font-medium text-foreground">{m.value}</span>
                </div>
              ))}
            </div>
          </PanelCard>
        </div>
      </div>

      {/* Row 3 — Lists */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <PanelCard
          title="Recent Alerts"
          action={<Button variant="ghost" size="sm" className="text-xs">View All</Button>}
        >
          <div className="space-y-3">
            {batteryAlerts.map((alert) => (
              <div key={alert.id} className="flex items-start gap-3 rounded-lg border border-border/50 p-3 transition-colors hover:bg-surface-elevated/30">
                <AlertTriangle className={cnIcon(alert.level)} />
                <div className="min-w-0 flex-1">
                  <p className="text-sm text-foreground">{alert.message}</p>
                  <p className="mt-0.5 text-xs text-muted">{alert.time}</p>
                </div>
                <Badge variant={alert.level === "warning" ? "warning" : alert.level === "success" ? "success" : "info"}>
                  {alert.level}
                </Badge>
              </div>
            ))}
          </div>
        </PanelCard>

        <PanelCard
          title="Recent Telemetry"
          action={<Button variant="ghost" size="sm" className="text-xs">View All</Button>}
        >
          <div className="space-y-2">
            {telemetryRows.map((row) => (
              <div key={row.label} className="flex items-center justify-between rounded-lg border border-border/50 px-3 py-2.5 hover:bg-surface-elevated/30">
                <div>
                  <p className="text-sm text-foreground">{row.label}</p>
                  <p className="text-xs text-muted">{row.time}</p>
                </div>
                <span className="text-sm font-semibold text-accent">{row.value}</span>
              </div>
            ))}
          </div>
        </PanelCard>

        <PanelCard
          title="System Logs"
          action={<Button variant="ghost" size="sm" className="text-xs">View All</Button>}
        >
          <div className="space-y-2">
            {activityFeed.map((log) => (
              <div key={log.id} className="flex items-start gap-3 rounded-lg border border-border/50 px-3 py-2.5 hover:bg-surface-elevated/30">
                <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-success" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm text-foreground">{log.message}</p>
                  <p className="text-xs text-muted">{log.time}</p>
                </div>
              </div>
            ))}
          </div>
        </PanelCard>
      </div>
    </AppShell>
  );
}

function cnIcon(level: string) {
  const base = "h-4 w-4 shrink-0 mt-0.5";
  if (level === "warning") return `${base} text-warning`;
  if (level === "success") return `${base} text-success`;
  return `${base} text-info`;
}
