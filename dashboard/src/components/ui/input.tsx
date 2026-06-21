import * as React from "react";
import { cn } from "@/lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => (
    <input
      type={type}
      className={cn(
        "flex h-10 w-full rounded-lg border-[3px] border-outline bg-white px-3 py-2 font-retro text-lg shadow-retro-sm file:border-0 file:bg-transparent placeholder:text-outline/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    />
  )
);
Input.displayName = "Input";

export { Input };
