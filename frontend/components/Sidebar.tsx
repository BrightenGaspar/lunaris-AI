"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  LayoutDashboard,
  BarChart3,
  Cpu,
  Database,
  CheckSquare,
  ShieldAlert,
  Cloud,
  Users,
  Settings,
  Crown,
  ChevronDown,
} from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onOpenUpload: () => void;
  onOpenChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  onOpenUpload,
  onOpenChat,
}) => {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "analytics", label: "Analytics", icon: BarChart3 },
    { id: "models", label: "AI Models", icon: Cpu },
    { id: "data", label: "Data", icon: Database, action: onOpenUpload },
    { id: "tasks", label: "Tasks", icon: CheckSquare },
    { id: "security", label: "Security", icon: ShieldAlert },
    { id: "cloud", label: "Cloud", icon: Cloud },
    { id: "users", label: "Users", icon: Users },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0a080d] border-r border-red-500/20 flex flex-col justify-between p-4 select-none shrink-0 h-screen sticky top-0 overflow-y-auto">
      <div>
        {/* Brand Logo Header */}
        <div className="flex items-center space-x-3 px-2 py-3 mb-6">
          <div className="relative w-8 h-8 rounded-full bg-gradient-to-br from-[#ffca65] via-[#ff3838] to-[#750014] shadow-[0_0_18px_rgba(255,25,50,0.8)]">
            <div className="absolute -right-0.5 top-0.5 w-5 h-5 rounded-full bg-[#0a080d]" />
          </div>
          <span className="font-bold text-lg tracking-wider font-mono text-white">
            LUNARIS <span className="text-red-500">AI</span>
          </span>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.action) {
                    item.action();
                  } else {
                    setActiveTab(item.id);
                  }
                }}
                className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-red-600 via-red-600 to-red-700 text-white shadow-[0_4px_20px_rgba(255,20,50,0.4)]"
                    : "text-slate-400 hover:text-slate-100 hover:bg-white/[0.04]"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Pro Card & User Profile */}
      <div className="space-y-4 pt-4 border-t border-slate-800/60">
        {/* Upgrade to Pro Banner */}
        <div className="relative rounded-2xl bg-gradient-to-b from-[#18121d] to-[#0d0912] border border-red-500/30 p-3.5 overflow-hidden shadow-[0_10px_30px_rgba(0,0,0,0.5)]">
          <div className="absolute -right-4 -top-4 w-20 h-20 rounded-full bg-red-600/20 blur-xl pointer-events-none" />
          
          <div className="flex items-start justify-between">
            <div>
              <h4 className="text-xs font-bold text-white">
                Upgrade to <span className="text-red-500">Pro</span>
              </h4>
              <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">
                Unlock advanced AI models and higher limits.
              </p>
            </div>
            <div className="relative w-9 h-9 rounded-full bg-gradient-to-br from-red-500 to-amber-500 shadow-[0_0_12px_rgba(255,30,50,0.8)] flex items-center justify-center shrink-0">
              <div className="w-2.5 h-2.5 rounded-full bg-black/40" />
            </div>
          </div>

          <button
            onClick={onOpenChat}
            className="w-full mt-3 py-1.5 px-3 bg-gradient-to-r from-[#850820] to-[#ff4720] hover:from-red-600 hover:to-orange-500 text-white rounded-lg text-[11px] font-semibold flex items-center justify-center space-x-1.5 shadow-[0_4px_15px_rgba(255,25,45,0.3)] transition-all"
          >
            <Crown className="w-3 h-3 text-amber-300" />
            <span>Upgrade Now</span>
          </button>
        </div>

        {/* User Account Info */}
        <div className="flex items-center justify-between p-2 rounded-xl bg-white/[0.02] border border-slate-800 hover:border-slate-700 transition-colors cursor-pointer">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-red-600 to-amber-600 flex items-center justify-center font-bold text-xs text-white shadow-[0_0_10px_rgba(255,50,50,0.4)]">
              SB
            </div>
            <div>
              <div className="text-xs font-semibold text-white">Steve Brighton</div>
              <div className="text-[10px] text-slate-500">Free Plan</div>
            </div>
          </div>
          <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
        </div>
      </div>
    </aside>
  );
};
