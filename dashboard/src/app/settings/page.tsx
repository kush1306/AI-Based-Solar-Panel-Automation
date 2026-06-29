"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PanelCard } from "@/components/cards/panel-card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { useSettings } from "@/lib/settings-provider";
import { cn } from "@/lib/utils";

const accentColors = [
  { label: "Amber", value: "#F59E0B" },
  { label: "Sky Blue", value: "#0EA5E9" },
  { label: "Emerald", value: "#10B981" },
  { label: "Orange", value: "#F97316" },
  { label: "Purple", value: "#A855F7" },
];

export default function SettingsPage() {
  const { settings, updateSettings, resetSettings } = useSettings();

  return (
    <AppShell
      title="Settings"
      description="Configure dashboard preferences, units, and system options"
    >
      <Tabs defaultValue="general">
        <TabsList className="mb-2">
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="units">Units</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
        </TabsList>

        <TabsContent value="general">
          <PanelCard title="General Settings" description="Location and appearance">
            <div className="max-w-md space-y-4">
              <div>
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  value={settings.location}
                  onChange={(e) => updateSettings({ location: e.target.value })}
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="timezone">Timezone</Label>
                <Input
                  id="timezone"
                  value={settings.timezone}
                  onChange={(e) => updateSettings({ timezone: e.target.value })}
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label>Accent Color</Label>
                <div className="mt-2 flex flex-wrap gap-2">
                  {accentColors.map((c) => (
                    <button
                      key={c.value}
                      type="button"
                      onClick={() => updateSettings({ accentColor: c.value })}
                      className={cn(
                        "h-9 w-9 rounded-lg border transition-all hover:scale-105",
                        settings.accentColor === c.value
                          ? "border-accent ring-2 ring-accent/30"
                          : "border-border hover:border-border/80"
                      )}
                      style={{ background: c.value }}
                      title={c.label}
                    />
                  ))}
                </div>
              </div>
            </div>
          </PanelCard>
        </TabsContent>

        <TabsContent value="notifications">
          <PanelCard title="Notification Settings" description="Alert and update preferences">
            <div className="flex max-w-md items-center justify-between rounded-lg border border-border/50 bg-background/40 px-4 py-3">
              <Label htmlFor="notifications">Enable Notifications</Label>
              <Switch
                id="notifications"
                checked={settings.notifications}
                onCheckedChange={(v) => updateSettings({ notifications: v })}
              />
            </div>
          </PanelCard>
        </TabsContent>

        <TabsContent value="units">
          <PanelCard title="Unit Preferences" description="Measurement system">
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
          </PanelCard>
        </TabsContent>

        <TabsContent value="system">
          <PanelCard title="System Settings" description="Demo mode and data source">
            <div className="max-w-md space-y-4">
              <div className="flex items-center justify-between rounded-lg border border-border/50 bg-background/40 px-4 py-3">
                <Label htmlFor="demo">Demo Mode</Label>
                <Switch
                  id="demo"
                  checked={settings.demoMode}
                  onCheckedChange={(v) => updateSettings({ demoMode: v })}
                />
              </div>
              <p className="text-sm text-muted">All data is simulated. No backend connected.</p>
              <Button variant="outline" onClick={resetSettings}>
                Reset to Defaults
              </Button>
            </div>
          </PanelCard>
        </TabsContent>
      </Tabs>
    </AppShell>
  );
}
