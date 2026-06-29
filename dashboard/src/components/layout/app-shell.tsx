"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";
import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";
import { useSidebar } from "./sidebar-context";
import { cn } from "@/lib/utils";

interface AppShellProps {
  title: string;
  description?: string;
  children: ReactNode;
  action?: ReactNode;
}

export function AppShell({ title, description, children, action }: AppShellProps) {
  const { collapsed } = useSidebar();

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div
        className={cn(
          "flex min-h-screen flex-col transition-all duration-300 ease-out",
          collapsed ? "pl-[72px]" : "pl-64"
        )}
      >
        <Topbar />
        <main className="flex-1 overflow-x-hidden p-4 md:p-6 lg:p-8">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="mx-auto w-full max-w-[1600px] space-y-6"
          >
            <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h1>
                {description && <p className="mt-1 text-sm text-muted">{description}</p>}
              </div>
              {action}
            </div>
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
}
