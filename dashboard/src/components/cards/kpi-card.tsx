"use client";

import { motion } from "framer-motion";
import { LucideIcon, TrendingDown, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";

interface KpiCardProps {
  title: string;
  value: string;
  subtitle?: string;
  trend?: string;
  trendUp?: boolean;
  icon: LucideIcon;
  accent?: "amber" | "sky" | "emerald" | "orange" | "purple";
}

const accentMap = {
  amber: "text-accent bg-accent/10 ring-accent/20",
  sky: "text-info bg-info/10 ring-info/20",
  emerald: "text-success bg-success/10 ring-success/20",
  orange: "text-warning bg-warning/10 ring-warning/20",
  purple: "text-purple-400 bg-purple-400/10 ring-purple-400/20",
};

export function KpiCard({ title, value, subtitle, trend, trendUp, icon: Icon, accent = "amber" }: KpiCardProps) {
  return (
    <motion.div whileHover={{ y: -2 }} transition={{ duration: 0.3 }}>
      <Card className="group p-5 transition-shadow duration-300 hover:shadow-glow">
        <div className="flex items-start justify-between">
          <div className="space-y-3">
            <p className="text-xs font-medium uppercase tracking-wider text-muted">{title}</p>
            <motion.p
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-2xl font-semibold tracking-tight text-foreground"
            >
              {value}
            </motion.p>
            {subtitle && <p className="text-xs text-muted">{subtitle}</p>}
            {trend && (
              <div className={cn("flex items-center gap-1 text-xs font-medium", trendUp ? "text-success" : "text-error")}>
                {trendUp ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                {trend}
              </div>
            )}
          </div>
          <div className={cn("flex h-10 w-10 items-center justify-center rounded-lg ring-1", accentMap[accent])}>
            <Icon className="h-5 w-5" />
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
