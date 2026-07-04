export const navItems = [
  { href: "/", label: "Dashboard", icon: "LayoutDashboard" },
  { href: "/solar-analytics", label: "Solar Analytics", icon: "BarChart3" },
  { href: "/ai-predictions", label: "AI Predictions", icon: "Brain" },
  { href: "/battery", label: "Battery Mgmt", icon: "Battery" },
  { href: "/energy-flow", label: "Energy Flow", icon: "Zap" },
  { href: "/weather", label: "Weather Intel", icon: "CloudSun" },
  { href: "/devices", label: "Device Monitor", icon: "Monitor" },
  { href: "/reports", label: "Reports", icon: "FileText" },
  { href: "/settings", label: "Settings", icon: "Settings" },
] as const;

export const categoryColors: Record<string, string> = {
  solar: "bg-butter",
  battery: "bg-sage",
  ai: "bg-sky",
  weather: "bg-pink",
  system: "bg-orange",
};
