"use client";

import { motion } from "framer-motion";
import { activityFeed, categoryColors } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

export function ActivityFeed() {
  return (
    <div className="max-h-72 space-y-2 overflow-y-auto pr-1">
      {activityFeed.map((event, i) => (
        <motion.div
          key={event.id}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.05 }}
          whileHover={{ x: 4 }}
          className="flex items-center gap-3 rounded-lg border-2 border-outline bg-cream p-2.5"
        >
          <div className={cn("flex h-9 w-9 shrink-0 items-center justify-center rounded-md border-2 border-outline text-lg", categoryColors[event.category])}>
            {event.icon}
          </div>
          <div className="min-w-0 flex-1">
            <p className="font-retro text-base leading-snug">{event.message}</p>
            <p className="font-retro text-sm opacity-60">{event.time}</p>
          </div>
          <span className={cn("hidden shrink-0 rounded border-2 border-outline px-1.5 py-0.5 font-pixel text-[5px] sm:inline", categoryColors[event.category])}>
            {event.category.toUpperCase()}
          </span>
        </motion.div>
      ))}
    </div>
  );
}
