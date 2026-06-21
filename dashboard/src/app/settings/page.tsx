"use client";

import { AppShell } from "@/components/AppShell";
import { WindowCard } from "@/components/WindowCard";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useSettings } from "@/lib/settings-provider";

const accentColors = [
  { label: "Butter Yellow", value: "#FFD84D" },
  { label: "Light Pink", value: "#FFB6D5" },
  { label: "Sage Green", value: "#A8D5BA" },
  { label: "Sky Blue", value: "#8FD3FF" },
  { label: "Orange", value: "#FF9F45" },
];

export default function SettingsPage() {
  const { settings, updateSettings, resetSettings } = useSettings();

  return (
    <AppShell title="Settings">
      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="units">Units</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
        </TabsList>

        <TabsContent value="general">
          <WindowCard title="General Settings">
            <div className="space-y-4 max-w-md">
              <div>
                <Label htmlFor="location">Location</Label>
                <Input id="location" value={settings.location} onChange={(e) => updateSettings({ location: e.target.value })} className="mt-1" />
              </div>
              <div>
                <Label htmlFor="timezone">Timezone</Label>
                <Input id="timezone" value={settings.timezone} onChange={(e) => updateSettings({ timezone: e.target.value })} className="mt-1" />
              </div>
              <div>
                <Label>Accent Color</Label>
                <div className="mt-2 flex flex-wrap gap-2">
                  {accentColors.map((c) => (
                    <button
                      key={c.value}
                      onClick={() => updateSettings({ accentColor: c.value })}
                      className={`h-10 w-10 rounded-lg border-[3px] transition-transform hover:scale-110 active:scale-95 ${settings.accentColor === c.value ? "border-outline shadow-retro ring-2 ring-outline" : "border-outline/40"}`}
                      style={{ background: c.value }}
                      title={c.label}
                    />
                  ))}
                </div>
              </div>
            </div>
          </WindowCard>
        </TabsContent>

        <TabsContent value="notifications">
          <WindowCard title="Notification Settings" headerColor="bg-pink">
            <div className="flex items-center justify-between max-w-md">
              <Label htmlFor="notifications">Enable Notifications</Label>
              <Switch id="notifications" checked={settings.notifications} onCheckedChange={(v) => updateSettings({ notifications: v })} />
            </div>
          </WindowCard>
        </TabsContent>

        <TabsContent value="units">
          <WindowCard title="Unit Preferences" headerColor="bg-sky">
            <div className="flex gap-3">
              {(["metric", "imperial"] as const).map((unit) => (
                <Button
                  key={unit}
                  variant={settings.units === unit ? "default" : "outline"}
                  onClick={() => updateSettings({ units: unit })}
                >
                  {unit.charAt(0).toUpperCase() + unit.slice(1)}
                </Button>
              ))}
            </div>
          </WindowCard>
        </TabsContent>

        <TabsContent value="system">
          <WindowCard title="System Settings" headerColor="bg-sage">
            <div className="space-y-4 max-w-md">
              <div className="flex items-center justify-between">
                <Label htmlFor="demo">Demo Mode</Label>
                <Switch id="demo" checked={settings.demoMode} onCheckedChange={(v) => updateSettings({ demoMode: v })} />
              </div>
              <p className="font-retro text-base opacity-70">All data is simulated. No backend connected.</p>
              <Button variant="outline" onClick={resetSettings}>Reset to Defaults</Button>
            </div>
          </WindowCard>
        </TabsContent>
      </Tabs>
    </AppShell>
  );
}
