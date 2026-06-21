"use client";

import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { WeatherCard } from "@/components/WeatherCard";
import { KPIWidget } from "@/components/KPIWidget";
import { DualBarChart } from "@/components/ChartWidgets";
import { Badge } from "@/components/ui/badge";
import { weatherForecast, historicalWeather, liveStats } from "@/lib/mock-data";
import { getAqiLabel } from "@/lib/utils";
import { MapPin } from "lucide-react";

export default function WeatherPage() {
  return (
    <AppShell title="Weather Intelligence">
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <WindowCard title="Current Conditions" className="lg:col-span-2">
            <WeatherCard />
          </WindowCard>

          <WindowCard title="Delhi Map" headerColor="bg-sky">
            <div className="flex flex-col items-center gap-3 py-4">
              <div className="relative flex h-40 w-full items-center justify-center rounded-lg border-[3px] border-outline bg-sage/30">
                <MapPin className="h-8 w-8 text-red-500" />
                <div className="absolute inset-0 grid grid-cols-4 grid-rows-3 gap-1 p-2 opacity-30">
                  {[...Array(12)].map((_, i) => (
                    <div key={i} className="rounded border border-outline bg-sky/50" />
                  ))}
                </div>
              </div>
              <p className="font-retro text-xl font-bold">Delhi, India</p>
              <Badge variant="warning">AQI {liveStats.aqi} — {getAqiLabel(liveStats.aqi)}</Badge>
            </div>
          </WindowCard>
        </div>

        <WindowCard title="5-Day Forecast">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
            {weatherForecast.map((day) => (
              <div key={day.day} className="flex flex-col items-center gap-2 rounded-retro border-[3px] border-outline bg-cream p-3 shadow-retro-sm">
                <p className="font-retro text-lg font-bold">{day.day}</p>
                <span className="text-3xl">{day.condition.includes("Rain") ? "🌧️" : day.condition.includes("Cloud") ? "⛅" : "☀️"}</span>
                <p className="font-retro text-base">{day.high}° / {day.low}°</p>
                <Badge variant={day.aqi > 120 ? "warning" : "success"}>AQI {day.aqi}</Badge>
              </div>
            ))}
          </div>
        </WindowCard>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <WindowCard title="Historical Weather">
            <DualBarChart data={historicalWeather.map((d) => ({ day: d.day, temp: d.temp, aqi: d.aqi / 3 }))} keys={["temp", "aqi"]} height={220} />
          </WindowCard>
          <WindowCard title="AQI Widgets" headerColor="bg-orange">
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: "PM2.5", value: "58 µg/m³" },
                { label: "PM10", value: "92 µg/m³" },
                { label: "O₃", value: "34 ppb" },
                { label: "NO₂", value: "28 ppb" },
              ].map((item) => (
                <KPIWidget key={item.label} title={item.label} value={item.value} icon="leaf" bg="bg-cream" />
              ))}
            </div>
          </WindowCard>
        </div>
      </div>
    </AppShell>
  );
}
