import os
import secrets
from flask import Flask, request, session, redirect, url_for, render_template_string
from supabase import create_client

# ============================================================
# LUNARIS AI
# Flask + Supabase + Email OTP
# Everything is contained in this single file.
# ============================================================

app = Flask(__name__)

# Secret key from environment or secure random token
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "PASTE_YOUR_SUPABASE_URL_HERE")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "PASTE_YOUR_SUPABASE_PUBLISHABLE_KEY_HERE")

# Initialize client if valid credentials exist
supabase = None
if SUPABASE_URL != "PASTE_YOUR_SUPABASE_URL_HERE" and SUPABASE_KEY != "PASTE_YOUR_SUPABASE_PUBLISHABLE_KEY_HERE":
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("[Supabase Warning] Could not initialize client:", e)

# ============================================================
# COMPLETE HTML + CSS
# ============================================================

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} | Lunaris AI</title>
<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

:root{
    --black:#050506;
    --panel:#0b0b0e;
    --panel2:#141418;
    --red:#ff1638;
    --burgundy:#780d25;
    --orange:#ff7417;
    --gold:#ffb52c;
    --green:#22d36b;
    --white:#f7f7f8;
    --gray:#a8a8b1;
}

html{
    min-height:100%;
}

body{
    min-height:100vh;
    font-family: Inter, Segoe UI, Arial, sans-serif;
    color:white;
    background:
        radial-gradient(
            circle at 50% 110%,
            rgba(255,20,40,.28),
            transparent 38%
        ),
        radial-gradient(
            circle at 5% 45%,
            rgba(170,0,30,.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 95% 45%,
            rgba(255,120,10,.15),
            transparent 30%
        ),
        #030304;
    overflow-x:hidden;
}

/* BACKGROUND */
.grid{
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:-10;
    background-image:
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
    background-size: 70px 70px;
}

.wave{
    position:fixed;
    z-index:-8;
    pointer-events:none;
    width:70vw;
    height:250px;
    border-radius:50%;
    border: 2px solid rgba(255,30,50,.55);
    filter: drop-shadow(0 0 18px rgba(255,20,40,.45));
}

.wave1{
    left:-27%;
    top:42%;
    transform: rotate(18deg);
}

.wave2{
    right:-29%;
    top:46%;
    transform: rotate(-18deg);
    border-color: rgba(255,125,20,.7);
}

.wave3{
    right:-12%;
    top:63%;
    width:55vw;
    border-color: rgba(255,60,20,.25);
}

.floor{
    position:fixed;
    z-index:-9;
    left:0;
    bottom:-120px;
    width:100%;
    height:340px;
    background: radial-gradient(ellipse at center, rgba(255,20,35,.25), transparent 60%);
}

/* NAVIGATION */
nav{
    height:82px;
    padding: 0 5%;
    display:flex;
    align-items:center;
    justify-content: space-between;
}

.brand{
    display:flex;
    align-items:center;
    gap:13px;
    font-size:20px;
    font-weight:700;
    letter-spacing:1px;
}

.brand-red{
    color:var(--red);
}

.logo{
    width:43px;
    height:43px;
    position:relative;
    border-radius:50%;
    background: radial-gradient(circle at 30% 25%, #ffc35b, #ff4035 20%, #b00627 48%, #250008 70%);
    box-shadow: 0 0 25px rgba(255,25,50,.6);
}

.logo:after{
    content:"";
    position:absolute;
    width:30px;
    height:30px;
    right:-2px;
    top:1px;
    border-radius:50%;
    background:#050506;
}

.nav-right{
    display:flex;
    gap:30px;
    align-items:center;
}

.nav-right a{
    color:#d8d8dc;
    text-decoration:none;
    font-size:14px;
}

.nav-right a:hover{
    color:var(--orange);
}

/* MAIN */
main{
    min-height: calc(100vh - 82px);
    display:flex;
    justify-content:center;
    align-items:center;
    padding: 65px 20px 70px;
}

/* CARD */
.card{
    width:470px;
    position:relative;
    padding: 90px 42px 38px;
    border-radius:27px;
    background: linear-gradient(145deg, rgba(21,21,24,.96), rgba(5,5,7,.98));
    border: 1px solid rgba(255,70,40,.4);
    box-shadow: 0 35px 100px rgba(0,0,0,.75), 0 0 40px rgba(255,20,40,.08);
}

.card:before{
    content:"";
    position:absolute;
    inset:-2px;
    padding:2px;
    border-radius:29px;
    pointer-events:none;
    background: linear-gradient(135deg, var(--red), transparent 25%, transparent 70%, var(--orange));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;
    mask-composite:exclude;
}

/* PLANET */
.planet-box{
    position:absolute;
    top:-70px;
    left:50%;
    transform: translateX(-50%);
    width:145px;
    height:145px;
    display:grid;
    place-items:center;
}

.planet{
    width:112px;
    height:112px;
    position:relative;
    border-radius:50%;
    background: radial-gradient(circle at 30% 25%, #ffd5a0, #ff6435 15%, #ce1634 37%, #53000f 62%, #070708 73%);
    box-shadow: 0 0 15px #ff1838, 0 0 45px rgba(255,24,56,.55), inset -18px -15px 30px #000;
}

.planet:after{
    content:"";
    position:absolute;
    inset:-18px;
    border-radius:50%;
    border: 2px solid rgba(255,125,30,.75);
    transform: rotate(-25deg) scaleY(.45);
}

.planet-box:after{
    content:"";
    position:absolute;
    width:9px;
    height:9px;
    right:1px;
    top:66px;
    border-radius:50%;
    background: var(--gold);
    box-shadow: 0 0 15px var(--gold);
}

/* HEADINGS */
.title{
    text-align:center;
    font-size:34px;
    letter-spacing:2px;
}

.title span{
    background: linear-gradient(90deg, var(--red), var(--orange));
    -webkit-background-clip:text;
    color:transparent;
}

.subtitle{
    margin: 11px 0 31px;
    text-align:center;
    color:#c6c6ce;
    font-size:10px;
    line-height:1.8;
    letter-spacing:3.5px;
}

/* MESSAGE */
.message{
    margin-bottom:20px;
    padding: 12px 15px;
    border-radius:11px;
    font-size:13px;
    line-height:1.5;
}

.message.error{
    background: rgba(255,25,55,.10);
    border: 1px solid rgba(255,25,55,.35);
    color:#ff8d9e;
}

.message.success{
    background: rgba(30,210,105,.09);
    border: 1px solid rgba(30,210,105,.30);
    color:#78eca8;
}

/* INPUT */
.field{
    margin-bottom:16px;
}

.field label{
    display:block;
    color:#b9b9c1;
    margin: 0 0 8px 4px;
    font-size:12px;
}

.input{
    width:100%;
    height:61px;
    padding: 0 18px;
    color:white;
    font-size:15px;
    outline:none;
    border-radius:15px;
    border: 1px solid rgba(255,255,255,.14);
    background: linear-gradient(120deg, rgba(255,255,255,.055), rgba(255,255,255,.025));
    transition:.25s;
}

.input:focus{
    border-color: rgba(255,105,30,.8);
    box-shadow: 0 0 0 3px rgba(255,70,30,.07), 0 0 20px rgba(255,40,25,.12);
}

.input::placeholder{
    color:#888891;
}

/* BUTTONS */
.primary{
    width:100%;
    height:61px;
    border:0;
    border-radius:15px;
    cursor:pointer;
    color:white;
    font-size:17px;
    font-weight:600;
    background: linear-gradient(100deg, #850820, #d51231 45%, #ff7817);
    box-shadow: 0 8px 30px rgba(255,25,45,.20);
    transition:.2s;
    text-decoration:none;
    display:flex;
    align-items:center;
    justify-content:center;
}

.primary:hover{
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(255,50,20,.32);
}

.secondary{
    width:100%;
    height:52px;
    margin-top:12px;
    border-radius:13px;
    cursor:pointer;
    color:#ddd;
    border: 1px solid rgba(255,255,255,.13);
    background: #111114;
}

.secondary:hover{
    background: #18181c;
}

/* OTP */
.otp-title{
    text-align:center;
    margin-bottom:10px;
}

.otp-description{
    text-align:center;
    color:#aaaab2;
    font-size:13px;
    line-height:1.7;
    margin-bottom:24px;
}

.email-display{
    color: var(--orange);
}

.otp{
    width:100%;
    height:70px;
    text-align:center;
    font-size:30px;
    font-weight:700;
    letter-spacing:15px;
    padding-left:15px;
    color:white;
    outline:none;
    border-radius:15px;
    border: 1px solid rgba(255,100,30,.45);
    background: #111115;
    margin-bottom:20px;
}

.otp:focus{
    border-color: var(--orange);
    box-shadow: 0 0 25px rgba(255,100,20,.15);
}

/* DASHBOARD */
.dashboard-card{
    width: min(950px, 94vw);
    position:relative;
    border-radius:26px;
    padding:35px;
    background: linear-gradient(145deg, rgba(18,18,22,.97), rgba(5,5,7,.98));
    border: 1px solid rgba(255,75,30,.30);
    box-shadow: 0 30px 100px rgba(0,0,0,.75);
}

.dashboard-header{
    display:flex;
    justify-content: space-between;
    align-items:center;
    margin-bottom:30px;
}

.dashboard-header h1{
    font-size:30px;
}

.dashboard-header p{
    color:#999;
    margin-top:8px;
}

.logout{
    text-decoration:none;
    color:white;
    padding: 11px 19px;
    border-radius:10px;
    background: #19191d;
    border: 1px solid rgba(255,255,255,.12);
}

.stats{
    display:grid;
    grid-template-columns: repeat(3,1fr);
    gap:18px;
}

.stat{
    padding:25px;
    min-height:130px;
    border-radius:17px;
    background: linear-gradient(140deg, #16161a, #0b0b0e);
    border: 1px solid rgba(255,255,255,.08);
}

.stat .label{
    color:#9d9da5;
    font-size:12px;
}

.stat h2{
    margin-top:14px;
    font-size:27px;
}

.red{ color:#ff3650; }
.orange{ color:#ff8a2a; }
.green{ color:#39dd7d; }

.launch-btn-box{
    margin-top:25px;
    display:flex;
    gap:15px;
}

/* MOBILE */
@media(max-width:600px){
    nav{ height:68px; padding: 0 18px; }
    .brand{ font-size:16px; }
    .logo{ width:34px; height:34px; }
    .logo:after{ width:23px; height:23px; }
    .nav-right{ display:none; }
    main{ min-height: calc(100dvh - 68px); padding: 90px 14px 40px; }
    .card{ width:100%; max-width:390px; padding: 80px 21px 27px; }
    .title{ font-size:27px; }
    .subtitle{ font-size:8px; letter-spacing:2.8px; }
    .planet{ width:96px; height:96px; }
    .planet-box{ top:-61px; }
    .input{ height:56px; }
    .primary{ height:57px; }
    .otp{ font-size:25px; letter-spacing:10px; }
    .stats{ grid-template-columns:1fr; }
    .dashboard-header{ align-items:flex-start; gap:20px; flex-direction:column; }
    .launch-btn-box{ flex-direction:column; }
}
</style>
</head>
<body>

<div class="grid"></div>
<div class="wave wave1"></div>
<div class="wave wave2"></div>
<div class="wave wave3"></div>
<div class="floor"></div>

<nav>
    <div class="brand">
        <div class="logo"></div>
        LUNARIS
        <span class="brand-red">AI</span>
    </div>

    <div class="nav-right">
        <a href="/">Login</a>
        <a href="https://github.com/BrightenGaspar/lunaris-AI" target="_blank">GitHub</a>
        <a href="#">Docs</a>
    </div>
</nav>

<main>
{% if page == "login" %}
<!-- LOGIN -->
<div class="card">
    <div class="planet-box">
        <div class="planet"></div>
    </div>

    <h1 class="title">
        LUNARIS <span>AI</span>
    </h1>

    <p class="subtitle">
        INTELLIGENCE FOR A BRIGHTER<br>TOMORROW
    </p>

    {% if error %}
    <div class="message error">
        {{ error }}
    </div>
    {% endif %}

    {% if message %}
    <div class="message success">
        {{ message }}
    </div>
    {% endif %}

    <form method="POST" action="/send-otp">
        <div class="field">
            <label>EMAIL ADDRESS</label>
            <input class="input" name="email" type="email" placeholder="you@example.com" required autocomplete="email">
        </div>

        <button class="primary" type="submit">
            Continue with Email &nbsp; →
        </button>
    </form>

    <div style="text-align:center; color:#777; font-size:12px; margin-top:25px; line-height:1.7;">
        We'll send a verification code to your email.
    </div>
</div>

{% elif page == "verify" %}
<!-- OTP VERIFICATION -->
<div class="card">
    <div class="planet-box">
        <div class="planet"></div>
    </div>

    <h1 class="title">
        LUNARIS <span>AI</span>
    </h1>

    <p class="subtitle">SECURE AUTHENTICATION</p>
    <h2 class="otp-title">Verify your account</h2>

    <p class="otp-description">
        Enter the six-digit code sent to<br>
        <span class="email-display">{{ email }}</span>
    </p>

    {% if error %}
    <div class="message error">{{ error }}</div>
    {% endif %}

    {% if message %}
    <div class="message success">{{ message }}</div>
    {% endif %}

    <form method="POST" action="/verify">
        <input class="otp" name="otp" type="text" inputmode="numeric" maxlength="6" pattern="[0-9]{6}" placeholder="000000" autocomplete="one-time-code" required>
        <button class="primary" type="submit">Verify Code &nbsp; →</button>
    </form>

    <form method="POST" action="/resend">
        <button class="secondary" type="submit">Resend OTP</button>
    </form>

    <form method="GET" action="/">
        <button class="secondary" type="submit">← Change Email</button>
    </form>
</div>

{% elif page == "dashboard" %}
<!-- DASHBOARD -->
<div class="dashboard-card">
    <div class="dashboard-header">
        <div>
            <h1>Welcome to <span class="red">Lunaris AI</span></h1>
            <p>Signed in as {{ email }}</p>
        </div>
        <a href="/logout" class="logout">Log Out</a>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="label">AUTHENTICATION</div>
            <h2 class="green">✓ Verified</h2>
        </div>
        <div class="stat">
            <div class="label">SOVEREIGN CORE</div>
            <h2 class="orange">Online</h2>
        </div>
        <div class="stat">
            <div class="label">SESSION</div>
            <h2 class="red">Active</h2>
        </div>
    </div>

    <div class="launch-btn-box">
        <a href="http://localhost:3001" target="_blank" class="primary" style="flex:1;">
            Open Lunaris Web App (Port 3001) &nbsp; 🚀
        </a>
        <a href="http://localhost:8000/docs" target="_blank" class="primary" style="flex:1; background: #1a1a24; border:1px solid #ff7417;">
            View API Docs (Port 8000) &nbsp; 📖
        </a>
    </div>
</div>
{% endif %}
</main>

<script>
const otpInput = document.querySelector(".otp");
if(otpInput){
    otpInput.addEventListener("input", function(){
        this.value = this.value.replace(/[^0-9]/g, "");
    });
}
</script>

</body>
</html>
"""

# ============================================================
# HOME / LOGIN
# ============================================================

@app.route("/")
def login():
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))

    return render_template_string(
        PAGE,
        title="Login",
        page="login",
        error=None,
        message=None
    )

# ============================================================
# SEND OTP
# ============================================================

@app.route("/send-otp", methods=["POST"])
def send_otp():
    email = request.form.get("email", "").strip().lower()

    if not email:
        return render_template_string(
            PAGE,
            title="Login",
            page="login",
            error="Please enter your email address.",
            message=None
        )

    if not supabase:
        # Development bypass mode if Supabase credentials are not yet set
        print(f"[Dev Auth Notice] Supabase credentials not set. Simulating OTP send to {email}")
        session["pending_email"] = email
        return redirect(url_for("verify_page"))

    try:
        supabase.auth.sign_in_with_otp({"email": email})
        session["pending_email"] = email
        return redirect(url_for("verify_page"))
    except Exception as e:
        print("SEND OTP ERROR:", e)
        return render_template_string(
            PAGE,
            title="Login",
            page="login",
            error="Could not send the verification code. Please check Supabase configuration.",
            message=None
        )

# ============================================================
# OTP PAGE
# ============================================================

@app.route("/verify")
def verify_page():
    email = session.get("pending_email")
    if not email:
        return redirect(url_for("login"))

    return render_template_string(
        PAGE,
        title="Verify",
        page="verify",
        email=email,
        error=None,
        message=None
    )

# ============================================================
# VERIFY OTP
# ============================================================

@app.route("/verify", methods=["POST"])
def verify():
    email = session.get("pending_email")
    if not email:
        return redirect(url_for("login"))

    otp = request.form.get("otp", "").strip()

    if len(otp) != 6 or not otp.isdigit():
        return render_template_string(
            PAGE,
            title="Verify",
            page="verify",
            email=email,
            error="Enter the six-digit verification code.",
            message=None
        )

    if not supabase:
        # Dev test verification
        session.clear()
        session["authenticated"] = True
        session["email"] = email
        session["user_id"] = "dev-user-id"
        return redirect(url_for("dashboard"))

    try:
        response = supabase.auth.verify_otp({
            "email": email,
            "token": otp,
            "type": "email"
        })

        if not response.user:
            raise Exception("Verification failed")

        session.clear()
        session["authenticated"] = True
        session["email"] = email
        session["user_id"] = str(response.user.id)

        return redirect(url_for("dashboard"))
    except Exception as e:
        print("VERIFY ERROR:", e)
        return render_template_string(
            PAGE,
            title="Verify",
            page="verify",
            email=email,
            error="That code is invalid or expired. Please check it and try again.",
            message=None
        )

# ============================================================
# RESEND OTP
# ============================================================

@app.route("/resend", methods=["POST"])
def resend():
    email = session.get("pending_email")
    if not email:
        return redirect(url_for("login"))

    if not supabase:
        return render_template_string(
            PAGE,
            title="Verify",
            page="verify",
            email=email,
            error=None,
            message="A new verification code has been simulated."
        )

    try:
        supabase.auth.sign_in_with_otp({"email": email})
        return render_template_string(
            PAGE,
            title="Verify",
            page="verify",
            email=email,
            error=None,
            message="A new verification code has been sent."
        )
    except Exception as e:
        print("RESEND ERROR:", e)
        return render_template_string(
            PAGE,
            title="Verify",
            page="verify",
            email=email,
            error="Please wait before requesting another code.",
            message=None
        )

# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template_string(
        PAGE,
        title="Dashboard",
        page="dashboard",
        email=session.get("email", "User")
    )

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    return redirect(url_for("login"))

# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    print("")
    print("==============================")
    print("   🌕 LUNARIS AI AUTH PORTAL")
    print("==============================")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
