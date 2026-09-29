"use client";

import React, { useState, useEffect } from "react";
import { CloudSun } from "lucide-react";

export const ClockWeatherWidget: React.FC = () => {
  const [timeStr, setTimeStr] = useState("23:45");
  const [dateStr, setDateStr] = useState("Mon, Sep 15, 2026");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      setTimeStr(`${hours}:${minutes}`);

      const options: Intl.DateTimeFormatOptions = {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric",
      };
      setDateStr(now.toLocaleDateString("en-US", options));
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="rounded-2xl bg-[#0f0b14] border border-red-500/20 p-4 flex flex-col justify-between shadow-[0_10px_30px_rgba(0,0,0,0.5)]">
      <div>
        <div className="text-[11px] text-slate-400 font-medium">
          {dateStr}
        </div>
        <div className="text-3xl font-extrabold text-red-500 font-mono tracking-wider mt-1 drop-shadow-[0_0_12px_rgba(255,20,50,0.6)]">
          {timeStr}
        </div>
      </div>

      <div className="flex items-center space-x-2.5 pt-3 border-t border-slate-800/60 mt-2">
        <div className="p-1.5 rounded-lg bg-amber-500/10 text-amber-400">
          <CloudSun className="w-4 h-4" />
        </div>
        <div>
          <div className="text-[11px] text-slate-400">Coimbatore, TN</div>
          <div className="text-xs font-semibold text-white flex items-center space-x-1.5">
            <span>27°C</span>
            <span className="text-[10px] text-slate-400 font-normal">Partly Cloudy</span>
          </div>
        </div>
      </div>
    </div>
  );
};
