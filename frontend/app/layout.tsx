import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lunaris AI — Sovereign Intelligence Interface",
  description: "Self-hosted private intelligence platform with ReAct reasoning, Vector RAG, and Voice",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
