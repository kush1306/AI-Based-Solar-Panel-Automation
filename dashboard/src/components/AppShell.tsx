import { ReactNode } from "react";
import { Topbar } from "@/components/Topbar";
import { Sidebar } from "@/components/Sidebar";
import { PageHeader } from "@/components/WindowCard";

export function AppShell({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="min-h-screen bg-cream">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute right-[5%] top-[15%] h-10 w-28 animate-pulse rounded-full border-2 border-outline/20 bg-sky/20" />
        <div className="absolute bottom-[20%] left-[30%] h-8 w-20 animate-pulse rounded-full border-2 border-outline/20 bg-sky/20" style={{ animationDelay: "2s" }} />
      </div>

      <Topbar />

      <div className="relative mx-auto flex max-w-[1600px] gap-4 p-4">
        <Sidebar />

        <main className="min-w-0 flex-1">
          <PageHeader title={title} />
          <div className="rounded-b-retro border-[3px] border-t-0 border-outline bg-white p-4 shadow-retro">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
