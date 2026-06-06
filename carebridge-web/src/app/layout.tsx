import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CareBridge — 养老机构家属沟通平台",
  description: "让家属随时了解老人在院情况，安心每一天",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full bg-gradient-to-br from-sky-50 via-white to-emerald-50">
        <header className="border-b border-sky-100 bg-white/80 backdrop-blur sticky top-0 z-10">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-3">
            <span className="text-2xl">🏥</span>
            <div>
              <h1 className="text-lg font-bold text-sky-700">CareBridge</h1>
              <p className="text-xs text-gray-400">养老机构家属沟通平台</p>
            </div>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
