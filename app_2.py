import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. KONFIGURASI HALAMAN & CLEAN LIGHT THEME CSS ---
st.set_page_config(
    page_title="Sustainable Optimization Dashboard - EPMS & AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* SIDEBAR CLEAN WHITE */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #334155 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
        color: #0284C7 !important;
    }

    /* Top Metric KPI Card */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .kpi-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .kpi-val {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0284C7;
        margin: 4px 0 2px 0;
    }
    .kpi-unit { font-size: 0.85rem; color: #64748B; font-weight: 600; }
    .kpi-sub { font-size: 0.72rem; color: #94A3B8; }
    
    /* PFD Live Container */
    .pfd-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .pfd-header {
        font-size: 0.88rem;
        font-weight: 700;
        color: #0284C7;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .node-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 8px;
    }
    .node-title { font-size: 0.75rem; font-weight: 700; color: #0369A1; }
    .node-val { font-size: 0.85rem; font-weight: 700; color: #0F172A; }
    .node-sub { font-size: 0.70rem; color: #64748B; }
    
    /* Advice Card */
    .advice-card {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #0284C7;
        border-radius: 8px;
        padding: 14px;
        margin-top: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .advice-title { font-size: 0.82rem; font-weight: 800; color: #0369A1; }
    .advice-text { font-size: 0.78rem; color: #1E293B; margin-top: 4px; line-height: 1.4; }
    
    /* Equipment Profile Card */
    .eq-profile-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        font-size: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .eq-tag { font-weight: 800; color: #0284C7; font-size: 0.82rem; }
    .badge-online { background-color: #DCFCE7; color: #15803D; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; }
    .badge-offline { background-color: #FFE4E6; color: #BE123C; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; }
    
    /* Flow Step */
    .flow-step {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 8px 10px;
        text-align: center;
        font-size: 0.72rem;
        font-weight: 600;
        color: #334155;
    }
    
    /* KOTAK NARASI PUTIH BERSIH & KONTRAST TINGGI */
    .narrative-box {
        background-color: #FFFFFF !important;
        border: 1px solid #BAE6FD !important;
        border-left: 6px solid #0284C7 !important;
        padding: 16px 20px !important;
        border-radius: 8px !important;
        margin-top: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    .narrative-box h4 {
        color: #0369A1 !important;
        margin-top: 0px !important;
        margin-bottom: 10px !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
    }
    .narrative-box ul {
        color: #334155 !important;
        margin-bottom: 0px !important;
        padding-left: 20px !important;
    }
    .narrative-box li {
        color: #334155 !important;
        margin-bottom: 8px !important;
        line-height: 1.6 !important;
        font-size: 0.88rem !important;
    }
    .narrative-box b, .narrative-box strong {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    .narrative-box code {
        background-color: #F1F5F9 !important;
        color: #BE185D !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
    }

    /* Chart Outer Box */
    .chart-wrapper {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL PLOTLY STYLING (CLEAN WHITE ENTERPRISE THEME) ---
def apply_light_theme(fig, title_text=""):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#0F172A", family="Segoe UI, sans-serif"),
        title=dict(
            text=f"<b>{title_text}</b>" if title_text else "",
            font=dict(color="#0284C7", size=13.5),
            x=0.02, y=0.95
        ),
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#475569", size=10),
            title_font=dict(color="#334155", size=11),
            linecolor="#CBD5E1"
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#475569", size=10),
            title_font=dict(color="#334155", size=11),
            linecolor="#CBD5E1"
        ),
        legend=dict(
            font=dict(color="#334155", size=10),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        ),
        margin=dict(l=25, r=25, t=40, b=25)
    )
    return fig

# Mini-Sparkline Generator (Light Mode)
def create_sparkline(data_points, color="#0284C7"):
    fig = go.Figure(go.Scatter(y=data_points, mode='lines', line=dict(color=color, width=2.0), hoverinfo='skip'))
    fig.update_layout(
        height=32, margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF'
    )
    return fig

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h3 style='color:#0284C7; margin-bottom:0;'>⚡ H-UTB</h3>", unsafe_allow_html=True)
    st.caption("EPMS + AI OPTIMIZATION")
    st.divider()
    
    menu = st.radio(
        "NAVIGATION MENU",
        ["🏠 HOME", "📊 OVERVIEW", "⚙️ EQUIPMENT", "⚡ ENERGY", "🌱 EMISSIONS", "🎯 OPTIMIZATION", "🔮 PREDICTION", "⚠️ ALERTS"],
        index=0
    )
    
    st.divider()
    st.markdown("""
    <div style="background:#F8FAFC; padding:12px; border-radius:6px; border:1px solid #E2E8F0; font-size:0.75rem;">
        <b style="color:#0284C7;">Priatna Ahmad</b><br>
        <span style="color:#64748B;">Optimization Engineer</span><br><br>
        <b style="color:#475569;">Department:</b> Energy Optimization<br>
        <b style="color:#475569;">Location:</b> Jambaran - Tiung Biru<br>
        <b style="color:#475569;">Role:</b> Engineer<br>
        <b style="color:#475569;">Access Level:</b> Full Access<br>
        <b style="color:#475569;">Status:</b> <span style="color:#16A34A; font-weight:bold;">● Online</span>
    </div>
    """, unsafe_allow_html=True)

# Top Bar Header
head_col1, head_col2 = st.columns([7, 3])
with head_col1:
    st.markdown(f"<h3 style='margin-bottom:0; color:#0F172A; font-weight:800;'>SUSTAINABLE OPTIMIZATION DASHBOARD — {menu}</h3>", unsafe_allow_html=True)
    st.markdown("<span style='color:#64748B; font-size:0.85rem; font-weight:600;'>Dynamic Data Driven Decision • Gas Processing Facility</span>", unsafe_allow_html=True)
with head_col2:
    st.markdown("""
    <div style='text-align:right; font-size:0.82rem; color:#64748B;'>
        <b style='color:#0F172A;'>13/08/2026 14:45:00</b> (UTC+7) &nbsp; 
        <span style='background:#EF4444; color:#FFF; padding:2px 6px; border-radius:10px; font-weight:bold; font-size:0.75rem;'>3 Active Alerts</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# MENU 1: HOME
# ==============================================================================
if menu == "🏠 HOME":
    # 6 Scorecards Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">TOTAL POWER PRODUCED</div><div class="kpi-val">11,588 <span class="kpi-unit">kW</span></div><div class="kpi-sub">Actual &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Target 12,000 kW</div></div>""", unsafe_allow_html=True)
        st.plotly_chart(create_sparkline([11400, 11520, 11480, 11550, 11588], "#0284C7"), use_container_width=True, key="spk1")
    with m2:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">TOTAL STEAM GENERATED</div><div class="kpi-val">137.3 <span class="kpi-unit">klb/hr</span></div><div class="kpi-sub">Actual &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Target 140.0 klb/hr</div></div>""", unsafe_allow_html=True)
        st.plotly_chart(create_sparkline([136.5, 137.0, 136.8, 137.2, 137.3], "#16A34A"), use_container_width=True, key="spk2")
    with m3:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">FUEL GAS CONSUMPTION</div><div class="kpi-val">4.61 <span class="kpi-unit">MMscfd</span></div><div class="kpi-sub">Actual &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Target 4.80 MMscfd</div></div>""", unsafe_allow_html=True)
        st.plotly_chart(create_sparkline([4.65, 4.62, 4.64, 4.60, 4.61], "#D97706"), use_container_width=True, key="spk3")
    with m4:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">CO₂ EMISSIONS</div><div class="kpi-val">25.0 <span class="kpi-unit">klb/hr</span></div><div class="kpi-sub">Actual &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Target &lt; 27.0 klb/hr</div></div>""", unsafe_allow_html=True)
        st.plotly_chart(create_sparkline([25.4, 25.2, 25.3, 25.1, 25.0], "#DC2626"), use_container_width=True, key="spk4")
    with m5:
        st.markdown("""<div class="kpi-card"><div class="kpi-title">OPERATING COST</div><div class="kpi-val">$ 68,540 <span class="kpi-unit">/hr</span></div><div class="kpi-sub">Actual &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Target $ 72,000 /hr</div></div>""", unsafe_allow_html=True)
        st.plotly_chart(create_sparkline([69200, 68900, 68700, 68600, 68540], "#6366F1"), use_container_width=True, key="spk5")
    with m6:
        fig_opt = go.Figure(go.Pie(values=[92.4, 7.6], hole=0.75, marker=dict(colors=["#16A34A", "#E2E8F0"]), textinfo='none', hoverinfo='none'))
        fig_opt.update_layout(height=75, width=75, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF')
        col_opt_t, col_opt_g = st.columns([6, 4])
        with col_opt_t:
            st.markdown("""<div style="padding-top:4px;"><div class="kpi-title">OVERALL OPTIMIZATION</div><div class="kpi-val" style="color:#16A34A; font-size:1.35rem;">92.4 %</div><div class="kpi-sub">SQP = 1 (Good)</div></div>""", unsafe_allow_html=True)
        with col_opt_g:
            st.plotly_chart(fig_opt, use_container_width=True, key="pie_opt")

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    # Middle Section (PFD Live + Advice)
    col_pfd, col_ai = st.columns([6.8, 3.2])
    with col_pfd:
        st.markdown("""
        <div class="pfd-container">
            <div class="pfd-header"><span>PLANT OVERVIEW (LIVE)</span><span style="font-size:0.7rem; background:#DCFCE7; color:#15803D; padding:2px 8px; border-radius:4px; font-weight:bold;">Auto Refresh ON</span></div>
        """, unsafe_allow_html=True)
        pfd_c1, pfd_c2, pfd_c3 = st.columns([3.2, 3.4, 3.4])
        with pfd_c1:
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-bottom:6px;'>GAS TURBINES</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="node-box"><div class="node-title">420-CG9201 <span style="color:#16A34A; float:right;">●</span></div><div class="node-val">5,888 kW</div><div class="node-sub">2.29 MMscfd</div></div>
            <div class="node-box"><div class="node-title">420-CG9301 <span style="color:#16A34A; float:right;">●</span></div><div class="node-val">5,700 kW</div><div class="node-sub">2.32 MMscfd</div></div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-top:14px; margin-bottom:6px;'>STEAM GENERATION</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="node-box">
                <div class="node-title">MP Boiler 410-F9101: <b style="color:#0F172A;">6.8 klb/hr</b></div>
                <div class="node-title">MP Boiler 410-F9201: <b style="color:#0F172A;">19.8 klb/hr</b></div>
                <div class="node-title">AGI WHB (321): <b style="color:#0F172A;">43.0 klb/hr</b></div>
                <div class="node-title">MPI WHB (460): <b style="color:#0F172A;">67.7 klb/hr</b></div>
            </div>
            """, unsafe_allow_html=True)
        with pfd_c2:
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-bottom:6px;'>POWER BUS</div>", unsafe_allow_html=True)
            st.markdown("""<div class="node-box" style="border-color:#BAE6FD; background:#F0F9FF; text-align:center;"><span style="font-size:1.2rem;">⚡</span><div class="node-val" style="color:#0284C7; font-size:1.1rem;">11,588 kW</div><div class="node-sub">Load 78.2 %</div></div>""", unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-top:14px; margin-bottom:6px;'>STEAM HEADER (MP)</div>", unsafe_allow_html=True)
            st.markdown("""<div class="node-box" style="border-color:#FED7AA; background:#FFF7ED;"><div class="node-val" style="color:#EA580C; font-size:1.05rem;">♨️ 137.3 klb/hr</div><div style="font-size:0.7rem; color:#475569; margin-top:4px;">Pressure: <b>35.2 barg</b><br>Temp: <b>390 °C</b></div></div>""", unsafe_allow_html=True)
        with pfd_c3:
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-bottom:6px;'>ELECTRIC MOTORS (MAJOR)</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem; background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                <div>⚙️ 211-PM9004 &nbsp;&nbsp;&nbsp; <span style="color:#16A34A; font-weight:bold;">On</span> &nbsp;&nbsp; 450 kW</div>
                <div>⚙️ 223-PM9002A &nbsp; <span style="color:#16A34A; font-weight:bold;">On</span> &nbsp;&nbsp; 315 kW</div>
                <div>⚙️ 232-PM9006 &nbsp;&nbsp;&nbsp; <span style="color:#16A34A; font-weight:bold;">On</span> &nbsp;&nbsp; 280 kW</div>
                <div>⚙️ 460-EM9101 &nbsp;&nbsp;&nbsp; <span style="color:#16A34A; font-weight:bold;">On</span> &nbsp;&nbsp; 210 kW</div>
                <span style="color:#64748B; font-size:0.68rem;">... 24 more running</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#475569; margin-top:10px; margin-bottom:6px;'>PROCESS UNITS (KEY)</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem; background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                <div>💧 Inlet Separation (221) <span style="color:#16A34A; float:right; font-weight:bold;">Stable</span></div>
                <div>⚗️ Cond. Stabilization (232) <span style="color:#16A34A; float:right; font-weight:bold;">Stable</span></div>
                <div>💨 Vapor Recovery (224) <span style="color:#16A34A; float:right; font-weight:bold;">Stable</span></div>
                <div>🔶 Sulfur Recovery (321) <span style="color:#16A34A; float:right; font-weight:bold;">Stable</span></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ai:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:0.80rem; font-weight:700; color:#0284C7; margin-bottom:8px;">AI PREDICTION <span style="color:#64748B; font-weight:normal;">(Next 60 min)</span></div>
            <table style="width:100%; font-size:0.72rem; color:#334155; border-collapse:collapse;">
                <tr style="color:#64748B; border-bottom:1px solid #E2E8F0;"><th align="left">Parameter</th><th align="right">Current</th><th align="right">Predicted</th><th align="center">Trend</th></tr>
                <tr><td>Power Demand</td><td align="right">11,588 kW</td><td align="right">12,150 kW</td><td align="center" style="color:#16A34A;">▲</td></tr>
                <tr><td>Steam Demand</td><td align="right">137.3 klb/hr</td><td align="right">142.2 klb/hr</td><td align="center" style="color:#16A34A;">▲</td></tr>
                <tr><td>Fuel Gas Use</td><td align="right">4.61 MMscfd</td><td align="right">4.90 MMscfd</td><td align="center" style="color:#16A34A;">▲</td></tr>
                <tr><td>CO₂ Emission</td><td align="right">25.0 klb/hr</td><td align="right">26.1 klb/hr</td><td align="center" style="color:#DC2626;">▲</td></tr>
                <tr><td>Operating Cost</td><td align="right">$68,540/hr</td><td align="right">$69,820/hr</td><td align="center" style="color:#DC2626;">▲</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="advice-card">
            <div class="advice-title">💡 OPTIMIZATION ADVICE <span style="float:right; background:#FEF3C7; color:#B45309; padding:1px 6px; border-radius:3px; font-size:0.65rem; font-weight:bold;">High Impact</span></div>
            <div class="advice-text"><b>Recommended Action:</b><br>Increase loading on <b>420-CG9201 by 300 kW</b> and reduce <b>420-CG9301 by 300 kW</b> to minimize fuel gas cost and CO₂ emission.</div>
            <div style="margin-top:8px; padding-top:8px; border-top:1px dashed #BAE6FD; font-size:0.72rem; display:flex; justify-content:space-between;">
                <div>Cost Saving:<br><b style="color:#16A34A;">$ 1,280 /hr</b></div>
                <div>Fuel Gas Saving:<br><b style="color:#16A34A;">0.18 MMscfd</b></div>
                <div>CO₂ Reduction:<br><b style="color:#16A34A;">0.6 klb/hr</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Narasi Rekayasa Proses Home
    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Dynamic Operational Status & Optimasi Sistem</h4>
        <ul>
            <li><b>Kondisi Operasi Fasilitas:</b> Pembangkitan listrik beroperasi stabil pada beban <b>11,588 kW (78.2% Load)</b>[cite: 1] dengan pasokan utama dari GTG <code>420-CG9201</code> dan <code>420-CG9301</code>[cite: 1]. Kebutuhan uap pabrik sebesar <b>137.3 klb/hr</b>[cite: 1] disuplai secara terintegrasi melalui pembakaran gas pada Fired Boilers (Unit 410)[cite: 1] serta pemulihan panas buang (*heat recovery*) dari Insinerator AGI (321) dan MPI (460)[cite: 1].</li>
            <li><b>Strategi Solver SQP:</b> Algoritma optimasi non-linear berhasil mencapai status konvergensi <b>GOOD SOLUTION (SQP Level 1)</b>[cite: 1], menghasilkan skor optimasi keseluruhan sebesar <b>92.4%</b>[cite: 1]. Beban MP Boiler <code>410-F9101</code> dialihkan sebesar <b>3.54 klb/hr</b> ke Boiler <code>410-F9201</code> untuk menekan konsumsi bahan bakar total hingga <b>20.38 kscfd</b>[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    # Dynamic Profiles & Health Summary
    eq1, eq2, eq3, eq4, eq5 = st.columns([2.3, 2.3, 2.3, 2.1, 2.0])
    with eq1:
        st.markdown("""<div class="eq-profile-card"><div class="eq-tag">410-F9101 <span style="color:#64748B; font-weight:normal;">MP BOILER</span> <span class="badge-online" style="float:right;">Online</span></div><div style="margin-top:6px; color:#334155;">Steam Flow: <b>6.8 klb/hr</b><br>Fuel Gas: <b>0.24 MMscfd</b><br>Efficiency: <b style="color:#16A34A;">87.6 %</b><br>Stack Temp: <b>248 °C</b><br>O₂ Excess: <b style="color:#0284C7;">3.2 %</b></div></div>""", unsafe_allow_html=True)
    with eq2:
        st.markdown("""<div class="eq-profile-card"><div class="eq-tag">420-CG9201 <span style="color:#64748B; font-weight:normal;">GAS TURBINE</span> <span class="badge-online" style="float:right;">Online</span></div><div style="margin-top:6px; color:#334155;">Power: <b>5,888 kW</b><br>Heat Rate: <b>16,107 Btu/kWh</b><br>Fuel Gas: <b>2.29 MMscfd</b><br>Efficiency: <b style="color:#16A34A;">29.4 %</b><br>Exhaust Temp: <b>482 °C</b></div></div>""", unsafe_allow_html=True)
    with eq3:
        st.markdown("""<div class="eq-profile-card"><div class="eq-tag">223-PM9002A <span style="color:#64748B; font-weight:normal;">MOTOR</span> <span class="badge-online" style="float:right;">Online</span></div><div style="margin-top:6px; color:#334155;">Power: <b>315 kW</b><br>Speed: <b>1,780 rpm</b><br>Current: <b>62 A</b><br>Vibration: <b style="color:#16A34A;">2.1 mm/s</b><br>Status: <b>Running 100%</b></div></div>""", unsafe_allow_html=True)
    with eq4:
        st.markdown("""<div class="eq-profile-card"><div class="eq-tag">232-EM9003A <span style="color:#64748B; font-weight:normal;">PUMP MOTOR</span> <span class="badge-offline" style="float:right;">Offline</span></div><div style="margin-top:6px; color:#64748B;">Power: <b>- kW</b><br>Speed: <b>- rpm</b><br>Current: <b>- A</b><br>Vibration: <b>- mm/s</b><br>Status: <b style="color:#64748B;">Standby Ready</b></div></div>""", unsafe_allow_html=True)
    with eq5:
        fig_health = go.Figure(go.Pie(
            labels=["Good", "Warning", "Critical", "Offline"],
            values=[46, 18, 6, 8], hole=0.7,
            marker=dict(colors=["#16A34A", "#F59E0B", "#EF4444", "#94A3B8"]),
            textinfo='none', hoverinfo='label+value'
        ))
        fig_health.update_layout(height=90, width=90, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF')
        col_h_pie, col_h_txt = st.columns([5, 5])
        with col_h_pie:
            st.plotly_chart(fig_health, use_container_width=True, key="pie_health")
        with col_h_txt:
            st.markdown("""<div style="font-size:0.68rem; line-height:1.3; margin-top:5px;"><b style="font-size:0.85rem; color:#0F172A;">78 TOTAL</b><br><span style="color:#16A34A;">● Good: 46</span><br><span style="color:#F59E0B;">● Warn: 18</span><br><span style="color:#EF4444;">● Crit: 6</span><br><span style="color:#94A3B8;">● Off: 8</span></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:10px 14px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="font-size:0.75rem; font-weight:800; color:#64748B; margin-bottom:8px;">DYNAMIC DATA DRIVEN DECISION FLOW</div>
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <div class="flow-step" style="flex:1;">📡 <b>REAL TIME DATA</b><br><span style="font-size:0.65rem; color:#64748B;">Sensors / DCS / Historian</span></div>
            <div style="color:#0284C7; font-weight:bold;">➔</div>
            <div class="flow-step" style="flex:1;">🔮 <b>AI PREDICTION</b><br><span style="font-size:0.65rem; color:#64748B;">Forecast Future Condition</span></div>
            <div style="color:#0284C7; font-weight:bold;">➔</div>
            <div class="flow-step" style="flex:1; border-color:#0284C7; background:#F0F9FF;">⚡ <b>H-SGOF OPTIMIZATION</b><br><span style="font-size:0.65rem; color:#0284C7; font-weight:bold;">Economic & Sustainable Optimum</span></div>
            <div style="color:#0284C7; font-weight:bold;">➔</div>
            <div class="flow-step" style="flex:1;">🎛️ <b>APC / MPC</b><br><span style="font-size:0.65rem; color:#64748B;">Advanced Process Control</span></div>
            <div style="color:#0284C7; font-weight:bold;">➔</div>
            <div class="flow-step" style="flex:1;">⚙️ <b>EXECUTION</b><br><span style="font-size:0.65rem; color:#64748B;">Plant Operation</span></div>
            <div style="color:#0284C7; font-weight:bold;">➔</div>
            <div class="flow-step" style="flex:1;">📈 <b>LEARN & IMPROVE</b><br><span style="font-size:0.65rem; color:#64748B;">Continuous Learning</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 2: OVERVIEW
# ==============================================================================
elif menu == "📊 OVERVIEW":
    st.subheader("📊 Gas Processing Facility Macro Overview")
    
    col_ov1, col_ov2 = st.columns([6, 4])
    with col_ov1:
        df_units = pd.DataFrame({
            "Unit": ["Unit 211 (Wellpad)", "Unit 221 (Separation)", "Unit 232 (Stabilizer)", "Unit 234 (Refrig)", "Unit 241 (AGRU)", "Unit 242 (CO2)", "Unit 260 (Sales Gas)", "Unit 321 (AGI)", "Unit 322 (AGEU)", "Unit 410 (Steam)", "Unit 420 (Power)"],
            "Load_MMscfd": [100.0, 98.5, 95.0, 92.0, 88.5, 85.0, 79.75, 4.5, 12.0, 137.3, 11.59],
            "Health_Score": [98, 95, 92, 90, 88, 94, 96, 85, 89, 91, 95]
        })
        fig_u = px.bar(df_units, x="Unit", y="Health_Score", color="Health_Score", color_continuous_scale="Blues", text="Health_Score")
        fig_u = apply_light_theme(fig_u, "Indeks Kesehatan Operasional per Sub-Unit Proses (%)")
        fig_u.update_layout(height=380)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(fig_u, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ov2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <h4 style="color:#0284C7; margin-top:0;">🔍 Ringkasan Status Fasilitas</h4>
            <p style="color:#334155; font-size:0.85rem;">• <b>Sales Gas Flow:</b> <span style="color:#16A34A; font-weight:bold;">79.75 MMSCFD</span> (100% Target Penjualan Tercapai)[cite: 1]</p>
            <p style="color:#334155; font-size:0.85rem;">• <b>Keandalan Kelistrikan:</b> <span style="color:#0284C7; font-weight:bold;">11.59 MW</span> disuplai oleh GTG 9201 & 9301 secara stabil[cite: 1].</p>
            <p style="color:#334155; font-size:0.85rem;">• <b>Status Optimasi SQP:</b> <span style="color:#16A34A; font-weight:bold;">Konvergen (Level 1)</span> dengan efisiensi pembebanan 92.4%[cite: 1].</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.dataframe(df_units, use_container_width=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Evaluasi Kinerja Makro Fasilitas</h4>
        <ul>
            <li><b>Kapasitas Pengolahan Hulu-ke-Hilir:</b> Gas mentah dari Wellpad (Unit 211) diproses melalui Separasi (221), AGRU (241), Dehidrasi/Refrigerasi (234), dan CO₂ Removal (242) hingga menghasilkan gas jual spesifikasi pipa transmisi sebesar <b>79.75 MMSCFD</b>[cite: 1].</li>
            <li><b>Pemantauan Integritas Unit:</b> Rata-rata skor kesehatan fasilitas berada pada tingkat <b>92.1%</b>, dengan perhatian pemeliharaan preventif diprioritaskan pada unit termal bertemperatur tinggi seperti Acid Gas Incinerator (Unit 321) dan Boiler (Unit 410)[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 3: EQUIPMENT
# ==============================================================================
elif menu == "⚙️ EQUIPMENT":
    st.subheader("⚙️ Matriks Kesehatan & Status Operasi Peralatan (78 Total Units)")
    
    eq_filter = st.selectbox("Pilih Kategori Peralatan:", ["Semua", "Gas Turbines", "Boilers & Burners", "Pumps & Motors", "Compressors"])
    
    df_eq_list = pd.DataFrame([
        {"Tag": "420-CG9101", "Category": "Gas Turbines", "Area": "Unit 420", "Status": "Standby", "Vibration": 0.5, "Health": "Good"},
        {"Tag": "420-CG9201", "Category": "Gas Turbines", "Area": "Unit 420", "Status": "Running", "Vibration": 2.3, "Health": "Good"},
        {"Tag": "420-CG9301", "Category": "Gas Turbines", "Area": "Unit 420", "Status": "Running", "Vibration": 3.8, "Health": "Warning"},
        {"Tag": "260-CG9101", "Category": "Gas Turbines", "Area": "Unit 260", "Status": "Running", "Vibration": 2.1, "Health": "Good"},
        {"Tag": "410-F9101", "Category": "Boilers & Burners", "Area": "Unit 410", "Status": "Running", "Vibration": 1.2, "Health": "Warning"},
        {"Tag": "410-F9201", "Category": "Boilers & Burners", "Area": "Unit 410", "Status": "Running", "Vibration": 1.5, "Health": "Good"},
        {"Tag": "223-PM9002A", "Category": "Pumps & Motors", "Area": "Unit 223", "Status": "Running", "Vibration": 2.1, "Health": "Good"},
        {"Tag": "223-PM9002B", "Category": "Pumps & Motors", "Area": "Unit 223", "Status": "Standby", "Vibration": 0.0, "Health": "Offline"},
        {"Tag": "440-CM9301A", "Category": "Compressors", "Area": "Unit 440", "Status": "Running", "Vibration": 2.9, "Health": "Good"},
        {"Tag": "460-CM2101", "Category": "Compressors", "Area": "Unit 460", "Status": "Running", "Vibration": 4.6, "Health": "Critical"},
    ])
    
    if eq_filter != "Semua":
        df_eq_list = df_eq_list[df_eq_list['Category'] == eq_filter]
        
    st.dataframe(df_eq_list, use_container_width=True, height=360)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Keandalan Peralatan (Reliability & Health Matrix)</h4>
        <ul>
            <li><b>Distribusi Kondisi Mesin Berputar:</b> Dari 78 unit peralatan terdaftar, <b>46 unit (59%)</b> berada dalam kondisi *Good*, <b>18 unit (23%)</b> dalam status *Warning*, <b>6 unit (8%)</b> dalam status *Critical*, dan <b>8 unit (10%)</b> berstatus *Offline/Standby*.</li>
            <li><b>Anomali Terdeteksi:</b> Kompresor <code>460-CM2101</code> menunjukkan kenaikan level vibrasi hingga <b>4.6 mm/s</b> (status *Critical*), memerlukan inspeksi penyelarasan poros (*shaft alignment*) dan pelumasan bearing. Turbin gas <code>420-CG9301</code> beroperasi dengan sedikit degradasi efisiensi termal sehingga bebannya direkomendasikan untuk diturunkan sebesar 300 kW[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 4: ENERGY
# ==============================================================================
elif menu == "⚡ ENERGY":
    st.subheader("⚡ Neraca Energi Terintegrasi & Intensitas Spesifik")
    
    col_en1, col_en2 = st.columns([5, 5])
    with col_en1:
        fig_wf = go.Figure(go.Waterfall(
            name="Energi", orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["GTG (Unit 420)", "AGRU (Unit 241)", "Sales Gas (Unit 260)", "Pemulihan WHB", "Net Plant Energy"],
            y=[191.0, 79.4, 34.4, -126.0, 178.8],
            connector={"line": {"color": "#94A3B8"}},
            decreasing={"marker": {"color": "#16A34A"}},
            increasing={"marker": {"color": "#DC2626"}},
            totals={"marker": {"color": "#0284C7"}}
        ))
        fig_wf = apply_light_theme(fig_wf, "Neraca Aliran Energi (Waterfall - MMbtu/hr)")
        fig_wf.update_layout(height=360)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(fig_wf, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_en2:
        df_steam_pie = pd.DataFrame({
            "Source": ["Fired Boiler F9101", "Fired Boiler F9201", "AGI WHB (321)", "MPI WHB (460)"],
            "Steam_klb": [6.8, 19.8, 43.0, 67.7]
        })
        fig_st_pie = px.pie(df_steam_pie, names="Source", values="Steam_klb", hole=0.45, color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_st_pie = apply_light_theme(fig_st_pie, "Distribusi Sumber Steam (Total: 137.3 klb/hr)")
        fig_st_pie.update_layout(height=360)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(fig_st_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Neraca Aliran Panas & Pemulihan Energi</h4>
        <ul>
            <li><b>Tingkat Pemulihan Panas (Heat Recovery Rate):</b> Fasilitas memulihkan energi termal sebesar <b>126.0 MMbtu/hr (35.3%)</b>[cite: 1] dari gas buang insinerator untuk memproduksi <b>110.7 klb/hr uap</b>[cite: 1], secara masif mereduksi kebutuhan pembakaran bahan bakar tambahan pada boiler konvensional.</li>
            <li><b>Konsumen Energi Dominan:</b> Pembangkit GTG Unit 420 mengonsumsi <b>191.0 MMbtu/hr</b>[cite: 1], disusul oleh Unit 241 (AGRU) sebesar <b>79.4 MMbtu/hr</b>[cite: 1] untuk memenuhi panas laten regenerasi larutan amine pada reboiler.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 5: EMISSIONS
# ==============================================================================
elif menu == "🌱 EMISSIONS":
    st.subheader("🌱 Inventarisasi Emisi Cerobong & Simulasi Pajak Karbon")
    
    col_em1, col_em2 = st.columns([5, 5])
    with col_em1:
        o2_range = np.linspace(0.5, 12, 100)
        loss_unburned = 15.0 / (o2_range**1.5)
        loss_stack = 0.8 * o2_range + 5.0
        efficiency = 100 - (loss_unburned + loss_stack)
        
        fig_o2 = go.Figure()
        fig_o2.add_trace(go.Scatter(x=o2_range, y=efficiency, name="Efisiensi (%)", line=dict(color="#16A34A", width=3)))
        fig_o2.add_vline(x=3.2, line_dash="dash", line_color="#0284C7", annotation_text="Optimum O2 (3.2%)", annotation_font_color="#0284C7")
        fig_o2.add_vline(x=7.83, line_dash="dash", line_color="#DC2626", annotation_text="Aktual (7.83%)", annotation_font_color="#DC2626")
        
        fig_o2 = apply_light_theme(fig_o2, "Korelasi Excess O2 Cerobong vs Efisiensi Burner")
        fig_o2.update_layout(xaxis_title="Kadar O2 Cerobong (% Vol Dry)", yaxis_title="Efisiensi (LHV %)", height=350)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(fig_o2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_em2:
        tax_rate = st.slider("Tarif Pajak Karbon (USD / ton CO2):", 1.0, 50.0, 2.0)
        annual_co2_ton = 25.0 * 0.453592 * 8760 * 0.95
        annual_tax = annual_co2_ton * tax_rate
        
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:18px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <h4 style="color:#0284C7; margin-top:0;">📊 Proyeksi Pajak Karbon Tahunan</h4>
            <p style="color:#334155;">Total Emisi CO₂: <b style="color:#0F172A;">{annual_co2_ton:,.0f} ton/tahun</b>[cite: 1]</p>
            <p style="color:#334155;">Liabilitas Pajak: <b style="color:#DC2626;">${annual_tax:,.2f} /tahun</b></p>
            <p style="color:#334155;">Estimasi IDR: <b style="color:#D97706;">Rp {annual_tax*16000/1e9:,.2f} Miliar</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Pembakaran: Excess O₂ Sweet Spot & Pengendalian Emisi</h4>
        <ul>
            <li><b>Prinsip The Combustion Sweet Spot:</b> Pembakaran optimal dicapai saat kelebihan oksigen cerobong berada pada rentang <b>2.0% – 3.2% O₂</b>. Pada kondisi aktual Boiler <code>410-F9101</code> (O₂ = 7.83%)[cite: 1], volume udara pendingin parasitik menurunkan efisiensi termal ke 80.85%[cite: 1]. Mengoreksi O₂ trim ke 3.2% menaikkan efisiensi di atas 85%[cite: 1].</li>
            <li><b>Mitigasi Emisi Scope 1:</b> Emisi CO₂ cerobong fasilitas tercatat sebesar <b>25.0 klb/hr (~94,000 ton CO₂/tahun)</b>[cite: 1]. Optimasi re-balancing SQP memangkas emisi karbon sekitar <b>~440 ton/tahun</b>[cite: 1], secara simultan menurunkan beban pajak karbon perusahaan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 6: OPTIMIZATION
# ==============================================================================
elif menu == "🎯 OPTIMIZATION":
    st.subheader("🎯 Solver Optimasi Non-Linear (SQP) & Penghematan Finansial")
    
    col_opt1, col_opt2 = st.columns([6, 4])
    with col_opt1:
        df_opt_compare = pd.DataFrame({
            "Equipment": ["Boiler F9101 (klb/h)", "Boiler F9201 (klb/h)", "GTG 9201 (kW)", "GTG 9301 (kW)"],
            "Aktual": [10.34, 16.29, 5888, 5700],
            "Optimum_SQP": [6.80, 19.83, 6188, 5400]
        })
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=df_opt_compare["Equipment"], y=df_opt_compare["Aktual"], name="Aktual", marker_color="#DC2626"))
        fig_comp.add_trace(go.Bar(x=df_opt_compare["Equipment"], y=df_opt_compare["Optimum_SQP"], name="Optimum SQP", marker_color="#16A34A"))
        fig_comp = apply_light_theme(fig_comp, "Komparasi Beban Operasi: Aktual vs Target SQP")
        fig_comp.update_layout(barmode='group', height=330)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_opt2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <h4 style="color:#0284C7; margin-top:0;">🏷️ Shadow Prices (Marginal Cost)</h4>
            <p style="color:#334155;">• MP Steam: <b style="color:#0F172A;">$0.020192 / klb</b>[cite: 1]</p>
            <p style="color:#334155;">• Fuel Gas: <b style="color:#0F172A;">$0.009937 / MMBtu</b>[cite: 1]</p>
            <p style="color:#334155;">• Boiler Feed Water: <b style="color:#0F172A;">$0.009988 / klb</b>[cite: 1]</p>
            <hr style="border-color:#E2E8F0;">
            <p style="color:#16A34A; font-size:0.85rem;"><b>Estimasi Penghematan Bahan Bakar:</b><br>+20.38 kscfd (Setara $1,280 / jam dampak finansial)[cite: 1]</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Finansial: Logika Solver SQP & Shadow Pricing</h4>
        <ul>
            <li><b>Solusi Pembebanan Ekonomis:</b> Solver SQP mengarahkan peningkatan pembebanan pada unit dengan efisiensi marjinal tertinggi (Boiler <code>410-F9201</code> dinaikkan dari 16.29 ke 19.83 klb/hr)[cite: 1], menghasilkan penghematan bahan bakar gas gabungan sebesar <b>20.38 kscfd</b>[cite: 1].</li>
            <li><b>Analisis Shadow Price:</b> Nilai pengali Lagrange $\lambda$ menunjukkan biaya oportunitas marginal utilitas: memproduksi 1 klb steam ekstra bernilai <b>$0.0202</b>[cite: 1], sementara biaya energi bahan bakar bernilai <b>$0.0099/MMBtu</b>[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 7: PREDICTION
# ==============================================================================
elif menu == "🔮 PREDICTION":
    st.subheader("🔮 AI Load Demand Forecasting (Time-Series Projections)")
    
    t_steps = pd.date_range(start="2026-08-13 14:45:00", periods=24, freq='15min')
    power_pred = 11588 + 400 * np.sin(np.linspace(0, 3, 24)) + np.random.normal(0, 50, 24)
    steam_pred = 137.3 + 5 * np.sin(np.linspace(0, 3, 24)) + np.random.normal(0, 0.5, 24)
    
    df_forecast = pd.DataFrame({"Timestamp": t_steps, "Power_Demand_kW": power_pred, "Steam_Demand_klb": steam_pred})
    
    fig_fc = make_subplots(specs=[[{"secondary_y": True}]])
    fig_fc.add_trace(go.Scatter(x=df_forecast["Timestamp"], y=df_forecast["Power_Demand_kW"], name="Beban Listrik (kW)", line=dict(color="#0284C7", width=2.5)), secondary_y=False)
    fig_fc.add_trace(go.Scatter(x=df_forecast["Timestamp"], y=df_forecast["Steam_Demand_klb"], name="Kebutuhan Steam (klb/hr)", line=dict(color="#EA580C", width=2.5, dash='dot')), secondary_y=True)
    
    fig_fc = apply_light_theme(fig_fc, "Proyeksi Beban 6 Jam ke Depan (Feedforward AI)")
    fig_fc.update_layout(height=380)
    fig_fc.update_yaxes(title_text="Daya Listrik (kW)", secondary_y=False, gridcolor="#F1F5F9")
    fig_fc.update_yaxes(title_text="Steam (klb/hr)", secondary_y=True, gridcolor="#F1F5F9")
    
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(fig_fc, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Peramalan AI: Proaktif Feedforward Dispatching</h4>
        <ul>
            <li><b>Prediksi Kebutuhan Beban:</b> Model peramalan memproyeksikan kenaikan permintaan daya listrik dari <b>11,588 kW menuju 12,150 kW</b> dan kenaikan kebutuhan uap dari <b>137.3 klb/hr menuju 142.2 klb/hr</b> dalam 60 menit ke depan.</li>
            <li><b>Strategi Feedforward:</b> Dengan mengetahui tren beban di masa depan, sistem dapat merekomendasikan kenaikan *firing rate* pada boiler dan turbin gas secara bertahap dan mulus, mencegah terjadinya lonjakan konsumsi bahan bakar transien (*fuel spiking*) dan penurunan tekanan uap (*steam header pressure dip*).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MENU 8: ALERTS
# ==============================================================================
elif menu == "⚠️ ALERTS":
    st.subheader("⚠️ Sistem Deteksi Anomali & Alarm Aktif (3 Events Detected)")
    
    df_alerts = pd.DataFrame([
        {"Waktu": "14:43:10", "Tag": "410-F9101", "Severity": "High", "Deskripsi": "Boiler 410-F9101 stack temperature high (>245°C)", "Tindakan": "Koreksi rasio udara O2 trim"},
        {"Waktu": "14:40:22", "Tag": "420-CG9301", "Severity": "Medium", "Deskripsi": "GT 420-CG9301 efficiency degradation detected", "Tindakan": "Turunkan beban 300 kW ke GTG 9201"},
        {"Waktu": "14:39:00", "Tag": "SYSTEM", "Severity": "Info", "Deskripsi": "New SQP optimization iteration completed successfully", "Tindakan": "Tinjau rekomendasi setpoint baru"}
    ])
    
    st.dataframe(df_alerts, use_container_width=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Manajemen Alarm & Tindakan Mitigasi Cepat</h4>
        <ul>
            <li><b>High Severity - Boiler 410-F9101:</b> Temperatur cerobong melebihi batas desain (248°C vs batas 245°C) yang dipicu oleh excess air 7.83%[cite: 1]. Tindakan: Operator disarankan mengeksekusi penutupan damper FD Fan secara bertahap.</li>
            <li><b>Medium Severity - GTG 420-CG9301:</b> Terdeteksi kenaikan *heat rate* spesifik[cite: 1]. Tindakan: Melakukan *load shifting* sebesar 300 kW ke unit GTG 9201 sesuai panduan modul *Optimization Advice*[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.markdown("<center style='color:#64748B; font-size:0.75rem;'>EPMS & AI Digital Twin • Pertamina EP Cepu - Jambaran Tiung Biru</center>", unsafe_allow_html=True)