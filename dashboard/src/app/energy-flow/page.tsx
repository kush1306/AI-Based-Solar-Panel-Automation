"use client";

import { motion } from "framer-motion";
import { ArrowDown, Battery, Home, Leaf, Sun, Zap } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { KpiCard } from "@/components/cards/kpi-card";
import { energyFlowDetailed } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

const nodes: {
  id: string;
  label: string;
  icon: LucideIcon;
  value: string;
  accent: string;
}[] = [
  {
    id: "solar",
    label: "Solar Panel",
    icon: Sun,
    value: `${energyFlowDetailed.generated} kWh`,
    accent: "text-accent bg-accent/10 ring-accent/20",
  },
  {
    id: "battery",
    label: "Battery",
    icon: Battery,
    value: `${energyFlowDetailed.stored} kWh stored`,
    accent: "text-success bg-success/10 ring-success/20",
  },
  {
    id: "home",
    label: "Home",
    icon: Home,
    value: `${energyFlowDetailed.consumed} kWh used`,
    accent: "text-warning bg-warning/10 ring-warning/20",
  },
  {
    id: "grid",
    label: "Grid Export",
    icon: Zap,
    value: `${energyFlowDetailed.exported} kWh`,
    accent: "text-info bg-info/10 ring-info/20",
  },
];

export default function EnergyFlowPage() {
  return (
    <AppShell
      title="Energy Flow"
      description="Real-time energy distribution across solar, storage, load, and grid"
    >
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          <KpiCard title="Generated" value={`${energyFlowDetailed.generated} kWh`} icon={Sun} accent="amber" />
          <KpiCard title="Stored" value={`${energyFlowDetailed.stored} kWh`} icon={Battery} accent="emerald" />
          <KpiCard title="Consumed" value={`${energyFlowDetailed.consumed} kWh`} icon={Zap} accent="orange" />
          <KpiCard title="Exported" value={`${energyFlowDetailed.exported} kWh`} icon={Leaf} accent="sky" />
        </div>

        <PanelCard title="System Energy Map" description="Energy path from generation to consumption">
          <div className="relative mx-auto flex max-w-sm flex-col items-center py-4">
            <div className="absolute left-1/2 top-8 h-[calc(100%-4rem)] w-px -translate-x-1/2 bg-border">
              <motion.div
                animate={{ y: ["-100%", "200%"] }}
                transition={{ repeat: Infinity, duration: 2.5, ease: "linear" }}
                className="h-12 w-px bg-gradient-to-b from-transparent via-accent to-transparent"
              />
            </div>

            {nodes.map((node, i) => {
              const Icon = node.icon;
              return (
                <div key={node.id} className="relative z-10 flex w-full flex-col items-center">
                  <motion.div
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.12 }}
                    className="w-full max-w-[220px] rounded-xl border border-border bg-surface-elevated/50 p-4 text-center shadow-sm transition-shadow hover:shadow-glow"
                  >
                    <div className={cn("mx-auto flex h-12 w-12 items-center justify-center rounded-lg ring-1", node.accent)}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <p className="mt-3 text-xs font-medium uppercase tracking-wider text-muted">{node.label}</p>
                    <p className="mt-1 text-lg font-semibold text-foreground">{node.value}</p>
                  </motion.div>
                  {i < nodes.length - 1 && (
                    <motion.div
                      animate={{ y: [0, 4, 0] }}
                      transition={{ repeat: Infinity, duration: 1.5, delay: i * 0.2 }}
                      className="my-2 text-muted"
                    >
                      <ArrowDown className="h-5 w-5" />
                    </motion.div>
                  )}
                </div>
              );
            })}
          </div>
        </PanelCard>

        <PanelCard title="Flow Simulation" description="Live energy routing sequence">
          <div className="flex flex-wrap items-center justify-center gap-3 py-6">
            {[
              { icon: Sun, label: "Solar", accent: "text-accent" },
              { icon: Battery, label: "Battery", accent: "text-success" },
              { icon: Home, label: "Home", accent: "text-warning" },
              { icon: Zap, label: "Grid", accent: "text-info" },
            ].map((step, i, arr) => (
              <div key={step.label} className="flex items-center gap-3">
                <motion.div
                  animate={
                    i === 0
                      ? { scale: [1, 1.08, 1] }
                      : i === 1
                        ? { opacity: [0.7, 1, 0.7] }
                        : i === 2
                          ? { y: [0, -3, 0] }
                          : { opacity: [1, 0.5, 1] }
                  }
                  transition={{ repeat: Infinity, duration: 2, delay: i * 0.3 }}
                  className="flex flex-col items-center gap-1.5 rounded-lg border border-border/50 px-4 py-3"
                >
                  <step.icon className={cn("h-6 w-6", step.accent)} />
                  <span className="text-xs text-muted">{step.label}</span>
                </motion.div>
                {i < arr.length - 1 && (
                  <span className="text-sm text-muted">→</span>
                )}
              </div>
            ))}
          </div>
        </PanelCard>
      </div>
    </AppShell>
  );
}
