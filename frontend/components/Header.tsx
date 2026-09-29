"use client";

import React from "react";
import { Search, Sun, Bell } from "lucide-react";

interface HeaderProps {
  onSearchFocus?: () => void;
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  onSearchSubmit: (e: React.FormEvent) => void;
}

export const Header: React.FC<HeaderProps> = ({
  searchQuery,
  setSearchQuery,
  onSearchSubmit,
}) => {
  return (
    <header className="h-16 px-6 border-b border-red-500/10 flex items-center justify-between bg-[#070509]/80 backdrop-blur-md sticky top-0 z-30">
      {/* Search Bar */}
      <form onSubmit={onSearchSubmit} className="flex-1 max-w-md">
        <div className="relative flex items-center">
          <Search className="absolute left-3.5 w-4 h-4 text-slate-500 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search anything..."
            className="w-full h-9 pl-10 pr-4 bg-[#141018]/90 border border-slate-800 rounded-full text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-red-500/60 focus:ring-1 focus:ring-red-500/30 transition-all font-sans"
          />
        </div>
      </form>

      {/* Right Controls */}
      <div className="flex items-center space-x-3.5">
        {/* Theme Toggle */}
        <button className="p-2 rounded-full bg-[#141018] border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-colors">
          <Sun className="w-4 h-4" />
        </button>

        {/* Notification Bell */}
        <div className="relative">
          <button className="p-2 rounded-full bg-[#141018] border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-colors">
            <Bell className="w-4 h-4" />
          </button>
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_#ff1638]" />
        </div>

        {/* User Avatar */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-red-600 to-amber-600 flex items-center justify-center font-bold text-xs text-white shadow-[0_0_12px_rgba(255,30,50,0.5)] cursor-pointer">
          SB
        </div>
      </div>
    </header>
  );
};
