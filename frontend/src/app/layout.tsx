import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgriSmart — Smart Farming Advisor",
  description:
    "AI-powered crop, fertilizer, and irrigation recommendations for sustainable farming",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
