"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
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
  type LucideIcon,
} from "lucide-react";
import { navItems } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { WindowControls } from "./WindowCard";

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

  return (
    <aside className="flex w-56 shrink-0 flex-col gap-4">
      <div className="overflow-hidden rounded-retro border-[3px] border-outline bg-white shadow-retro">
        <div className="flex items-center justify-between border-b-[3px] border-outline bg-pink px-3 py-2">
          <span className="font-pixel text-[8px] uppercase">Menu</span>
          <WindowControls />
        </div>
        <nav className="flex flex-col gap-1 bg-cream p-2">
          {navItems.map((item) => {
            const Icon = iconMap[item.icon];
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2.5 rounded-lg border-2 px-3 py-2 font-retro text-base transition-all hover:-translate-y-0.5 hover:border-outline hover:bg-sky active:translate-y-0.5",
                  active
                    ? "border-outline bg-butter shadow-retro-sm"
                    : "border-transparent"
                )}
              >
                <Icon className="h-4 w-4 stroke-[2.5px]" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Solar panel illustration */}
      <div className="overflow-hidden rounded-retro border-[3px] border-outline shadow-retro">
        <svg viewBox="0 0 160 120" className="w-full bg-sky">
          <rect width="160" height="80" fill="#8FD3FF" />
          <rect y="80" width="160" height="40" fill="#A8D5BA" stroke="#222" strokeWidth="2" />
          <ellipse cx="35" cy="22" rx="16" ry="8" fill="white" stroke="#222" strokeWidth="1.5" />
          <ellipse cx="120" cy="18" rx="18" ry="9" fill="white" stroke="#222" strokeWidth="1.5" />
          <g transform="translate(55,38) rotate(-12)">
            <rect width="50" height="32" fill="#4A90D9" stroke="#222" strokeWidth="2" />
            <line x1="17" y1="0" x2="17" y2="32" stroke="#222" />
            <line x1="33" y1="0" x2="33" y2="32" stroke="#222" />
            <line x1="0" y1="11" x2="50" y2="11" stroke="#222" />
            <line x1="0" y1="22" x2="50" y2="22" stroke="#222" />
            <rect x="22" y="32" width="6" height="14" fill="#888" stroke="#222" />
          </g>
          <ellipse cx="25" cy="88" rx="10" ry="8" fill="#5CB85C" stroke="#222" />
          <ellipse cx="135" cy="92" rx="8" ry="6" fill="#5CB85C" stroke="#222" />
        </svg>
      </div>
    </aside>
  );
}
