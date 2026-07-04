"use client";

import { AlertTriangle, Battery } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { BatteryGauge, LineTrendChart, DualBarChart } from "@/components/charts/chart-widgets";
import { Badge } from "@/components/ui/badge";
import { batteryTrend, chargeHistory, batteryAlerts, batteryOverview } from "@/lib/mock-data";

export default function BatteryPage() {
  return (
    <AppShell
      title="Battery Management"
      description="State of charge, charge cycles, and battery health monitoring"
    >
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <PanelCard title="Battery Overview" description="Real-time battery status" className="lg:col-span-1">
            <div className="flex flex-col items-center gap-4">
              <BatteryGauge value={batteryOverview.soc} />
              <div className="w-full space-y-2 border-t border-border pt-4">
                {[
                  { label: "Health", value: `${batteryOverview.health}%` },
                  { label: "Temperature", value: `${batteryOverview.temperature}°C` },
                  { label: "Charge Rate", value: batteryOverview.chargeRate },
                  { label: "Discharge Rate", value: batteryOverview.dischargeRate },
                ].map((item) => (
                  <div key={item.label} className="flex justify-between text-xs">
                    <span className="text-muted">{item.label}</span>
                    <span className="font-medium text-foreground">{item.value}</span>
                  </div>
                ))}
                <div className="flex items-center gap-2 pt-1">
                  <Battery className="h-4 w-4 text-success" />
                  <span className="text-xs font-medium text-success">{batteryOverview.status}</span>
                </div>
              </div>
            </div>
          </PanelCard>

          <PanelCard title="Battery SOC Trend" description="State of charge throughout the day" className="lg:col-span-2">
            <LineTrendChart
              data={batteryTrend.map((d) => ({ time: d.time, soc: d.soc }))}
              dataKey="soc"
              color="#10B981"
              height={250}
            />
          </PanelCard>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <PanelCard title="Charge History" description="Weekly charge and discharge cycles">
            <DualBarChart
              data={chargeHistory.map((d) => ({ day: d.day, charge: d.charge, discharge: d.discharge }))}
              keys={["charge", "discharge"]}
              height={220}
            />
          </PanelCard>
          <PanelCard title="Battery Alerts" description="Recent battery events">
            <div className="space-y-3">
              {batteryAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className="flex items-start gap-3 rounded-lg border border-border/50 p-3 transition-colors hover:bg-surface-elevated/30"
                >
                  <AlertTriangle
                    className={`mt-0.5 h-4 w-4 shrink-0 ${
                      alert.level === "warning"
                        ? "text-warning"
                        : alert.level === "success"
                          ? "text-success"
                          : "text-info"
                    }`}
                  />
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
        </div>
      </div>
    </AppShell>
  );
}
