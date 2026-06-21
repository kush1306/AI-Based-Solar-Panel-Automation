"use client";

import { motion } from "framer-motion";
import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { KPIWidget } from "@/components/KPIWidget";
import { ForecastBarChart } from "@/components/ChartWidgets";
import { Badge } from "@/components/ui/badge";
import {
  aiOrientation,
  aiConsumption,
  predictionHistory,
  modelPerformance,
  forecastData,
} from "@/lib/mock-data";

export default function AIPredictionsPage() {
  return (
    <AppShell title="AI Predictions">
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <WindowCard title="Solar Orientation AI">
            <div className="space-y-4">
              <div className="flex justify-center">
                <svg viewBox="0 0 100 70" className="h-24 w-36 rounded-lg border-2 border-outline bg-sky">
                  <g transform="rotate(-20 50 40)">
                    <rect x="20" y="20" width="60" height="30" fill="#4A90D9" stroke="#222" strokeWidth="2" />
                    <rect x="47" y="50" width="6" height="12" fill="#888" stroke="#222" />
                  </g>
                </svg>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div className="rounded-lg border-2 border-outline bg-cream p-3 text-center">
                  <p className="font-retro text-sm opacity-70">Recommended Tilt</p>
                  <p className="font-retro text-3xl font-bold text-red-500">{aiOrientation.recommendedTilt}°</p>
                </div>
                <div className="rounded-lg border-2 border-outline bg-cream p-3 text-center">
                  <p className="font-retro text-sm opacity-70">Expected Gain</p>
                  <p className="font-retro text-3xl font-bold text-green-600">+{aiOrientation.expectedGain}%</p>
                </div>
              </div>
              <div>
                <div className="flex justify-between font-retro text-lg"><span>Confidence</span><span>{aiOrientation.confidence}%</span></div>
                <div className="mt-1 h-4 overflow-hidden rounded-full border-2 border-outline">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${aiOrientation.confidence}%` }} className="h-full bg-sage" />
                </div>
              </div>
            </div>
          </WindowCard>

          <WindowCard title="Consumption Forecast AI" headerColor="bg-sky">
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                <KPIWidget title="Next Hour Load" value={`${aiConsumption.nextHourLoad} kWh`} icon="pulse" bg="bg-pink" />
                <KPIWidget title="Peak Time" value={aiConsumption.peakTime} icon="sun" bg="bg-butter" />
              </div>
              <div>
                <div className="flex justify-between font-retro text-lg"><span>Accuracy Score</span><span>{aiConsumption.accuracy}%</span></div>
                <div className="mt-1 h-4 overflow-hidden rounded-full border-2 border-outline">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${aiConsumption.accuracy}%` }} className="h-full bg-pink" />
                </div>
              </div>
              <ForecastBarChart data={forecastData} height={140} />
            </div>
          </WindowCard>
        </div>

        <WindowCard title="Prediction History">
          <div className="overflow-x-auto">
            <table className="w-full font-retro text-base">
              <thead>
                <tr className="border-b-2 border-outline text-left">
                  {["ID", "Type", "Prediction", "Actual", "Accuracy", "Date"].map((h) => (
                    <th key={h} className="p-2">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {predictionHistory.map((row) => (
                  <tr key={row.id} className="border-b border-outline/30 hover:bg-cream">
                    <td className="p-2">{row.id}</td>
                    <td className="p-2"><Badge variant={row.type === "Tilt" ? "info" : "default"}>{row.type}</Badge></td>
                    <td className="p-2">{row.prediction}</td>
                    <td className="p-2">{row.actual}</td>
                    <td className="p-2 font-bold text-green-600">{row.accuracy}%</td>
                    <td className="p-2">{row.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </WindowCard>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          {modelPerformance.map((model) => (
            <WindowCard key={model.name} title={model.name} headerColor="bg-sage">
              <p className="font-retro text-3xl font-bold">{model.accuracy}%</p>
              <p className="font-retro text-lg opacity-70">Accuracy</p>
              <Badge variant="success" className="mt-2">{model.status}</Badge>
            </WindowCard>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
