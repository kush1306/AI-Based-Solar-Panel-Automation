"use client";

import { CloudRain, CloudSun, Leaf, MapPin, Sun } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { KpiCard } from "@/components/cards/kpi-card";
import { DualBarChart } from "@/components/charts/chart-widgets";
import { Badge } from "@/components/ui/badge";
import { weatherForecast, historicalWeather, liveStats } from "@/lib/mock-data";
import { getAqiLabel } from "@/lib/utils";

function forecastIcon(condition: string): LucideIcon {
  if (condition.includes("Rain")) return CloudRain;
  if (condition.includes("Cloud")) return CloudSun;
  return Sun;
}

const weatherMetrics = [
  { label: "Temperature", value: `${liveStats.temperature}°C` },
  { label: "Humidity", value: `${liveStats.humidity}%` },
  { label: "Cloud Cover", value: `${liveStats.cloudCover}%` },
  { label: "Wind Speed", value: `${liveStats.windSpeed} km/h` },
  { label: "GHI", value: "785 W/m²" },
  { label: "AQI", value: `${liveStats.aqi} ${getAqiLabel(liveStats.aqi)}` },
];

export default function WeatherPage() {
  return (
    <AppShell
      title="Weather Intelligence"
      description="Environmental conditions and air quality for solar performance forecasting"
    >
      <div className="space-y-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <PanelCard title="Current Conditions" description="Live environmental readings" className="lg:col-span-2">
            <div className="space-y-4">
              <div className="flex items-center gap-4 rounded-lg border border-border/50 bg-background/40 p-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-accent/10 ring-1 ring-accent/20">
                  <Sun className="h-7 w-7 text-accent" />
                </div>
                <div>
                  <p className="text-3xl font-semibold text-foreground">{liveStats.temperature}°C</p>
                  <p className="text-sm text-muted">
                    AQI {liveStats.aqi} · {getAqiLabel(liveStats.aqi)}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                {weatherMetrics.map((m) => (
                  <div
                    key={m.label}
                    className="flex items-center justify-between rounded-lg border border-border/50 bg-background/40 px-3 py-2"
                  >
                    <span className="text-xs text-muted">{m.label}</span>
                    <span className="text-sm font-medium text-foreground">{m.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </PanelCard>

          <PanelCard title="Delhi Map" description="Monitoring station location">
            <div className="flex flex-col items-center gap-3 py-2">
              <div className="relative flex h-40 w-full items-center justify-center rounded-lg border border-border bg-surface-elevated/50">
                <MapPin className="h-8 w-8 text-error" />
                <div className="absolute inset-0 grid grid-cols-4 grid-rows-3 gap-1 p-2 opacity-20">
                  {[...Array(12)].map((_, i) => (
                    <div key={i} className="rounded border border-border bg-info/30" />
                  ))}
                </div>
              </div>
              <p className="text-lg font-semibold text-foreground">Delhi, India</p>
              <Badge variant="warning">
                AQI {liveStats.aqi} — {getAqiLabel(liveStats.aqi)}
              </Badge>
            </div>
          </PanelCard>
        </div>

        <PanelCard title="5-Day Forecast" description="Extended weather outlook">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
            {weatherForecast.map((day) => {
              const Icon = forecastIcon(day.condition);
              return (
                <div
                  key={day.day}
                  className="flex flex-col items-center gap-2 rounded-xl border border-border/50 bg-background/40 p-4 transition-colors hover:bg-surface-elevated/30"
                >
                  <p className="text-sm font-semibold text-foreground">{day.day}</p>
                  <Icon className="h-8 w-8 text-accent" />
                  <p className="text-xs text-muted">{day.condition}</p>
                  <p className="text-sm font-medium text-foreground">
                    {day.high}° / {day.low}°
                  </p>
                  <Badge variant={day.aqi > 120 ? "warning" : "success"}>AQI {day.aqi}</Badge>
                </div>
              );
            })}
          </div>
        </PanelCard>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <PanelCard title="Historical Weather" description="Temperature and air quality trends">
            <DualBarChart
              data={historicalWeather.map((d) => ({ day: d.day, temp: d.temp, aqi: d.aqi / 3 }))}
              keys={["temp", "aqi"]}
              height={220}
            />
          </PanelCard>
          <PanelCard title="Air Quality Metrics" description="Pollutant concentration levels">
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: "PM2.5", value: "58 µg/m³" },
                { label: "PM10", value: "92 µg/m³" },
                { label: "O₃", value: "34 ppb" },
                { label: "NO₂", value: "28 ppb" },
              ].map((item) => (
                <KpiCard key={item.label} title={item.label} value={item.value} icon={Leaf} accent="emerald" />
              ))}
            </div>
          </PanelCard>
        </div>
      </div>
    </AppShell>
  );
}
