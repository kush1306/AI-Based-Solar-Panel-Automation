"use client";

import { motion } from "framer-motion";
import { Sun, Battery, Gauge, Activity, PiggyBank, Leaf } from "lucide-react";
import { cn } from "@/lib/utils";

const icons: Record<string, React.ReactNode> = {
  sun: <Sun className="h-10 w-10 text-orange stroke-[2.5px]" />,
  battery: <Battery className="h-10 w-10 text-green-700 stroke-[2.5px]" />,
  tilt: <Gauge className="h-10 w-10 text-blue-600 stroke-[2.5px]" />,
  pulse: <Activity className="h-10 w-10 text-blue-500 stroke-[2.5px]" />,
  piggy: <PiggyBank className="h-10 w-10 text-orange stroke-[2.5px]" />,
  leaf: <Leaf className="h-10 w-10 text-green-600 stroke-[2.5px]" />,
};

interface KPIWidgetProps {
  title: string;
  value: string;
  trend?: string;
  trendUp?: boolean;
  subtext?: string;
  icon: string;
  bg?: string;
}

export function KPIWidget({ title, value, trend, trendUp, subtext, icon, bg = "bg-cream" }: KPIWidgetProps) {
  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={cn("flex items-center gap-3 rounded-retro border-[3px] border-outline p-4 shadow-retro", bg)}
    >
      <div className="shrink-0">{icons[icon]}</div>
      <div className="min-w-0 flex-1">
        <p className="font-retro text-base opacity-80">{title}</p>
        <p className="font-retro text-2xl font-bold leading-tight">{value}</p>
        {trend && (
          <p className={cn("font-retro text-base", trendUp ? "text-green-600" : "text-red-500")}>
            {trendUp ? "▲" : "▼"} {trend}
          </p>
        )}
        {subtext && (
          <p className={cn("font-retro text-base font-bold", icon === "aqi" ? "text-orange" : "text-red-500")}>
            {subtext}
          </p>
        )}
      </div>
    </motion.div>
  );
}
