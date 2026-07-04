# -*- coding: utf-8 -*-
"""
battery_optimizer.py — Rule-based + LP battery optimizer
Week 2, Member 2 | AI Solar Panel Automation System
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List
from scipy.optimize import linprog


@dataclass
class BatteryConfig:
    capacity_kwh: float          = 5.0
    initial_soc: float           = 0.50
    min_soc: float               = 0.20
    max_soc: float               = 0.95
    charge_efficiency: float     = 0.92
    discharge_efficiency: float  = 0.92
    max_charge_rate_kw: float    = 2.5
    max_discharge_rate_kw: float = 2.5


@dataclass
class SolarConfig:
    panel_capacity_kwp: float = 3.0
    system_efficiency: float  = 0.80
    pr_ratio: float           = 0.80


@dataclass
class TariffConfig:
    """Delhi BSES domestic tariff (INR)."""
    grid_import_inr_per_kwh: float     = 8.0
    solar_export_inr_per_kwh: float    = 3.0
    fixed_charges_inr_per_month: float = 150.0
    tou_peak_hours: List[int]          = field(default_factory=lambda: list(range(17, 23)))
    tou_peak_rate: float               = 10.0
    tou_offpeak_rate: float            = 5.0


# ── helpers ──────────────────────────────────────────────────────────────────

def solar_kw(ghi_wm2: float, sc: SolarConfig) -> float:
    return max(0.0, sc.panel_capacity_kwp * (ghi_wm2/1000) * sc.system_efficiency * sc.pr_ratio)

def hour_tariff(h: int, tc: TariffConfig):
    is_peak = h in tc.tou_peak_hours
    return (tc.tou_peak_rate if is_peak else tc.tou_offpeak_rate), is_peak


# ── Rule-based optimizer ─────────────────────────────────────────────────────

class RuleBasedOptimizer:
    """
    Greedy real-time optimizer.
    Priority: solar first → charge battery surplus → discharge at peak.
    """
    def __init__(self, battery=None, solar=None, tariff=None):
        self.batt   = battery or BatteryConfig()
        self.solar  = solar   or SolarConfig()
        self.tariff = tariff  or TariffConfig()

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        soc, records = self.batt.initial_soc, []
        for _, row in df.iterrows():
            h   = row["time"].hour
            dem = float(row.get("demand_kw", 0.5))
            ghi = float(row.get("shortwave_radiation", 0.0))
            gen = solar_kw(ghi, self.solar)
            rate, peak = hour_tariff(h, self.tariff)
            net = gen - dem

            g_imp = g_exp = bc = bd = 0.0
            if net >= 0:
                bc  = min(net, self.batt.max_charge_rate_kw,
                           (self.batt.max_soc - soc)*self.batt.capacity_kwh
                           / max(self.batt.charge_efficiency, 1e-6))
                bc  = max(0.0, bc)
                g_exp = max(0.0, net - bc)
                soc += bc*self.batt.charge_efficiency / self.batt.capacity_kwh
            else:
                deficit = abs(net)
                if peak or h >= 18:
                    avail = min(deficit, self.batt.max_discharge_rate_kw,
                                (soc - self.batt.min_soc)*self.batt.capacity_kwh
                                *self.batt.discharge_efficiency)
                    bd    = max(0.0, avail)
                    soc  -= bd / (self.batt.discharge_efficiency*self.batt.capacity_kwh)
                    g_imp = max(0.0, deficit - bd)
                else:
                    if soc > 0.90:
                        avail = min(deficit, self.batt.max_discharge_rate_kw,
                                    (soc-self.batt.min_soc)*self.batt.capacity_kwh
                                    *self.batt.discharge_efficiency)
                        bd   = max(0.0, avail)
                        soc -= bd / (self.batt.discharge_efficiency*self.batt.capacity_kwh)
                    g_imp = max(0.0, deficit - bd)

            soc = float(np.clip(soc, 0, 1))
            records.append({
                "time": row["time"], "demand_kw": dem, "solar_gen_kw": gen,
                "battery_soc": round(soc,4),
                "battery_soc_kwh": round(soc*self.batt.capacity_kwh,4),
                "battery_charge_kw": round(bc,4), "battery_discharge_kw": round(bd,4),
                "grid_import_kw": round(g_imp,4), "grid_export_kw": round(g_exp,4),
                "is_peak_hour": peak, "tariff_inr_per_kwh": rate,
                "grid_cost_inr": round(g_imp*rate, 4),
                "export_earn_inr": round(g_exp*self.tariff.solar_export_inr_per_kwh, 4),
                "net_cost_inr": round(g_imp*rate - g_exp*self.tariff.solar_export_inr_per_kwh, 4),
            })
        return pd.DataFrame(records)


# ── LP day-ahead optimizer ───────────────────────────────────────────────────

class LPDayAheadOptimizer:
    """
    Linear Programming optimizer for a 24-hour horizon.
    Minimises total INR cost given perfect foresight of demand + solar.
    """
    def __init__(self, battery=None, solar=None, tariff=None):
        self.batt   = battery or BatteryConfig()
        self.solar  = solar   or SolarConfig()
        self.tariff = tariff  or TariffConfig()

    def optimize_day(self, demand_kw, ghi_wm2, initial_soc=None) -> pd.DataFrame:
        H    = 24
        soc0 = initial_soc if initial_soc is not None else self.batt.initial_soc
        gen  = np.array([solar_kw(g, self.solar) for g in ghi_wm2])
        tar  = np.array([hour_tariff(h, self.tariff)[0] for h in range(H)])
        er   = self.tariff.solar_export_inr_per_kwh

        # Vars per hour: [import, charge, discharge, export]
        c = np.zeros(H*4)
        for h in range(H):
            c[4*h]   =  tar[h]
            c[4*h+3] = -er

        bounds = []
        for _ in range(H):
            bounds += [(0,None),(0,self.batt.max_charge_rate_kw),
                       (0,self.batt.max_discharge_rate_kw),(0,None)]

        # Power balance: import + solar + discharge = demand + charge + export
        A_eq = np.zeros((H,H*4)); b_eq = np.zeros(H)
        for h in range(H):
            A_eq[h,4*h]=1; A_eq[h,4*h+1]=-1; A_eq[h,4*h+2]=1; A_eq[h,4*h+3]=-1
            b_eq[h] = demand_kw[h] - gen[h]

        # SoC bounds
        A_ub_r, b_ub_r = [], []
        for h in range(H):
            row = np.zeros(H*4)
            for t in range(h+1):
                row[4*t+1] =  self.batt.charge_efficiency / self.batt.capacity_kwh
                row[4*t+2] = -1.0/(self.batt.discharge_efficiency*self.batt.capacity_kwh)
            A_ub_r.append(row);   b_ub_r.append(self.batt.max_soc - soc0)
            A_ub_r.append(-row);  b_ub_r.append(-(self.batt.min_soc - soc0))

        res = linprog(c, A_ub=np.array(A_ub_r), b_ub=np.array(b_ub_r),
                      A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

        if not res.success:
            # fallback: no battery
            records = []
            for h in range(H):
                imp = max(0, demand_kw[h]-gen[h]); exp = max(0, gen[h]-demand_kw[h])
                _, pk = hour_tariff(h, self.tariff)
                records.append({"hour":h,"demand_kw":demand_kw[h],"solar_gen_kw":gen[h],
                                 "battery_soc":soc0,"battery_charge_kw":0,"battery_discharge_kw":0,
                                 "grid_import_kw":imp,"grid_export_kw":exp,"is_peak_hour":pk,
                                 "tariff_inr_per_kwh":tar[h],
                                 "grid_cost_inr":imp*tar[h],
                                 "export_earn_inr":exp*er,
                                 "net_cost_inr":imp*tar[h]-exp*er})
            return pd.DataFrame(records)

        x = res.x
        soc = soc0; records = []
        for h in range(H):
            imp_kw=max(0,x[4*h]); ch=max(0,x[4*h+1]); dis=max(0,x[4*h+2]); exp=max(0,x[4*h+3])
            soc += (ch*self.batt.charge_efficiency - dis/self.batt.discharge_efficiency)/self.batt.capacity_kwh
            soc  = float(np.clip(soc,0,1))
            _, pk = hour_tariff(h, self.tariff)
            records.append({"hour":h,"demand_kw":demand_kw[h],"solar_gen_kw":gen[h],
                             "battery_soc":round(soc,4),"battery_charge_kw":round(ch,4),
                             "battery_discharge_kw":round(dis,4),"grid_import_kw":round(imp_kw,4),
                             "grid_export_kw":round(exp,4),"is_peak_hour":pk,
                             "tariff_inr_per_kwh":tar[h],
                             "grid_cost_inr":round(imp_kw*tar[h],4),
                             "export_earn_inr":round(exp*er,4),
                             "net_cost_inr":round(imp_kw*tar[h]-exp*er,4)})
        return pd.DataFrame(records)


def annual_report(opt_df: pd.DataFrame) -> dict:
    total_demand = opt_df["demand_kw"].sum()
    total_solar  = opt_df["solar_gen_kw"].sum()
    total_import = opt_df["grid_import_kw"].sum()
    total_export = opt_df["grid_export_kw"].sum()
    total_cost   = opt_df["grid_cost_inr"].sum()
    total_earn   = opt_df["export_earn_inr"].sum()
    net_cost     = opt_df["net_cost_inr"].sum()
    baseline     = total_demand * 7.0
    savings      = baseline - net_cost
    self_suf     = (1 - total_import/max(total_demand,1e-6)) * 100

    return {
        "total_demand_kwh":      round(total_demand,2),
        "total_solar_kwh":       round(total_solar,2),
        "total_import_kwh":      round(total_import,2),
        "total_export_kwh":      round(total_export,2),
        "grid_cost_inr":         round(total_cost,2),
        "export_earn_inr":       round(total_earn,2),
        "net_cost_inr":          round(net_cost,2),
        "baseline_cost_inr":     round(baseline,2),
        "annual_savings_inr":    round(savings,2),
        "monthly_avg_saving_inr":round(savings/12,2),
        "self_sufficiency_pct":  round(self_suf,2),
    }
