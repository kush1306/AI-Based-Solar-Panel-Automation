import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function randomInRange(min: number, max: number, decimals = 1) {
  const value = Math.random() * (max - min) + min;
  return Number(value.toFixed(decimals));
}

export function formatCurrency(value: number) {
  return `₹${value.toFixed(1)}`;
}

export function formatKw(value: number) {
  return `${value.toFixed(2)} kW`;
}

export function formatKwh(value: number) {
  return `${value.toFixed(2)} kWh`;
}

export function getAqiLabel(aqi: number) {
  if (aqi <= 50) return "GOOD";
  if (aqi <= 100) return "SATISFACTORY";
  if (aqi <= 200) return "MODERATE";
  if (aqi <= 300) return "POOR";
  return "HAZARDOUS";
}
