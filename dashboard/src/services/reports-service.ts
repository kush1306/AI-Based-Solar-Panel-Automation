import { apiService } from "@/services/api-service";
import { mapMonthlyReports, mapReportSummary } from "@/services/mappers";
import type { MonthlyReportPoint, ReportSummary } from "@/types/api";

export interface ReportsPageData {
  reportSummary: ReportSummary;
  monthlyReports: MonthlyReportPoint[];
}

export async function fetchReportsPageData(): Promise<ReportsPageData> {
  const [energyPage, charts] = await Promise.all([
    apiService.listEnergy({ page_size: 500 }),
    apiService.getDashboardCharts(24 * 30),
  ]);

  const monthlyReports = mapMonthlyReports(energyPage.items, charts);

  return {
    monthlyReports,
    reportSummary: mapReportSummary(monthlyReports),
  };
}
