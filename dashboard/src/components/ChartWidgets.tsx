"use client";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const retroTooltip = {
  contentStyle: {
    background: "#FFF9EF",
    border: "3px solid #222222",
    borderRadius: "8px",
    fontFamily: "VT323, monospace",
    fontSize: "16px",
  },
};

const COLORS = ["#FFD84D", "#FFB6D5", "#A8D5BA", "#8FD3FF", "#FF9F45"];

interface ChartProps {
  data: Record<string, unknown>[];
  height?: number;
}

export function GenerationConsumptionChart({ data, height = 220 }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#22222233" />
        <XAxis dataKey="time" tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <YAxis tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <Tooltip {...retroTooltip} />
        <Legend wrapperStyle={{ fontFamily: "VT323", fontSize: 14 }} />
        <Bar dataKey="generation" fill="#FFD84D" stroke="#222" strokeWidth={2} radius={[4, 4, 0, 0]} />
        <Bar dataKey="consumption" fill="#FFB6D5" stroke="#222" strokeWidth={2} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function LineTrendChart({ data, dataKey, color = "#A8D5BA", height = 200 }: ChartProps & { dataKey: string; color?: string }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#22222233" />
        <XAxis dataKey={Object.keys(data[0] ?? {})[0]} tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <YAxis tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <Tooltip {...retroTooltip} />
        <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={3} dot={{ fill: color, stroke: "#222", strokeWidth: 2, r: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function AreaTrendChart({ data, dataKey, color = "#8FD3FF", height = 200 }: ChartProps & { dataKey: string; color?: string }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#22222233" />
        <XAxis dataKey={Object.keys(data[0] ?? {})[0]} tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <YAxis tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <Tooltip {...retroTooltip} />
        <Area type="monotone" dataKey={dataKey} stroke={color} fill={color} fillOpacity={0.5} strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function DualBarChart({ data, keys, height = 200 }: ChartProps & { keys: [string, string] }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#22222233" />
        <XAxis dataKey={Object.keys(data[0] ?? {})[0]} tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <YAxis tick={{ fontFamily: "VT323", fontSize: 14 }} />
        <Tooltip {...retroTooltip} />
        <Legend wrapperStyle={{ fontFamily: "VT323", fontSize: 14 }} />
        <Bar dataKey={keys[0]} fill="#FFD84D" stroke="#222" strokeWidth={2} />
        <Bar dataKey={keys[1]} fill="#FFB6D5" stroke="#222" strokeWidth={2} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function EfficiencyGauge({ value }: { value: number }) {
  const data = [{ name: "Efficiency", value }, { name: "Remaining", value: 100 - value }];
  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie data={data} cx="50%" cy="70%" startAngle={180} endAngle={0} innerRadius={50} outerRadius={70} dataKey="value" stroke="#222" strokeWidth={2}>
            <Cell fill="#A8D5BA" />
            <Cell fill="#FFF9EF" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-x-0 top-12 text-center">
        <p className="font-retro text-3xl font-bold">{value}%</p>
        <p className="font-retro text-sm opacity-70">EFFICIENCY</p>
      </div>
    </div>
  );
}

export function ForecastBarChart({ data, height = 160 }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <XAxis dataKey="time" tick={{ fontFamily: "VT323", fontSize: 12 }} />
        <YAxis tick={{ fontFamily: "VT323", fontSize: 12 }} />
        <Tooltip {...retroTooltip} />
        <Bar dataKey="value" fill="#FFB6D5" stroke="#222" strokeWidth={2} radius={[3, 3, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export { COLORS };
