"use client";

import { liveStats } from "@/lib/mock-data";
import { getAqiLabel } from "@/lib/utils";
import { Thermometer, Wind, Droplets, Cloud, ShieldAlert } from "lucide-react";

const items = [
  { label: "Temperature", value: `${liveStats.temperature}°C`, icon: Thermometer, color: "bg-butter" },
  { label: "AQI", value: liveStats.aqi.toString(), icon: ShieldAlert, color: "bg-sage" },
  { label: "Humidity", value: `${liveStats.humidity}%`, icon: Droplets, color: "bg-sky" },
  { label: "Wind", value: `${liveStats.windSpeed} km/h`, icon: Wind, color: "bg-pink" },
  { label: "Cloud Cover", value: `${liveStats.cloudCover}%`, icon: Cloud, color: "bg-cream" },
];

export function WeatherCard() {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3 rounded-lg border-2 border-outline bg-sky p-3">
        <span className="text-4xl">☀️</span>
        <div>
          <p className="font-retro text-2xl font-bold">Sunny</p>
          <p className="font-retro text-base text-orange">AQI: {getAqiLabel(liveStats.aqi)}</p>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        {items.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className={`flex flex-col items-center gap-1 rounded-lg border-2 border-outline p-3 ${color}`}>
            <Icon className="h-6 w-6 stroke-[2.5px]" />
            <span className="font-retro text-sm opacity-70">{label}</span>
            <span className="font-retro text-lg font-bold">{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
