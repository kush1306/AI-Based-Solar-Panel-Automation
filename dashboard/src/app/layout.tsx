import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { SettingsProvider } from "@/lib/settings-provider";
import { SidebarProvider } from "@/components/layout/sidebar-context";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Solar Intelligence Platform",
  description: "Enterprise solar energy monitoring and AI analytics",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans`}>
        <SettingsProvider>
          <SidebarProvider>{children}</SidebarProvider>
        </SettingsProvider>
      </body>
    </html>
  );
}
