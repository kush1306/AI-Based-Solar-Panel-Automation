"use client";

import { motion } from "framer-motion";
import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { BatteryCard } from "@/components/BatteryCard";
import { LineTrendChart, DualBarChart } from "@/components/ChartWidgets";
import { Badge } from "@/components/ui/badge";
import { batteryTrend, chargeHistory, batteryAlerts } from "@/lib/mock-data";

export default function BatteryPage() {
  return (
    <AppShell title="Battery Management">
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <WindowCard title="Battery Overview" className="lg:col-span-1" headerColor="bg-sage">
            <div className="flex flex-col items-center gap-4">
              <motion.div
                animate={{ scale: [1, 1.02, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="text-7xl"
              >
                🔋
              </motion.div>
              <BatteryCard />
            </div>
          </WindowCard>

          <WindowCard title="Battery SOC Trend" className="lg:col-span-2">
            <LineTrendChart data={batteryTrend.map((d) => ({ time: d.time, soc: d.soc }))} dataKey="soc" color="#A8D5BA" height={250} />
          </WindowCard>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <WindowCard title="Charge History">
            <DualBarChart data={chargeHistory.map((d) => ({ day: d.day, charge: d.charge, discharge: d.discharge }))} keys={["charge", "discharge"]} height={220} />
          </WindowCard>
          <WindowCard title="Battery Alerts" headerColor="bg-orange">
            <div className="space-y-2">
              {batteryAlerts.map((alert) => (
                <div key={alert.id} className="flex items-start gap-3 rounded-lg border-2 border-outline bg-cream p-3">
                  <Badge variant={alert.level === "warning" ? "warning" : alert.level === "success" ? "success" : "info"}>
                    {alert.level.toUpperCase()}
                  </Badge>
                  <div>
                    <p className="font-retro text-base">{alert.message}</p>
                    <p className="font-retro text-sm opacity-60">{alert.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </WindowCard>
        </div>
      </div>
    </AppShell>
  );
}
