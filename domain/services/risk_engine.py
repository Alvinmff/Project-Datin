"""
Adaptive AI Risk Engine
Advanced risk scoring with climatology-based thresholds and anomaly detection
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..entities.risk_assessment import RiskAssessment, RiskLevel, RiskFactor


@dataclass
class AdaptiveRiskConfig:
    """Configuration for adaptive risk scoring"""
    
    # Weights for each factor (must sum to 1.0)
    rainfall_weight: float = 0.25
    temperature_weight: float = 0.20
    wind_weight: float = 0.20
    pressure_weight: float = 0.15
    humidity_weight: float = 0.20
    
    # Percentile thresholds for anomaly detection
    percentile_high: float = 90.0   # High threshold percentile
    percentile_low: float = 10.0     # Low threshold percentile
    
    # Absolute thresholds (fallback)
    rain_threshold_mm: float = 300.0
    rain_max_threshold_mm: float = 400.0  # Maximum rainfall threshold for adaptive scoring
    temp_max_threshold_c: float = 35.0
    wind_max_threshold_kt: float = 25.0
    pressure_std_threshold: float = 3.0
    humidity_high_threshold: float = 85.0
    
    # Seasonality factors (month -> multiplier)
    season_rainy: List[int] = None  # Months: Nov-Mar
    
    def __post_init__(self):
        if self.season_rainy is None:
            self.season_rainy = [11, 12, 1, 2, 3]


class RiskEngine:
    """
    Adaptive AI Risk Engine for Weather Assessment
    
    Features:
    - Climatology-based thresholds (per-station, per-month)
    - Multi-factor weighted scoring
    - Trend analysis
    - Anomaly detection (Z-score)
    - Seasonality adjustment
    """
    
    def __init__(self, config: Optional[AdaptiveRiskConfig] = None):
        self.config = config or AdaptiveRiskConfig()
        self._climatology_cache: Dict[str, pd.DataFrame] = {}
    
    def calculate_risk(
        self,
        df: pd.DataFrame,
        station: str,
        use_adaptive: bool = True
    ) -> RiskAssessment:
        """
        Calculate risk assessment for given weather data
        
        Args:
            df: DataFrame with weather data
            station: Station name
            use_adaptive: Use adaptive thresholds vs fixed
            
        Returns:
            RiskAssessment object
        """
        
        if df.empty:
            return self._empty_assessment(station)
        
        # Get period info
        period_start = df['Tanggal_DT'].min()
        period_end = df['Tanggal_DT'].max()
        
        # Get statistics
        stats = self._calculate_statistics(df)
        
        if use_adaptive:
            # Adaptive scoring with climatology
            scores = self._adaptive_scoring(df, stats, period_start.month)
        else:
            # Legacy static scoring
            scores = self._static_scoring(df, stats)
        
        # Calculate total score
        total_score = (
            scores['rainfall'] * self.config.rainfall_weight +
            scores['temperature'] * self.config.temperature_weight +
            scores['wind'] * self.config.wind_weight +
            scores['pressure'] * self.config.pressure_weight +
            scores['humidity'] * self.config.humidity_weight
        )
        
        # Apply seasonality adjustment
        season_factor = self._get_seasonality_factor(period_start.month)
        adjusted_score = min(total_score * season_factor, 100.0)
        
        # Identify dominant factors
        dominant_factors = self._identify_dominant_factors(scores, df, stats)
        
        # Count anomalies
        anomaly_count = self._count_anomalies(df, stats)
        
        # Create factor details
        factors = self._create_factor_details(scores, df, stats)
        
        return RiskAssessment.calculate(
            station=station,
            period_start=period_start,
            period_end=period_end,
            risk_score=adjusted_score,
            rainfall_score=scores['rainfall'],
            temperature_score=scores['temperature'],
            wind_score=scores['wind'],
            pressure_score=scores['pressure'],
            humidity_score=scores['humidity'],
            factors=factors,
            data_points=len(df),
            anomaly_count=anomaly_count,
            dominant_factors=dominant_factors,
        )
    
    def _calculate_statistics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate basic statistics from data"""
        
        stats = {}
        
        # Rainfall
        stats['rain_total'] = df['Rain'].sum()
        stats['rain_max'] = df['Rain'].max()
        stats['rain_mean'] = df['Rain'].mean()
        
        # Temperature
        stats['t_max'] = df['T_Max'].max()
        stats['t_min'] = df['T_Min'].min()
        stats['t_avg'] = df['T_Avg'].mean()
        
        # Wind
        stats['ws_max'] = df['WS_Max'].max()
        stats['ws_avg'] = df['WS_Avg'].mean()
        
        # Pressure
        stats['pressure_mean'] = df['Pressure'].mean()
        stats['pressure_std'] = df['Pressure'].std()
        
        # Humidity
        stats['rh_avg'] = df['RH_Avg'].mean()
        
        # Trends (slope)
        stats['rain_slope'] = self._calculate_slope(df['Rain'].values)
        stats['temp_slope'] = self._calculate_slope(df['T_Avg'].values)
        
        return stats
    
    def _calculate_slope(self, values: np.ndarray) -> float:
        """Calculate linear trend slope"""
        if len(values) < 2:
            return 0.0
        x = np.arange(len(values))
        return float(np.polyfit(x, values, 1)[0])
    
    def _adaptive_scoring(
        self, 
        df: pd.DataFrame, 
        stats: Dict[str, float],
        month: int
    ) -> Dict[str, float]:
        """
        Adaptive scoring using climatology-based percentiles
        """
        scores = {}
        
        # ===== RAINFALL SCORING (0-25) =====
        # Calculate percentile rank of current rainfall
        clim = self._get_climatology(df.get('station', [None])[0] if 'station' in df.columns else None, month)
        
        rain_percentile = self._calculate_percentile_rank(
            stats['rain_total'], 
            clim.get('rain_p10', 0),
            clim.get('rain_p90', self.config.rain_max_threshold_mm)
        )
        
        # Score based on percentile (higher = more extreme)
        if rain_percentile >= 90:
            scores['rainfall'] = 25.0
        elif rain_percentile >= 75:
            scores['rainfall'] = 20.0
        elif rain_percentile >= 50:
            scores['rainfall'] = 12.0
        elif rain_percentile >= 25:
            scores['rainfall'] = 6.0
        else:
            scores['rainfall'] = 2.0
        
        # Add consecutive rain days bonus
        consecutive_rain = self._count_consecutive_rain(df)
        if consecutive_rain >= 5:
            scores['rainfall'] = min(scores['rainfall'] + 5, 25.0)
        
        # ===== TEMPERATURE SCORING (0-20) =====
        if stats['t_max'] >= self.config.temp_max_threshold_c:
            scores['temperature'] = 20.0
        elif stats['t_max'] >= 33:
            scores['temperature'] = 15.0
        elif stats['t_max'] >= 31:
            scores['temperature'] = 10.0
        elif stats['t_max'] >= 29:
            scores['temperature'] = 5.0
        else:
            scores['temperature'] = 2.0
        
        # Add heat wave detection (consecutive hot days)
        hot_days = self._count_hot_days(df)
        if hot_days >= 3:
            scores['temperature'] = min(scores['temperature'] + 5, 20.0)
        
        # ===== WIND SCORING (0-20) =====
        if stats['ws_max'] >= self.config.wind_max_threshold_kt:
            scores['wind'] = 20.0
        elif stats['ws_max'] >= 20:
            scores['wind'] = 15.0
        elif stats['ws_max'] >= 15:
            scores['wind'] = 10.0
        elif stats['ws_max'] >= 10:
            scores['wind'] = 5.0
        else:
            scores['wind'] = 2.0
        
        # ===== PRESSURE SCORING (0-15) =====
        if stats['pressure_std'] > self.config.pressure_std_threshold:
            scores['pressure'] = 15.0
        elif stats['pressure_std'] > 2:
            scores['pressure'] = 10.0
        elif stats['pressure_std'] > 1:
            scores['pressure'] = 5.0
        else:
            scores['pressure'] = 2.0
        
        # ===== HUMIDITY SCORING (0-20) =====
        if stats['rh_avg'] > self.config.humidity_high_threshold:
            scores['humidity'] = 20.0
        elif stats['rh_avg'] > 80:
            scores['humidity'] = 15.0
        elif stats['rh_avg'] > 70:
            scores['humidity'] = 10.0
        elif stats['rh_avg'] > 60:
            scores['humidity'] = 5.0
        else:
            scores['humidity'] = 2.0
        
        return scores
    
    def _static_scoring(
        self, 
        df: pd.DataFrame, 
        stats: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Legacy static scoring (original algorithm)
        """
        scores = {
            'rainfall': 0.0,
            'temperature': 0.0,
            'wind': 0.0,
            'pressure': 0.0,
            'humidity': 0.0,
        }
        
        # Rainfall
        if stats['rain_total'] > self.config.rain_threshold_mm:
            scores['rainfall'] = 30.0
        elif stats['rain_total'] > 200:
            scores['rainfall'] = 20.0
        elif stats['rain_total'] > 100:
            scores['rainfall'] = 10.0
        
        # Temperature
        if stats['t_max'] >= self.config.temp_max_threshold_c:
            scores['temperature'] = 20.0
        elif stats['t_max'] >= 33:
            scores['temperature'] = 12.0
        
        # Wind
        if stats['ws_max'] >= self.config.wind_max_threshold_kt:
            scores['wind'] = 20.0
        elif stats['ws_max'] >= 15:
            scores['wind'] = 10.0
        
        # Pressure
        if stats['pressure_std'] > self.config.pressure_std_threshold:
            scores['pressure'] = 15.0
        
        # Humidity
        if stats['rh_avg'] > self.config.humidity_high_threshold:
            scores['humidity'] = 15.0
        
        return scores
    
    def _get_climatology(self, station: Optional[str], month: int) -> Dict[str, float]:
        """
        Get climatological values for the station and month
        In production, this would load from historical data
        """
        # Default climatology values (can be customized per station)
        # These are typical values for East Java region
        
        # Rainy season (Nov-Mar) vs Dry season (Apr-Oct)
        is_rainy = month in self.config.season_rainy
        
        if is_rainy:
            return {
                'rain_p10': 50.0,
                'rain_p50': 150.0,
                'rain_p90': 350.0,
                'rain_max_threshold_mm': 400.0,
                'temp_avg': 26.0,
                'temp_max_avg': 30.0,
                'rh_avg': 80.0,
            }
        else:
            return {
                'rain_p10': 0.0,
                'rain_p50': 20.0,
                'rain_p90': 80.0,
                'rain_max_threshold_mm': 150.0,
                'temp_avg': 28.0,
                'temp_max_avg': 33.0,
                'rh_avg': 65.0,
            }
    
    def _calculate_percentile_rank(
        self, 
        value: float, 
        p10: float, 
        p90: float
    ) -> float:
        """Calculate percentile rank (0-100)"""
        if p90 <= p10:
            return 50.0
        
        rank = ((value - p10) / (p90 - p10)) * 100
        return max(0, min(100, rank))
    
    def _get_seasonality_factor(self, month: int) -> float:
        """Get seasonality adjustment factor"""
        # Rainy season increases risk scores
        if month in self.config.season_rainy:
            return 1.15  # 15% increase
        else:
            return 1.0
    
    def _count_consecutive_rain(self, df: pd.DataFrame) -> int:
        """Count maximum consecutive days with rain"""
        rain_days = (df['Rain'] > 0).astype(int)
        
        max_consecutive = 0
        current = 0
        
        for val in rain_days:
            if val == 1:
                current += 1
                max_consecutive = max(max_consecutive, current)
            else:
                current = 0
        
        return max_consecutive
    
    def _count_hot_days(self, df: pd.DataFrame) -> int:
        """Count days with temperature above threshold"""
        return len(df[df['T_Max'] >= 35])
    
    def _identify_dominant_factors(
        self, 
        scores: Dict[str, float],
        df: pd.DataFrame,
        stats: Dict[str, float]
    ) -> List[str]:
        """Identify dominant risk factors"""
        dominant = []
        
        # Factor thresholds (normalized to weight)
        threshold_rain = 15 * self.config.rainfall_weight
        threshold_temp = 12 * self.config.temperature_weight
        threshold_wind = 12 * self.config.wind_weight
        threshold_pressure = 8 * self.config.pressure_weight
        threshold_humidity = 12 * self.config.humidity_weight
        
        if scores['rainfall'] >= threshold_rain:
            if stats['rain_total'] > 300:
                dominant.append("Akumulasi curah hujan sangat tinggi")
            elif stats['rain_total'] > 200:
                dominant.append("Akumulasi curah hujan tinggi")
            else:
                dominant.append("Curah hujan signifikan")
        
        if scores['temperature'] >= threshold_temp:
            if stats['t_max'] >= 37:
                dominant.append("Suhu maksimum ekstrem (Heatwave)")
            elif stats['t_max'] >= 35:
                dominant.append("Suhu maksimum tinggi")
            else:
                dominant.append("Suhu udara tinggi")
        
        if scores['wind'] >= threshold_wind:
            if stats['ws_max'] >= 30:
                dominant.append("Kecepatan angin sangat kencang")
            elif stats['ws_max'] >= 25:
                dominant.append("Kecepatan angin kencang")
            else:
                dominant.append("Kecepatan angin tinggi")
        
        if scores['pressure'] >= threshold_pressure:
            dominant.append("Fluktuasi tekanan udara signifikan")
        
        if scores['humidity'] >= threshold_humidity:
            dominant.append("Kelembapan udara sangat tinggi")
        
        return dominant[:5]  # Limit to top 5
    
    def _count_anomalies(self, df: pd.DataFrame, stats: Dict[str, float]) -> int:
        """Count number of anomalous data points using Z-score"""
        anomaly_count = 0
        
        # Check each parameter
        for col in ['T_Avg', 'Rain', 'RH_Avg', 'Pressure', 'WS_Max']:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                
                if std > 0:
                    z_scores = np.abs((df[col] - mean) / std)
                    anomaly_count += np.sum(z_scores > 2)
        
        return int(anomaly_count)
    
    def _create_factor_details(
        self,
        scores: Dict[str, float],
        df: pd.DataFrame,
        stats: Dict[str, float]
    ) -> List[RiskFactor]:
        """Create detailed factor information"""
        
        factors = []
        
        factors.append(RiskFactor(
            name="Curah Hujan",
            value=stats.get('rain_total', 0),
            threshold=self.config.rain_threshold_mm,
            contribution=scores['rainfall'] * self.config.rainfall_weight,
            normalized_score=scores['rainfall'] / 25.0
        ))
        
        factors.append(RiskFactor(
            name="Suhu Maksimum",
            value=stats.get('t_max', 0),
            threshold=self.config.temp_max_threshold_c,
            contribution=scores['temperature'] * self.config.temperature_weight,
            normalized_score=scores['temperature'] / 20.0
        ))
        
        factors.append(RiskFactor(
            name="Kecepatan Angin",
            value=stats.get('ws_max', 0),
            threshold=self.config.wind_max_threshold_kt,
            contribution=scores['wind'] * self.config.wind_weight,
            normalized_score=scores['wind'] / 20.0
        ))
        
        factors.append(RiskFactor(
            name="Tekanan Udara",
            value=stats.get('pressure_std', 0),
            threshold=self.config.pressure_std_threshold,
            contribution=scores['pressure'] * self.config.pressure_weight,
            normalized_score=scores['pressure'] / 15.0
        ))
        
        factors.append(RiskFactor(
            name="Kelembapan",
            value=stats.get('rh_avg', 0),
            threshold=self.config.humidity_high_threshold,
            contribution=scores['humidity'] * self.config.humidity_weight,
            normalized_score=scores['humidity'] / 20.0
        ))
        
        return factors
    
    def _empty_assessment(self, station: str) -> RiskAssessment:
        """Create empty assessment for no data"""
        now = datetime.now()
        return RiskAssessment(
            station=station,
            period_start=now,
            period_end=now,
            risk_score=0.0,
            risk_level=RiskLevel.NORMAL,
            recommendation="Data tidak tersedia"
        )


# Export default engine instance
default_risk_engine = RiskEngine()

