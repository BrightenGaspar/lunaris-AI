"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Redirect to main chat app
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen w-full bg-[#030204] text-white flex flex-col justify-between relative overflow-hidden font-sans select-none">
      {/* Background Ambience & Red Energy Ribbons */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-red-600/10 blur-[130px] rounded-full" />
        <div className="absolute -bottom-20 left-0 right-0 h-80 bg-gradient-to-t from-red-600/25 via-red-950/10 to-transparent blur-2xl" />
        <div className="absolute -left-[20%] top-[40%] w-[65vw] h-[240px] rounded-full border-2 border-red-500/40 rotate-[16deg] shadow-[0_0_30px_rgba(255,20,50,0.5)]" />
        <div className="absolute -right-[22%] top-[45%] w-[65vw] h-[240px] rounded-full border-2 border-orange-500/50 -rotate-[16deg] shadow-[0_0_35px_rgba(255,100,20,0.45)]" />
      </div>

      {/* Top Navbar */}
      <header className="relative z-20 h-20 px-6 md:px-12 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {/* Crescent Planet Logo */}
          <div className="relative w-9 h-9 rounded-full bg-gradient-to-br from-[#ffca65] via-[#ff3838] to-[#750014] shadow-[0_0_20px_rgba(255,25,50,0.8)]">
            <div className="absolute -right-0.5 top-0.5 w-6 h-6 rounded-full bg-[#030204]" />
          </div>
          <span className="font-bold text-xl tracking-wider font-mono">
            LUNARIS <span className="text-red-500">AI</span>
          </span>
        </div>

        <div className="hidden md:flex items-center space-x-7 text-sm text-slate-300">
          <a href="#" className="hover:text-orange-400 transition-colors">About</a>
          <a href="#" className="hover:text-orange-400 transition-colors">Help</a>
          <div className="w-4 h-4 rounded-full border border-slate-500 flex items-center justify-center cursor-pointer hover:border-white">
            <div className="w-1.5 h-1.5 bg-slate-300 rounded-full" />
          </div>
        </div>
      </header>

      {/* Center Auth Card */}
      <main className="relative z-10 flex-1 flex items-center justify-center px-4 py-8">
        <div className="relative w-full max-w-[460px] bg-[#0a080c]/95 border border-red-500/40 rounded-[28px] p-8 md:p-10 shadow-[0_30px_100px_rgba(0,0,0,0.9),0_0_50px_rgba(255,20,50,0.18)] backdrop-blur-xl">
          {/* Top Planet Orb Dock */}
          <div className="absolute -top-16 left-1/2 -translate-x-1/2 w-32 h-32 flex items-center justify-center">
            <div className="relative w-24 h-24 rounded-full bg-gradient-to-br from-[#ffe1b3] via-[#ff6238] to-[#4a000d] shadow-[0_0_25px_rgba(255,20,50,0.9),0_0_60px_rgba(255,20,50,0.6)]">
              {/* Saturn-like ring */}
              <div className="absolute -inset-4 rounded-full border-2 border-orange-500/80 rotate-[-22deg] scale-y-[0.42] shadow-[0_0_15px_rgba(255,100,20,0.5)]" />
            </div>
            {/* Orbit satellite gold dot */}
            <div className="absolute right-1 top-14 w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_12px_#ffb834]" />
          </div>

          <div className="mt-8 text-center space-y-1">
            <h1 className="text-2xl md:text-3xl font-bold tracking-wider">
              LUNARIS <span className="text-red-500">AI</span>
            </h1>
            <p className="text-[10px] uppercase font-semibold text-slate-400 tracking-[0.25em]">
              Intelligence for a Brighter Tomorrow
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-7 space-y-4">
            {/* Email / Username Input */}
            <div className="relative flex items-center">
              <Mail className="absolute left-4 w-4 h-4 text-slate-500" />
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email or Username"
                required
                className="w-full h-12 bg-[#16121a]/80 border border-red-500/25 rounded-xl pl-11 pr-4 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all"
              />
            </div>

            {/* Password Input */}
            <div className="relative flex items-center">
              <Lock className="absolute left-4 w-4 h-4 text-slate-500" />
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                className="w-full h-12 bg-[#16121a]/80 border border-red-500/25 rounded-xl pl-11 pr-11 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 text-slate-500 hover:text-white"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between text-xs pt-1">
              <label className="flex items-center space-x-2 text-slate-400 cursor-pointer">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                  className="rounded border-slate-700 text-red-500 focus:ring-0 accent-red-600 w-3.5 h-3.5"
                />
                <span>Remember me</span>
              </label>
              <a href="#" className="text-red-400 hover:text-orange-400 transition-colors">
                Forgot Password?
              </a>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full h-12 mt-2 bg-gradient-to-r from-[#7c071d] via-[#d81333] to-[#ff7315] rounded-xl font-semibold text-sm shadow-[0_8px_30px_rgba(255,20,50,0.35)] hover:shadow-[0_12px_40px_rgba(255,50,30,0.55)] hover:-translate-y-0.5 transition-all flex items-center justify-center space-x-2"
            >
              <span>Log In</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Social Divider */}
          <div className="relative my-6 flex items-center justify-center">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-800" />
            </div>
            <span className="relative bg-[#0a080c] px-3 text-[10px] font-semibold tracking-wider text-slate-500 uppercase">
              Or continue with
            </span>
          </div>

          {/* Social OAuth Buttons */}
          <div className="grid grid-cols-3 gap-3">
            {/* Google */}
            <button className="h-11 rounded-xl bg-[#141219]/90 border border-slate-800 hover:border-red-500/40 hover:bg-[#1f1b26] flex items-center justify-center transition-all">
              <svg className="w-4 h-4" viewBox="0 0 24 24">
                <path fill="#EA4335" d="M12 5c1.7 0 3 .6 4 1.5l3-3C17.2 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"/>
                <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
                <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8s.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.3 0 12s.7 3.3 1.9 5.7l3.7-2.9z"/>
                <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.4-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"/>
              </svg>
            </button>

            {/* GitHub */}
            <button className="h-11 rounded-xl bg-[#141219]/90 border border-slate-800 hover:border-red-500/40 hover:bg-[#1f1b26] flex items-center justify-center transition-all">
              <svg className="w-4 h-4 fill-white" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
              </svg>
            </button>

            {/* Microsoft */}
            <button className="h-11 rounded-xl bg-[#141219]/90 border border-slate-800 hover:border-red-500/40 hover:bg-[#1f1b26] flex items-center justify-center transition-all">
              <svg className="w-4 h-4" viewBox="0 0 23 23">
                <path fill="#f35325" d="M1 1h10v10H1z"/>
                <path fill="#81bc06" d="M12 1h10v10H12z"/>
                <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                <path fill="#ffba08" d="M12 12h10v10H12z"/>
              </svg>
            </button>
          </div>

          {/* Sign Up Prompt */}
          <div className="mt-6 text-center text-xs text-slate-400">
            Don't have an account?{" "}
            <Link href="/" className="text-red-400 hover:text-orange-400 font-semibold ml-1 transition-colors">
              Sign Up
            </Link>
          </div>
        </div>
      </main>

      <footer className="relative z-10 py-4 text-center text-[11px] text-slate-600 font-mono">
        Lunaris AI Sovereign Intelligence • Air-Gapped & Zero Cloud Telemetry
      </footer>
    </div>
  );
}
