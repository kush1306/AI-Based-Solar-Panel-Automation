"use client";

import { motion } from "framer-motion";
import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { KPIWidget } from "@/components/KPIWidget";
import { energyFlowDetailed } from "@/lib/mock-data";

const nodes = [
  { id: "solar", label: "Solar Panel", icon: "☀️", value: `${energyFlowDetailed.generated} kWh`, color: "bg-butter", x: "50%", y: "5%" },
  { id: "battery", label: "Battery", icon: "🔋", value: `${energyFlowDetailed.stored} kWh stored`, color: "bg-sage", x: "50%", y: "30%" },
  { id: "home", label: "Home", icon: "🏠", value: `${energyFlowDetailed.consumed} kWh used`, color: "bg-pink", x: "50%", y: "55%" },
  { id: "grid", label: "Grid Export", icon: "⚡", value: `${energyFlowDetailed.exported} kWh`, color: "bg-sky", x: "50%", y: "80%" },
];

export default function EnergyFlowPage() {
  return (
    <AppShell title="Energy Flow">
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <KPIWidget title="Generated" value={`${energyFlowDetailed.generated} kWh`} icon="sun" bg="bg-butter" />
          <KPIWidget title="Stored" value={`${energyFlowDetailed.stored} kWh`} icon="battery" bg="bg-sage" />
          <KPIWidget title="Consumed" value={`${energyFlowDetailed.consumed} kWh`} icon="pulse" bg="bg-pink" />
          <KPIWidget title="Exported" value={`${energyFlowDetailed.exported} kWh`} icon="leaf" bg="bg-sky" />
        </div>

        <WindowCard title="System Energy Map" headerColor="bg-sky">
          <div className="relative mx-auto min-h-[480px] max-w-md">
            {/* Animated pipes background */}
            <div className="absolute left-1/2 top-0 h-full w-3 -translate-x-1/2 border-x-2 border-outline bg-orange/30">
              <motion.div
                animate={{ y: ["-100%", "100%"] }}
                transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                className="h-8 w-full bg-orange"
              />
            </div>

            {nodes.map((node, i) => (
              <motion.div
                key={node.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.15 }}
                whileHover={{ scale: 1.08, rotate: [-1, 1, 0] }}
                className={`absolute left-1/2 w-48 -translate-x-1/2 rounded-retro border-[3px] border-outline p-4 text-center shadow-retro ${node.color}`}
                style={{ top: node.y }}
              >
                <span className="text-3xl">{node.icon}</span>
                <p className="mt-1 font-pixel text-[7px]">{node.label.toUpperCase()}</p>
                <p className="font-retro text-lg font-bold">{node.value}</p>
                {i < nodes.length - 1 && (
                  <motion.div
                    animate={{ y: [0, 6, 0] }}
                    transition={{ repeat: Infinity, duration: 1.2, delay: i * 0.2 }}
                    className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-xl"
                  >
                    ▼
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </WindowCard>

        <WindowCard title="Flow Simulation" headerColor="bg-butter">
          <div className="flex items-center justify-center gap-4 py-6 font-retro text-xl">
            <motion.span animate={{ x: [0, 10, 0] }} transition={{ repeat: Infinity, duration: 1.5 }}>☀️</motion.span>
            <span>→</span>
            <motion.span animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.3 }}>🔋</motion.span>
            <span>→</span>
            <motion.span animate={{ y: [0, -4, 0] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.6 }}>🏠</motion.span>
            <span>→</span>
            <motion.span animate={{ opacity: [1, 0.5, 1] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.9 }}>⚡</motion.span>
          </div>
        </WindowCard>
      </div>
    </AppShell>
  );
}
