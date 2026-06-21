import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants = {
    default: "bg-butter",
    success: "bg-sage",
    warning: "bg-orange",
    danger: "bg-pink",
    info: "bg-sky",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-md border-2 border-outline px-2 py-0.5 font-retro text-sm",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}

export { Badge };
