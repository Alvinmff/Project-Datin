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
import plotly.graph_objects as go

# ===== IMPORTS FROM CLEAN ARCHITECTURE =====
from config import get_settings
from domain.services.risk_engine import RiskEngine
from domain.services.statistics_engine import StatisticsEngine
from infrastructure.repositories.weather_repository import WeatherRepository
from presentation.components.charts import ChartManager
from presentation.components.widgets import CopyButton, RiskGauge, AlertBox

# ===== NEW THEME SYSTEM =====
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="BMKG Weather Intelligence v1.0",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


def render_background_label(text: str, icon: str = "", key: str = None):
    """Render a styled background label that matches the current theme"""
    if st.session_state.theme == 'light':
        bg_color = "#f1f5f9"
        border_color = "#e2e8f0"
        text_color = "#333333"
    else:
        bg_color = "#1a2332"
        border_color = "#30363d"
        text_color = "#94a3b8"
    
    st.markdown(f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 6px 12px;
        margin-bottom: 8px;
        display: inline-block;
    ">
        <span style="color: {text_color}; font-size: 0.85rem; font-weight: 500;">
            {icon} {text}
        </span>
    </div>
    """, unsafe_allow_html=True)


# Load assets on startup
load_assets()

# Apply theme via JavaScript - more reliable method
theme = st.session_state.theme
if theme == "light":
    # Inject light mode CSS - clean corporate look
    st.markdown(
        """
        <script>
        // Add light-mode class to body
        (function() {
            document.body.classList.add("light-mode");
            document.body.classList.remove("dark-mode");
            var app = document.querySelector('.stApp');
            if (app) {
                app.classList.add('light-mode');
                app.classList.remove('dark-mode');
            }
        })();
        </script>
        <style>
        /* Force light mode backgrounds */
        .light-mode, 
        .light-mode .stApp,
        .light-mode [data-testid="stAppViewContainer"],
        .light-mode [data-testid="stMainContent"],
        .light-mode .block-container,
        body.light-mode,
        body.light-mode .stApp {
            background-color: #f8fafc !important;
            background: #f8fafc !important;
        }
        /* Light mode sidebar */
        .light-mode [data-testid="stSidebar"],
        body.light-mode [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        /* Light mode text */
        .light-mode p, 
        .light-mode span, 
        .light-mode div,
        .light-mode label,
        body.light-mode p,
        body.light-mode span,
        body.light-mode div,
        body.light-mode label {
            color: #111827 !important;
        }
        /* Light mode headers */
        .light-mode h1, 
        .light-mode h2, 
        .light-mode h3,
        body.light-mode h1,
        body.light-mode h2,
        body.light-mode h3 {
            color: #1e3a8a !important;
        }
        /* Light mode inputs */
        .light-mode .stSelectbox > div > div,
        .light-mode .stMultiSelect > div > div,
        body.light-mode .stSelectbox > div > div,
        body.light-mode .stMultiSelect > div > div {
            background-color: #ffffff !important;
            color: #111827 !important;
            border-color: #e2e8f0 !important;
        }
        /* Light mode metrics */
        .light-mode [data-testid="stMetricValue"],
        body.light-mode [data-testid="stMetricValue"] {
            color: #2563eb !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    # Apply dark mode CSS - cyberpunk look
    st.markdown(
        """
        <script>
        // Add dark-mode class to body
        (function() {
            document.body.classList.add("dark-mode");
            document.body.classList.remove("light-mode");
            var app = document.querySelector('.stApp');
            if (app) {
                app.classList.add('dark-mode');
                app.classList.remove('light-mode');
            }
        })();
        </script>
        <style>
        /* Force dark mode backgrounds */
        .dark-mode,
        .dark-mode .stApp,
        .dark-mode [data-testid="stAppViewContainer"],
        .dark-mode [data-testid="stMainContent"],
        .dark-mode .block-container,
        body.dark-mode,
        body.dark-mode .stApp {
            background-color: #0a0e17 !important;
            background: #0a0e17 !important;
        }
        /* Dark mode sidebar */
        .dark-mode [data-testid="stSidebar"],
        body.dark-mode [data-testid="stSidebar"] {
            background-color: #111827 !important;
            background: #111827 !important;
            border-right: 1px solid #30363d !important;
        }
        /* Dark mode text */
        .dark-mode p, 
        .dark-mode span, 
        .dark-mode div,
        .dark-mode label,
        body.dark-mode p,
        body.dark-mode span,
        body.dark-mode div,
        body.dark-mode label {
            color: #e0e7ff !important;
        }
        /* Dark mode headers */
        .dark-mode h1, 
        .dark-mode h2, 
        .dark-mode h3,
        body.dark-mode h1,
        body.dark-mode h2,
        body.dark-mode h3 {
            color: #00f5ff !important;
        }
        /* Dark mode inputs */
        .dark-mode .stSelectbox > div > div,
        .dark-mode .stMultiSelect > div > div,
        body.dark-mode .stSelectbox > div > div,
        body.dark-mode .stMultiSelect > div > div {
            background-color: #1a2332 !important;
            color: #e0e7ff !important;
            border-color: #30363d !important;
        }
        /* Dark mode metrics */
        .dark-mode [data-testid="stMetricValue"],
        body.dark-mode [data-testid="stMetricValue"] {
            color: #00f5ff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


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


def get_plotly_layout():
    if st.session_state.theme == "light":
        return dict(
            template="plotly_white",
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(color="#111111")
        )
    else:
        return dict(
            template="plotly_dark",
            paper_bgcolor="#0a0e17",
            plot_bgcolor="#0a0e17",
            font=dict(color="#e0e7ff")
        )

# ===== SIDEBAR =====
def render_sidebar():
    """Render sidebar with station and filter controls"""
        
    with st.sidebar:
        
    # Logo and title - theme aware
        if st.session_state.theme == "light":
            logo_html = """
            <div style="text-align: center; padding: 20px 0;">
                <img src="https://www.meteoalor.id/assets/images/logo.png" width="100" 
                     style="border-radius: 50%; border: 2px solid #2563eb; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);">
                <h3 style="margin-top:15px; color: #1e3a8a;">BMKG Jatim Monitor</h3>
                <p style="color: #64748b; font-size: 0.8rem;">v2.0 Corporate Edition</p>
            </div>
            """
        else:
            logo_html = """
            <div style="text-align: center; padding: 20px 0;">
                <img src="https://www.meteoalor.id/assets/images/logo.png" width="100" 
                     style="border-radius: 50%; border: 2px solid #00f5ff; box-shadow: 0 0 20px #00f5ff50;">
                <h3 style="margin-top:15px; color: #00f5ff;">BMKG Jatim Monitor</h3>
                <p style="color: #64748b; font-size: 0.8rem;">v2.0 Futuristic Edition</p>
            </div>
            """
        st.markdown(logo_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== THEME TOGGLE =====
        st.markdown("### 🎨 Theme Mode")

        theme_option = st.radio(
            "Choose Theme",
            ["Dark Mode", "Light Mode"],
            index=0 if st.session_state.theme == "dark" else 1
        )

        if theme_option == "Dark Mode":
            st.session_state.theme = "dark"
        else:
            st.session_state.theme = "light"

        st.markdown("---")
        
        # Station selector with background label
        render_background_label("📍 Pilih Stasiun")
        selected_station = st.selectbox(
            "pilih_stasiun",
            settings.stations,
            index=5,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Load data for selected station
        df_raw = repository.get_station_data(selected_station)
        
        if df_raw is not None:
            # Year selector with background label
            years = repository.get_available_years(selected_station)
            if years:
                render_background_label("📅 Pilih Tahun")
                sel_year = st.selectbox(
                    "pilih_tahun",
                    years,
                    index=len(years)-1,
                    label_visibility="collapsed"
                )
                
                # Month selector with background label
                months = repository.get_available_months(selected_station, sel_year)
                render_background_label("📆 Pilih Bulan")
                sel_month = st.selectbox(
                    "pilih_bulan",
                    ["Semua"] + months,
                    label_visibility="collapsed"
                )
                
                # Day selector (if month selected) with background label
                if sel_month != "Semua":
                    days = repository.get_available_days(selected_station, sel_year, months.index(sel_month) + 1 if isinstance(sel_month, int) else int(sel_month) if sel_month != "Semua" else None)
                    if days and sel_month != "Semua":
                        # Convert month to int if it's string
                        month_idx = list(range(1, 13))["Semua":months].index(sel_month) + 1 if isinstance(sel_month, str) else sel_month
                        days = repository.get_available_days(selected_station, sel_year, month_idx)
                        if days:
                            render_background_label("🗓️ Pilih Hari")
                            sel_days = st.multiselect(
                                "pilih_hari",
                                days,
                                label_visibility="collapsed"
                            )
                        else:
                            sel_days = []
                    else:
                        sel_days = []
                else:
                    sel_days = []
                
                st.markdown("---")
                
                # Date range option with background label
                render_background_label("📅 Rentang Tanggal")
                use_range = st.checkbox("Gunakan Rentang Tanggal", value=False)
                
                if use_range:
                    render_background_label("🗓️ Pilih Tanggal")
                    date_range = st.date_input(
                        "input_tanggal",
                        value=(
                            repository.get_date_range(selected_station)[0] if repository.get_date_range(selected_station) else pd.Timestamp.now(),
                            repository.get_date_range(selected_station)[1] if repository.get_date_range(selected_station) else pd.Timestamp.now()
                        ),
                        label_visibility="collapsed"
                    )
                else:
                    date_range = None
                
                return selected_station, df_raw, sel_year, sel_month, sel_days, use_range, date_range
        
        return selected_station, None, None, None, None, False, None


# ===== MAIN CONTENT =====
def main():
    """Main application entry point"""
    
    # Theme-aware header styling
    if st.session_state.theme == "light":
        header_html = """
        <div style="text-align: center; padding: 20px 0 40px;">
            <h1 style="color: #1e3a8a;">🌤️ BMKG Weather Intelligence</h1>
            <p style="color: #475569; font-size: 1.1rem;">
                Sistem Pemantauan Cuaca Cerdas dengan AI Adaptive Scoring
            </p>
        </div>
        """
    else:
        header_html = """
        <div style="text-align: center; padding: 20px 0 40px;">
            <h1>🌤️ BMKG Weather Intelligence</h1>
            <p style="color: #94a3b8; font-size: 1.1rem;">
                Sistem Pemantauan Cuaca Cerdas dengan AI Adaptive Scoring
            </p>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Sidebar
    station, df_raw, sel_year, sel_month, sel_days, use_range, date_range = render_sidebar()
    
    # Centered Risk Gauge below the header
    if df_raw is not None:
        # Apply filters
        df_f = apply_filters(df_raw, sel_year, sel_month, sel_days, use_range, date_range)
        
        if df_f is not None and not df_f.empty:
            # ===== RISK ASSESSMENT =====
            assessment = risk_engine.calculate_risk(df_f, station, use_adaptive=True)
            
            # Render period caption
            if sel_month != "Semua":
                st.caption(f"Periode: {sel_month}/{sel_year}")
            elif sel_year:
                st.caption(f"Tahun: {sel_year}")
            
            # Render risk gauge centered below the header
            st.markdown("<div style='text-align:center; margin: 20px 0;'>", unsafe_allow_html=True)
            RiskGauge.render(assessment.risk_score, assessment.risk_level.value, station, st.session_state.theme)
            st.markdown("</div>", unsafe_allow_html=True)
            
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
                st.metric("Angin Max", f"{df_f['WS_Max'].max():.1f} KT")
            
            # ===== TABS FOR DIFFERENT VIEWS =====
            tab1, tab2, tab3, tab4 = st.tabs(["📈Charts", "📊Statistics", "📋Reports", "🔧Data"])
            
            with tab1:
                render_charts(df_f)
            
            with tab2:
                render_statistics(df_f, sel_year=sel_year, station=station, df_raw=df_raw)
            
            with tab3:
                render_reports(assessment)
            
            with tab4:
                render_data_table(df_f, sel_month)
        
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
        st.subheader("🌡️ Tren Suhu")
        fig_temp = chart_manager.temperature_trend(df, st.session_state.theme)
        st.plotly_chart(fig_temp, width="stretch")
        
    
    with col2:
        st.subheader("🪁 Windrose (Arah Angin)")
        fig_wind = chart_manager.windrose(df, st.session_state.theme)
        st.plotly_chart(fig_wind, width="stretch")
        
    
    # Row 2: Pressure and Humidity
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("⏲️ Tekanan Udara")
        fig_press = chart_manager.pressure_chart(df, st.session_state.theme)
        st.plotly_chart(fig_press, width="stretch")
        
    
    with col4:
        st.subheader("💧 Kelembapan Udara")
        fig_hum = chart_manager.humidity_chart(df, st.session_state.theme)
        st.plotly_chart(fig_hum, width="stretch")
        
    
    # Row 3: Rainfall
    st.subheader("🌧️ Curah Hujan")
    fig_rain = chart_manager.rainfall_chart(df, st.session_state.theme)
    st.plotly_chart(fig_rain, width="stretch")
    


def render_statistics(df, sel_year=None, station=None, df_raw=None):
    """Render statistical analysis"""
    
    # Climate Analytics Section
    st.markdown("---")
    st.header(f"📊 Climate Analytics & Matrices - {sel_year}")

    # Helper function to load all station data
    def load_all_data():
        """Load data from all stations"""
        all_stations_data = {}
        for stn in settings.stations:
            data = repository.get_station_data(stn)
            if data is not None and not data.empty:
                all_stations_data[stn] = data
        return all_stations_data

    # 1. Matriks Hari Hujan Bulanan (Semua Stasiun)
    st.subheader(f"🌧️ Matriks Hari Hujan Bulanan (Semua Stasiun) - {sel_year}")
    with st.spinner("Mengolah data seluruh stasiun..."):
        all_stns = load_all_data()
        hh_matrix = []
        for name, data in all_stns.items():
            dy = data[data['year'] == sel_year]
            row = {"Stasiun": name}
            for m in range(1, 13):
                # Hari Hujan didefinisikan jika Rain > 0
                row[f"Bln {m}"] = int(((dy['month'] == m) & (dy['Rain'] > 0)).sum())
            hh_matrix.append(row)
        
        df_hh = pd.DataFrame(hh_matrix)
        st.dataframe(df_hh.style.background_gradient(cmap='Blues', subset=df_hh.columns[1:]), use_container_width=True)

    # 2. Tabel Unsur Iklim Per Tahun (Sesuai Gambar)
    st.subheader(f"📑 Ringkasan Unsur Iklim Tahunan: {station}")
    
    # Ambil data tahunan untuk stasiun terpilih
    if df_raw is not None:
        stn_years = sorted(df_raw['year'].dropna().unique().astype(int))
        summary_data = []

        for yr in stn_years:
            df_yr = df_raw[df_raw['year'] == yr]
            if df_yr.empty: continue
            
            # Handle RH columns safely
            rh_cols = [col for col in ['RH07','RH13','RH18'] if col in df_yr.columns]
            if rh_cols:
                rh_min = df_yr[rh_cols].min().min()
                rh_max = df_yr[rh_cols].max().max()
            else:
                rh_min = rh_max = 0
            
            # Handle Wind - calm if WS_Avg is 0 or very low
            ws_min_val = df_yr['WS_Avg'].min() if 'WS_Avg' in df_yr.columns else 0
            wind_min = "calm" if ws_min_val < 0.5 else f"{ws_min_val:.1f}"
            
            summary_data.append({
                "Tahun": str(yr),
                "Suhu - Min": f"{df_yr['T_Min'].min():.1f}" if 'T_Min' in df_yr.columns else "N/A",
                "Suhu - Rata2": f"{df_yr['T_Avg'].mean():.1f}" if 'T_Avg' in df_yr.columns else "N/A",
                "Suhu - Max": f"{df_yr['T_Max'].max():.1f}" if 'T_Max' in df_yr.columns else "N/A",
                "RH - Min": f"{rh_min:.1f}",
                "RH - Rata2": f"{df_yr['RH_Avg'].mean():.1f}" if 'RH_Avg' in df_yr.columns else "N/A",
                "RH - Max": f"{rh_max:.1f}",
                "Angin - Min": wind_min,
                "Angin - Rata2": f"{df_yr['WS_Avg'].mean():.1f}" if 'WS_Avg' in df_yr.columns else "N/A",
                "Angin - Max": f"{df_yr['WS_Max'].max():.1f}" if 'WS_Max' in df_yr.columns else "N/A",
                "Tekanan - Min": f"{df_yr['Pressure'].min():.1f}" if 'Pressure' in df_yr.columns else "N/A",
                "Tekanan - Rata2": f"{df_yr['Pressure'].mean():.1f}" if 'Pressure' in df_yr.columns else "N/A",
                "Tekanan - Max": f"{df_yr['Pressure'].max():.1f}" if 'Pressure' in df_yr.columns else "N/A",
                "Curah Hujan (mm)": f"{df_yr['Rain'].sum():.1f}" if 'Rain' in df_yr.columns else "N/A",
                "Hari Hujan (hari)": int((df_yr['Rain'] > 0).sum()) if 'Rain' in df_yr.columns else 0,
                "Penyinaran (%)": f"{df_yr['Sun'].mean():.1f}" if 'Sun' in df_yr.columns else "N/A"
            })

        if summary_data:
            df_summary = pd.DataFrame(summary_data).set_index("Tahun").T
            st.table(df_summary)
        else:
            st.info("Tidak ada data ringkasan tersedia.")

    # 3. Profil Suhu Bulanan (Visualisasi & Tabel)
    st.subheader(f"🌡️ Profil Suhu Bulanan - {sel_year}")
    if df_raw is not None:
        df_mon_temp = df_raw[df_raw['year'] == sel_year].groupby('month').agg({
            'T_Min': 'mean',
            'T_Avg': 'mean',
            'T_Max': 'mean'
        }).reset_index()

        # Choose template based on theme
        plot_template = "plotly_dark" if st.session_state.theme == "dark" else "plotly_white"

        fig_mon_temp = go.Figure()
        fig_mon_temp.add_trace(go.Bar(x=df_mon_temp['month'], y=df_mon_temp['T_Max'], name="Rata2 Max", marker_color='#e74c3c'))
        fig_mon_temp.add_trace(go.Bar(x=df_mon_temp['month'], y=df_mon_temp['T_Avg'], name="Rata2 Harian", marker_color='#f1c40f'))
        fig_mon_temp.add_trace(go.Bar(x=df_mon_temp['month'], y=df_mon_temp['T_Min'], name="Rata2 Min", marker_color='#3498db'))
        
        fig_mon_temp.update_layout(
            template=plot_template, barmode='group', 
            xaxis=dict(tickmode='linear', title="Bulan"),
            yaxis=dict(title="Suhu (°C)")
        )
        st.plotly_chart(fig_mon_temp, use_container_width=True)

        # with st.expander("👁️ Lihat Tabel Data Mentah"):
        #   st.dataframe(df, use_container_width=True)

    st.markdown("---")
    
    st.subheader("🧠 Analisis Statistik Lanjutan")
    
    # Run statistical analysis
    stats_results = stats_engine.analyze(df)
    
   # Display results
    for param, result in stats_results.items():
        with st.expander(f"📊 {param}"):

            c1, c2, c3 = st.columns(3)

            with c1:
                # Khusus Rain tampilkan Total
                if param == "Rain":
                    st.metric("Total", f"{result.total:.2f}")
                else:
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
    fig_gauge = chart_manager.risk_gauge(assessment.risk_score, assessment.risk_level.value,st.session_state.theme)
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


def render_data_table(df, sel_month=None):
    """Render data table view with optional monthly aggregation"""
    
    st.subheader("🔧 Data Operation")
    
    # Toggle for monthly aggregation
    col_view1, col_view2 = st.columns([3, 1])
    
    with col_view1:
        pass
    
    with col_view2:
        # Show aggregation option when viewing full year OR single month
        if sel_month == "Semua" or (sel_month is not None and sel_month != "Semua"):
            agg_option = st.radio(
                "📊 Tampilan Data",
                ["Data Stasiun", "Data Analisis"],
                horizontal=True,
                help="Pilih 'Rata-rata per Bulan' untuk melihat nilai rata-rata per bulan saja"
            )
        else:
            agg_option = "Data Stasiun"
    
    # Apply aggregation if user selects monthly view
    df_display = df.copy()
    
    # Toggle untuk pilihan kolom analisis bulanan
    show_analysis_cols = False
    
    # Cek apakah kita perlu tampilkan opsi analisis (untuk semua bulan ATAU 1 bulan dengan data > 1 hari)
    show_analysis_options = (sel_month == "Semua" or (sel_month is not None and sel_month != "Semua"))
    
    if agg_option == "Data Analisis" and show_analysis_options:
        # Tambah toggle untuk pilih jenis analisis
        st.markdown("---")
        col_an1, col_an2 = st.columns([2, 1])
        
        with col_an1:
            analysis_type = st.radio(
                "📈 Jenis Analisis per Bulan",
                ["Rata-rata (Mean)", "Absolut (Max/Min)", "Semua Statistik"],
                horizontal=True,
                help="Pilih jenis statistik yang ingin ditampilkan per bulan"
            )
        
        # Tentukan kolom mana yang akan ditampilkan berdasarkan pilihan
        if analysis_type == "Absolut (Max/Min)":
            # Untuk analisis absolut, hitung max/min per bulan
            numeric_cols = df_display.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            # Hapus kolom non-numerik yang tidak perlu
            exclude_cols = ['year', 'month', 'day', 'Tanggal_DT']
            numeric_cols = [c for c in numeric_cols if c not in exclude_cols]
            
            # Agregasi dengan max dan min
            agg_dict = {}
            for col in numeric_cols:
                agg_dict[col] = ['mean', 'max', 'min']
            
            # Jika memilih 1 bulan tertentu, group by month juga tetap dilakukan
            df_display = df_display.groupby('month').agg(agg_dict).reset_index()
            
            # Ratakan multi-level column names
            df_display.columns = ['_'.join(col).strip('_') if col[1] else col[0] for col in df_display.columns]
            
            # Tambahkan nama bulan
            month_names = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 
                           5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 
                           9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
            df_display.insert(0, 'Bulan', df_display['month'].map(month_names))
            
            # Drop month numeric column
            if 'month' in df_display.columns:
                df_display = df_display.drop(columns=['month'])
            
            show_analysis_cols = True
            st.caption("📊 Menampilkan nilai MAX dan MIN absolute per bulan")
            
        elif analysis_type == "Semua Statistik":
            # Untuk semua statistik (mean, max, min, sum untuk Rain)
            numeric_cols = df_display.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            # Hapus kolom non-numerik yang tidak perlu
            exclude_cols = ['year', 'month', 'day', 'Tanggal_DT']
            numeric_cols = [c for c in numeric_cols if c not in exclude_cols]
            
            # Agregasi dengan berbagai fungsi
            agg_dict = {}
            for col in numeric_cols:
                if col == 'Rain':
                    agg_dict[col] = ['mean', 'max', 'min', 'sum']
                else:
                    agg_dict[col] = ['mean', 'max', 'min']
            
            # Jika memilih 1 bulan tertentu, group by month juga tetap dilakukan
            df_display = df_display.groupby('month').agg(agg_dict).reset_index()
            
            # Ratakan multi-level column names
            df_display.columns = ['_'.join(col).strip('_') if col[1] else col[0] for col in df_display.columns]
            
            # Tambahkan nama bulan
            month_names = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 
                           5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 
                           9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
            df_display.insert(0, 'Bulan', df_display['month'].map(month_names))
            
            # Drop month numeric column
            if 'month' in df_display.columns:
                df_display = df_display.drop(columns=['month'])
            
            show_analysis_cols = True
            st.caption("📊 Menampilkan semua statistik (Mean, Max, Min, Total Rain) per bulan")
            
        else:
            # Default: hanya rata-rata (mean)
            numeric_cols = df_display.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            # Group by month and calculate mean
            df_display = df_display.groupby('month').agg({
                col: 'mean' for col in numeric_cols
            }).reset_index()
            
            # Add month name for display
            month_names = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 
                           5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 
                           9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
            df_display['Bulan'] = df_display['month'].map(month_names)
            
            # Reorder columns - put month name first
            cols = df_display.columns.tolist()
            cols = ['Bulan'] + [c for c in cols if c not in ['Bulan', 'month']]
            df_display = df_display[cols]
            
            # Drop the numeric month column as we have the name now
            if 'month' in df_display.columns:
                df_display = df_display.drop(columns=['month'])
            
            # Tentukan caption berdasarkan pilihan bulan
            if sel_month == "Semua":
                st.caption("📊 Menampilkan nilai rata-rata per bulan (1 row per bulan)")
            else:
                st.caption(f"📊 Menampilkan nilai rata-rata bulan {sel_month}")
    
    with st.expander("👁️ Lihat Tabel Data"):
        st.dataframe(df_display, use_container_width=True, height=400)
    
    # Download option - download the displayed data (aggregated or not)
    csv = df_display.to_csv(index=False).encode('utf-8')
    
    # Determine filename based on view mode
    if agg_option == "Rata-rata per Bulan":
        filename_suffix = "monthly_avg"
    else:
        filename_suffix = pd.Timestamp.now().strftime('%Y%m%d')
    
    st.download_button(
        "📥 Download CSV",
        csv,
        f"weather_data_{filename_suffix}.csv",
        "text/csv"
    )


# ===== ENTRY POINT =====
if __name__ == "__main__":
    main()

