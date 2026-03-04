"""
Constants for BMKG Weather Intelligence Application
"""

# Station List
STATIONS = [
    "Stageof Tretes",
    "Stamet Kalianget",
    "Stamet Tuban",
    "Staklim Malang",
    "Stamet Banyuwangi",
    "Stamet Juanda",
    "Stamet Bawean",
    "Stageof Karang Kates",
    "Stamet Perak 1",
    "Stamar Perak 2",
    "Stageof Nganjuk"
]

# Station Codes
STATION_CODES = {
    "Stageof Tretes": "TRT",
    "Stamet Kalianget": "KLT",
    "Stamet Tuban": "TBN",
    "Staklim Malang": "MLG",
    "Stamet Banyuwangi": "BWI",
    "Stamet Juanda": "JUA",
    "Stamet Bawean": "BWN",
    "Stageof Karang Kates": "KRK",
    "Stamet Perak 1": "PRK1",
    "Stamar Perak 2": "PRK2",
    "Stageof Nganjuk": "NGJ",
}

# Risk Level Colors
RISK_COLORS = {
    "NORMAL": "#00ff9d",
    "WATCH": "#58a6ff", 
    "WARNING": "#ffa500",
    "ALERT": "#ff6b35",
    "CRITICAL": "#ff3366"
}

# Risk Level Emojis
RISK_EMOJIS = {
    "NORMAL": "🟢",
    "WATCH": "🔵",
    "WARNING": "🟡",
    "ALERT": "🟠",
    "CRITICAL": "🔴"
}

# Parameter Display Names
PARAMETER_NAMES = {
    "T_Avg": "Suhu Rata-rata",
    "T_Max": "Suhu Maksimum",
    "T_Min": "Suhu Minimum",
    "Rain": "Curah Hujan",
    "RH_Avg": "Kelembapan Rata-rata",
    "Pressure": "Tekanan Udara",
    "WS_Max": "Kecepatan Angin Maksimum",
    "WS_Avg": "Kecepatan Angin Rata-rata",
    "Sun": "Penyinaran Matahari"
}

# Parameter Units
PARAMETER_UNITS = {
    "T_Avg": "°C",
    "T_Max": "°C",
    "T_Min": "°C",
    "Rain": "mm",
    "RH_Avg": "%",
    "Pressure": "mb",
    "WS_Max": "knot",
    "WS_Avg": "knot",
    "Sun": "%"
}

# Wind Direction Labels
WIND_DIRECTIONS = {
    "N": "Utara",
    "NE": "Timur Laut",
    "E": "Timur",
    "SE": "Tenggara",
    "S": "Selatan",
    "SW": "Barat Daya",
    "W": "Barat",
    "NW": "Barat Laut"
}

# Month Names (Indonesian)
MONTH_NAMES = {
    1: "Januari",
    2: "Februari", 
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember"
}

# Season Names (Indonesian)
SEASON_NAMES = {
    "rainy": "Musim Hujan",
    "dry": "Musim Kemarau",
    "transition": "Musim Pancaroba"
}

# Weather Icons (Emoji)
WEATHER_ICONS = {
    "sunny": "☀️",
    "cloudy": "☁️",
    "rainy": "🌧️",
    "stormy": "⛈️",
    "windy": "💨",
    "foggy": "🌫️",
    "hot": "🔥",
    "cold": "❄️"
}

# File Extensions
EXCEL_EXTENSIONS = ['.xlsx', '.xls']

# Date Formats
DATE_FORMATS = {
    "short": "%d/%m/%y",
    "medium": "%d %b %Y",
    "long": "%d %B %Y",
    "iso": "%Y-%m-%d"
}

# Chart Colors
CHART_COLORS = [
    "#00f5ff",  # Cyan
    "#ff00ff",  # Magenta
    "#00ff9d",  # Green
    "#ffa500",  # Orange
    "#ff3366",  # Red
    "#58a6ff",  # Blue
    "#9b59b6",  # Purple
    "#f1c40f",  # Yellow
]

# Animation Durations (ms)
ANIMATION_DURATION = {
    "fast": 150,
    "normal": 300,
    "slow": 500
}

# Cache Settings
CACHE_TTL = 3600  # seconds
CACHE_MAX_SIZE = 100  # number of entries

