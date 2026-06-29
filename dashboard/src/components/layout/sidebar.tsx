"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  BarChart3,
  Brain,
  Battery,
  Zap,
  CloudSun,
  Monitor,
  FileText,
  Settings,
  Sun,
  type LucideIcon,
} from "lucide-react";
import { navItems } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { useSidebar } from "./sidebar-context";

const iconMap: Record<string, LucideIcon> = {
  LayoutDashboard,
  BarChart3,
  Brain,
  Battery,
  Zap,
  CloudSun,
  Monitor,
  FileText,
  Settings,
};

export function Sidebar() {
  const pathname = usePathname();
  const { collapsed } = useSidebar();

  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 256 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      className="fixed left-0 top-0 z-40 flex h-screen flex-col border-r border-border bg-surface"
    >
      <div className={cn("flex h-16 items-center gap-3 border-b border-border px-4", collapsed && "justify-center px-2")}>
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent/10 ring-1 ring-accent/20">
          <Sun className="h-5 w-5 text-accent" />
        </div>
        {!collapsed && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="min-w-0">
            <p className="truncate text-sm font-semibold text-foreground">Solar Intelligence</p>
            <p className="truncate text-xs text-muted">Platform</p>
          </motion.div>
        )}
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-3">
        {navItems.map((item) => {
          const Icon = iconMap[item.icon];
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              title={collapsed ? item.label : undefined}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                active
                  ? "bg-accent/10 text-accent ring-1 ring-accent/20"
                  : "text-muted hover:bg-surface-elevated hover:text-foreground",
                collapsed && "justify-center px-2"
              )}
            >
              <Icon className={cn("h-[18px] w-[18px] shrink-0", active && "text-accent")} />
              {!collapsed && <span className="truncate">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {!collapsed && (
        <div className="border-t border-border p-4">
          <div className="rounded-xl border border-border bg-background/50 p-3">
            <p className="text-xs font-medium text-muted">System Status</p>
            <div className="mt-2 flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success opacity-40" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-success" />
              </span>
              <span className="text-xs font-medium text-success">Operational</span>
            </div>
          </div>
        </div>
      )}
    </motion.aside>
  );
}
