"use client";

import { MapPin, Thermometer, ShieldAlert, Clock, CalendarDays } from "lucide-react";
import { liveStats } from "@/lib/mock-data";
import { useClock } from "@/hooks/use-clock";
import { WindowControls } from "./WindowCard";

export function Topbar() {
  const { time, date } = useClock();

  return (
    <header className="sticky top-0 z-50 flex flex-wrap items-center justify-between gap-3 border-b-[3px] border-outline bg-butter px-4 py-2.5">
      <div className="flex items-center gap-3">
        <span className="text-2xl">☀️</span>
        <h1 className="font-pixel text-[8px] leading-relaxed sm:text-[9px]">
          SMART SOLAR OPTIMIZATION SYSTEM
        </h1>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {[
          { icon: MapPin, label: "DELHI, INDIA", color: "bg-butter" },
          { icon: Thermometer, label: `${liveStats.temperature}°C`, color: "bg-sky" },
          { icon: ShieldAlert, label: `AQI ${liveStats.aqi}`, color: "bg-sage" },
          { icon: Clock, label: time, color: "bg-pink" },
          { icon: CalendarDays, label: date, color: "bg-cream" },
        ].map(({ icon: Icon, label, color }) => (
          <div key={label} className={`flex items-center gap-1.5 rounded-md border-2 border-outline px-2 py-1 font-retro text-sm ${color}`}>
            <Icon className="h-3.5 w-3.5 stroke-[2.5px]" />
            <span className="hidden sm:inline">{label}</span>
            <span className="sm:hidden">{label.split(" ")[0]}</span>
          </div>
        ))}
      </div>

      <WindowControls />
    </header>
  );
}
