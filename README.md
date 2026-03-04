# 🌦️ BMKG Weather Intelligence v2.0

Sistem Pemantauan Cuaca Cerdas dengan AI Adaptive Scoring - **Futuristic Edition**

## 🎯 Fitur Utama

- **Clean Architecture** - Struktur modular dengan Domain, Application, Infrastructure, dan Presentation layers
- **AI Adaptive Scoring** - Penilaian risiko berbasis climatology dan percentile
- **Futuristic UI** - Tampilan cyberpunk modern dengan glassmorphism dan efek neon
- **Analisis Statistik Lanjutan** - Trend analysis, anomaly detection, dan distribusi data

## 📁 Struktur Project

```
webbmkg/
├── app.py                      # Entry point Streamlit
├── PROJECT_PLAN.md             # Rencana pengembangan
├── README.md                   # Dokumentasi
├── requirements.txt            # Dependencies
├── .streamlit/
│   └── config.toml             # Konfigurasi Streamlit
├── config/                     # Konfigurasi aplikasi
│   ├── __init__.py
│   └── settings.py
├── domain/                     # Business Logic Layer
│   ├── __init__.py
│   ├── entities/               # Model data
│   │   ├── __init__.py
│   │   ├── weather_data.py
│   │   ├── station.py
│   │   └── risk_assessment.py
│   └── services/               # Risk Engine & Statistics Engine
│       ├── __init__.py
│       ├── risk_engine.py
│       └── statistics_engine.py
├── application/                # Use Cases Layer
│   ├── __init__.py
│   ├── ports/                  # Interface definitions
│   │   ├── __init__.py
│   │   ├── data_port.py
│   │   └── report_port.py
│   └── usecases/               # LoadWeatherData, AnalyzeRisk, GenerateReport
│       ├── __init__.py
│       ├── load_weather_data.py
│       ├── analyze_risk.py
│       └── generate_report.py
├── infrastructure/             # Data Layer
│   ├── __init__.py
│   ├── data_loaders/           # Excel loader
│   │   ├── __init__.py
│   │   └── excel_loader.py
│   └── repositories/           # Repository pattern
│       ├── __init__.py
│       └── weather_repository.py
├── presentation/               # UI Layer
│   ├── __init__.py
│   ├── components/             # Charts, Metrics, Widgets
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── metrics.py
│   │   └── widgets.py
│   └── pages/
│       └── __init__.py
├── assets/                     # External assets
│   ├── css/
│   │   └── style.css          # Futuristic CSS
│   └── js/
│       └── app.js              # Interactive JavaScript
├── data/                       # Data Excel stations
│   ├── Stamet Juanda.xlsx
│   ├── Staklim Malang.xlsx
│   └── ... (11 stations total)
└── utils/                      # Constants
    ├── __init__.py
    └── constants.py
    └── theme.py
```

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Siapkan Data

Pastikan file Excel stations ada di folder `data/` dengan format:
- `Stamet Juanda.xlsx`
- `Staklim Malang.xlsx`
- dll.

### 3. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501`

## 🧠 AI Adaptive Scoring

Sistem penilaian risiko yang cerdas:

### Algoritma:
1. **Climatology-Based** - Threshold berdasarkan data historis per stasiun
2. **Multi-Factor Weighted** - Bobot dinamis untuk setiap parameter
3. **Trend Analysis** - Deteksi perubahan signifikan
4. **Anomaly Detection** - Identifikasi outlier menggunakan Z-score
5. **Seasonality Adjustment** - Faktor musiman (musim hujan vs kemarau)

### Kategori Risiko:
| Level | Skor | Emoji | Deskripsi |
|-------|------|-------|-----------|
| NORMAL | 0-30 | 🟢 | Kondisi stabil |
| WATCH | 30-50 | 🔵 | Pemantauan berkala |
| WARNING | 50-70 | 🟡 | Variabilitas signifikan |
| ALERT | 70-85 | 🟠 | Monitoring intensif |
| CRITICAL | 85-100 | 🔴 | Potensi ekstrem tinggi |

## 🎨 Tema Futuristic

- **Glassmorphism Cards** - Kartu dengan efek kaca
- **Neon Glow Effects** - Efek glow pada elemen penting
- **Animated Gradients** - Gradasi animasi
- **Cyberpunk Color Palette** - Palet warna cyan, magenta, green

## 📊 Parameter Cuaca

- 🌡️ **Suhu** - Rata-rata, Maksimum, Minimum
- 💧 **Curah Hujan** - Total, Intensitas
- 💨 **Kelembapan** - RH 07:00, 13:00, 18:00
- 🪁 **Angin** - Kecepatan, Arah
- ⏲️ **Tekanan Udara** - Nilai dan variabilitas

## 🔧 Teknologi

- **Streamlit** - Framework web
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **Pydantic** - Data validation
- **NumPy** - Numerical computing

## 📝 Lisensi

BMKG East Java - 2024

---

*Generated with BMKG Weather Intelligence AI System v2.0*

