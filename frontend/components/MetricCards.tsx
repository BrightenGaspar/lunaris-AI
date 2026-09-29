"use client";

import React from "react";
import { Database, Cpu, Users, Zap, TrendingUp } from "lucide-react";

export const MetricCards: React.FC = () => {
  const metrics = [
    {
      title: "Total Data",
      value: "1.2M",
      change: "↑ 12.5%",
      icon: Database,
      sparkType: "bar",
      sparkValues: [40, 60, 50, 75, 60, 90, 100],
    },
    {
      title: "AI Models",
      value: "8",
      change: "↑ 2 today",
      icon: Cpu,
      sparkType: "bar",
      sparkValues: [20, 40, 30, 60, 80, 70, 90],
    },
    {
      title: "Active Users",
      value: "56,291",
      change: "↑ 8.3%",
      icon: Users,
      sparkType: "line",
      sparkValues: [30, 45, 40, 65, 55, 80, 95],
    },
    {
      title: "System Uptime",
      value: "99.2%",
      change: "↑ 0.4%",
      icon: Zap,
      sparkType: "line",
      sparkValues: [90, 92, 91, 95, 96, 98, 99],
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((m, idx) => {
        const Icon = m.icon;
        return (
          <div
            key={idx}
            className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-4 flex flex-col justify-between hover:border-red-500/40 transition-all shadow-[0_8px_25px_rgba(0,0,0,0.4)]"
          >
            <div className="flex items-center space-x-2.5">
              <div className="p-2 rounded-xl bg-red-600/10 text-red-500 border border-red-500/20">
                <Icon className="w-4 h-4" />
              </div>
              <span className="text-xs text-slate-400 font-medium">{m.title}</span>
            </div>

            <div className="flex items-end justify-between mt-3">
              <div>
                <div className="text-xl font-bold text-white font-mono">{m.value}</div>
                <div className="text-[10px] text-red-400 font-medium mt-0.5">{m.change}</div>
              </div>

              {/* Mini Sparkline Chart */}
              <div className="flex items-end space-x-1 h-7">
                {m.sparkType === "bar" ? (
                  m.sparkValues.map((val, i) => (
                    <div
                      key={i}
                      style={{ height: `${val}%` }}
                      className="w-1.5 bg-red-600/80 rounded-t-sm"
                    />
                  ))
                ) : (
                  <svg className="w-16 h-7 overflow-visible">
                    <polyline
                      fill="none"
                      stroke="#ff1638"
                      strokeWidth="2"
                      points="0,20 10,15 20,18 30,8 40,12 50,4 60,2"
                    />
                  </svg>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
