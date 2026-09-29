import os
import secrets
from flask import Flask, request, session, redirect, url_for, render_template_string
from supabase import create_client

# ============================================================
# LUNARIS AI — Sovereign Intelligence Platform
# High-Fidelity Cyber-Celestial Authentication Portal
# ============================================================

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

SUPABASE_URL = os.getenv("SUPABASE_URL", "PASTE_YOUR_SUPABASE_URL_HERE")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "PASTE_YOUR_SUPABASE_PUBLISHABLE_KEY_HERE")

supabase = None
if SUPABASE_URL != "PASTE_YOUR_SUPABASE_URL_HERE" and SUPABASE_KEY != "PASTE_YOUR_SUPABASE_PUBLISHABLE_KEY_HERE":
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("[Supabase Warning] Could not initialize client:", e)

# ============================================================
# HIGH-FIDELITY HTML + CYBER-MECH CSS
# Matches Lunaris AI Design System (Mobile / Tablet / Desktop)
# ============================================================

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} | Lunaris AI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

:root{
    --bg-black:#030204;
    --red-core:#ff1538;
    --red-glow:rgba(255, 21, 56, 0.65);
    --red-ambient:rgba(235, 15, 45, 0.18);
    --orange-accent:#ff7417;
    --gold-accent:#ffb834;
    --card-bg:rgba(10, 8, 12, 0.94);
    --input-bg:rgba(22, 18, 26, 0.75);
    --input-border:rgba(255, 60, 80, 0.28);
    --input-focus:rgba(255, 80, 50, 0.9);
}

body{
    min-height:100vh;
    background-color: var(--bg-black);
    font-family: 'Inter', -apple-system, sans-serif;
    color: #f1f1f5;
    overflow-x:hidden;
    position:relative;
    display:flex;
    flex-direction:column;
    background-image: 
        radial-gradient(circle at 50% 115%, rgba(255, 20, 45, 0.38) 0%, transparent 45%),
        radial-gradient(circle at 10% 45%, rgba(180, 10, 30, 0.25) 0%, transparent 35%),
        radial-gradient(circle at 90% 45%, rgba(255, 110, 20, 0.22) 0%, transparent 35%);
}

/* CYBERSPACE BACKGROUND PARTICLES & WAVES */
.cosmic-nebula{
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:-10;
    background: 
        radial-gradient(ellipse at 50% 50%, rgba(255, 30, 60, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(255, 120, 20, 0.08) 0%, transparent 40%);
}

.energy-ribbon{
    position:fixed;
    pointer-events:none;
    z-index:-8;
    width:75vw;
    height:280px;
    border-radius:50%;
    border: 2px solid rgba(255, 30, 60, 0.55);
    filter: drop-shadow(0 0 25px rgba(255, 20, 50, 0.6));
}

.ribbon-left{
    left:-25%;
    top:40%;
    transform: rotate(16deg);
}

.ribbon-right{
    right:-28%;
    top:44%;
    transform: rotate(-16deg);
    border-color: rgba(255, 120, 25, 0.65);
    filter: drop-shadow(0 0 28px rgba(255, 100, 20, 0.55));
}

.ground-reflection{
    position:fixed;
    left:0;
    bottom:-140px;
    width:100%;
    height:380px;
    z-index:-9;
    background: radial-gradient(ellipse at center, rgba(255, 20, 40, 0.32) 0%, transparent 65%);
    filter: blur(20px);
}

/* TOP NAVIGATION */
nav{
    height:80px;
    padding:0 5%;
    display:flex;
    align-items:center;
    justify-content:space-between;
    z-index:20;
}

.brand-wrapper{
    display:flex;
    align-items:center;
    gap:12px;
    text-decoration:none;
}

.crescent-logo{
    width:36px;
    height:36px;
    position:relative;
    border-radius:50%;
    background: radial-gradient(circle at 35% 30%, #ffca65, #ff3838 35%, #96041c 70%);
    box-shadow: 0 0 20px rgba(255, 25, 50, 0.85);
}

.crescent-logo::after{
    content:"";
    position:absolute;
    width:25px;
    height:25px;
    right:-1px;
    top:1px;
    border-radius:50%;
    background: var(--bg-black);
}

.brand-text{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 22px;
    letter-spacing: 2px;
    color: #ffffff;
}

.brand-text span{
    color: var(--red-core);
}

.nav-links{
    display:flex;
    align-items:center;
    gap:28px;
}

.nav-links a{
    color:#b3b3c2;
    text-decoration:none;
    font-size:14px;
    font-weight:500;
    transition:color .2s;
}

.nav-links a:hover{
    color: var(--orange-accent);
}

.theme-toggle{
    cursor:pointer;
    display:flex;
    align-items:center;
    color:#c4c4d0;
}

/* CENTER PORTAL CONTAINER */
main{
    flex:1;
    display:flex;
    align-items:center;
    justify-content:center;
    padding: 70px 20px 80px;
    z-index:10;
}

/* CYBER-MECH CHASSIS CARD */
.cyber-card{
    width:480px;
    position:relative;
    padding: 85px 40px 36px;
    background: var(--card-bg);
    border-radius: 28px;
    border: 1.5px solid rgba(255, 60, 80, 0.45);
    box-shadow: 
        0 30px 100px rgba(0, 0, 0, 0.9),
        0 0 50px rgba(255, 20, 50, 0.18),
        inset 0 0 30px rgba(255, 20, 40, 0.08);
    backdrop-filter: blur(16px);
}

/* Cyber Bezel Corner Accents */
.cyber-card::before{
    content:"";
    position:absolute;
    inset:-2px;
    border-radius:30px;
    padding:2px;
    pointer-events:none;
    background: linear-gradient(135deg, var(--red-core), rgba(255, 20, 50, 0.1) 30%, rgba(255, 120, 20, 0.1) 70%, var(--orange-accent));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

/* Top Planet Orb */
.orb-dock{
    position:absolute;
    top:-68px;
    left:50%;
    transform: translateX(-50%);
    width:136px;
    height:136px;
    display:grid;
    place-items:center;
}

.cosmic-planet{
    width:104px;
    height:104px;
    position:relative;
    border-radius:50%;
    background: radial-gradient(circle at 32% 28%, #ffe1b3 0%, #ff6238 18%, #cb1233 42%, #4a000d 72%, #080608 85%);
    box-shadow: 
        0 0 20px rgba(255, 20, 50, 0.9),
        0 0 50px rgba(255, 20, 50, 0.6),
        inset -16px -14px 28px #000;
}

/* Planetary Ring */
.cosmic-planet::after{
    content:"";
    position:absolute;
    inset:-16px;
    border-radius:50%;
    border: 2.5px solid rgba(255, 130, 35, 0.85);
    transform: rotate(-22deg) scaleY(0.42);
    box-shadow: 0 0 15px rgba(255, 100, 20, 0.5);
}

/* Satellite Dot */
.orb-dock::after{
    content:"";
    position:absolute;
    width:9px;
    height:9px;
    right:3px;
    top:62px;
    border-radius:50%;
    background: var(--gold-accent);
    box-shadow: 0 0 16px var(--gold-accent), 0 0 30px var(--gold-accent);
}

/* CARD HEADERS */
.portal-title{
    font-family: 'Rajdhani', sans-serif;
    text-align:center;
    font-size:32px;
    font-weight:700;
    letter-spacing:2px;
    margin-top:4px;
}

.portal-title span{
    color: var(--red-core);
}

.portal-subtitle{
    font-family: 'Rajdhani', sans-serif;
    text-align:center;
    font-size:11px;
    letter-spacing:3.2px;
    color:#a8a8b8;
    margin: 6px 0 26px;
    font-weight:600;
}

/* MESSAGES */
.alert-box{
    margin-bottom:18px;
    padding: 12px 16px;
    border-radius:12px;
    font-size:13px;
    line-height:1.4;
}

.alert-error{
    background: rgba(255, 25, 60, 0.12);
    border: 1px solid rgba(255, 30, 60, 0.4);
    color: #ff94a4;
}

.alert-success{
    background: rgba(35, 215, 115, 0.12);
    border: 1px solid rgba(35, 215, 115, 0.4);
    color: #84f2b1;
}

/* FORM FIELDS */
.form-group{
    margin-bottom:14px;
    position:relative;
}

.input-container{
    position:relative;
    display:flex;
    align-items:center;
}

.field-icon{
    position:absolute;
    left:16px;
    width:18px;
    height:18px;
    color:#8e8e9e;
    pointer-events:none;
}

.toggle-eye{
    position:absolute;
    right:16px;
    cursor:pointer;
    color:#8e8e9e;
    transition:color .2s;
}

.toggle-eye:hover{
    color:#fff;
}

.cyber-input{
    width:100%;
    height:54px;
    padding: 0 44px;
    background: var(--input-bg);
    border: 1px solid var(--input-border);
    border-radius: 14px;
    color: #fff;
    font-size: 14px;
    outline:none;
    transition: all .25s ease;
}

.cyber-input:focus{
    border-color: var(--input-focus);
    box-shadow: 
        0 0 0 3px rgba(255, 60, 40, 0.12),
        0 0 22px rgba(255, 30, 50, 0.25);
    background: rgba(28, 22, 34, 0.9);
}

.cyber-input::placeholder{
    color: #6a6a7a;
}

/* UTILITY ROW */
.options-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin: 12px 2px 20px;
    font-size:12px;
}

.remember-box{
    display:flex;
    align-items:center;
    gap:8px;
    color:#a8a8b8;
    cursor:pointer;
    user-select:none;
}

.remember-box input[type="checkbox"]{
    accent-color: var(--red-core);
    cursor:pointer;
    width:15px;
    height:15px;
}

.forgot-link{
    color: #ff4760;
    text-decoration:none;
    font-weight:500;
    transition:color .2s;
}

.forgot-link:hover{
    color: var(--orange-accent);
}

/* PRIMARY LOGIN BUTTON */
.btn-login{
    width:100%;
    height:56px;
    border:none;
    border-radius: 14px;
    background: linear-gradient(95deg, #7c071d 0%, #d81333 45%, #ff7315 100%);
    color: #ffffff;
    font-family: 'Rajdhani', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 1px;
    cursor:pointer;
    box-shadow: 0 8px 30px rgba(255, 20, 50, 0.35);
    transition: all .25s ease;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:8px;
}

.btn-login:hover{
    transform: translateY(-2px);
    box-shadow: 0 12px 38px rgba(255, 40, 30, 0.55);
}

/* DIVIDER */
.oauth-divider{
    display:flex;
    align-items:center;
    margin: 24px 0 16px;
    gap:12px;
    color:#6e6e7e;
    font-size:11px;
    font-weight:600;
    letter-spacing:1.5px;
}

.oauth-divider::before,
.oauth-divider::after{
    content:"";
    flex:1;
    height:1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
}

/* SOCIAL OAUTH BUTTONS */
.oauth-grid{
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap:14px;
    margin-bottom:22px;
}

.oauth-btn{
    height:48px;
    display:flex;
    align-items:center;
    justify-content:center;
    background: rgba(20, 18, 25, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    cursor:pointer;
    transition: all .2s ease;
}

.oauth-btn:hover{
    background: rgba(32, 28, 40, 0.95);
    border-color: rgba(255, 60, 50, 0.4);
    transform: translateY(-1px);
}

/* FOOTER SIGNUP */
.signup-footer{
    text-align:center;
    font-size:13px;
    color:#8c8c9c;
}

.signup-footer a{
    color: #ff3e58;
    text-decoration:none;
    font-weight:600;
    margin-left:4px;
    transition:color .2s;
}

.signup-footer a:hover{
    color: var(--orange-accent);
}

/* DASHBOARD STYLING */
.dashboard-card{
    width: min(980px, 94vw);
    background: var(--card-bg);
    border-radius: 28px;
    border: 1.5px solid rgba(255, 60, 80, 0.35);
    box-shadow: 0 35px 110px rgba(0, 0, 0, 0.9);
    padding: 38px;
}

.dash-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:32px;
}

.stats-grid{
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap:20px;
}

.stat-box{
    padding:24px;
    border-radius:18px;
    background: rgba(18, 16, 22, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* RESPONSIVE BREAKPOINTS (Mobile & Tablet) */
@media(max-width:640px){
    nav{ height:65px; padding:0 18px; }
    .nav-links{ display:none; }
    .cyber-card{ width:100%; max-width:390px; padding: 75px 22px 28px; }
    .portal-title{ font-size:26px; }
    .cosmic-planet{ width:88px; height:88px; }
    .orb-dock{ top:-56px; }
    .stats-grid{ grid-template-columns: 1fr; }
    .dash-header{ flex-direction:column; align-items:flex-start; gap:16px; }
}
</style>
</head>
<body>

<div class="cosmic-nebula"></div>
<div class="energy-ribbon ribbon-left"></div>
<div class="energy-ribbon ribbon-right"></div>
<div class="ground-reflection"></div>

<nav>
    <a href="/" class="brand-wrapper">
        <div class="crescent-logo"></div>
        <div class="brand-text">LUNARIS <span>AI</span></div>
    </a>
    <div class="nav-links">
        <a href="#">About</a>
        <a href="#">Help</a>
        <div class="theme-toggle" title="Toggle theme">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        </div>
    </div>
</nav>

<main>
{% if page == "login" %}
<!-- CYBER-MECH LOGIN PORTAL CARD -->
<div class="cyber-card">
    <div class="orb-dock">
        <div class="cosmic-planet"></div>
    </div>

    <h1 class="portal-title">LUNARIS <span>AI</span></h1>
    <p class="portal-subtitle">INTELLIGENCE FOR A BRIGHTER TOMORROW</p>

    {% if error %}
    <div class="alert-box alert-error">{{ error }}</div>
    {% endif %}

    {% if message %}
    <div class="alert-box alert-success">{{ message }}</div>
    {% endif %}

    <form method="POST" action="/login">
        <div class="form-group">
            <div class="input-container">
                <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                    <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
                </svg>
                <input class="cyber-input" name="email" type="email" placeholder="Email or Username" required autocomplete="email">
            </div>
        </div>

        <div class="form-group">
            <div class="input-container">
                <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect width="18" height="11" x="3" y="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <input id="pwd-input" class="cyber-input" name="password" type="password" placeholder="Password" autocomplete="current-password">
                <div class="toggle-eye" onclick="togglePasswordVisibility()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                </div>
            </div>
        </div>

        <div class="options-row">
            <label class="remember-box">
                <input type="checkbox" name="remember" checked>
                <span>Remember me</span>
            </label>
            <a href="/send-otp-view" class="forgot-link">Forgot Password?</a>
        </div>

        <button class="btn-login" type="submit">
            Log In &nbsp; →
        </button>
    </form>

    <div class="oauth-divider">OR CONTINUE WITH</div>

    <div class="oauth-grid">
        <!-- Google -->
        <button class="oauth-btn" type="button" title="Continue with Google">
            <svg width="19" height="19" viewBox="0 0 24 24">
                <path fill="#EA4335" d="M12 5c1.7 0 3 .6 4 1.5l3-3C17.2 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"/>
                <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
                <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8s.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.3 0 12s.7 3.3 1.9 5.7l3.7-2.9z"/>
                <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.4-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"/>
            </svg>
        </button>

        <!-- GitHub -->
        <button class="oauth-btn" type="button" title="Continue with GitHub">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
            </svg>
        </button>

        <!-- Microsoft -->
        <button class="oauth-btn" type="button" title="Continue with Microsoft">
            <svg width="19" height="19" viewBox="0 0 23 23">
                <path fill="#f35325" d="M1 1h10v10H1z"/>
                <path fill="#81bc06" d="M12 1h10v10H12z"/>
                <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                <path fill="#ffba08" d="M12 12h10v10H12z"/>
            </svg>
        </button>
    </div>

    <div class="signup-footer">
        Don't have an account?<a href="/send-otp-view">Sign Up</a>
    </div>
</div>

{% elif page == "verify" %}
<!-- OTP VERIFICATION VIEW -->
<div class="cyber-card">
    <div class="orb-dock">
        <div class="cosmic-planet"></div>
    </div>

    <h1 class="portal-title">LUNARIS <span>AI</span></h1>
    <p class="portal-subtitle">SECURE EMAIL VERIFICATION</p>

    {% if error %}
    <div class="alert-box alert-error">{{ error }}</div>
    {% endif %}

    {% if message %}
    <div class="alert-box alert-success">{{ message }}</div>
    {% endif %}

    <p style="text-align:center; font-size:13px; color:#aaaab2; margin-bottom:20px;">
        Enter the 6-digit code sent to<br>
        <span style="color:var(--orange-accent); font-weight:600;">{{ email }}</span>
    </p>

    <form method="POST" action="/verify">
        <div class="form-group">
            <input class="cyber-input" style="text-align:center; font-size:24px; letter-spacing:8px; font-weight:700;" name="otp" type="text" inputmode="numeric" maxlength="6" pattern="[0-9]{6}" placeholder="000000" autocomplete="one-time-code" required>
        </div>
        <button class="btn-login" type="submit">Verify Code &nbsp; →</button>
    </form>

    <form method="POST" action="/resend" style="margin-top:12px;">
        <button type="submit" style="width:100%; height:46px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:12px; color:#ddd; cursor:pointer;">Resend Code</button>
    </form>

    <div class="signup-footer" style="margin-top:20px;">
        <a href="/">← Return to Login</a>
    </div>
</div>

{% elif page == "dashboard" %}
<!-- AUTHENTICATED DASHBOARD -->
<div class="dashboard-card">
    <div class="dash-header">
        <div>
            <h1 style="font-family:'Rajdhani', sans-serif; font-size:32px;">Welcome to <span style="color:var(--red-core);">Lunaris AI</span></h1>
            <p style="color:#8e8e9e; font-size:14px; margin-top:4px;">Signed in as {{ email }}</p>
        </div>
        <a href="/logout" style="text-decoration:none; color:#fff; padding:10px 18px; border-radius:10px; background:#18161e; border:1px solid rgba(255,255,255,0.12); font-size:13px;">Log Out</a>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div style="font-size:11px; color:#8e8e9e; letter-spacing:1px;">AUTHENTICATION</div>
            <h2 style="color:#39dd7d; font-size:26px; margin-top:8px;">✓ Verified</h2>
        </div>
        <div class="stat-box">
            <div style="font-size:11px; color:#8e8e9e; letter-spacing:1px;">SOVEREIGN CORE</div>
            <h2 style="color:#ff8a2a; font-size:26px; margin-top:8px;">Online</h2>
        </div>
        <div class="stat-box">
            <div style="font-size:11px; color:#8e8e9e; letter-spacing:1px;">SESSION MEMORY</div>
            <h2 style="color:#ff3650; font-size:26px; margin-top:8px;">Active</h2>
        </div>
    </div>

    <div style="display:flex; gap:16px; margin-top:30px;">
        <a href="http://localhost:3001" target="_blank" class="btn-login" style="flex:1; text-decoration:none;">
            Launch Sovereign Web App (Port 3001) &nbsp; 🚀
        </a>
        <a href="http://localhost:8000/docs" target="_blank" class="btn-login" style="flex:1; text-decoration:none; background:#191620; border:1px solid var(--orange-accent);">
            API Documentation (Port 8000) &nbsp; 📖
        </a>
    </div>
</div>
{% endif %}
</main>

<script>
function togglePasswordVisibility() {
    const pwd = document.getElementById("pwd-input");
    if (pwd) {
        pwd.type = pwd.type === "password" ? "text" : "password";
    }
}
</script>

</body>
</html>
"""

# ============================================================
# FLASK ROUTING & SUPABASE AUTH LOGIC
# ============================================================

@app.route("/")
def index():
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))
    return render_template_string(PAGE, title="Sign In", page="login", error=None, message=None)

@app.route("/login", methods=["POST"])
def login_handler():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not email:
        return render_template_string(PAGE, title="Sign In", page="login", error="Please enter your email address.", message=None)

    # Supabase password auth if password provided
    if password and supabase:
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                session.clear()
                session["authenticated"] = True
                session["email"] = email
                session["user_id"] = str(res.user.id)
                return redirect(url_for("dashboard"))
        except Exception as e:
            return render_template_string(PAGE, title="Sign In", page="login", error="Invalid credentials. Try email OTP.", message=None)

    # If no password or fallback, send email OTP
    if supabase:
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            session["pending_email"] = email
            return redirect(url_for("verify_view"))
        except Exception as e:
            print("OTP Send error:", e)

    # Dev fallback simulation
    session.clear()
    session["authenticated"] = True
    session["email"] = email
    session["user_id"] = "dev-sovereign-user"
    return redirect(url_for("dashboard"))

@app.route("/send-otp-view")
def send_otp_view():
    return render_template_string(PAGE, title="Sign Up / OTP", page="login", error=None, message="Enter your email to receive an instant verification code.")

@app.route("/verify")
def verify_view():
    email = session.get("pending_email", "user@example.com")
    return render_template_string(PAGE, title="Verify OTP", page="verify", email=email, error=None, message=None)

@app.route("/verify", methods=["POST"])
def verify_code():
    email = session.get("pending_email")
    otp = request.form.get("otp", "").strip()

    if not email:
        return redirect(url_for("index"))

    if len(otp) != 6 or not otp.isdigit():
        return render_template_string(PAGE, title="Verify OTP", page="verify", email=email, error="Enter the 6-digit verification code.", message=None)

    if supabase:
        try:
            res = supabase.auth.verify_otp({"email": email, "token": otp, "type": "email"})
            if res.user:
                session.clear()
                session["authenticated"] = True
                session["email"] = email
                session["user_id"] = str(res.user.id)
                return redirect(url_for("dashboard"))
        except Exception as e:
            return render_template_string(PAGE, title="Verify OTP", page="verify", email=email, error="Invalid or expired OTP code.", message=None)

    session.clear()
    session["authenticated"] = True
    session["email"] = email
    session["user_id"] = "dev-verified-user"
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("index"))
    return render_template_string(PAGE, title="Dashboard", page="dashboard", email=session.get("email", "Sovereign User"))

@app.route("/logout")
def logout():
    session.clear()
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("🌕 Lunaris AI Cyber-Celestial Auth Portal starting at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
