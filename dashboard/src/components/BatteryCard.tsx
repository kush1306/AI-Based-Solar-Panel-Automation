"use client";

import { motion } from "framer-motion";
import { batteryOverview } from "@/lib/mock-data";

export function BatteryCard({ compact = false }: { compact?: boolean }) {
  const { soc, health, temperature, chargeRate, dischargeRate, status } = batteryOverview;

  return (
    <div className={compact ? "space-y-3" : "space-y-4"}>
      <div className="flex items-center justify-center gap-1">
        <div className="relative h-14 w-32 overflow-hidden rounded-lg border-[3px] border-outline bg-cream">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${soc}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="absolute inset-y-0 left-0 bg-sage"
          />
          <span className="absolute inset-0 flex items-center justify-center font-retro text-xl font-bold">
            {soc}%
          </span>
        </div>
        <div className="h-6 w-3 rounded-r-md border-[3px] border-l-0 border-outline bg-outline" />
      </div>

      <div className="grid grid-cols-2 gap-2">
        {[
          { label: "Health", value: `${health}%` },
          { label: "Temp", value: `${temperature}°C` },
          { label: "Charge", value: chargeRate, color: "text-green-600" },
          { label: "Discharge", value: dischargeRate, color: "text-red-500" },
        ].map((item) => (
          <div key={item.label} className="rounded-lg border-2 border-outline bg-cream p-2 text-center">
            <p className="font-retro text-sm opacity-70">{item.label}</p>
            <p className={`font-retro text-lg font-bold ${item.color ?? ""}`}>{item.value}</p>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-center gap-2">
        <span className="h-2 w-2 animate-pulse rounded-full border-2 border-outline bg-green-500" />
        <span className="font-retro text-lg font-bold text-green-600">{status}</span>
      </div>
    </div>
  );
}
