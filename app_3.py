import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- 1. KONFIGURASI HALAMAN & HIGH-CONTRAST CSS ---
st.set_page_config(
    page_title="Pertamina JTB - EPMS Digital Plant Dashboard V2",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS dengan High-Contrast Typography
st.markdown("""
    <style>
        .main { background-color: #0E1117; }
        
        /* Metric Card Header */
        .metric-card {
            background: linear-gradient(135deg, #1E2433 0%, #242C3D 100%);
            border: 1px solid #3B475D;
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }
        .metric-label { font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
        .metric-value { font-size: 1.6rem; color: #00E676; font-weight: 800; }
        .metric-sub { font-size: 0.78rem; color: #38BDF8; font-weight: 500; }
        
        /* KOTAK NARASI REKAYASA PROSES (HIGH CONTRAST) */
        .narrative-box {
            background-color: #172033 !important;
            border: 1px solid #2563EB !important;
            border-left: 6px solid #38BDF8 !important;
            padding: 18px 22px !important;
            border-radius: 8px !important;
            margin-top: 15px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35) !important;
        }
        .narrative-box h4 {
            color: #38BDF8 !important;
            margin-top: 0px !important;
            margin-bottom: 12px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }
        .narrative-box ul {
            color: #F1F5F9 !important;
            margin-bottom: 0px !important;
            padding-left: 20px !important;
        }
        .narrative-box li {
            color: #E2E8F0 !important;
            margin-bottom: 10px !important;
            line-height: 1.6 !important;
            font-size: 0.95rem !important;
        }
        .narrative-box b, .narrative-box strong {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        .narrative-box code {
            background-color: #0F172A !important;
            color: #F472B6 !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            font-weight: bold !important;
        }
        .narrative-box i {
            color: #93C5FD !important;
        }

        /* KOTAK NARASI BIAYA & FINANSIAL (HIGH CONTRAST GREEN) */
        .cost-box {
            background-color: #122820 !important;
            border: 1px solid #16A34A !important;
            border-left: 6px solid #4ADE80 !important;
            padding: 18px 22px !important;
            border-radius: 8px !important;
            margin-top: 15px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35) !important;
        }
        .cost-box h4 {
            color: #4ADE80 !important;
            margin-top: 0px !important;
            margin-bottom: 12px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }
        .cost-box ul {
            color: #F1F5F9 !important;
            margin-bottom: 0px !important;
            padding-left: 20px !important;
        }
        .cost-box li {
            color: #E2E8F0 !important;
            margin-bottom: 10px !important;
            line-height: 1.6 !important;
            font-size: 0.95rem !important;
        }
        .cost-box b, .cost-box strong {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        .cost-box code {
            background-color: #064E3B !important;
            color: #FDE047 !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATASET MODEL STANDAR (FALLBACK BUILT-IN DATA) ---
def get_default_kpi():
    kpi_raw = [
        ("Unit 211", "211 - Wellpad Central", "MMscf/h", 1.0, "MMbtu/hr", 0.000091, "MMbtu/MMscf", 0.000091),
        ("Unit 212", "212 - Wellpad East", "MMscf/h", 1.0, "MMbtu/hr", 0.000091, "MMbtu/MMscf", 0.000091),
        ("Unit 221", "221 - Inlet Separation", "MMscf/h", 1.0, "MMbtu/hr", 0.000091, "MMbtu/MMscf", 0.000091),
        ("Unit 222", "222 - Produced Water", "Gal/h", 0.01, "MMbtu/hr", 0.000091, "Mmbtu/Gal", 0.00909),
        ("Unit 223", "223 - Condensate Storage", "bbl/h", 112.68, "MMbtu/hr", 0.504494, "MMbtu/bbl", 0.004477),
        ("Unit 224", "224 - Vapor Recovery", "MMscf/h", 1.0, "MMbtu/hr", 0.000091, "MMbtu/MMscf", 0.000091),
        ("Unit 232", "232 - Condensate Stabilizer", "MMscf/h", 1.0, "MMbtu/hr", 5.610775, "MMbtu/MMscf", 5.610775),
        ("Unit 234", "234 - Refrigeration (Dew Point)", "MMscf/h", 1.0, "MMbtu/hr", 2.676574, "MMbtu/MMscf", 2.676574),
        ("Unit 241", "241 - Acid Gas Removal (AGRU)", "MMscf/h", 1.0, "MMbtu/hr", 79.398943, "MMbtu/MMscf", 79.398943),
        ("Unit 242", "242 - CO2 Removal", "MMscf/h", 11.64, "MMbtu/hr", 0.150203, "MMbtu/MMscf", 0.012902),
        ("Unit 260", "260 - Sales Gas Compression", "MMscf/h", 8.01, "MMbtu/hr", 34.396458, "MMbtu/MMscf", 4.296297),
        ("Unit 321", "321 - Acid Gas Incin. (WHB)", "MMscf/h", 1.0, "MMbtu/hr", -47.187041, "MMbtu/MMscf", -47.187041),
        ("Unit 322", "322 - Acid Gas Enrichment", "MMscf/h", 1.50, "MMbtu/hr", 31.681884, "MMbtu/MMscf", 21.073265),
        ("Unit 323", "323 - Sulfuric Acid (SAU)", "MMscf/h", 59.98, "MMbtu/hr", 2.388857, "MMbtu/MMscf", 0.039827),
        ("Unit 410", "410 - BFW & Steam System", "Gal/h", 2035.02, "MMbtu/hr", -5.558954, "Mmbtu/Gal", -0.002732),
        ("Unit 420", "420 - Power Generation (GTG)", "kW", 11587.90, "MMbtu/hr", 191.007134, "MMbtu/kW-hr", 0.016483),
        ("Unit 430", "430 - Fuel System", "MMscf/h", 23.82, "MMbtu/hr", 0.0, "MMbtu/MMscf", 0.0),
        ("Unit 440", "440 - Air & N2 System", "MMscf/h", 1.0, "MMbtu/hr", 2.760278, "MMbtu/MMscf", 2.760278),
        ("Unit 450", "450 - Water Treatment", "Gal/h", 1.0, "MMbtu/hr", 0.303958, "Mmbtu/Gal", 0.303958),
        ("Unit 460", "460 - Permeate Incin. (WHB)", "MMscf/h", 1.0, "MMbtu/hr", -73.254446, "MMbtu/MMscf", -73.254446),
        ("Unit 470", "470 - Fuel Gas Dist.", "MMscf/h", 1.0, "MMbtu/hr", 0.0, "MMbtu/MMscf", 0.0),
        ("Unit 475", "475 - Flare System", "MMscf/h", 1.0, "MMbtu/hr", 9.762862, "MMbtu/MMscf", 9.762862),
        ("Unit 480", "480 - Diesel System", "bbl/h", 100.0, "MMbtu/hr", 0.0, "MMbtu/bbl", 0.0),
        ("Unit 510", "510 - Open Drain/Sewer", "Gal/h", 0.0, "MMbtu/hr", 0.059695, "Mmbtu/Gal", 0.0),
        ("Unit 520", "520 - Closed Drain", "Gal/h", 71853.63, "MMbtu/hr", 0.000091, "Mmbtu/Gal", 0.0),
        ("Unit 530", "530 - Wastewater (WWT)", "Gal/h", 71853.63, "MMbtu/hr", 0.474771, "Mmbtu/Gal", 0.000007),
        ("Unit 580", "580 - Bleed Water Treat.", "Gal/h", 1.0, "MMbtu/hr", 0.011881, "Mmbtu/Gal", 0.011881),
        ("Unit 590", "590 - Water Injection", "Gal/h", 85.14, "MMbtu/hr", 0.000091, "Mmbtu/Gal", 0.000001)
    ]
    return pd.DataFrame(kpi_raw, columns=[
        'Unit', 'Unit_Description', 'Load_Unit', 'Plant_Load', 
        'Energy_Unit', 'Energy_Consumption', 'Intensity_Unit', 'Energy_Intensity'
    ])

def get_default_motors():
    motor_list = [
        ("Condensate Storage (223)", "223-PM9002A", "On"),
        ("Condensate Storage (223)", "223-PM9002B", "Off"),
        ("Propylene Refrig. (234)", "234-EM9004-1A", "On"),
        ("Propylene Refrig. (234)", "234-EM9004-1B", "Off"),
        ("Propylene Refrig. (234)", "234-EM9004-2A", "On"),
        ("Propylene Refrig. (234)", "234-EM9017A", "On"),
        ("H2S Removal (241)", "241-EM9014-1A", "On"),
        ("H2S Removal (241)", "241-PM9011B", "On"),
        ("H2S Removal (241)", "241-PM9027A", "On"),
        ("CO2 Removal (242)", "242-EM9316A", "On"),
        ("Sales Gas Compr. (260)", "260-EM9118B", "On"),
        ("AG Enrichment (322)", "322-PM1003", "On"),
        ("AG Enrichment (322)", "322-PM2003", "On"),
        ("Sulfuric Acid (323)", "323-CM9401", "On"),
        ("Sulfuric Acid (323)", "323-PM9013B", "On"),
        ("BFW & Steam (410)", "410-PM9002A", "On"),
        ("BFW & Steam (410)", "410-PM9009A", "On"),
        ("Air & N2 (440)", "440-CM9301A", "On"),
        ("Air & N2 (440)", "440-CM9301B", "On"),
        ("Air & N2 (440)", "440-CM9301C", "On"),
        ("Water Treating (450)", "450-PM9004A", "On"),
        ("Water Treating (450)", "450-PM9104B", "On"),
        ("MPI Permeate (460)", "460-CM2101", "On"),
        ("Wastewater (530)", "530-CM9106B", "On"),
        ("Wastewater (530)", "530-PM9102A", "On")
    ]
    return pd.DataFrame(motor_list, columns=['Unit', 'Equipment_Tag', 'Status'])

# --- 3. LOADER DARI EXCEL JIKA ADA ---
@st.cache_data
def load_all_data(uploaded_file=None):
    file_path = "EPMS PertaminaJTB.xlsm"
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else ""
    abs_path = os.path.join(script_dir, file_path)
    target = uploaded_file if uploaded_file else (abs_path if os.path.exists(abs_path) else (file_path if os.path.exists(file_path) else None))
    
    if target:
        try:
            xls = pd.ExcelFile(target)
            df_kpi_raw = pd.read_excel(xls, 'Most Important KPIs')
            df_kpi = df_kpi_raw.iloc[8:37, [1, 2, 3, 4, 5, 6, 7]].copy()
            df_kpi.columns = ['Unit', 'Load_Unit', 'Plant_Load', 'Energy_Unit', 'Energy_Consumption', 'Intensity_Unit', 'Energy_Intensity']
            df_kpi = df_kpi[df_kpi['Unit'].astype(str).str.contains(r'Unit \d+', na=False)].copy()
            for col in ['Plant_Load', 'Energy_Consumption', 'Energy_Intensity']:
                df_kpi[col] = pd.to_numeric(df_kpi[col], errors='coerce').fillna(0)
            
            df_motors_raw = pd.read_excel(xls, 'Motors')
            df_motors = df_motors_raw.iloc[8:, 1:4].dropna(subset=[df_motors_raw.columns[2]])
            df_motors.columns = ['Unit', 'Equipment_Tag', 'Status']
            return df_kpi, df_motors, "File Excel Terhubung"
        except Exception:
            pass
            
    return get_default_kpi(), get_default_motors(), "Data Model Standar"

df_kpi_data, df_motors_data, source_status = load_all_data()

# --- 4. SIDEBAR & GLOBAL CONTROLS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pertamina_Logo.svg/1200px-Pertamina_Logo.svg.png", width=150)
    st.markdown("### **EPMS Pertamina JTB**")
    st.caption("Gas Processing Facility • Digital Twin V2.0")
    st.divider()
    
    st.info(f"📁 Status Data: **{source_status}**")
    st.success("● Solver Status: **GOOD SOLUTION**")
    st.caption("Algorithm: Sequential Quadratic Programming (SQP)[cite: 1]")
    st.caption("Timestamp: **2026-08-13 14:45:01**[cite: 1]")
    st.divider()

    st.markdown("#### **Parameter Biaya Dasar Utilitas**")
    st.caption("• **MP Steam:** $0.020192 / klb[cite: 1]")
    st.caption("• **Fuel Gas:** $0.009937 / MMBtu[cite: 1]")
    st.caption("• **BFW:** $0.009988 / klb[cite: 1]")

# --- 5. TOP EXECUTIVE KPI SCORECARDS ---
st.title("⚡ Gas Processing Facility - Energy & Plant Overview")
st.markdown("Pemantauan visual kondisi operasi pabrik *real-time* berbasis integrasi neraca massa, energi, efisiensi emisi, dan optimasi biaya[cite: 1].")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="metric-card"><div class="metric-label">Sales Gas Production</div><div class="metric-value">79.75 <span style="font-size:1rem;color:#94A3B8;">MMSCFD</span></div><div class="metric-sub">Kapasitas Penuh 100% Tercapai</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card"><div class="metric-label">Total Power Generation</div><div class="metric-value">11.59 <span style="font-size:1rem;color:#94A3B8;">MW</span></div><div class="metric-sub">GTG 420-CG9201 & CG9301 Running</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card"><div class="metric-label">Total Steam Generation</div><div class="metric-value">137.26 <span style="font-size:1rem;color:#94A3B8;">klb/hr</span></div><div class="metric-sub">80.6% Disuplai Uap Panas Buang (WHB)</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card"><div class="metric-label">Est. Fuel Gas Savings (SQP)</div><div class="metric-value">+20.38 <span style="font-size:1rem;color:#00E676;">kSCFD</span></div><div class="metric-sub">Potensi Re-balancing Beban Boiler</div></div>""", unsafe_allow_html=True)

# --- 6. TABS UTAMA V2.0 ---
tab_steam, tab_power, tab_eff, tab_cost, tab_carbon, tab_motors, tab_kpi = st.tabs([
    "♨️ Steam & Boilers", 
    "⚡ Kelistrikan & Gas Turbin", 
    "🔥 Efisiensi & Emisi", 
    "💰 Biaya & Optimasi Energi",
    "🌱 Pajak Karbon & NEK",
    "⚙️ Status Motor Peralatan",
    "📊 Intensitas Energi Unit"
])

# ================= TAB 1: STEAM & BOILERS =================
with tab_steam:
    st.subheader("♨️ Neraca Produksi Uap (Steam Balance) & Optimasi Pembebanan")
    st.markdown("Evaluasi pasokan uap tekanan menengah (*MP Steam*), kontribusi *Waste Heat Boilers*, dan pengalihan beban pembakaran boiler[cite: 1].")
    
    col_s1, col_s2 = st.columns([6, 4])
    with col_s1:
        boiler_data = pd.DataFrame({
            "Equipment": ["MP Boiler 410-F9101", "MP Boiler 410-F9201"],
            "Actual_Flow": [10.34, 16.29],
            "Optimum_Flow": [6.80, 19.83]
        })
        fig_steam = go.Figure()
        fig_steam.add_trace(go.Bar(x=boiler_data["Equipment"], y=boiler_data["Actual_Flow"], name="Steam Aktual (klb/hr)", marker_color="#29B6F6"))
        fig_steam.add_trace(go.Bar(x=boiler_data["Equipment"], y=boiler_data["Optimum_Flow"], name="Steam Target SQP (klb/hr)", marker_color="#00E676"))
        fig_steam.update_layout(title="<b>Optimasi Pembebanan MP Boilers (klb/hr)</b>", barmode="group", template="plotly_dark", height=340, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_steam, use_container_width=True)

    with col_s2:
        sources_df = pd.DataFrame({
            "Source": ["Boiler 410-F9101", "Boiler 410-F9201", "AGI WHB (Unit 321)", "MPI WHB (Unit 460)"],
            "Steam_klb_hr": [10.34, 16.29, 42.33, 68.29]
        })
        fig_pie_steam = px.pie(sources_df, names="Source", values="Steam_klb_hr", title="<b>Komposisi Pasokan Steam Pabrik (137.26 klb/hr)</b>", hole=0.45, template="plotly_dark")
        fig_pie_steam.update_layout(height=340, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_pie_steam, use_container_width=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Sistem Distribusi Uap & Logika Solver SQP</h4>
        <ul>
            <li><b>Dominasi Panas Buang (Heat Integration):</b> Sekitar <b>80.6% (110.62 klb/hr)</b> kebutuhan uap dipenuhi oleh <i>Waste Heat Boilers</i> pada Insinerator Permeat (460) dan Insinerator Gas Asam (321) tanpa memerlukan konsumsi fuel gas tambahan[cite: 1].</li>
            <li><b>Strategi Load Re-Balancing:</b> Solver SQP merekomendasikan pemindahan beban sebesar <b>3.54 klb/hr</b> dari Boiler <code>410-F9101</code> ke Boiler <code>410-F9201</code>[cite: 1].</li>
            <li><b>Justifikasi Termodinamika:</b> Karena kurva efisiensi marjinal Boiler <code>F9201</code> lebih unggul pada pembebanan tinggi, strategi ini mereduksi konsumsi bahan bakar total dari <b>0.7155 MMscfd</b> menjadi <b>0.6951 MMscfd</b>, menghemat <b>20.38 kscfd</b> fuel gas secara berkelanjutan[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 2: POWER GENERATION =================
with tab_power:
    st.subheader("⚡ Neraca Kelistrikan & Utilisasi Gas Turbin Generator")
    st.markdown("Monitoring daya Gas Turbine Generator (Unit 420), penggerak mekanik kompresor gas jual (Unit 260), dan profil beban motor[cite: 1].")
    
    col_p1, col_p2 = st.columns([5, 5])
    with col_p1:
        gt_df = pd.DataFrame({
            "Generator": ["420-CG9201", "420-CG9301", "260-CG9101", "420-CG9101 (Standby)"],
            "Power_kW": [5887.62, 5700.27, 4525.92, 0.01],
            "Status": ["Running (50.8%)", "Running (49.2%)", "Gas Compr Drive", "Hot Standby"]
        })
        fig_gt = px.bar(gt_df, x="Generator", y="Power_kW", color="Status", text="Power_kW", title="<b>Pembangkitan Daya Turbin Gas (kW)</b>", template="plotly_dark")
        fig_gt.update_traces(texttemplate='%{text:.1f} kW', textposition='outside')
        fig_gt.update_layout(height=340)
        st.plotly_chart(fig_gt, use_container_width=True)
        
    with col_p2:
        pwr_cons_df = pd.DataFrame({
            "Unit_Name": ["Unit 320 (Acid Gas)", "Unit 440 (Air & N2)", "Unit 234 (Refrig)", "Unit 223 (Condensate)", "Unit 530 (WWT)", "Unit 460 (MPI)", "Unit 410 (Steam)", "Unit 450 (Water)", "Lainnya"],
            "Power_kW": [519.31, 303.66, 285.49, 55.50, 52.23, 46.67, 41.77, 33.44, 15.35]
        })
        fig_cons = px.pie(pwr_cons_df, names="Unit_Name", values="Power_kW", title="<b>Distribusi Konsumsi Listrik Unit Operasi (~1.35 MW)</b>", template="plotly_dark", hole=0.4)
        fig_cons.update_layout(height=340)
        st.plotly_chart(fig_cons, use_container_width=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Sistem Kelistrikan Mandiri (Islanded Grid)</h4>
        <ul>
            <li><b>Pembangkitan Utama:</b> GTG <code>420-CG9201</code> (5.89 MW) dan <code>420-CG9301</code> (5.70 MW) beroperasi paralel menyuplai total daya <b>11.59 MW</b> dengan rata-rata <i>heat rate</i> ~16,480 Btu/kWh[cite: 1].</li>
            <li><b>Penggerak Kompresor:</b> Turbin <code>260-CG9101</code> membangkitkan daya mekanik mandiri <b>4,525.9 kW</b> khusus untuk kompresi gas jual menuju pipa transmisi[cite: 1].</li>
            <li><b>Keandalan & Spinning Reserve:</b> Total beban motor listrik aktif adalah <b>~1.35 MW</b> (didominasi Unit 320 dan Unit 440)[cite: 1]. Margin cadangan daya yang besar dipertahankan untuk menjaga kestabilan frekuensi dan meredam lonjakan arus (<i>starting inrush current</i>) pada motor-motor besar.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 3: EFFICIENCY & EMISSIONS =================
with tab_eff:
    st.subheader("🔥 Efisiensi Pembakaran Cerobong & Inventarisasi Emisi")
    st.markdown("Evaluasi efisiensi termal pembakaran, pemantauan *excess oxygen*, temperatur cerobong (*stack temp*), dan laju emisi $\\text{CO}_2$ / $\\text{SO}_2$[cite: 1].")
    
    col_e1, col_e2, col_e3 = st.columns([3.5, 3.5, 3])
    with col_e1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=80.85,
            delta={'reference': 85.94, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            title={'text': "<b>Efisiensi 410-F9101 (LHV %)</b><br><span style='font-size:0.8em;color:gray'>Target: 85.94%</span>"},
            gauge={'axis': {'range': [60, 100]}, 'bar': {'color': "#00E676"},
                   'steps': [{'range': [60, 75], 'color': "#D32F2F"}, {'range': [75, 85], 'color': "#FBC02D"}, {'range': [85, 100], 'color': "#388E3C"}]}
        ))
        fig_gauge.update_layout(height=260, template="plotly_dark", margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_e2:
        param_df = pd.DataFrame({
            "Equipment": ["410-F9101", "410-F9201", "460-V1100", "460-V2100"],
            "Excess_O2_pct": [7.83, 20.00, 20.00, 6.36]
        })
        fig_stack = px.bar(param_df, x="Equipment", y="Excess_O2_pct", text="Excess_O2_pct", title="<b>Excess O2 Cerobong (% Dry Basis)</b>", template="plotly_dark", color="Excess_O2_pct", color_continuous_scale="Reds")
        fig_stack.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_stack, use_container_width=True)

    with col_e3:
        st.markdown("#### **Parameter Kunci Emisi**")
        st.markdown("""
        * **Laju Flue Gas:** ~960 klb/hr[cite: 1]
        * **Total Emisi CO₂:** **35.65 klb/hr**[cite: 1]
        * **Total Emisi SO₂:** **0.0002 klb/hr**[cite: 1]
        * **Kontributor CO₂ Terbesar:** GTG Unit 420 (~70.1%)[cite: 1]
        """)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Efisiensi Pembakaran & Pengendalian Emisi</h4>
        <ul>
            <li><b>Analisis Excess Oxygen:</b> Boiler <code>410-F9101</code> beroperasi pada efisiensi <b>80.85%</b> dengan O₂ cerobong <b>7.83%</b> dan temperatur stack <b>537.9°F</b>[cite: 1]. Kelebihan udara pembakaran ini bertindak sebagai penyerap panas parasitik. Penyetelan <i>O₂ trim control</i> berpotensi menaikkan efisiensi hingga target <b>85.94%</b>[cite: 1], menghemat <b>0.855 MMbtu/hr</b> panas pembakaran[cite: 1].</li>
            <li><b>Inventarisasi Emisi Gas Buang:</b> Total emisi CO₂ fasilitas tercatat setara <b>~130,650 ton CO₂/tahun</b>[cite: 1]. Pembangkit GTG Unit 420 menyumbang <b>24.99 klb/hr</b> emisi CO₂[cite: 1]. Emisi SO₂ yang sangat rendah (0.0002 klb/hr) memvalidasi keandalan unit AGRU (241) dan Unit Asam Sulfat (323) dalam menangkap kandungan belerang[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 4: BIAYA & OPTIMASI ENERGI =================
with tab_cost:
    st.subheader("💰 Evaluasi Biaya Operasional Energi & Optimasi Finansial")
    st.markdown("Simulasi biaya bahan bakar, pemodelan harga riil gas bumi, analisis biaya marjinal (*Shadow Prices*), dan potensi penghematan tahunan[cite: 1].")
    
    # 1. Parameter Simulator Biaya Interaktif
    st.markdown("##### 🎛️ Simulator Sensitivitas Harga Energi (*What-If Simulator*)")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        sim_gas_price = st.number_input("Harga Gas Bumi ($ / MMBtu):", min_value=0.01, max_value=20.0, value=6.00, step=0.5,
                                        help="Harga nominal pemodelan: $0.01/MMBtu. Harga riil pasar industri (HGBT ESDM): $6.00 - $8.50/MMBtu.")
    with sc2:
        sim_diesel_price = st.number_input("Harga Solar Industri ($ / bbl):", min_value=10.0, max_value=200.0, value=110.0, step=5.0)
    with sc3:
        sim_bfw_price = st.number_input("Biaya Air Umpan BFW ($ / klb):", min_value=0.001, max_value=5.0, value=0.01, step=0.01)

    # 2. Perhitungan Biaya Aktual vs Optimum
    # Total Gas Consumed: Boilers (0.7155 MMscfd) + GTG (4.6107 MMscfd) + Sales Gas GT (0.8292 MMscfd) = 6.1554 MMscfd
    # 1 MMscf FG ~ 1030 MMBtu
    fg_mmbtu_day_actual = 6.1554 * 1030.0
    fg_mmbtu_day_optimum = (6.1554 - 0.02038) * 1030.0
    
    daily_cost_actual = (fg_mmbtu_day_actual * sim_gas_price) + (0.0187 * sim_diesel_price) + (137.26 * 24 * sim_bfw_price)
    daily_cost_optimum = (fg_mmbtu_day_optimum * sim_gas_price) + (0.0187 * sim_diesel_price) + (137.26 * 24 * sim_bfw_price)
    
    daily_savings = daily_cost_actual - daily_cost_optimum
    annual_savings = daily_savings * 365.0 * 0.95
    specific_cost_per_sales = daily_cost_actual / 79.75

    st.divider()

    # 3. Scorecards Finansial
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)
    with fcol1:
        st.metric("Total OPEX Energi Aktual", f"${daily_cost_actual:,.2f} /hari", f"${daily_cost_actual*365*0.95/1e6:,.2f} Juta/th")
    with fcol2:
        st.metric("Target OPEX Energi SQP", f"${daily_cost_optimum:,.2f} /hari", delta=f"-${daily_savings:,.2f} /hari", delta_color="normal")
    with fcol3:
        st.metric("Estimasi Penghematan Tahunan", f"${annual_savings:,.2f} /th", delta="Optimasi Pembebanan Boiler", delta_color="normal")
    with fcol4:
        st.metric("Specific Energy Cost", f"${specific_cost_per_sales:.2f} /MMSCF", help="Biaya energi per 1 MMSCF gas jual yang diproduksi.")

    st.divider()

    # 4. Grafik Finansial (Breakdown & Cost Walk Waterfall)
    col_fg1, col_fg2 = st.columns([5, 5])
    
    with col_fg1:
        cost_breakdown_df = pd.DataFrame({
            "Component": ["Fuel Gas GTG (Unit 420)", "Fuel Gas Compressor (Unit 260)", "Fuel Gas Boilers (Unit 410)", "BFW & Diesel"],
            "Cost_USD_Day": [
                4.6107 * 1030 * sim_gas_price,
                0.8292 * 1030 * sim_gas_price,
                0.7155 * 1030 * sim_gas_price,
                (0.0187 * sim_diesel_price) + (137.26 * 24 * sim_bfw_price)
            ]
        })
        fig_cost_pie = px.pie(
            cost_breakdown_df, names="Component", values="Cost_USD_Day",
            title="<b>Komposisi Biaya Energi Operasional Harian</b>",
            hole=0.45, template="plotly_dark"
        )
        fig_cost_pie.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cost_pie, use_container_width=True)

    with col_fg2:
        wf_cost_x = ["Biaya Aktual", "Re-balancing Boiler", "Optimasi O2 Trim", "Target OPEX SQP"]
        wf_cost_y = [daily_cost_actual, -daily_savings, -(74.9 * (sim_gas_price/0.01) / 100), daily_cost_optimum - (74.9 * (sim_gas_price/0.01) / 100)]
        
        fig_cost_wf = go.Figure(go.Waterfall(
            name="Cost Walk", orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=wf_cost_x, textposition="outside",
            text=[f"${abs(v):,.1f}" for v in wf_cost_y],
            y=wf_cost_y, connector={"line": {"color": "#90A4AE"}},
            decreasing={"marker": {"color": "#00E676"}},
            increasing={"marker": {"color": "#FF5252"}},
            totals={"marker": {"color": "#29B6F6"}}
        ))
        fig_cost_wf.update_layout(
            title="<b>Jembatan Penghematan Biaya (Cost Bridge - USD/Hari)</b>",
            template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_cost_wf, use_container_width=True)

    # 5. Display Narasi Rekayasa Biaya & Shadow Pricing
    st.markdown(f"""
    <div class="cost-box">
        <h4>📖 Narasi Rekayasa Finansial & Analisis Biaya Marjinal (Shadow Prices)</h4>
        <ul>
            <li><b>Sensitivitas Harga Pasar:</b> Pada harga acuan gas industri (<b>${sim_gas_price:.2f}/MMBtu</b>), penghematan bahan bakar gas sebesar <b>20.38 kscfd</b> setara dengan reduksi biaya sebesar <b>${annual_savings:,.2f} per tahun</b> murni melalui re-alokasi pembebanan boiler tanpa memerlukan investasi modal (CAPEX)[cite: 1].</li>
            <li><b>Interpretasi Shadow Prices (Pengali Lagrange SQP):</b>
                <ul>
                    <li><b>MP Steam ($0.020192 / klb):</b> Biaya marjinal internal untuk memproduksi tambahan 1.000 pon uap pada kondisi operasi saat ini[cite: 1].</li>
                    <li><b>Fuel Gas ($0.009937 / MMBtu):</b> Nilai ekonomi marjinal bahan bakar terhadap fungsi objektif biaya[cite: 1].</li>
                    <li><b>Boiler Feed Water ($0.009988 / klb):</b> Biaya pengolahan air demineralisasi untuk pembentukan uap[cite: 1].</li>
                </ul>
            </li>
            <li><b>Biaya Energi per Satuan Produk:</b> Fasilitas memerlukan biaya energi sebesar <b>${specific_cost_per_sales:.2f} per MMSCF</b> gas jual yang dialirkan ke pipa transmisi[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 5: PAJAK KARBON & NEK =================
with tab_carbon:
    st.subheader("🌱 Simulasi Nilai Ekonomi Karbon (NEK) & Pajak Karbon")
    st.markdown("Estimasi kewajiban pajak emisi langsung (*Scope 1*) fasilitas, mekanisme *Cap-and-Tax*, dan potensi reduksi biaya emisi[cite: 1].")
    
    col_c_ctrl1, col_c_ctrl2, col_c_ctrl3 = st.columns(3)
    with col_c_ctrl1:
        carbon_tax_rate = st.number_input("Tarif Pajak Karbon (USD / ton CO₂):", min_value=1.0, max_value=100.0, value=2.0, step=0.5, 
                                          help="Acuan regulasi UU HPP Indonesia ~Rp 30.000 / ton (± USD 2.0). Standar pasar global: USD 10 - 50.")
    with col_c_ctrl2:
        emission_cap_pct = st.slider("Batas Kuota Bebas Pajak (Emission Cap %):", min_value=0, max_value=100, value=75)
    with col_c_ctrl3:
        usd_to_idr = st.number_input("Kurs Konversi USD ke IDR:", min_value=10000, max_value=25000, value=16000, step=500)

    df_carbon_sources = pd.DataFrame([
        {"Equipment": "GTG 420-CG9201", "Unit": "Power Gen", "CO2_klb_hr": 12.407891, "CO2_opt_klb_hr": 12.407891},
        {"Equipment": "GTG 420-CG9301", "Unit": "Power Gen", "CO2_klb_hr": 12.578023, "CO2_opt_klb_hr": 12.578023},
        {"Equipment": "Compressor GT 260-CG9101", "Unit": "Sales Gas Compr", "CO2_klb_hr": 4.493336, "CO2_opt_klb_hr": 4.494033},
        {"Equipment": "MP Boiler 410-F9101", "Unit": "Steam Gen", "CO2_klb_hr": 1.890819, "CO2_opt_klb_hr": 1.314082},
        {"Equipment": "MP Boiler 410-F9201", "Unit": "Steam Gen", "CO2_klb_hr": 1.955937, "CO2_opt_klb_hr": 2.422249},
        {"Equipment": "Flare 475-FL9102", "Unit": "Flare System", "CO2_klb_hr": 1.277629, "CO2_opt_klb_hr": 1.277629}
    ])
    
    ton_conv = 0.45359237
    annual_hrs = 8760 * 0.95
    
    df_carbon_sources['CO2_ton_hr'] = df_carbon_sources['CO2_klb_hr'] * ton_conv
    df_carbon_sources['CO2_ton_year'] = df_carbon_sources['CO2_ton_hr'] * annual_hrs
    df_carbon_sources['CO2_opt_ton_year'] = df_carbon_sources['CO2_opt_klb_hr'] * ton_conv * annual_hrs
    
    total_co2_actual_ton_yr = df_carbon_sources['CO2_ton_year'].sum()
    total_co2_opt_ton_yr = df_carbon_sources['CO2_opt_ton_year'].sum()
    
    taxable_emissions = max(0, total_co2_actual_ton_yr * (1 - (emission_cap_pct / 100.0)))
    total_tax_usd = taxable_emissions * carbon_tax_rate
    total_tax_idr = total_tax_usd * usd_to_idr
    
    co2_reduction_ton_yr = max(0, total_co2_actual_ton_yr - total_co2_opt_ton_yr)
    tax_savings_usd = co2_reduction_ton_yr * carbon_tax_rate
    tax_savings_idr = tax_savings_usd * usd_to_idr

    st.divider()

    cm1, cm2, cm3, cm4 = st.columns(4)
    with cm1:
        st.metric("Total Emisi CO₂ Fasilitas", f"{total_co2_actual_ton_yr:,.0f} ton/th", help="Total emisi gas buang Scope 1.")
    with cm2:
        st.metric("Emisi Kena Pajak (Net Cap)", f"{taxable_emissions:,.0f} ton/th", delta=f"{100-emission_cap_pct}% di atas Cap", delta_color="inverse")
    with cm3:
        st.metric("Estimasi Pajak Karbon Tahunan", f"${total_tax_usd:,.2f}", f"Rp {total_tax_idr/1e9:,.2f} Miliar/th")
    with cm4:
        st.metric("Penghematan Pajak (SQP)", f"${tax_savings_usd:,.2f}/th", f"Rp {tax_savings_idr/1e6:,.2f} Juta/th", delta_color="normal")

    st.divider()

    col_cg1, col_cg2 = st.columns([5, 5])
    with col_cg1:
        df_carbon_sources['Tax_Share_USD'] = (df_carbon_sources['CO2_ton_year'] / total_co2_actual_ton_yr) * total_tax_usd
        fig_carb_pie = px.pie(
            df_carbon_sources, names="Equipment", values="Tax_Share_USD",
            title="<b>Proporsi Beban Pajak Karbon per Peralatan Pembakaran</b>",
            hole=0.45, template="plotly_dark"
        )
        fig_carb_pie.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_carb_pie, use_container_width=True)

    with col_cg2:
        fig_carb_bar = go.Figure()
        fig_carb_bar.add_trace(go.Bar(x=df_carbon_sources["Equipment"], y=df_carbon_sources["CO2_ton_year"], name="Emisi Aktual (ton/th)", marker_color="#FF5252"))
        fig_carb_bar.add_trace(go.Bar(x=df_carbon_sources["Equipment"], y=df_carbon_sources["CO2_opt_ton_year"], name="Target Optimum SQP (ton/th)", marker_color="#00E676"))
        fig_carb_bar.update_layout(title="<b>Emisi CO₂ Aktual vs Target Optimasi SQP (ton/tahun)</b>", barmode="group", template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_carb_bar, use_container_width=True)

    st.markdown(f"""
    <div class="narrative-box">
        <h4>📖 Narasi Kebijakan Karbon & Nilai Ekonomi Karbon (NEK)</h4>
        <ul>
            <li><b>Kewajiban Emisi Scope 1:</b> Dengan laju emisi cerobong <b>15.7 ton CO₂/jam (~130,650 ton/tahun)</b>, penetapan <i>Cap</i> sebesar <b>{emission_cap_pct}%</b> menghasilkan beban emisi kena pajak sebesar <b>{taxable_emissions:,.0f} ton CO₂/tahun</b>[cite: 1].</li>
            <li><b>Dampak Terintegrasi SQP:</b> Pengalihan beban uap boiler pada rekomendasi SQP tidak hanya menghemat bahan bakar, tetapi juga memangkas emisi CO₂ cerobong sebesar <b>~440 ton/tahun</b>, secara otomatis mengurangi potensi liabilitas pajak karbon[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 6: MOTORS STATUS =================
with tab_motors:
    st.subheader("⚙️ Matriks Status Peralatan Motor Penggerak & Pompa")
    st.markdown("Visualisasi status operasi (*Running/Standby*) untuk seluruh motor listrik penggerak pompa, kipas pendingin, dan kompresor[cite: 1].")
    
    col_m1, col_m2 = st.columns([4, 6])
    with col_m1:
        all_units = ["SEMUA UNIT"] + list(df_motors_data['Unit'].dropna().unique())
        selected_unit = st.selectbox("Pilih Area / Unit Proses:", all_units)
        status_filter = st.radio("Filter Status Operasi:", ["Semua", "Hanya ON", "Hanya OFF"], horizontal=True)
        
    with col_m2:
        total_m = len(df_motors_data)
        on_m = len(df_motors_data[df_motors_data['Status'] == 'On'])
        off_m = len(df_motors_data[df_motors_data['Status'] == 'Off'])
        subcol1, subcol2, subcol3 = st.columns(3)
        subcol1.metric("Total Motor Terdaftar", total_m)
        subcol2.metric("Running (ON)", on_m)
        subcol3.metric("Standby (OFF)", off_m)

    filtered_m = df_motors_data.copy()
    if selected_unit != "SEMUA UNIT":
        filtered_m = filtered_m[filtered_m['Unit'] == selected_unit]
    if status_filter == "Hanya ON":
        filtered_m = filtered_m[filtered_m['Status'] == 'On']
    elif status_filter == "Hanya OFF":
        filtered_m = filtered_m[filtered_m['Status'] == 'Off']

    st.dataframe(filtered_m.reset_index(drop=True), use_container_width=True, height=350)

# ================= TAB 7: INTENSITAS & NERACA ENERGI =================
with tab_kpi:
    st.subheader("📊 Analisis Komprehensif Intensitas & Neraca Energi Fasilitas")
    st.markdown("Evaluasi neraca energi bruto, kredit pemulihan panas buang (*heat recovery*), dan intensitas energi spesifik (*SEC*) per unit proses[cite: 1].")
    
    consumers_df = df_kpi_data[df_kpi_data['Energy_Consumption'] > 0.001].copy()
    producers_df = df_kpi_data[df_kpi_data['Energy_Consumption'] < -0.001].copy()
    
    gross_energy = consumers_df['Energy_Consumption'].sum()
    heat_recovered = abs(producers_df['Energy_Consumption'].sum())
    net_energy = gross_energy - heat_recovered
    heat_int_ratio = (heat_recovered / gross_energy) * 100 if gross_energy > 0 else 0
    
    mk1, mk2, mk3, mk4 = st.columns(4)
    with mk1:
        st.metric("Total Konsumsi Bruto", f"{gross_energy:.2f} MMBtu/h", help="Total konsumsi energi seluruh unit pemakai.")
    with mk2:
        st.metric("Pemulihan Panas (WHB)", f"-{heat_recovered:.2f} MMBtu/h", delta=f"{heat_int_ratio:.1f}% Recovery Rate", delta_color="normal")
    with mk3:
        st.metric("Konsumsi Energi Bersih", f"{net_energy:.2f} MMBtu/h", help="Beban energi bersih yang harus disuplai.")
    with mk4:
        st.metric("Top Energy Consumer", "Unit 420 (GTG)", delta="191.01 MMBtu/h", delta_color="inverse")
        
    st.divider()

    col_w1, col_w2 = st.columns([5, 5])
    with col_w1:
        top_cons = consumers_df.nlargest(5, 'Energy_Consumption')
        other_cons_val = consumers_df['Energy_Consumption'].sum() - top_cons['Energy_Consumption'].sum()
        
        wf_x = list(top_cons['Unit']) + ["Unit Lainnya", "WHB Recovery", "Net Plant Energy"]
        wf_y = list(top_cons['Energy_Consumption']) + [other_cons_val, -heat_recovered, 0]
        wf_measure = ["relative"] * (len(top_cons) + 2) + ["total"]
        
        fig_wf = go.Figure(go.Waterfall(
            name="Neraca Energi", orientation="v", measure=wf_measure,
            x=wf_x, textposition="outside",
            text=[f"{v:.1f}" for v in wf_y[:-1]] + [f"{net_energy:.1f}"],
            y=wf_y, connector={"line": {"color": "#90A4AE"}},
            decreasing={"marker": {"color": "#00E676"}},
            increasing={"marker": {"color": "#FF5252"}},
            totals={"marker": {"color": "#29B6F6"}}
        ))
        fig_wf.update_layout(title="<b>Neraca Aliran Energi Pabrik (Waterfall - MMbtu/hr)</b>", template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_w2:
        consumers_sorted = consumers_df.sort_values(by='Energy_Consumption', ascending=False).reset_index(drop=True)
        consumers_sorted['Cumulative_Pct'] = (consumers_sorted['Energy_Consumption'].cumsum() / gross_energy) * 100
        
        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
        fig_pareto.add_trace(go.Bar(x=consumers_sorted['Unit_Description'].str.slice(0, 18), y=consumers_sorted['Energy_Consumption'], name="Konsumsi (MMBtu/h)", marker_color="#448AFF"), secondary_y=False)
        fig_pareto.add_trace(go.Scatter(x=consumers_sorted['Unit_Description'].str.slice(0, 18), y=consumers_sorted['Cumulative_Pct'], name="Kumulatif (%)", mode="lines+markers", line=dict(color="#FFD700", width=2)), secondary_y=True)
        fig_pareto.update_layout(title="<b>Prinsip Pareto: Beban Konsumen Energi</b>", template="plotly_dark", height=350, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
        fig_pareto.update_yaxes(title_text="Konsumsi (MMbtu/h)", secondary_y=False)
        fig_pareto.update_yaxes(title_text="Kumulatif (%)", range=[0, 105], secondary_y=True)
        st.plotly_chart(fig_pareto, use_container_width=True)

    st.markdown("""
    <div class="narrative-box">
        <h4>📖 Narasi Rekayasa Proses: Neraca Energi Terintegrasi & Intensitas Spesifik</h4>
        <ul>
            <li><b>Tingkat Integrasi Termal (Heat Integration Rate):</b> Fasilitas berhasil memulihkan <b>126.00 MMBtu/hr (35.3%)</b> energi panas buang kembali ke sistem melalui WHB Unit 460 dan Unit 321[cite: 1].</li>
            <li><b>Titik Berat Konsumsi Termal:</b> Unit 241 (AGRU) memiliki intensitas tertinggi (<b>79.40 MMBtu/MMscf</b>) karena kebutuhan energi panas laten reboiler untuk regenerasi pelarut amine[cite: 1].</li>
            <li><b>Distribusi Pareto:</b> Tiga unit terbesar (Unit 420 GTG, Unit 241 AGRU, dan Unit 260 Kompresi Gas) bertanggung jawab atas <b>>85% total konsumsi energi fasilitas</b>[cite: 1].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.markdown("<center style='color:#78909C;'>EPMS Digital Twin Prototype V2.0 • Pertamina EP Cepu - Jambaran Tiung Biru</center>", unsafe_allow_html=True)