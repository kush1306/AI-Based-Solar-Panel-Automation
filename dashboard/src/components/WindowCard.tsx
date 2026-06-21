"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface WindowCardProps {
  title: string;
  children: ReactNode;
  headerColor?: string;
  className?: string;
  action?: ReactNode;
}

export function WindowCard({
  title,
  children,
  headerColor = "bg-pink",
  className,
  action,
}: WindowCardProps) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={cn("rounded-retro border-[3px] border-outline bg-white shadow-retro overflow-hidden", className)}
    >
      <div className={cn("flex items-center justify-between border-b-[3px] border-outline px-3 py-2", headerColor)}>
        <span className="font-pixel text-[8px] uppercase tracking-wide">{title}</span>
        <div className="flex items-center gap-1.5">
          {action}
          <WindowControls />
        </div>
      </div>
      <div className="p-4">{children}</div>
    </motion.div>
  );
}

export function WindowControls() {
  return (
    <div className="flex gap-1">
      <button className="h-3.5 w-3.5 rounded-sm border-2 border-outline bg-butter text-[8px] leading-none hover:scale-110 active:scale-95">_</button>
      <button className="h-3.5 w-3.5 rounded-sm border-2 border-outline bg-sage text-[8px] leading-none hover:scale-110 active:scale-95">□</button>
      <button className="h-3.5 w-3.5 rounded-sm border-2 border-outline bg-red-400 text-[8px] leading-none hover:scale-110 active:scale-95">×</button>
    </div>
  );
}

export function PageHeader({ title }: { title: string }) {
  return (
    <div className="rounded-t-retro border-[3px] border-b-0 border-outline bg-pink px-4 py-2 flex items-center justify-between">
      <span className="font-pixel text-[10px] uppercase">{title}</span>
      <WindowControls />
    </div>
  );
}
