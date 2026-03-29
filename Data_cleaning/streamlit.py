"""
CloudPulse · Demand Intelligence Dashboard
Milestone 4: Forecast Integration & Capacity Planning
Regions: US-East, US-West, India-West, India-South
Services: Compute, Storage
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import math

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CloudPulse · Demand Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  GLOBAL CSS — Clean, friendly, readable design
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f1117;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.6rem 2rem 3rem; max-width: 1600px; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #151820;
    border-right: 1px solid rgba(148,163,184,.1);
}
section[data-testid="stSidebar"] > div { padding-top: 0.5rem; }

/* HERO BANNER */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #151820 100%);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1.1;
}
.hero-title em { color: #38bdf8; font-style: normal; }
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    color: #64748b;
    margin-top: .4rem;
    letter-spacing: .05em;
}
.hero-desc {
    font-size: .88rem;
    color: #94a3b8;
    margin-top: .5rem;
    max-width: 520px;
    line-height: 1.5;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    background: rgba(52,211,153,.08);
    border: 1px solid rgba(52,211,153,.25);
    border-radius: 100px;
    padding: .35rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem;
    color: #34d399;
    font-weight: 500;
}
.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #34d399;
    animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }

.drift-badge {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    background: rgba(248,113,113,.08);
    border: 1px solid rgba(248,113,113,.3);
    border-radius: 100px;
    padding: .35rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem;
    color: #f87171;
}

/* SECTION HEADERS */
.section-header {
    font-size: .82rem;
    font-weight: 700;
    color: #64748b;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin: 1.4rem 0 .8rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,.06);
}

/* METRIC CARDS */
.metrics-grid { display: grid; gap: 1rem; margin-bottom: 1.4rem; }
.metrics-4 { grid-template-columns: repeat(4, 1fr); }
.metrics-5 { grid-template-columns: repeat(5, 1fr); }
.metric-card {
    background: #1a1f2e;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.metric-card:hover { border-color: rgba(56,189,248,.25); }
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.mc-blue::after   { background: linear-gradient(90deg, #38bdf8, #818cf8); }
.mc-green::after  { background: linear-gradient(90deg, #34d399, #22d3ee); }
.mc-amber::after  { background: linear-gradient(90deg, #fbbf24, #fb923c); }
.mc-purple::after { background: linear-gradient(90deg, #a78bfa, #c084fc); }
.mc-rose::after   { background: linear-gradient(90deg, #fb7185, #f97316); }
.mc-teal::after   { background: linear-gradient(90deg, #2dd4bf, #34d399); }
.mc-sky::after    { background: linear-gradient(90deg, #7dd3fc, #38bdf8); }

.metric-label {
    font-size: .72rem;
    font-weight: 600;
    color: #64748b;
    letter-spacing: .07em;
    text-transform: uppercase;
    margin-bottom: .6rem;
}
.metric-icon { font-size: 1.1rem; margin-bottom: .4rem; display: block; }
.metric-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1;
}
.metric-note {
    font-size: .75rem;
    color: #64748b;
    margin-top: .45rem;
    line-height: 1.4;
}
.metric-note.good  { color: #34d399; }
.metric-note.bad   { color: #f87171; }
.metric-note.warn  { color: #fbbf24; }

/* ALERT BOXES */
.alert-box {
    border-radius: 12px;
    padding: .85rem 1.2rem;
    margin-bottom: 1rem;
    font-size: .84rem;
    display: flex;
    align-items: flex-start;
    gap: .75rem;
    line-height: 1.5;
}
.alert-icon { font-size: 1.1rem; margin-top: .05rem; flex-shrink: 0; }
.alert-text { flex: 1; }
.alert-title { font-weight: 700; margin-bottom: .15rem; font-size: .86rem; }
.alert-ok   { background: rgba(52,211,153,.08); border: 1px solid rgba(52,211,153,.2); color: #34d399; }
.alert-warn { background: rgba(251,191,36,.08); border: 1px solid rgba(251,191,36,.22); color: #fbbf24; }
.alert-err  { background: rgba(248,113,113,.08); border: 1px solid rgba(248,113,113,.22); color: #f87171; }
.alert-info { background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.22); color: #38bdf8; }
.alert-text span { color: #94a3b8; font-size: .82rem; }

/* PIPELINE STEPS */
.pipeline { display: flex; align-items: center; gap: 0; flex-wrap: wrap; row-gap: .6rem; margin: .8rem 0 1.4rem; }
.pipe-step {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 8px;
    padding: .4rem .85rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .73rem;
    color: #94a3b8;
    white-space: nowrap;
}
.pipe-step.active { border-color: rgba(56,189,248,.4); color: #38bdf8; background: rgba(56,189,248,.07); }
.pipe-step.warn   { border-color: rgba(251,191,36,.35); color: #fbbf24; background: rgba(251,191,36,.06); }
.pipe-step.danger { border-color: rgba(248,113,113,.35); color: #f87171; background: rgba(248,113,113,.06); }
.pipe-step.good   { border-color: rgba(52,211,153,.35); color: #34d399; background: rgba(52,211,153,.06); }
.pipe-arrow { color: #334155; padding: 0 .4rem; font-size: 1rem; }

/* TOOLTIP HELPER */
.tooltip-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: .35rem 0;
    border-bottom: 1px solid rgba(255,255,255,.04);
    font-size: .83rem;
}
.tooltip-row:last-child { border-bottom: none; }
.tooltip-key { color: #64748b; }
.tooltip-val { color: #f1f5f9; font-weight: 600; }

/* CHART CONTAINER */
.chart-wrap {
    background: #151820;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 1rem 1rem .5rem;
    margin-bottom: 1rem;
}
.chart-title {
    font-size: .85rem;
    font-weight: 700;
    color: #94a3b8;
    margin-bottom: .5rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.chart-desc { font-size: .77rem; color: #475569; margin-bottom: .6rem; line-height: 1.5; }

/* LOG BOX */
.log-box {
    background: #0b0f1a;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .73rem;
    color: #64748b;
    max-height: 220px;
    overflow-y: auto;
    line-height: 1.8;
}
.log-ts   { color: #334155; }
.log-ok   { color: #34d399; }
.log-err  { color: #f87171; }
.log-warn { color: #fbbf24; }
.log-info { color: #38bdf8; }

/* HELP TEXT / EXPLANATION */
.explain-box {
    background: rgba(56,189,248,.05);
    border-left: 3px solid #38bdf8;
    border-radius: 0 10px 10px 0;
    padding: .8rem 1.1rem;
    font-size: .82rem;
    color: #94a3b8;
    margin: .6rem 0 1rem;
    line-height: 1.6;
}
.explain-box strong { color: #38bdf8; }

.divider {
    border: none;
    height: 1px;
    margin: 1.6rem 0;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,.12), transparent);
}

/* SIDEBAR LABELS */
.sidebar-label {
    font-size: .72rem;
    font-weight: 700;
    color: #475569;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .35rem;
    margin-top: .9rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PLOTLY THEME
# ══════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#94a3b8", size=12),
    title_font=dict(family="Plus Jakarta Sans, sans-serif", color="#e2e8f0", size=13, weight=700),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)",
               tickfont=dict(size=11), zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.07)",
               tickfont=dict(size=11), zeroline=False),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#1e293b", bordercolor="rgba(56,189,248,.3)",
                    font=dict(family="Plus Jakarta Sans", size=12, color="#e2e8f0")),
)
MARGIN = dict(l=8, r=8, t=40, b=8)
LEGEND = dict(bgcolor="rgba(255,255,255,0.04)", bordercolor="rgba(255,255,255,0.08)",
              borderwidth=1, font=dict(size=11))

COLORS = dict(
    blue="#38bdf8", indigo="#818cf8", green="#34d399",
    amber="#fbbf24", rose="#fb7185", purple="#c084fc", teal="#2dd4bf"
)

# Region & service color maps
REGION_COLORS = {
    "US-East":    "#38bdf8",
    "US-West":    "#818cf8",
    "India-West": "#34d399",
    "India-South":"#fbbf24",
}
SERVICE_COLORS = {
    "Compute": "#38bdf8",
    "Storage": "#34d399",
}

# ══════════════════════════════════════════════════════════════════
#  FIXED REGIONS & SERVICES
# ══════════════════════════════════════════════════════════════════
ALL_REGIONS  = ["US-East", "US-West", "India-West", "India-South"]
ALL_SERVICES = ["Compute", "Storage"]


# ══════════════════════════════════════════════════════════════════
#  DATA GENERATION
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def generate_data():
    np.random.seed(42)
    n     = 180
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    trend    = np.linspace(0, 130, n)
    seasonal = 45 * np.sin(np.linspace(0, 4 * np.pi, n))
    noise    = np.random.normal(0, 20, n)
    base     = 680 + trend + seasonal + noise

    df = pd.DataFrame({
        "timestamp":          dates,
        "region_name":        np.random.choice(ALL_REGIONS, n, p=[.30, .25, .25, .20]),
        "service_category":   np.random.choice(ALL_SERVICES, n, p=[.55, .45]),
        "actual_usage":       np.clip(base, 500, 1100).astype(int),
        "allocated_capacity": np.clip(base + np.random.randint(30, 110, n), 550, 1200).astype(int),
        "operational_cost":   np.random.randint(2200, 5500, n),
        "availability_ratio": np.clip(np.random.normal(.974, .008, n), .940, .9999),
        "net_customer_change":np.random.randint(3, 28, n),
        "p99_latency_ms":     np.random.randint(18, 95, n),
        "incidents":          np.random.choice([0, 0, 0, 0, 1, 2], n),
    })
    df["forecast"]    = (df["actual_usage"] + np.random.normal(0, 30, n) + np.linspace(-15, 28, n)).astype(int)
    df["forecast_lo"] = (df["forecast"] - np.random.randint(30, 60, n)).astype(int)
    df["forecast_hi"] = (df["forecast"] + np.random.randint(30, 60, n)).astype(int)
    df["utilization_pct"] = (df["actual_usage"] / df["allocated_capacity"] * 100).round(1)
    df["error"]       = df["forecast"] - df["actual_usage"]
    df["abs_error"]   = df["error"].abs()
    df["pct_error"]   = (df["abs_error"] / df["actual_usage"] * 100).round(2)
    return df


def rmse(actual, forecast):
    return math.sqrt(np.mean((np.array(actual) - np.array(forecast)) ** 2))

def mae_fn(actual, forecast):
    return np.mean(np.abs(np.array(actual) - np.array(forecast)))


# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 1rem; border-bottom:1px solid rgba(255,255,255,.07); margin-bottom:1rem;">
      <div style="font-size:1.3rem; font-weight:800; color:#f1f5f9;">⚡ CloudPulse</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:.68rem; color:#475569; margin-top:.25rem;">
        DEMAND INTELLIGENCE · M4
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">📍 Navigation</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", [
        "📊  Capacity Overview",
        "🔮  Forecast Explorer",
        "🤖  Model Deployment",
        "⏱️  Automation & Pipeline",
        "🩺  Monitoring & Retraining",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">📁 Data Source</div>', unsafe_allow_html=True)
    file = st.file_uploader("Upload forecast CSV", type=["csv"], label_visibility="collapsed")
    if file:
        df_raw = pd.read_csv(file)
        df_raw["timestamp"] = pd.to_datetime(df_raw["timestamp"])
        # Filter to allowed regions/services only
        df_raw = df_raw[df_raw["region_name"].isin(ALL_REGIONS) & df_raw["service_category"].isin(ALL_SERVICES)]
        st.markdown('<div class="alert-box alert-ok"><span class="alert-icon">✅</span><div class="alert-text">Custom CSV loaded</div></div>', unsafe_allow_html=True)
    else:
        df_raw = generate_data()
        st.markdown('<div class="alert-box alert-info"><span class="alert-icon">ℹ️</span><div class="alert-text">Using demo dataset</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">🗺️ Regions</div>', unsafe_allow_html=True)
    st.caption("Select one or more regions to compare")
    region = st.multiselect("Regions", ALL_REGIONS, default=ALL_REGIONS, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">⚙️ Services</div>', unsafe_allow_html=True)
    st.caption("Compute = CPU/RAM usage · Storage = disk/data usage")
    service = st.multiselect("Services", ALL_SERVICES, default=ALL_SERVICES, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">📅 Date Range</div>', unsafe_allow_html=True)
    min_d, max_d = df_raw["timestamp"].min().date(), df_raw["timestamp"].max().date()
    dr = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d,
                       label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">🎛️ Chart Options</div>', unsafe_allow_html=True)
    show_ci      = st.toggle("Show Confidence Bands", value=True,
                              help="Shaded area shows the 10–90th percentile range of predicted values")
    show_anomaly = st.toggle("Highlight Anomalies", value=True,
                              help="Orange diamonds mark days where actual usage diverged unusually from forecast")
    ma_win       = st.slider("Smoothing Window (days)", 3, 21, 7,
                              help="Moving average window — higher = smoother line, lower = more detail")

    st.markdown('<div class="sidebar-label">🚨 Alert Threshold</div>', unsafe_allow_html=True)
    st.caption("RMSE above this value triggers a drift alert")
    rmse_thresh = st.slider("RMSE Alert Threshold", 30, 150, 70, label_visibility="collapsed")

# ── Apply filters ──
if len(dr) == 2:
    s_d, e_d = dr
    df_raw = df_raw[(df_raw["timestamp"].dt.date >= s_d) & (df_raw["timestamp"].dt.date <= e_d)]

if not region:
    region = ALL_REGIONS
if not service:
    service = ALL_SERVICES

df = df_raw[df_raw["region_name"].isin(region) & df_raw["service_category"].isin(service)].copy().sort_values("timestamp")

# ── Computed KPIs ──
cur_rmse   = rmse(df["actual_usage"], df["forecast"]) if len(df) > 0 else 0
cur_mae    = mae_fn(df["actual_usage"], df["forecast"]) if len(df) > 0 else 0
mape_val   = (df["abs_error"] / df["actual_usage"]).mean() * 100 if len(df) > 0 else 0
peak_row   = df.loc[df["forecast"].idxmax()] if len(df) > 0 else None
growth     = ((df.tail(30)["forecast"].mean() - df.head(30)["actual_usage"].mean())
              / df.head(30)["actual_usage"].mean() * 100) if len(df) >= 60 else 0
drift_flag = cur_rmse > rmse_thresh


# ══════════════════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════════════════
PAGE_INFO = {
    "📊  Capacity Overview":      ("Capacity Overview",    "How much cloud we're using vs what's predicted"),
    "🔮  Forecast Explorer":      ("Forecast Explorer",    "How accurate are our demand predictions?"),
    "🤖  Model Deployment":       ("Model Deployment",     "How the prediction model is served in production"),
    "⏱️  Automation & Pipeline":  ("Automation Pipeline",  "Scheduled jobs that keep forecasts up to date"),
    "🩺  Monitoring & Retraining":("Model Health Monitor", "Detecting when the model needs retraining"),
}
pt, pd_desc = PAGE_INFO[page]

badge_html = (
    '<span class="drift-badge">⚠ DRIFT DETECTED — Check Monitoring tab</span>'
    if drift_flag else
    '<span class="live-badge"><span class="live-dot"></span>LIVE MONITORING</span>'
)

st.markdown(f"""
<div class="hero">
  <div>
    <div class="hero-title">Cloud<em>Pulse</em> · {pt}</div>
    <div class="hero-desc">{pd_desc}</div>
    <div class="hero-sub">
      Regions: {", ".join(region)} &nbsp;·&nbsp;
      Services: {", ".join(service)} &nbsp;·&nbsp;
      {len(df):,} records &nbsp;·&nbsp;
      {datetime.now().strftime('%d %b %Y  %H:%M UTC')}
    </div>
  </div>
  <div style="display:flex; flex-direction:column; align-items:flex-end; gap:.5rem;">
    {badge_html}
    <div style="font-size:.75rem; color:#334155; text-align:right;">
      RMSE: {cur_rmse:.1f} &nbsp;|&nbsp; Threshold: {rmse_thresh}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE 1 — CAPACITY OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "📊  Capacity Overview":

    total_fc   = df["forecast"].sum() if len(df) > 0 else 0
    total_act  = df["actual_usage"].sum() if len(df) > 0 else 0
    avg_avail  = df["availability_ratio"].mean() if len(df) > 0 else 0
    total_cost = df["operational_cost"].sum() if len(df) > 0 else 0
    peak_day   = peak_row["timestamp"].strftime("%d %b") if peak_row is not None else "N/A"
    peak_fc    = int(peak_row["forecast"]) if peak_row is not None else 0
    g_dir      = "good" if growth >= 0 else "bad"
    g_sym      = "▲" if growth >= 0 else "▼"
    rmse_cls   = "bad" if drift_flag else "good"
    rmse_note  = f"⚠ Above alert threshold ({rmse_thresh})" if drift_flag else f"✓ Within threshold ({rmse_thresh})"

    if drift_flag:
        st.markdown(f"""
        <div class="alert-box alert-err">
          <span class="alert-icon">🚨</span>
          <div class="alert-text">
            <div class="alert-title">Model Drift Detected</div>
            <span>RMSE is {cur_rmse:.1f}, which exceeds your alert threshold of {rmse_thresh}.
            This means the model's predictions have become less accurate. Go to
            <strong>Monitoring &amp; Retraining</strong> for details and next steps.</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Cards ──
    st.markdown('<div class="section-header">📌 Key Numbers at a Glance</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid metrics-4">
      <div class="metric-card mc-blue">
        <span class="metric-icon">📈</span>
        <div class="metric-label">Total Forecast Demand</div>
        <div class="metric-value">{total_fc:,.0f}</div>
        <div class="metric-note">Predicted total usage across all selected filters</div>
      </div>
      <div class="metric-card mc-amber">
        <span class="metric-icon">⛰️</span>
        <div class="metric-label">Peak Day Forecast</div>
        <div class="metric-value">{peak_day}</div>
        <div class="metric-note">{peak_fc:,} units — highest predicted day</div>
      </div>
      <div class="metric-card mc-green">
        <span class="metric-icon">📊</span>
        <div class="metric-label">Demand Growth</div>
        <div class="metric-value">{abs(growth):.1f}%</div>
        <div class="metric-note {g_dir}">{g_sym} Last 30d vs first 30d average</div>
      </div>
      <div class="metric-card mc-{'rose' if drift_flag else 'purple'}">
        <span class="metric-icon">🎯</span>
        <div class="metric-label">Forecast Accuracy (RMSE)</div>
        <div class="metric-value">{cur_rmse:.1f}</div>
        <div class="metric-note {rmse_cls}">{rmse_note}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="explain-box">💡 <strong>How to read this page:</strong> The main chart shows actual usage (solid line) vs what the model predicted (dashed line). The shaded area is the confidence band — we expect actual usage to land within this range 90% of the time. Orange diamonds highlight unusual spikes or dips.</div>', unsafe_allow_html=True)

    # ── Main Time-Series ──
    st.markdown('<div class="section-header">📈 Actual Usage vs Forecast Over Time</div>', unsafe_allow_html=True)
    daily = (df.groupby("timestamp")
               .agg(actual=("actual_usage","mean"), forecast=("forecast","mean"),
                    fc_lo=("forecast_lo","mean"), fc_hi=("forecast_hi","mean"))
               .reset_index())
    daily["ma_a"] = daily["actual"].rolling(ma_win, center=True).mean()
    daily["ma_f"] = daily["forecast"].rolling(ma_win, center=True).mean()
    err_std = (daily["forecast"] - daily["actual"]).std()
    daily["anomaly"] = abs(daily["forecast"] - daily["actual"]) > 1.8 * err_std

    fig1 = go.Figure()
    if show_ci:
        fig1.add_trace(go.Scatter(
            x=pd.concat([daily["timestamp"], daily["timestamp"][::-1]]),
            y=pd.concat([daily["fc_hi"], daily["fc_lo"][::-1]]),
            fill="toself", fillcolor="rgba(129,140,248,0.1)",
            line=dict(color="rgba(0,0,0,0)"), name="Confidence Band (90%)", hoverinfo="skip"))
    fig1.add_trace(go.Scatter(x=daily["timestamp"], y=daily["actual"],
        mode="lines", name="Actual Usage", line=dict(color=COLORS["blue"], width=1.5), opacity=.4))
    fig1.add_trace(go.Scatter(x=daily["timestamp"], y=daily["ma_a"],
        mode="lines", name=f"Actual ({ma_win}d avg)", line=dict(color=COLORS["blue"], width=2.5)))
    fig1.add_trace(go.Scatter(x=daily["timestamp"], y=daily["ma_f"],
        mode="lines", name=f"Forecast ({ma_win}d avg)", line=dict(color=COLORS["purple"], width=2.5, dash="dot")))
    if show_anomaly:
        anom = daily[daily["anomaly"]]
        fig1.add_trace(go.Scatter(x=anom["timestamp"], y=anom["actual"],
            mode="markers", name="Unusual Spike/Dip",
            marker=dict(color=COLORS["amber"], size=10, symbol="diamond",
                        line=dict(color="#fff", width=1.5))))
    fig1.update_layout(**CHART_LAYOUT, height=370,
                       title="Daily Average Usage: Actual (blue) vs Forecast (purple dashed)")
    fig1.update_layout(margin=MARGIN, legend=LEGEND)
    st.plotly_chart(fig1, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Region & Service Breakdown ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">🌐 Usage by Region</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">Total actual usage and forecast per region. Longer bars = higher demand.</div>', unsafe_allow_html=True)
        rdf = (df.groupby("region_name")
                 .agg(actual=("actual_usage","sum"), forecast=("forecast","sum"))
                 .reset_index().sort_values("actual"))
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=rdf["region_name"], x=rdf["actual"], orientation="h",
            name="Actual", marker_color=[REGION_COLORS.get(r, COLORS["blue"]) for r in rdf["region_name"]],
            opacity=.8))
        fig2.add_trace(go.Bar(y=rdf["region_name"], x=rdf["forecast"], orientation="h",
            name="Forecast", marker_color=[REGION_COLORS.get(r, COLORS["blue"]) for r in rdf["region_name"]],
            opacity=.4))
        fig2.update_layout(**CHART_LAYOUT, height=300, barmode="overlay",
                           title="Actual (solid) vs Forecast (faint) by Region")
        fig2.update_layout(margin=MARGIN, legend=LEGEND)
        st.plotly_chart(fig2, width="stretch")

    with col2:
        st.markdown('<div class="section-header">⚙️ Compute vs Storage Usage</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">Monthly breakdown of Compute (CPU/RAM) and Storage (disk) usage over time.</div>', unsafe_allow_html=True)
        svc_t  = df.groupby(["timestamp","service_category"])["actual_usage"].mean().reset_index()
        svc_t["period"] = svc_t["timestamp"].dt.to_period("M").astype(str)
        svc_m  = svc_t.groupby(["period","service_category"])["actual_usage"].mean().reset_index()
        fig3   = go.Figure()
        for svc in ALL_SERVICES:
            sd = svc_m[svc_m["service_category"] == svc]
            if len(sd) > 0:
                fig3.add_trace(go.Bar(x=sd["period"], y=sd["actual_usage"], name=svc,
                    marker_color=SERVICE_COLORS[svc]))
        fig3.update_layout(**CHART_LAYOUT, height=300, barmode="stack",
                           title="Monthly Average: Compute (blue) + Storage (green)")
        fig3.update_layout(margin=MARGIN, legend=LEGEND)
        fig3.update_xaxes(tickangle=-30)
        st.plotly_chart(fig3, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">✅ Availability vs 99.5% SLA Target</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">Green line = uptime ratio. The dashed amber line is our 99.5% SLA commitment. Stay above it.</div>', unsafe_allow_html=True)
        av  = df.groupby("timestamp")["availability_ratio"].mean().reset_index()
        av["ma"] = av["availability_ratio"].rolling(ma_win, center=True).mean()
        figA = go.Figure()
        figA.add_hline(y=0.995, line_dash="dash", line_color=COLORS["amber"],
                       annotation_text="99.5% SLA Target", annotation_font_size=11,
                       annotation_font_color=COLORS["amber"])
        figA.add_trace(go.Scatter(x=av["timestamp"], y=av["availability_ratio"],
            mode="lines", name="Daily", line=dict(color=COLORS["indigo"], width=1), opacity=.25))
        figA.add_trace(go.Scatter(x=av["timestamp"], y=av["ma"],
            mode="lines", name=f"{ma_win}d Average", line=dict(color=COLORS["green"], width=2.5),
            fill="tonexty", fillcolor="rgba(52,211,153,0.05)"))
        figA.update_layout(**CHART_LAYOUT, height=290)
        figA.update_layout(margin=MARGIN, legend=LEGEND,
                           yaxis=dict(tickformat=".2%", range=[.93, 1.0],
                                      gridcolor="rgba(255,255,255,0.05)"))
        st.plotly_chart(figA, width="stretch")

    with col4:
        st.markdown('<div class="section-header">💰 Daily Operational Cost</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">Bars = daily cost in USD. The amber line shows the 7-day average trend.</div>', unsafe_allow_html=True)
        cd  = df.groupby("timestamp")["operational_cost"].sum().reset_index()
        cd["ma"] = cd["operational_cost"].rolling(7).mean()
        figC = go.Figure()
        figC.add_trace(go.Bar(x=cd["timestamp"], y=cd["operational_cost"], name="Daily Cost",
            marker=dict(color=cd["operational_cost"],
                        colorscale=[[0,"rgba(56,189,248,.35)"],[1,"rgba(129,140,248,.8)"]],
                        showscale=False), opacity=.75))
        figC.add_trace(go.Scatter(x=cd["timestamp"], y=cd["ma"], mode="lines",
            name="7-day Average", line=dict(color=COLORS["amber"], width=2.3)))
        figC.update_layout(**CHART_LAYOUT, height=290, barmode="overlay")
        figC.update_layout(margin=MARGIN, legend=LEGEND)
        st.plotly_chart(figC, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Heatmap ──
    st.markdown('<div class="section-header">🗺️ Usage Heatmap: Region × Service</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-desc">Brighter = higher total usage. Helps identify which region+service combination drives the most demand.</div>', unsafe_allow_html=True)
    pivot = df.pivot_table(values="actual_usage", index="region_name",
                           columns="service_category", aggfunc="sum").fillna(0)
    # Ensure all regions/services are present
    for r in ALL_REGIONS:
        if r not in pivot.index:
            pivot.loc[r] = 0
    for s in ALL_SERVICES:
        if s not in pivot.columns:
            pivot[s] = 0
    pivot = pivot[ALL_SERVICES].reindex(ALL_REGIONS).fillna(0)

    figH = go.Figure(go.Heatmap(
        z=pivot.values, x=list(pivot.columns), y=list(pivot.index),
        colorscale=[[0,"#0f172a"],[.35,"#1e3a5f"],[.7,"#38bdf8"],[1,"#bae6fd"]],
        text=pivot.values.astype(int), texttemplate="%{text:,}",
        textfont=dict(size=14, color="#f1f5f9"),
        hovertemplate="<b>%{y} · %{x}</b><br>Total Usage: %{z:,}<extra></extra>"))
    figH.update_layout(**CHART_LAYOUT, height=250)
    figH.update_layout(margin=dict(l=8, r=8, t=12, b=8))
    st.plotly_chart(figH, width="stretch")

    with st.expander("🔍 View Raw Data Table"):
        cols = [c for c in ["timestamp","region_name","service_category","actual_usage",
                             "forecast","forecast_lo","forecast_hi","error",
                             "operational_cost","availability_ratio","utilization_pct"] if c in df.columns]
        st.caption("Tip: Use the column headers to sort. 'Error' = Forecast − Actual. Green = under-prediction, Red = over-prediction.")
        st.dataframe(
            df[cols].style
              .background_gradient(subset=["actual_usage"], cmap="Blues")
              .background_gradient(subset=["error"], cmap="RdYlGn_r")
              .format({"actual_usage":"{:,.0f}", "forecast":"{:,.0f}",
                       "forecast_lo":"{:,.0f}", "forecast_hi":"{:,.0f}",
                       "error":"{:+,.0f}", "operational_cost":"${:,.0f}",
                       "availability_ratio":"{:.3%}", "utilization_pct":"{:.1f}%"}),
            width="stretch", height=360)


# ══════════════════════════════════════════════════════════════════
#  PAGE 2 — FORECAST EXPLORER
# ══════════════════════════════════════════════════════════════════
elif page == "🔮  Forecast Explorer":

    dir_acc = (np.sign(df["forecast"].diff()) == np.sign(df["actual_usage"].diff())).mean() * 100 if len(df) > 1 else 0

    st.markdown('<div class="explain-box">💡 <strong>What do these numbers mean?</strong> — <strong>RMSE</strong> and <strong>MAE</strong> measure average prediction error in the same units as usage (lower = better). <strong>MAPE</strong> is the error as a percentage. <strong>Directional Accuracy</strong> tells us how often the model correctly predicted whether usage would go up or down. <strong>Bias</strong> tells us if the model systematically over- or under-predicts (ideal = 0).</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🎯 Forecast Accuracy Metrics</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid metrics-5">
      <div class="metric-card mc-blue">
        <span class="metric-icon">📐</span>
        <div class="metric-label">RMSE</div>
        <div class="metric-value">{cur_rmse:.1f}</div>
        <div class="metric-note">Avg prediction error in usage units</div>
      </div>
      <div class="metric-card mc-green">
        <span class="metric-icon">📏</span>
        <div class="metric-label">MAE</div>
        <div class="metric-value">{cur_mae:.1f}</div>
        <div class="metric-note">Simpler average absolute error</div>
      </div>
      <div class="metric-card mc-amber">
        <span class="metric-icon">%</span>
        <div class="metric-label">MAPE</div>
        <div class="metric-value">{mape_val:.1f}%</div>
        <div class="metric-note">Error as a % of actual usage</div>
      </div>
      <div class="metric-card mc-purple">
        <span class="metric-icon">🧭</span>
        <div class="metric-label">Directional Accuracy</div>
        <div class="metric-value">{dir_acc:.1f}%</div>
        <div class="metric-note">Correct up/down prediction %</div>
      </div>
      <div class="metric-card mc-teal">
        <span class="metric-icon">⚖️</span>
        <div class="metric-label">Forecast Bias</div>
        <div class="metric-value">{df['error'].mean():+.1f}</div>
        <div class="metric-note">Positive = over-predicts · Negative = under-predicts</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📈 Forecast vs Actual with Confidence Bands</div>', unsafe_allow_html=True)
    d2 = (df.groupby("timestamp")
            .agg(actual=("actual_usage","mean"), forecast=("forecast","mean"),
                 fc_lo=("forecast_lo","mean"), fc_hi=("forecast_hi","mean"))
            .reset_index())
    d2["ma_f"] = d2["forecast"].rolling(ma_win, center=True).mean()

    figF = go.Figure()
    if show_ci:
        figF.add_trace(go.Scatter(
            x=pd.concat([d2["timestamp"], d2["timestamp"][::-1]]),
            y=pd.concat([d2["fc_hi"], d2["fc_lo"][::-1]]),
            fill="toself", fillcolor="rgba(129,140,248,0.1)",
            line=dict(color="rgba(0,0,0,0)"), name="90% Confidence Band", hoverinfo="skip"))
    figF.add_trace(go.Scatter(x=d2["timestamp"], y=d2["actual"],
        mode="lines", name="Actual Usage", line=dict(color=COLORS["blue"], width=2.5)))
    figF.add_trace(go.Scatter(x=d2["timestamp"], y=d2["forecast"],
        mode="lines", name="Forecast", line=dict(color=COLORS["purple"], width=2, dash="dot"), opacity=.75))
    figF.add_trace(go.Scatter(x=d2["timestamp"], y=d2["ma_f"],
        mode="lines", name=f"Forecast ({ma_win}d avg)", line=dict(color=COLORS["rose"], width=2.2)))
    figF.update_layout(**CHART_LAYOUT, height=380,
                       title="Blue = actual usage · Purple dashed = raw forecast · Red = smoothed forecast")
    figF.update_layout(margin=MARGIN, legend=LEGEND)
    st.plotly_chart(figF, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="section-header">📉 Forecast Error Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">Blue bars = forecast was higher than actual. Red bars = forecast was lower. The green shaded area is the "acceptable" tolerance zone.</div>', unsafe_allow_html=True)
        ed = df.groupby("timestamp").agg(error=("error","mean")).reset_index()
        ed["ma_err"] = ed["error"].rolling(ma_win, center=True).mean()
        figE = go.Figure()
        figE.add_hrect(y0=-rmse_thresh/2, y1=rmse_thresh/2,
                       fillcolor="rgba(52,211,153,0.05)", layer="below", line_width=0,
                       annotation_text="Tolerance zone", annotation_font_size=10,
                       annotation_font_color="#334155")
        figE.add_trace(go.Bar(x=ed["timestamp"], y=ed["error"], name="Daily Error",
            marker_color=np.where(ed["error"] >= 0, "rgba(56,189,248,.55)", "rgba(248,113,113,.55)")))
        figE.add_trace(go.Scatter(x=ed["timestamp"], y=ed["ma_err"],
            mode="lines", name=f"Trend ({ma_win}d avg)", line=dict(color=COLORS["amber"], width=2.2)))
        figE.update_layout(**CHART_LAYOUT, height=300, title="Error = Forecast − Actual (ideal = near zero)")
        figE.update_layout(margin=MARGIN, legend=LEGEND)
        st.plotly_chart(figE, width="stretch")

    with col2:
        st.markdown('<div class="section-header">📊 Error Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-desc">A well-calibrated model has errors centered at 0. A skewed distribution signals systematic bias.</div>', unsafe_allow_html=True)
        figH2 = go.Figure()
        figH2.add_trace(go.Histogram(x=df["error"], nbinsx=30,
            marker=dict(color="rgba(129,140,248,.7)", line=dict(color="rgba(129,140,248,.25)", width=.5))))
        figH2.add_vline(x=0, line_color=COLORS["green"], line_width=1.5, line_dash="dot",
                        annotation_text="Zero (ideal)", annotation_font_size=10,
                        annotation_font_color=COLORS["green"])
        figH2.add_vline(x=df["error"].mean(), line_color=COLORS["amber"], line_width=1.5,
                        annotation_text=f"Actual mean = {df['error'].mean():.1f}",
                        annotation_font_size=10, annotation_font_color=COLORS["amber"])
        figH2.update_layout(**CHART_LAYOUT, height=300,
                            title="Distribution of daily errors (ideal = centred on green line)")
        figH2.update_layout(margin=MARGIN, showlegend=False)
        st.plotly_chart(figH2, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🌐 Forecast Accuracy by Region & Service</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        r_rmse = (df.groupby("region_name")
                    .apply(lambda g: rmse(g["actual_usage"], g["forecast"]))
                    .reset_index(name="rmse").sort_values("rmse"))
        figR = go.Figure(go.Bar(
            y=r_rmse["region_name"], x=r_rmse["rmse"], orientation="h",
            marker=dict(color=[REGION_COLORS.get(r, COLORS["blue"]) for r in r_rmse["region_name"]]),
            text=r_rmse["rmse"].round(1), textposition="outside",
            textfont=dict(color="#94a3b8", size=11)))
        figR.add_vline(x=rmse_thresh, line_dash="dash", line_color=COLORS["rose"],
                       annotation_text=f"Alert threshold ({rmse_thresh})",
                       annotation_font_size=10, annotation_font_color=COLORS["rose"])
        figR.update_layout(**CHART_LAYOUT, height=260, title="RMSE per Region — lower is better")
        figR.update_layout(margin=MARGIN, showlegend=False)
        st.plotly_chart(figR, width="stretch")

    with col4:
        s_rmse = (df.groupby("service_category")
                    .apply(lambda g: rmse(g["actual_usage"], g["forecast"]))
                    .reset_index(name="rmse").sort_values("rmse"))
        figS = go.Figure(go.Bar(
            y=s_rmse["service_category"], x=s_rmse["rmse"], orientation="h",
            marker=dict(color=[SERVICE_COLORS.get(s, COLORS["green"]) for s in s_rmse["service_category"]]),
            text=s_rmse["rmse"].round(1), textposition="outside",
            textfont=dict(color="#94a3b8", size=11)))
        figS.add_vline(x=rmse_thresh, line_dash="dash", line_color=COLORS["rose"],
                       annotation_text=f"Alert threshold ({rmse_thresh})",
                       annotation_font_size=10, annotation_font_color=COLORS["rose"])
        figS.update_layout(**CHART_LAYOUT, height=260, title="RMSE per Service Type — lower is better")
        figS.update_layout(margin=MARGIN, showlegend=False)
        st.plotly_chart(figS, width="stretch")


# ══════════════════════════════════════════════════════════════════
#  PAGE 3 — MODEL DEPLOYMENT
# ══════════════════════════════════════════════════════════════════
elif page == "🤖  Model Deployment":

    st.markdown("""
    <div class="alert-box alert-info">
      <span class="alert-icon">ℹ️</span>
      <div class="alert-text">
        <div class="alert-title">What is this page?</div>
        <span>This documents how the forecast model is packaged and served in production.
        The FastAPI service receives requests and returns predictions in real time.
        The batch job runs daily to regenerate <code>forecast_output.csv</code>.</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📌 Deployment Status</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid metrics-4">
      <div class="metric-card mc-green">
        <span class="metric-icon">🚀</span>
        <div class="metric-label">Model Status</div>
        <div class="metric-value" style="font-size:1.3rem;">Active</div>
        <div class="metric-note good">POST /predict endpoint live</div>
      </div>
      <div class="metric-card mc-blue">
        <span class="metric-icon">🏷️</span>
        <div class="metric-label">Model Version</div>
        <div class="metric-value" style="font-size:1.5rem;">v3.2</div>
        <div class="metric-note">xgb_model_v3.pkl</div>
      </div>
      <div class="metric-card mc-purple">
        <span class="metric-icon">🔄</span>
        <div class="metric-label">Last Retrained</div>
        <div class="metric-value" style="font-size:1.3rem;">{(datetime.now()-timedelta(days=3)).strftime('%d %b')}</div>
        <div class="metric-note">3 days ago · Auto-triggered</div>
      </div>
      <div class="metric-card mc-amber">
        <span class="metric-icon">⚡</span>
        <div class="metric-label">Avg Response Time</div>
        <div class="metric-value">24ms</div>
        <div class="metric-note good">Real-time endpoint</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🏗️ How Data Flows Through the System</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline">
      <span class="pipe-step active">📥 New Usage Data</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">🔧 Preprocessing</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">🤖 XGBoost Model</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">🌐 FastAPI /predict</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📄 forecast_output.csv</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📊 Dashboard</span><span class="pipe-arrow">→</span>
      <span class="pipe-step">✅ Capacity Decision</span>
    </div>
    <div class="pipeline" style="margin-top:.3rem;">
      <span class="pipe-step warn">📡 Monitor RMSE</span>
      <span class="pipe-arrow">→</span>
      <span class="pipe-step warn">🚨 Exceeds Threshold?</span>
      <span class="pipe-arrow">→</span>
      <span class="pipe-step danger">🔄 Trigger Retrain</span>
      <span class="pipe-arrow">→</span>
      <span class="pipe-step good">🚀 Deploy New Model</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">⚡ Real-Time Prediction API</div>', unsafe_allow_html=True)
        st.caption("This FastAPI service accepts a single record and returns a forecast instantly.")
        st.code("""# api/main.py — Real-time prediction endpoint
from fastapi import FastAPI, HTTPException
import joblib, pandas as pd, logging

app   = FastAPI(title="CloudPulse Prediction API")
model = joblib.load("xgb_model_v3.pkl")  # loaded once at startup

@app.post("/predict")
def predict(payload: dict):
    try:
        df  = pd.DataFrame([payload])
        df  = preprocess(df)           # same steps used in training
        out = model.predict(df).tolist()
        return {"forecast": out, "model_version": "v3.2"}
    except KeyError as e:
        raise HTTPException(400, f"Missing field: {e}")
    except Exception as e:
        logging.error(f"/predict failed: {e}")
        raise HTTPException(500, "Prediction failed")

# Example request:
# POST /predict
# {"region":"US-East","service":"Compute","date":"2024-06-01",...}
# → {"forecast": [834], "model_version": "v3.2"}
""", language="python")

    with col2:
        st.markdown('<div class="section-header">📦 Daily Batch Prediction</div>', unsafe_allow_html=True)
        st.caption("Runs every morning to update forecast_output.csv for the dashboard.")
        st.code("""# batch_predict.py — Daily batch job
import joblib, pandas as pd, logging
from datetime import datetime

model = joblib.load("xgb_model_v3.pkl")

def run_batch():
    df = pd.read_csv("new_data.csv")

    # Handle missing values before predicting
    if df.isnull().any().any():
        logging.warning("Missing values found — filling with median")
        df = df.fillna(df.median(numeric_only=True))

    df = preprocess(df)               # re-uses saved scaler/encoder
    df["forecast"]    = model.predict(df)
    df["forecast_lo"] = df["forecast"] - 45  # 10th percentile
    df["forecast_hi"] = df["forecast"] + 45  # 90th percentile

    df.to_csv("forecast_output.csv", index=False)
    logging.info(f"[{datetime.now()}] Batch OK — {len(df)} rows")

if __name__ == "__main__":
    run_batch()
""", language="python")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📄 Required Output File Schema</div>', unsafe_allow_html=True)
    st.caption("forecast_output.csv must contain these columns to work with the dashboard.")
    schema = pd.DataFrame({
        "Column":      ["timestamp","actual_usage","forecast","forecast_lo","forecast_hi",
                        "region_name","service_category","operational_cost","availability_ratio"],
        "Type":        ["datetime","int","int","int","int","str","str","int","float"],
        "Description": ["Date of the prediction period","Recorded actual resource usage",
                        "Point forecast (50th percentile)","Lower bound — 10th percentile",
                        "Upper bound — 90th percentile",
                        "One of: US-East / US-West / India-West / India-South",
                        "Compute or Storage","Daily cost in USD","Uptime ratio (0.0 – 1.0)"],
        "Required?":   ["✅ Yes","✅ Yes","✅ Yes","⬜ Recommended","⬜ Recommended",
                        "✅ Yes","✅ Yes","⬜ Optional","⬜ Optional"],
    })
    st.dataframe(schema, width="stretch", hide_index=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📚 Model Version History</div>', unsafe_allow_html=True)
    st.caption("Every retrained model is logged. We only deploy if RMSE improves.")
    versions = pd.DataFrame({
        "Version": ["v1.0","v2.0","v2.1","v3.0","v3.2"],
        "Date":    ["2024-01-10","2024-02-15","2024-03-01","2024-04-20","2024-06-03"],
        "RMSE":    [95.4, 78.2, 72.1, 65.8, round(cur_rmse,1)],
        "MAE":     [71.2, 58.6, 55.3, 50.1, round(cur_mae,1)],
        "Reason for Retrain": ["Initial training","Scheduled monthly","Drift alert (RMSE=98.3)",
                                "Drift alert (RMSE=91.0)","Scheduled monthly"],
        "Status":  ["Retired","Retired","Retired","Retired","🟢 Production"],
    })
    st.dataframe(versions, width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE 4 — AUTOMATION & PIPELINE
# ══════════════════════════════════════════════════════════════════
elif page == "⏱️  Automation & Pipeline":

    st.markdown("""
    <div class="alert-box alert-ok">
      <span class="alert-icon">✅</span>
      <div class="alert-text">
        <div class="alert-title">Pipeline is Running Normally</div>
        <span>The daily scheduler runs automatically at 06:00 UTC every day.
        It ingests new data, generates forecasts, and alerts the team if accuracy drops.
        No manual intervention needed.</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📌 Pipeline Health Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid metrics-4">
      <div class="metric-card mc-green">
        <span class="metric-icon">🕕</span>
        <div class="metric-label">Last Successful Run</div>
        <div class="metric-value" style="font-size:1.2rem;">06:00 UTC</div>
        <div class="metric-note good">Completed in 4.2 seconds</div>
      </div>
      <div class="metric-card mc-blue">
        <span class="metric-icon">📋</span>
        <div class="metric-label">Records Processed</div>
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-note">Written to forecast_output.csv</div>
      </div>
      <div class="metric-card mc-purple">
        <span class="metric-icon">⏰</span>
        <div class="metric-label">Schedule</div>
        <div class="metric-value" style="font-size:1.2rem;">Daily</div>
        <div class="metric-note">06:00 UTC · cron: 0 6 * * *</div>
      </div>
      <div class="metric-card mc-amber">
        <span class="metric-icon">⚠️</span>
        <div class="metric-label">Failures (Last 30 days)</div>
        <div class="metric-value">1</div>
        <div class="metric-note warn">Missing input CSV — auto-recovered</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔄 Step-by-Step Pipeline Flow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline">
      <span class="pipe-step active">⏰ Scheduler fires at 06:00</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📥 Ingest new_data.csv</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">🔧 Preprocess features</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">🤖 Generate forecasts</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📄 Write forecast_output.csv</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📊 Dashboard updates</span>
    </div>
    <div class="pipeline" style="margin-top:.3rem;">
      <span class="pipe-step warn">⬇ Also: compute RMSE</span>
      <span class="pipe-arrow">→</span>
      <span class="pipe-step warn">RMSE &gt; {rmse_thresh}?</span>
      <span class="pipe-arrow">→</span>
      <span class="pipe-step danger">🚨 Send alert + trigger retrain</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">⏰ Scheduler Code</div>', unsafe_allow_html=True)
        st.caption("Runs as a background process on the server. No manual triggers needed.")
        st.code("""# scheduler.py
import schedule, time, logging
from batch_predict import run_batch
from monitoring    import check_rmse

RMSE_THRESHOLD = 70   # matches dashboard slider

def pipeline_job():
    logging.info("Scheduler triggered pipeline")
    try:
        run_batch()                         # Step 1: generate forecasts
        rmse_val = check_rmse()             # Step 2: measure accuracy
        if rmse_val > RMSE_THRESHOLD:
            logging.warning(f"DRIFT: RMSE={rmse_val:.1f}")
            send_alert(rmse_val)            # Step 3: alert + retrain
        logging.info(f"Pipeline OK · RMSE={rmse_val:.1f}")
    except FileNotFoundError:
        logging.error("new_data.csv missing — pipeline aborted")
    except Exception as e:
        logging.error(f"Pipeline error: {e}")

schedule.every().day.at("06:00").do(pipeline_job)
while True:
    schedule.run_pending()
    time.sleep(30)
""", language="python")

    with col2:
        st.markdown('<div class="section-header">🚨 Automated Alerting & Pre-Scaling</div>', unsafe_allow_html=True)
        st.caption("When forecasts exceed capacity thresholds, the infra team is notified automatically.")
        st.code("""# alerts.py
def send_alert(rmse_val: float):
    \"\"\"Notify the team when model accuracy drops.\"\"\"
    msg = (
        f"[CloudPulse] Drift Alert\\n"
        f"RMSE: {rmse_val:.1f} (threshold: {RMSE_THRESHOLD})\\n"
        f"Action: review retraining pipeline"
    )
    logging.warning(msg)
    # Production: Slack webhook / email / PagerDuty

def check_capacity_ceiling(forecast_df, ceiling=0.80):
    \"\"\"Alert when forecast exceeds 80% of provisioned capacity.
    This triggers pre-scaling — adding resources BEFORE demand peaks.\"\"\"
    at_risk = forecast_df[
        forecast_df["forecast"] / forecast_df["allocated_capacity"]
        > ceiling
    ]
    for _, row in at_risk.iterrows():
        logging.warning(
            f"CAPACITY RISK: {row['timestamp'].date()} — "
            f"forecast {row['forecast']} > {ceiling*100:.0f}% of capacity. "
            f"Pre-scale resources now."
        )
    return at_risk
""", language="python")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 Pipeline Run Log — Last 14 Days</div>', unsafe_allow_html=True)
    log_html = ""
    for i in range(14, 0, -1):
        d    = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        ok   = i != 11
        rows = np.random.randint(170, 185)
        rval = round(cur_rmse + np.random.uniform(-8, 12), 1)
        secs = round(np.random.uniform(3.8, 5.2), 1)
        if ok:
            log_html += (f'<span class="log-ts">{d} 06:00:04</span>  '
                         f'<span class="log-ok">SUCCESS</span>  '
                         f'· {rows} rows written · RMSE={rval} · {secs}s<br>')
        else:
            log_html += (f'<span class="log-ts">{d} 06:00:01</span>  '
                         f'<span class="log-err">FAILED</span>  '
                         f'· FileNotFoundError: new_data.csv not found<br>')
    st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  PAGE 5 — MONITORING & RETRAINING
# ══════════════════════════════════════════════════════════════════
elif page == "🩺  Monitoring & Retraining":

    if drift_flag:
        st.markdown(f"""
        <div class="alert-box alert-err">
          <span class="alert-icon">🚨</span>
          <div class="alert-text">
            <div class="alert-title">Model Drift Detected — Action Required</div>
            <span>Current RMSE is {cur_rmse:.1f}, which exceeds your alert threshold of {rmse_thresh}.
            This means the model's predictions have degraded. The retraining pipeline should be triggered.
            Lower the RMSE threshold slider if you want earlier warnings.</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-box alert-ok">
          <span class="alert-icon">✅</span>
          <div class="alert-text">
            <div class="alert-title">Model is Healthy</div>
            <span>Current RMSE is {cur_rmse:.1f}, within the alert threshold of {rmse_thresh}.
            Monitoring continues normally. The model will be automatically retrained if RMSE exceeds {rmse_thresh}.</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    dir_acc = (np.sign(df["forecast"].diff()) == np.sign(df["actual_usage"].diff())).mean() * 100 if len(df) > 1 else 0

    st.markdown('<div class="explain-box">💡 <strong>What is model drift?</strong> — Over time, usage patterns change (new customers, seasonal shifts, infrastructure upgrades). When this happens, a model trained on old data becomes less accurate. We detect this by watching the RMSE: if it rises above the threshold, we automatically retrain the model on the latest data.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📌 Current Model Health</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metrics-grid metrics-5">
      <div class="metric-card mc-{'rose' if drift_flag else 'green'}">
        <span class="metric-icon">{'🚨' if drift_flag else '✅'}</span>
        <div class="metric-label">Current RMSE</div>
        <div class="metric-value">{cur_rmse:.1f}</div>
        <div class="metric-note {'bad' if drift_flag else 'good'}">Alert threshold: {rmse_thresh}</div>
      </div>
      <div class="metric-card mc-blue">
        <span class="metric-icon">📏</span>
        <div class="metric-label">Current MAE</div>
        <div class="metric-value">{cur_mae:.1f}</div>
        <div class="metric-note">Mean absolute error</div>
      </div>
      <div class="metric-card mc-amber">
        <span class="metric-icon">🧭</span>
        <div class="metric-label">Directional Accuracy</div>
        <div class="metric-value">{dir_acc:.1f}%</div>
        <div class="metric-note">Up/down prediction accuracy</div>
      </div>
      <div class="metric-card mc-purple">
        <span class="metric-icon">{'⚠️' if drift_flag else '🟢'}</span>
        <div class="metric-label">Drift Status</div>
        <div class="metric-value" style="font-size:1.1rem;">{'DRIFT' if drift_flag else 'Stable'}</div>
        <div class="metric-note {'warn' if drift_flag else 'good'}">
          {'Retrain now' if drift_flag else 'Monitoring OK'}
        </div>
      </div>
      <div class="metric-card mc-teal">
        <span class="metric-icon">🔄</span>
        <div class="metric-label">Last Retrained</div>
        <div class="metric-value" style="font-size:1.1rem;">3 days ago</div>
        <div class="metric-note">v3.2 deployed</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Rolling RMSE ──
    st.markdown('<div class="section-header">📉 14-Day Rolling RMSE — Is the Model Getting Worse?</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-desc">Each point = RMSE computed over the past 14 days. Points above the red dashed line trigger a retraining alert. Green zone = healthy. Red zone = action needed.</div>', unsafe_allow_html=True)
    dates_s = sorted(df["timestamp"].unique())
    roll_rmse, roll_dates = [], []
    for i in range(14, len(dates_s)):
        w = df[df["timestamp"].isin(dates_s[i-14:i])]
        if len(w) > 0:
            roll_rmse.append(rmse(w["actual_usage"], w["forecast"]))
            roll_dates.append(dates_s[i])
    rmse_df = pd.DataFrame({"date": roll_dates, "rmse": roll_rmse})

    figM = go.Figure()
    figM.add_hrect(y0=0, y1=rmse_thresh, fillcolor="rgba(52,211,153,0.04)", layer="below", line_width=0)
    figM.add_hrect(y0=rmse_thresh, y1=rmse_thresh*1.6, fillcolor="rgba(248,113,113,0.04)", layer="below", line_width=0)
    figM.add_hline(y=rmse_thresh, line_dash="dash", line_color=COLORS["rose"],
                   annotation_text=f"Alert threshold — retrain if RMSE crosses this ({rmse_thresh})",
                   annotation_font_size=11, annotation_font_color=COLORS["rose"])
    if len(rmse_df) > 0:
        figM.add_trace(go.Scatter(x=rmse_df["date"], y=rmse_df["rmse"],
            mode="lines+markers", name="14-day Rolling RMSE",
            line=dict(color=COLORS["amber"], width=2.5),
            marker=dict(size=5,
                        color=[COLORS["rose"] if v > rmse_thresh else COLORS["green"] for v in rmse_df["rmse"]])))
    figM.update_layout(**CHART_LAYOUT, height=320,
                       title="Rolling RMSE — green zone = healthy, red zone = retrain needed")
    figM.update_layout(margin=MARGIN, legend=LEGEND)
    st.plotly_chart(figM, width="stretch")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">📊 Data Drift Detection</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-box alert-warn">
          <span class="alert-icon">⚠️</span>
          <div class="alert-text">
            <div class="alert-title">What is data drift?</div>
            <span>Data drift = the <em>inputs</em> to the model have changed distribution (e.g., usage patterns shifted).
            Detected by comparing current input stats to the training baseline using a KS-test.</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.code("""# Data drift — compare feature distributions (KS-test)
from scipy import stats

def detect_data_drift(train_df, new_df, feature, alpha=0.05):
    \"\"\"If p-value < 0.05, the distribution has shifted = data drift.\"\"\"
    stat, p_val = stats.ks_2samp(
        train_df[feature].dropna(),
        new_df[feature].dropna()
    )
    drifted = p_val < alpha
    logging.info(f"{feature}: p={p_val:.4f} "
                 f"{'→ DRIFT DETECTED' if drifted else '→ OK'}")
    return drifted

# Run on every batch cycle for key features
for col in ["actual_usage", "operational_cost", "p99_latency_ms"]:
    detect_data_drift(train_baseline, new_data, col)
""", language="python")

    with col2:
        st.markdown('<div class="section-header">🎯 Concept Drift Detection</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-box alert-err">
          <span class="alert-icon">🚨</span>
          <div class="alert-text">
            <div class="alert-title">What is concept drift?</div>
            <span>Concept drift = the <em>relationship</em> between inputs and the target has changed
            (e.g., a new region was added, or service patterns fundamentally shifted).
            Only detectable by comparing predictions to actuals over time.</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.code("""# Concept drift — monitor RMSE vs training baseline
RMSE_BASELINE = 55.0   # best RMSE from training
DRIFT_MARGIN  = 0.25   # 25% degradation = alert

def check_concept_drift(actual, predicted):
    \"\"\"Log predictions at inference time; join with actuals later.
    This logging is as important as the model itself.\"\"\"
    current_rmse = math.sqrt(
        sum((a-p)**2 for a,p in zip(actual, predicted)) / len(actual)
    )
    threshold = RMSE_BASELINE * (1 + DRIFT_MARGIN)
    if current_rmse > threshold:
        logging.warning(f"CONCEPT DRIFT: RMSE={current_rmse:.2f}")
        return True   # trigger retraining pipeline
    return False
""", language="python")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔄 Retraining Pipeline</div>', unsafe_allow_html=True)
    st.caption("The model is only deployed if it performs better than the current production model.")
    st.code("""# retraining_pipeline.py
import joblib, logging, math, datetime
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

PROD_PATH = "xgb_model_v3.pkl"

def retrain_if_better():
    # Step 1: Load latest data
    df = pd.read_csv("updated_data.csv")
    df = preprocess(df)

    # Step 2: 80/20 train/test split
    split = int(len(df) * 0.8)
    X_tr, X_te = df.iloc[:split].drop("actual_usage", axis=1), df.iloc[split:].drop("actual_usage", axis=1)
    y_tr, y_te = df.iloc[:split]["actual_usage"],              df.iloc[split:]["actual_usage"]

    # Step 3: Train new model
    new_model = XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05)
    new_model.fit(X_tr, y_tr)

    # Step 4: Compare new vs current production model
    new_rmse  = math.sqrt(mean_squared_error(y_te, new_model.predict(X_te)))
    prod_rmse = math.sqrt(mean_squared_error(y_te, joblib.load(PROD_PATH).predict(X_te)))

    # Step 5: Only deploy if new model is strictly better
    if new_rmse < prod_rmse:
        ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        new_path = f"xgb_model_{ts}.pkl"    # versioned backup
        joblib.dump(new_model, new_path)
        joblib.dump(new_model, PROD_PATH)   # update production
        logging.info(f"DEPLOYED: RMSE {prod_rmse:.1f} → {new_rmse:.1f}")
    else:
        logging.warning(f"NOT deployed: new model worse ({new_rmse:.1f} vs {prod_rmse:.1f})")

    log_retrain_event(prod_rmse, new_rmse, len(df))
""", language="python")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔁 The Full Monitoring → Retraining Loop</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline">
      <span class="pipe-step active">🤖 Model Predicts</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📋 Actuals Recorded</span><span class="pipe-arrow">→</span>
      <span class="pipe-step active">📡 RMSE Computed</span><span class="pipe-arrow">→</span>
      <span class="pipe-step danger">RMSE &gt; Threshold?</span><span class="pipe-arrow">→</span>
      <span class="pipe-step warn">🔄 Retrain Pipeline</span><span class="pipe-arrow">→</span>
      <span class="pipe-step good">✅ Evaluate New Model</span><span class="pipe-arrow">→</span>
      <span class="pipe-step good">🚀 Deploy if Better ↺</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Retraining History</div>', unsafe_allow_html=True)
    retrain_events = [
        ("2024-01-10","v1.0", 95.4, None,              "n/a",   "Initial training — baseline established",            "ok"),
        ("2024-02-15","v2.0", 95.4, 78.2,              "+17.2", "Scheduled monthly retrain · deployed",               "ok"),
        ("2024-03-01","v2.1", 78.2, 72.1,              "+6.1",  "Drift alert (RMSE=98.3) triggered · deployed",       "ok"),
        ("2024-04-01","v2.1", 72.1, 74.8,              "-2.7",  "Scheduled retrain · NOT deployed (new was worse)",   "warn"),
        ("2024-04-20","v3.0", 72.1, 65.8,              "+6.3",  "Drift alert (RMSE=91.0) triggered · deployed",       "ok"),
        ("2024-06-03","v3.2", 65.8, round(cur_rmse,1), f"+{65.8-cur_rmse:.1f}", "Scheduled retrain · deployed",      "ok"),
    ]
    log_html = ""
    for date, ver, before, after, delta, reason, status in retrain_events:
        cls    = "log-ok" if status == "ok" else "log-warn"
        symbol = "✅" if status == "ok" else "⚠️"
        after_s = str(after) if after else "—"
        log_html += (f'<span class="log-ts">{date}</span>  <span class="log-ts">[{ver}]</span>  '
                     f'<span class="{cls}">{symbol}</span>  '
                     f'RMSE: {before} → <b style="color:#f1f5f9">{after_s}</b>  ({delta} units)  · {reason}<br>')
    st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:2.5rem; padding-top:1.2rem;
            border-top:1px solid rgba(255,255,255,0.06);
            display:flex; justify-content:space-between; align-items:center;
            font-family:'JetBrains Mono',monospace; font-size:.68rem; color:#1e293b;">
  <span>⚡ CloudPulse · Milestone 4 · Regions: US-East, US-West, India-West, India-South · Services: Compute, Storage</span>
  <span>{len(df):,} records · RMSE {cur_rmse:.1f} · {datetime.now().strftime('%H:%M:%S UTC')}</span>
</div>
""", unsafe_allow_html=True)
