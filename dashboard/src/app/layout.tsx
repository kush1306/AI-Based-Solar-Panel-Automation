import type { Metadata } from "next";
import { SettingsProvider } from "@/lib/settings-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Solar Optimization System",
  description: "Retro solar dashboard demo — frontend only, mock data",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <SettingsProvider>{children}</SettingsProvider>
      </body>
    </html>
  );
}
