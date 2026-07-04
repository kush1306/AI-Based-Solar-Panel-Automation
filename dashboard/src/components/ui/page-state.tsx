"use client";

import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface PageStateProps {
  loading: boolean;
  error: string | null;
  empty?: boolean;
  emptyMessage?: string;
  onRetry: () => void;
  children: React.ReactNode;
  skeleton?: React.ReactNode;
  className?: string;
}

function DefaultSkeleton() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {[...Array(6)].map((_, index) => (
          <div key={index} className="h-28 rounded-xl border border-border bg-surface-elevated/40" />
        ))}
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="h-72 rounded-xl border border-border bg-surface-elevated/40" />
        <div className="h-72 rounded-xl border border-border bg-surface-elevated/40" />
      </div>
    </div>
  );
}

function StateMessage({
  title,
  message,
  onRetry,
  tone = "error",
}: {
  title: string;
  message: string;
  onRetry: () => void;
  tone?: "error" | "empty";
}) {
  return (
    <div className="flex min-h-[320px] flex-col items-center justify-center rounded-xl border border-border bg-surface-elevated/20 px-6 py-12 text-center">
      <div
        className={cn(
          "mb-4 flex h-12 w-12 items-center justify-center rounded-full",
          tone === "error" ? "bg-error/10 text-error" : "bg-muted/10 text-muted",
        )}
      >
        <AlertTriangle className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-semibold text-foreground">{title}</h3>
      <p className="mt-2 max-w-md text-sm text-muted">{message}</p>
      <Button className="mt-6" onClick={onRetry}>
        <RefreshCw className="h-4 w-4" />
        Retry
      </Button>
    </div>
  );
}

export function PageState({
  loading,
  error,
  empty = false,
  emptyMessage = "No data available yet.",
  onRetry,
  children,
  skeleton,
  className,
}: PageStateProps) {
  if (loading) {
    return <div className={className}>{skeleton ?? <DefaultSkeleton />}</div>;
  }

  if (error) {
    return (
      <div className={className}>
        <StateMessage title="Unable to load data" message={error} onRetry={onRetry} tone="error" />
      </div>
    );
  }

  if (empty) {
    return (
      <div className={className}>
        <StateMessage title="Nothing to show" message={emptyMessage} onRetry={onRetry} tone="empty" />
      </div>
    );
  }

  return <>{children}</>;
}
