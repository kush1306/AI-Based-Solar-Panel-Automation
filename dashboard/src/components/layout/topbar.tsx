"use client";

import { Bell, Menu, Search, User } from "lucide-react";
import { useClock } from "@/hooks/use-clock";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useSidebar } from "./sidebar-context";

export function Topbar() {
  const { toggle, collapsed } = useSidebar();
  const { time, date } = useClock();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border bg-background/80 px-6 backdrop-blur-xl">
      <Button variant="ghost" size="icon" onClick={toggle} className="shrink-0 text-muted hover:text-foreground">
        <Menu className="h-5 w-5" />
      </Button>

      <div className="relative hidden max-w-md flex-1 md:block">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
        <Input
          placeholder="Search telemetry, alerts, reports..."
          className="h-9 border-border bg-surface pl-9 text-sm"
        />
      </div>

      <div className="ml-auto flex items-center gap-3">
        <div className="hidden text-right sm:block">
          <p className="text-sm font-medium text-foreground">{time}</p>
          <p className="text-xs text-muted">{date}</p>
        </div>

        <Button variant="ghost" size="icon" className="relative text-muted hover:text-foreground">
          <Bell className="h-5 w-5" />
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-error" />
        </Button>

        <div className="flex items-center gap-2 rounded-lg border border-border bg-surface px-3 py-1.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-surface-elevated">
            <User className="h-4 w-4 text-muted" />
          </div>
          <div className="hidden sm:block">
            <p className="text-xs font-medium text-foreground">Operator</p>
            <p className="text-[10px] text-muted">Engineering</p>
          </div>
        </div>
      </div>

      <span className="sr-only">{collapsed ? "Sidebar collapsed" : "Sidebar expanded"}</span>
    </header>
  );
}
