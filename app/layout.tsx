import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "../components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "智能求职助手",
  description: "集改简历、写自荐信、搜工作和投简历为一体的智能系统",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="bg-white border-t py-6">
            <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
              © {new Date().getFullYear()} 智能求职助手 | 集改简历、写自荐信、搜工作和投简历为一体的智能系统
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
