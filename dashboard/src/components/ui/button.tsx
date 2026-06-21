import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap font-retro text-lg transition-all focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 border-[3px] border-outline",
  {
    variants: {
      variant: {
        default: "bg-butter text-outline shadow-retro hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-retro-sm",
        secondary: "bg-sage text-outline shadow-retro hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-retro-sm",
        outline: "bg-cream text-outline shadow-retro hover:bg-sky active:shadow-retro-sm",
        ghost: "border-transparent shadow-none hover:bg-sky/50",
        pink: "bg-pink text-outline shadow-retro hover:-translate-y-0.5 active:shadow-retro-sm",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-8 px-3 text-base",
        lg: "h-12 px-6",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
