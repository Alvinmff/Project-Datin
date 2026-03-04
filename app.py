"""
BMKG Weather Intelligence - Main Application
=============================================
A futuristic weather monitoring dashboard with Clean Architecture
Version 2.0 - Modernized & AI-Enhanced

Author: BMKG East Java
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Import external CSS and JS
import streamlit.components.v1 as components

# ===== IMPORTS FROM CLEAN ARCHITECTURE =====
from config import get_settings
from domain.services.risk_engine import RiskEngine
from domain.services.statistics_engine import StatisticsEngine
from infrastructure.repositories.weather_repository import WeatherRepository
from presentation.components.charts import ChartManager
from presentation.components.widgets import CopyButton, RiskGauge, AlertBox

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="BMKG Weather Intelligence v2.0",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SESSION STATE FOR THEME =====
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'night'  # Default to night mode

def toggle_theme():
    """Toggle between day and night mode"""
    st.session_state.theme_mode = 'day' if st.session_state.theme_mode == 'night' else 'night'

# ===== DYNAMIC CSS BASED ON THEME =====
def get_theme_css():
    """Get CSS based on current theme mode"""
    if st.session_state.theme_mode == 'day':
        return """
    <style>
    /* Day Mode - Light Background */
    .stApp { 
        background-color: #f8fafc; 
        color: #1e293b;
    }
    
    /* Override Streamlit defaults */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #0ea5e9;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.2);
    }
    
    [data-testid="stMetricValue"] { 
        color: #0ea5e9; 
        font-weight: bold; 
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] { 
        color: #64748b; 
        font-size: 0.85rem; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1, h2, h3 { 
        color: #0f172a; 
    }
    
    h1 {
        background: linear-gradient(90deg, #0ea5e9, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Inputs */
    .stSelectbox, .stMultiSelect {
        background: #ffffff;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e920, #8b5cf620);
        border-color: #0ea5e9;
    }
    
    /* DataFrame */
    [data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0ea5e9;
    }
    
    /* Risk level colors - Day mode */
    .risk-normal { border-color: #10b981 !important; }
    .risk-watch { border-color: #3b82f6 !important; }
    .risk-warning { border-color: #f59e0b !important; }
    .risk-alert { border-color: #f97316 !important; }
    .risk-critical { border-color: #ef4444 !important; }
    
    /* Text colors for day mode */
    .stText, .stMarkdown p, p {
        color: #1e293b !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0ea5e9;
        color: white;
    }
    </style>
"""
    else:
        return """
    <style>
    /* Night Mode - Dark Background */
    .stApp { 
        background-color: #0a0e17; 
        color: #e0e7ff;
    }
    
    /* Override Streamlit defaults */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #00f5ff;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }
    
    [data-testid="stMetricValue"] { 
        color: #00f5ff; 
        font-weight: bold; 
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
    }
    
    [data-testid="stMetricLabel"] { 
        color: #94a3b8; 
        font-size: 0.85rem; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1, h2, h3 { 
        color: #f0f6fc; 
    }
    
    h1 {
        background: linear-gradient(90deg, #00f5ff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #30363d;
    }
    
    /* Inputs */
    .stSelectbox, .stMultiSelect {
        background: #1a2332;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a2332;
        border: 1px solid #30363d;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff20, #ff00ff20);
        border-color: #00f5ff;
    }
    
    /* DataFrame */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 12px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a2332;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111827;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00f5ff;
    }
    
    /* Risk level colors */
    .risk-normal { border-color: #00ff9d !important; }
    .risk-watch { border-color: #58a6ff !important; }
    .risk-warning { border-color: #ffa500 !important; }
    .risk-alert { border-color: #ff6b35 !important; }
    .risk-critical { border-color: #ff3366 !important; }
    </style>
"""

# ===== LOAD EXTERNAL ASSETS =====
def load_assets():
    """Load external CSS and JavaScript files"""
    
    # Load CSS
    css_path = Path("assets/css/style.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Load JavaScript
    js_path = Path("assets/js/app.js")
    if js_path.exists():
        with open(js_path, "r") as f:
            components.html(f"<script>{f.read()}</script>", height=0)

# Load assets on startup
load_assets()

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
    /* Base theme */
    .stApp { 
        background-color: #0a0e17; 
        color: #e0e7ff;
    }
    
    /* Override Streamlit defaults */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #00f5ff;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    }
    
    [data-testid="stMetricValue"] { 
        color: #00f5ff; 
        font-weight: bold; 
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
    }
    
    [data-testid="stMetricLabel"] { 
        color: #94a3b8; 
        font-size: 0.85rem; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1, h2, h3 { 
        color: #f0f6fc; 
    }
    
    h1 {
        background: linear-gradient(90deg, #00f5ff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #30363d;
    }
    
    /* Inputs */
    .stSelectbox, .stMultiSelect {
        background: #1a2332;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a2332;
        border: 1px solid #30363d;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff20, #ff00ff20);
        border-color: #00f5ff;
    }
    
    /* DataFrame */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 12px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a2332;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111827;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00f5ff;
    }
    
    /* Risk level colors */
    .risk-normal { border-color: #00ff9d !important; }
    .risk-watch { border-color: #58a6ff !important; }
    .risk-warning { border-color: #ffa500 !important; }
    .risk-alert { border-color: #ff6b35 !important; }
    .risk-critical { border-color: #ff3366 !important; }
    </style>
""", unsafe_allow_html=True)


# ===== INITIALIZE SERVICES =====
@st.cache_resource
def get_services():
    """Initialize and cache services"""
    settings = get_settings()
    risk_engine = RiskEngine()
    stats_engine = StatisticsEngine()
    repository = WeatherRepository()
    chart_manager = ChartManager()
    return settings, risk_engine, stats_engine, repository, chart_manager


settings, risk_engine, stats_engine, repository, chart_manager = get_services()


# ===== SIDEBAR =====
def render_sidebar():
    """Render sidebar with station and filter controls"""
    
    with st.sidebar:
        # Theme toggle
        col_theme1, col_theme2 = st.columns([3, 1])
        with col_theme1:
            if st.session_state.theme_mode == 'day':
                st.markdown("☀️ **Mode Siang**")
            else:
                st.markdown("🌙 **Mode Malam**")
        with col_theme2:
            if st.button("🔄", help="Ganti Tema"):
                toggle_theme()
                st.rerun()
        
        st.markdown("---")
        
        # Logo and title
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <img src="https://www.meteoalor.id/assets/images/logo.png" width="100" 
                 style="border-radius: 50%; border: 2px solid #00f5ff; box-shadow: 0 0 20px #00f5ff50;">
            <h3 style="margin-top:15px; color: #00f5ff;">BMKG Weather AI</h3>
            <p style="color: #64748b; font-size: 0.8rem;">v2.0 Futuristic Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Station selector
        selected_station = st.selectbox(
            "📍 Pilih Stasiun",
            settings.stations,
            index=5  # Default to Juanda
        )
        
        st.markdown("---")
        
        # Load data for selected station
        df_raw = repository.get_station_data(selected_station)
        
        if df_raw is not None:
            # Year selector
            years = repository.get_available_years(selected_station)
            if years:
                sel_year = st.selectbox("📅 Tahun", years, index=len(years)-1)
                
                # Month selector
                months = repository.get_available_months(selected_station, sel_year)
                sel_month = st.selectbox("📆 Bulan", ["Semua"] + months)
                
                # Day selector (if month selected)
                if sel_month != "Semua":
                    days = repository.get_available_days(selected_station, sel_year, months.index(sel_month) + 1 if isinstance(sel_month, int) else int(sel_month) if sel_month != "Semua" else None)
                    if days and sel_month != "Semua":
                        # Convert month to int if it's string
                        month_idx = list(range(1, 13))["Semua":months].index(sel_month) + 1 if isinstance(sel_month, str) else sel_month
                        days = repository.get_available_days(selected_station, sel_year, month_idx)
                        if days:
                            sel_days = st.multiselect("🗓️ Pilih Hari", days)
                        else:
                            sel_days = []
                    else:
                        sel_days = []
                else:
                    sel_days = []
                
                st.markdown("---")
                
                # Date range option
                use_range = st.checkbox("📅 Gunakan Rentang Tanggal", value=False)
                
                if use_range:
                    date_range = st.date_input(
                        "Pilih Rentang Tanggal",
                        value=(
                            repository.get_date_range(selected_station)[0] if repository.get_date_range(selected_station) else pd.Timestamp.now(),
                            repository.get_date_range(selected_station)[1] if repository.get_date_range(selected_station) else pd.Timestamp.now()
                        )
                    )
                else:
                    date_range = None
                
                return selected_station, df_raw, sel_year, sel_month, sel_days, use_range, date_range
        
        return selected_station, None, None, None, None, False, None


# ===== MAIN CONTENT =====
def main():
    """Main application entry point"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 40px;">
        <h1>🌤️ BMKG Weather Intelligence</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Sistem Pemantauan Cuaca Cerdas dengan AI Adaptive Scoring
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    station, df_raw, sel_year, sel_month, sel_days, use_range, date_range = render_sidebar()
    
    if df_raw is not None:
        # Apply filters
        df_f = apply_filters(df_raw, sel_year, sel_month, sel_days, use_range, date_range)
        
        if df_f is not None and not df_f.empty:
            # ===== RISK ASSESSMENT =====
            assessment = risk_engine.calculate_risk(df_f, station, use_adaptive=True)
            
            # Header row with risk indicator
            col_title, col_risk = st.columns([3, 1])
            
            with col_title:
                st.markdown(f"### 📊 {station}")
                if sel_month != "Semua":
                    st.caption(f"Periode: {sel_month}/{sel_year}")
                elif sel_year:
                    st.caption(f"Tahun: {sel_year}")
            
            with col_risk:
                RiskGauge.render(assessment.risk_score, assessment.risk_level.value, station)
            
            # ===== KPI METRICS =====
            st.markdown("---")
            
            k1, k2, k3, k4, k5 = st.columns(5)
            
            with k1:
                st.metric("Suhu Avg", f"{df_f['T_Avg'].mean():.1f} °C")
            with k2:
                st.metric("Suhu Max", f"{df_f['T_Max'].max():.1f} °C")
            with k3:
                st.metric("RH Avg", f"{df_f['RH_Avg'].mean():.1f} %")
            with k4:
                st.metric("Total Hujan", f"{df_f['Rain'].sum():.1f} mm")
            with k5:
                st.metric("Angin Max", f"{df_f['WS_Max'].max():.1f} knt")
            
            # ===== TABS FOR DIFFERENT VIEWS =====
            tab1, tab2, tab3, tab4 = st.tabs(["📈Charts", "📊Statistics", "📋Reports", "🔧Data"])
            
            with tab1:
                render_charts(df_f)
            
            with tab2:
                render_statistics(df_f)
            
            with tab3:
                render_reports(assessment)
            
            with tab4:
                render_data_table(df_f)
        
        else:
            AlertBox.render("Tidak ada data untuk periode yang dipilih", "warning")
    
    else:
        AlertBox.render(
            "⚠️ Data tidak ditemukan. Pastikan file Excel ada di folder 'data/'.",
            "error"
        )
        
        st.markdown("""
        ### 📁 Struktur Folder yang Diharapkan:
        ```
        webbmkg/
        ├── app.py
        ├── data/
        │   ├── Stamet Juanda.xlsx
        │   ├── Staklim Malang.xlsx
        │   └── ... (file stations lainnya)
        └── assets/
            ├── css/
            │   └── style.css
            └── js/
                └── app.js
        ```
        """)


def apply_filters(df, year, month, days, use_range, date_range):
    """Apply data filters"""
    
    df_f = df.copy()
    
    if use_range and date_range is not None and len(date_range) == 2:
        # Date range filter (priority)
        start_date, end_date = date_range
        df_f = df_f[
            (df_f['Tanggal_DT'] >= pd.to_datetime(start_date)) &
            (df_f['Tanggal_DT'] <= pd.to_datetime(end_date))
        ].copy()
    else:
        # Year filter
        if year is not None:
            df_f = df_f[df_f['year'] == year].copy()
        
        # Month filter
        if month != "Semua" and month is not None:
            if isinstance(month, str):
                month = list(range(1, 13))[["Semua", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"].index(month)] if month != "Semua" else None
            
            if month:
                df_f = df_f[df_f['month'] == month].copy()
                
                # Day filter
                if days:
                    df_f = df_f[df_f['day'].isin(days)].copy()
    
    return df_f


def render_charts(df):
    """Render chart components"""
    
    # Row 1: Temperature and Windrose
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🌡️ Tren Suhu Harian")
        fig_temp = chart_manager.temperature_trend(df)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("🪁 Windrose (Arah Angin)")
        fig_wind = chart_manager.windrose(df)
        st.plotly_chart(fig_wind, use_container_width=True)
    
    # Row 2: Pressure and Humidity
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("⏲️ Tekanan Udara")
        fig_press = chart_manager.pressure_chart(df)
        st.plotly_chart(fig_press, use_container_width=True)
    
    with col4:
        st.subheader("💧 Kelembapan Udara")
        fig_hum = chart_manager.humidity_chart(df)
        st.plotly_chart(fig_hum, use_container_width=True)
    
    # Row 3: Rainfall
    st.subheader("🌧️ Curah Hujan")
    fig_rain = chart_manager.rainfall_chart(df)
    st.plotly_chart(fig_rain, use_container_width=True)


def render_statistics(df):
    """Render statistical analysis"""
    
    st.subheader("🧠 Analisis Statistik Lanjutan")
    
    # Run statistical analysis
    stats_results = stats_engine.analyze(df)
    
    # Display results
    for param, result in stats_results.items():
        with st.expander(f"📊 {param}"):
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.metric("Mean", f"{result.mean:.2f}")
                st.metric("Median", f"{result.median:.2f}")
            
            with c2:
                st.metric("Std Dev", f"{result.std:.2f}")
                st.metric("Min", f"{result.min:.2f}")
            
            with c3:
                st.metric("Max", f"{result.max:.2f}")
                st.metric("Anomali", f"{result.anomaly_count}")
            
            # Trend
            st.markdown(f"**Tren:** {result.trend_direction} (slope: {result.trend_slope:.4f})")
    
    # Generate narrative
    st.markdown("---")
    stat_narrative = stats_engine.generate_narrative(stats_results)
    st.text_area("Laporan Statistik", stat_narrative, height=300)
    CopyButton.render(stat_narrative, "📋 Copy Laporan")


def render_reports(assessment):
    """Render risk assessment reports"""
    
    st.subheader("📋 Laporan Penilaian Risiko")
    
    # Risk gauge
    fig_gauge = chart_manager.risk_gauge(assessment.risk_score, assessment.risk_level.value)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Report text
    report_text = assessment.to_report_text()
    st.text_area("Laporan Lengkap", report_text, height=350)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        CopyButton.render(report_text, "📋 Copy Laporan")
    
    # Factor breakdown
    st.markdown("---")
    st.subheader("📊 Detail Faktor Risiko")
    
    factor_data = {
        "Curah Hujan": assessment.rainfall_score,
        "Suhu": assessment.temperature_score,
        "Angin": assessment.wind_score,
        "Tekanan": assessment.pressure_score,
        "Kelembapan": assessment.humidity_score
    }
    
    for factor, score in factor_data.items():
        st.progress(score / 25 if factor == "Curah Hujan" else score / 20, text=f"{factor}: {score:.1f}")
    
    # Dominant factors
    if assessment.dominant_factors:
        st.markdown("### 🎯 Faktor Dominan:")
        for factor in assessment.dominant_factors:
            st.markdown(f"- {factor}")


def render_data_table(df):
    """Render data table view"""
    
    st.subheader("🔧 Data Mentah")
    
    with st.expander("👁️ Lihat Tabel Data"):
        st.dataframe(df, use_container_width=True, height=400)
    
    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV",
        csv,
        f"weather_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )


# ===== ENTRY POINT =====
if __name__ == "__main__":
    main()

