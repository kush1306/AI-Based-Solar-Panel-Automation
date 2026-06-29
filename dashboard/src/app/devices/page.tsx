"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { DataTable } from "@/components/tables/data-table";
import { Badge } from "@/components/ui/badge";
import { devices } from "@/lib/mock-data";
import { Wifi, WifiOff } from "lucide-react";

export default function DevicesPage() {
  const online = devices.filter((d) => d.status === "online").length;

  return (
    <AppShell
      title="Device Monitor"
      description="Connected hardware status and uptime tracking"
    >
      <div className="space-y-4">
        <div className="flex gap-3">
          <Badge variant="success">{online} Online</Badge>
          <Badge variant="error">{devices.length - online} Offline</Badge>
        </div>

        <PanelCard title="Connected Devices" description={`${devices.length} devices registered`}>
          <DataTable
            columns={[
              { key: "id", header: "Device ID", className: "font-medium" },
              { key: "name", header: "Name" },
              {
                key: "type",
                header: "Type",
                render: (row) => <Badge variant="info">{String(row.type)}</Badge>,
              },
              {
                key: "status",
                header: "Status",
                render: (row) => (
                  <span className="flex items-center gap-1.5">
                    {row.status === "online" ? (
                      <>
                        <Wifi className="h-4 w-4 text-success" />
                        <Badge variant="success">Online</Badge>
                      </>
                    ) : (
                      <>
                        <WifiOff className="h-4 w-4 text-error" />
                        <Badge variant="error">Offline</Badge>
                      </>
                    )}
                  </span>
                ),
              },
              { key: "lastUpdate", header: "Last Update" },
              { key: "uptime", header: "Uptime" },
            ]}
            data={devices}
          />
        </PanelCard>
      </div>
    </AppShell>
  );
}
