"""
Configuration Management Module
Handles all application settings and constants
"""
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path


@dataclass
class Settings:
    """Application Settings"""
    
    # App Config
    app_name: str = "BMKG Weather Intelligence"
    app_version: str = "2.0.0"
    app_icon: str = "📡"
    
    # Paths
    data_dir: Path = field(default_factory=lambda: Path("data"))
    assets_dir: Path = field(default_factory=lambda: Path("assets"))
    
    # Theme
    theme: Dict[str, str] = field(default_factory=lambda: {
        "bg_primary": "#0a0e17",
        "bg_secondary": "#111827",
        "bg_card": "#1a2332",
        "accent_cyan": "#00f5ff",
        "accent_magenta": "#ff00ff",
        "accent_green": "#00ff9d",
        "accent_orange": "#ff6b35",
        "accent_red": "#ff3366",
        "text_primary": "#e0e7ff",
        "text_secondary": "#94a3b8",
    })
    
    # Risk Thresholds
    risk_thresholds: Dict[str, int] = field(default_factory=lambda: {
        "critical": 85,
        "alert": 70,
        "warning": 50,
        "watch": 30,
    })
    
    # Risk Weights (for AI scoring)
    risk_weights: Dict[str, float] = field(default_factory=lambda: {
        "rainfall": 0.25,
        "temperature": 0.20,
        "wind": 0.20,
        "pressure": 0.15,
        "humidity": 0.20,
    })
    
    # Station List
    stations: List[str] = field(default_factory=lambda: [
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
    ])
    
    # Column Mappings
    column_mappings: Dict[str, str] = field(default_factory=lambda: {
        "T '07.00": 'T07', 
        "T '13.00": 'T13', 
        "T '18.00": 'T18',
        'TRata2': 'T_Avg', 
        'TMax': 'T_Max', 
        'TMin': 'T_Min',
        'Curah Hujan (mm)': 'Rain', 
        'SS (%)': 'Sun',
        'Tekanan Udara (mb)': 'Pressure', 
        'RH07.00': 'RH07', 
        'RH13.00': 'RH13', 
        'RH18.00': 'RH18', 
        'RHRata2': 'RH_Avg',
        'Kec Rata2': 'WS_Avg', 
        'Arah Terbanyak': 'WD_Most',
        'Kec,Max': 'WS_Max', 
        'Arah': 'WD_Max'
    })
    
    # Invalid values to clean
    invalid_values: List[str] = field(default_factory=lambda: ['-', 'ttu', 'TTU', '8888', ''])
    
    # Pagination
    default_page_size: int = 50
    
    # Cache TTL
    cache_ttl: int = 3600  # seconds
    
    # Logging
    log_level: str = "INFO"


# Global instance
_settings: Settings = None


def get_settings() -> Settings:
    """Get or create settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

