"use client";

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Legend,
} from "recharts";

const tooltipStyle = {
  contentStyle: {
    background: "#18181B",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "8px",
    fontSize: "12px",
    color: "#FAFAFA",
  },
  itemStyle: { color: "#FAFAFA" },
  labelStyle: { color: "#A1A1AA" },
};

interface ChartProps {
  data: Record<string, unknown>[];
  height?: number;
}

export function PowerGenerationChart({ data, height = 320 }: ChartProps) {
  const chartData = data.map((d) => ({
    time: d.time,
    actual: Number(d.generation) * 1000,
    predicted: Number(d.generation) * 850,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="actualGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#0EA5E9" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#0EA5E9" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} unit=" W" />
        <Tooltip {...tooltipStyle} />
        <Legend wrapperStyle={{ fontSize: 12, paddingTop: 12 }} />
        <Area type="monotone" dataKey="actual" name="Actual Power (W)" stroke="#0EA5E9" fill="url(#actualGrad)" strokeWidth={2} />
        <Line type="monotone" dataKey="predicted" name="Predicted Power (W)" stroke="#10B981" strokeDasharray="4 4" dot={false} strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function GenerationConsumptionChart({ data, height = 260 }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} barGap={4}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <Tooltip {...tooltipStyle} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        <Bar dataKey="generation" name="Generation" fill="#F59E0B" radius={[4, 4, 0, 0]} />
        <Bar dataKey="consumption" name="Consumption" fill="#0EA5E9" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function LineTrendChart({ data, dataKey, color = "#10B981", height = 220 }: ChartProps & { dataKey: string; color?: string }) {
  const xKey = Object.keys(data[0] ?? {})[0];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <Tooltip {...tooltipStyle} />
        <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2} dot={{ fill: color, r: 3, strokeWidth: 0 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function AreaTrendChart({ data, dataKey, color = "#0EA5E9", height = 220 }: ChartProps & { dataKey: string; color?: string }) {
  const xKey = Object.keys(data[0] ?? {})[0];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id={`grad-${dataKey}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.25} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <Tooltip {...tooltipStyle} />
        <Area type="monotone" dataKey={dataKey} stroke={color} fill={`url(#grad-${dataKey})`} strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function DualBarChart({ data, keys, height = 220 }: ChartProps & { keys: [string, string] }) {
  const xKey = Object.keys(data[0] ?? {})[0];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} barGap={4}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
        <XAxis dataKey={xKey} axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <Tooltip {...tooltipStyle} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        <Bar dataKey={keys[0]} fill="#F59E0B" radius={[3, 3, 0, 0]} />
        <Bar dataKey={keys[1]} fill="#0EA5E9" radius={[3, 3, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function BatteryGauge({ value }: { value: number }) {
  const data = [
    { name: "SOC", value },
    { name: "Remaining", value: 100 - value },
  ];
  return (
    <div className="relative mx-auto w-full max-w-[200px]">
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="70%"
            startAngle={180}
            endAngle={0}
            innerRadius={55}
            outerRadius={75}
            dataKey="value"
            stroke="none"
          >
            <Cell fill="#10B981" />
            <Cell fill="#27272A" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-x-0 top-10 text-center">
        <p className="text-3xl font-semibold text-foreground">{value}%</p>
        <p className="text-xs text-muted">State of Charge</p>
      </div>
    </div>
  );
}

export function ForecastBarChart({ data, height = 160 }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <YAxis axisLine={false} tickLine={false} tick={{ fill: "#71717A", fontSize: 11 }} />
        <Tooltip {...tooltipStyle} />
        <Bar dataKey="value" fill="#F59E0B" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function EfficiencyGauge({ value }: { value: number }) {
  return <BatteryGauge value={value} />;
}
