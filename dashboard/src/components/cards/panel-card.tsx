"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface PanelCardProps {
  title: string;
  description?: string;
  children: ReactNode;
  className?: string;
  action?: ReactNode;
}

export function PanelCard({ title, description, children, className, action }: PanelCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      whileHover={{ y: -2 }}
      className={cn("h-full", className)}
    >
      <Card className="flex h-full flex-col transition-shadow duration-300 hover:shadow-glow">
        <CardHeader className="flex-row items-start justify-between space-y-0">
          <div>
            <CardTitle>{title}</CardTitle>
            {description && <CardDescription className="mt-1">{description}</CardDescription>}
          </div>
          {action}
        </CardHeader>
        <CardContent className="flex-1">{children}</CardContent>
      </Card>
    </motion.div>
  );
}
