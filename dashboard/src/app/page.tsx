"use client";

import { motion } from "framer-motion";
import { AppShell } from "@/components/AppShell";
import { KPIWidget } from "@/components/KPIWidget";
import { SolarFactoryBanner } from "@/components/SolarFactoryBanner";
import { WindowCard } from "@/components/WindowCard";
import { BatteryCard } from "@/components/BatteryCard";
import { WeatherCard } from "@/components/WeatherCard";
import { ActivityFeed } from "@/components/ActivityFeed";
import {
  GenerationConsumptionChart,
  EfficiencyGauge,
  ForecastBarChart,
} from "@/components/ChartWidgets";
import {
  kpiCards,
  hourlyGeneration,
  forecastData,
  energyFlow,
  liveStats,
} from "@/lib/mock-data";

function SolarPanelIllustration({ tilt }: { tilt: number }) {
  return (
    <svg viewBox="0 0 120 80" className="w-full rounded-lg border-2 border-outline bg-sky">
      <rect y="60" width="120" height="20" fill="#A8D5BA" stroke="#222" strokeWidth="1" />
      <g transform={`translate(60,50) rotate(${-tilt}) translate(-30,-18)`}>
        <rect width="60" height="36" fill="#4A90D9" stroke="#222" strokeWidth="2" />
        <line x1="20" y1="0" x2="20" y2="36" stroke="#222" />
        <line x1="40" y1="0" x2="40" y2="36" stroke="#222" />
        <line x1="0" y1="12" x2="60" y2="12" stroke="#222" />
        <line x1="0" y1="24" x2="60" y2="24" stroke="#222" />
        <rect x="27" y="36" width="6" height="14" fill="#888" stroke="#222" />
      </g>
      <text x="60" y="14" textAnchor="middle" fontSize="12" fill="#222" fontFamily="monospace">{tilt}°</text>
    </svg>
  );
}

export default function DashboardPage() {
  return (
    <AppShell title="Dashboard">
      <div className="space-y-4">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {kpiCards.map((card, i) => (
            <motion.div key={card.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <KPIWidget {...card} />
            </motion.div>
          ))}
        </div>

        <SolarFactoryBanner />

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {/* Solar Orientation */}
          <WindowCard title="Solar Orientation">
            <div className="space-y-3">
              <SolarPanelIllustration tilt={liveStats.currentTilt} />
              <div className="grid grid-cols-2 gap-2">
                {[
                  { label: "Current Tilt", value: `${liveStats.currentTilt}°` },
                  { label: "Recommended", value: `${liveStats.recommendedTilt}°`, highlight: true },
                  { label: "Expected Gain", value: `+${liveStats.expectedGain}%`, green: true },
                  { label: "Servo Status", value: liveStats.servoStatus, green: true },
                ].map((s) => (
                  <div key={s.label} className="rounded-lg border-2 border-outline bg-cream p-2">
                    <p className="font-retro text-sm opacity-70">{s.label}</p>
                    <p className={`font-retro text-xl font-bold ${s.highlight ? "text-red-500" : s.green ? "text-green-600" : ""}`}>{s.value}</p>
                  </div>
                ))}
              </div>
            </div>
          </WindowCard>

          {/* Energy Flow */}
          <WindowCard title="Energy Flow" headerColor="bg-sage">
            <div className="flex flex-col items-center gap-1">
              {energyFlow.map((step, i) => (
                <div key={step.id} className="flex flex-col items-center">
                  <motion.div whileHover={{ scale: 1.05 }} className={`flex w-full max-w-[200px] flex-col items-center gap-1 rounded-retro border-[3px] border-outline p-3 shadow-retro-sm ${step.color}`}>
                    <span className="text-2xl">{step.icon}</span>
                    <span className="font-pixel text-[6px]">{step.label.toUpperCase()}</span>
                    <span className="font-retro text-lg font-bold">{step.value}</span>
                  </motion.div>
                  {i < energyFlow.length - 1 && (
                    <motion.span animate={{ y: [0, 4, 0] }} transition={{ repeat: Infinity, duration: 1 }} className="my-1 text-lg">▼</motion.span>
                  )}
                </div>
              ))}
            </div>
          </WindowCard>
        </div>

        {/* AI Predictions */}
        <WindowCard title="AI Predictions" headerColor="bg-sky">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <p className="mb-2 font-pixel text-[7px]">SOLAR ORIENTATION AI</p>
              <div className="space-y-2">
                <div className="flex justify-between font-retro text-lg"><span>Confidence</span><span className="font-bold">{liveStats.orientationConfidence}%</span></div>
                <div className="h-3 overflow-hidden rounded-full border-2 border-outline bg-cream">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${liveStats.orientationConfidence}%` }} className="h-full bg-sage" />
                </div>
                <p className="font-retro text-lg">Recommended Tilt: <strong className="text-red-500">{liveStats.recommendedTilt}°</strong></p>
              </div>
            </div>
            <div>
              <p className="mb-2 font-pixel text-[7px]">CONSUMPTION FORECAST AI</p>
              <div className="space-y-2">
                <div className="flex justify-between font-retro text-lg"><span>Confidence</span><span className="font-bold">{liveStats.consumptionConfidence}%</span></div>
                <div className="h-3 overflow-hidden rounded-full border-2 border-outline bg-cream">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${liveStats.consumptionConfidence}%` }} className="h-full bg-pink" />
                </div>
                <ForecastBarChart data={forecastData} />
              </div>
            </div>
          </div>
        </WindowCard>

        {/* Bottom row */}
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <WindowCard title="Generation vs Consumption" className="lg:col-span-1">
            <GenerationConsumptionChart data={hourlyGeneration} />
          </WindowCard>
          <WindowCard title="System Efficiency" headerColor="bg-butter">
            <EfficiencyGauge value={liveStats.systemEfficiency} />
            <div className="mt-2 flex items-center justify-center gap-2">
              <span className="h-2 w-2 animate-pulse rounded-full border border-outline bg-green-500" />
              <span className="font-retro text-lg font-bold text-green-600">OPTIMAL</span>
            </div>
          </WindowCard>
          <WindowCard title="Battery Status" headerColor="bg-sage">
            <BatteryCard compact />
          </WindowCard>
        </div>

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <WindowCard title="Weather Summary" headerColor="bg-sky">
            <WeatherCard />
          </WindowCard>
          <WindowCard title="Activity Feed" headerColor="bg-pink">
            <ActivityFeed />
          </WindowCard>
        </div>
      </div>
    </AppShell>
  );
}
