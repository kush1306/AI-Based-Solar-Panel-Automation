"use client";

import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { Badge } from "@/components/ui/badge";
import { devices } from "@/lib/mock-data";
import { Wifi, WifiOff } from "lucide-react";

export default function DevicesPage() {
  const online = devices.filter((d) => d.status === "online").length;

  return (
    <AppShell title="Device Monitor">
      <div className="space-y-4">
        <div className="flex gap-3">
          <Badge variant="success">{online} Online</Badge>
          <Badge variant="danger">{devices.length - online} Offline</Badge>
        </div>

        <WindowCard title="Connected Devices">
          <div className="overflow-x-auto">
            <table className="w-full font-retro text-base">
              <thead>
                <tr className="border-b-2 border-outline text-left">
                  {["Device ID", "Name", "Type", "Status", "Last Update", "Uptime"].map((h) => (
                    <th key={h} className="p-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {devices.map((device) => (
                  <tr key={device.id} className="border-b border-outline/20 hover:bg-cream">
                    <td className="p-3 font-bold">{device.id}</td>
                    <td className="p-3">{device.name}</td>
                    <td className="p-3"><Badge variant="info">{device.type}</Badge></td>
                    <td className="p-3">
                      <span className="flex items-center gap-1.5">
                        {device.status === "online" ? (
                          <><Wifi className="h-4 w-4 text-green-600" /><Badge variant="success">Online</Badge></>
                        ) : (
                          <><WifiOff className="h-4 w-4 text-red-500" /><Badge variant="danger">Offline</Badge></>
                        )}
                      </span>
                    </td>
                    <td className="p-3">{device.lastUpdate}</td>
                    <td className="p-3">{device.uptime}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </WindowCard>
      </div>
    </AppShell>
  );
}
