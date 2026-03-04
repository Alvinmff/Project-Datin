"""
Statistics Engine
Advanced statistical analysis for weather data
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatisticalResult:
    """Statistical analysis result for a single parameter"""
    parameter: str
    mean: float
    std: float
    max: float
    min: float
    median: float
    q25: float
    q75: float
    iqr: float
    skewness: float
    kurtosis: float
    trend_slope: float
    trend_direction: str
    anomaly_count: int
    anomaly_percentage: float
    percentile_90: float
    percentile_10: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "parameter": self.parameter,
            "mean": round(self.mean, 2),
            "std": round(self.std, 2),
            "max": round(self.max, 2),
            "min": round(self.min, 2),
            "median": round(self.median, 2),
            "q25": round(self.q25, 2),
            "q75": round(self.q75, 2),
            "iqr": round(self.iqr, 2),
            "skewness": round(self.skewness, 3),
            "kurtosis": round(self.kurtosis, 3),
            "trend_slope": round(self.trend_slope, 4),
            "trend_direction": self.trend_direction,
            "anomaly_count": self.anomaly_count,
            "anomaly_percentage": round(self.anomaly_percentage, 1),
            "percentile_90": round(self.percentile_90, 2),
            "percentile_10": round(self.percentile_10, 2),
        }
    
    def get_narrative(self) -> str:
        """Generate narrative description"""
        variability = "tinggi" if self.std > self.mean * 0.3 else "normal" if self.std > self.mean * 0.15 else "rendah"
        
        trend_desc = {
            "increasing": "meningkat signifikan",
            "decreasing": "menurun signifikan", 
            "stable": "relatif stabil"
        }.get(self.trend_direction, "tidak diketahui")
        
        return f"""
Parameter {self.parameter}:
- Rata-rata: {self.mean:.2f} dengan variabilitas {variability}
- Rentang: {self.min:.2f} - {self.max:.2f}
- Tren: {trend_desc}
- Anomali: {self.anomaly_count} kejadian ({self.anomaly_percentage:.1f}%)
"""


class StatisticsEngine:
    """
    Advanced Statistical Analysis Engine
    
    Features:
    - Descriptive statistics
    - Trend analysis (linear regression)
    - Anomaly detection (Z-score)
    - Percentile analysis
    - Distribution analysis (skewness, kurtosis)
    """
    
    def __init__(self):
        self.parameters = ['T_Avg', 'T_Max', 'T_Min', 'Rain', 'RH_Avg', 'Pressure', 'WS_Max', 'Sun']
    
    def analyze(self, df: pd.DataFrame) -> Dict[str, StatisticalResult]:
        """
        Perform comprehensive statistical analysis
        
        Args:
            df: DataFrame with weather data
            
        Returns:
            Dictionary mapping parameter names to StatisticalResult
        """
        results = {}
        
        for param in self.parameters:
            if param in df.columns:
                result = self._analyze_parameter(df[param], param)
                results[param] = result
        
        return results
    
    def _analyze_parameter(self, series: pd.Series, param_name: str) -> StatisticalResult:
        """Analyze a single parameter"""
        
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return self._empty_result(param_name)
        
        # Basic statistics
        mean = clean_series.mean()
        std = clean_series.std()
        max_val = clean_series.max()
        min_val = clean_series.min()
        median = clean_series.median()
        q25 = clean_series.quantile(0.25)
        q75 = clean_series.quantile(0.75)
        iqr = q75 - q25
        
        # Percentiles
        percentile_90 = clean_series.quantile(0.90)
        percentile_10 = clean_series.quantile(0.10)
        
        # Distribution
        skewness = clean_series.skew()
        kurtosis = clean_series.kurtosis()
        
        # Trend (linear regression)
        trend_slope = self._calculate_trend(clean_series.values)
        trend_direction = self._interpret_trend(trend_slope)
        
        # Anomaly detection (Z-score > 2)
        if std > 0:
            z_scores = np.abs((clean_series - mean) / std)
            anomaly_count = int(np.sum(z_scores > 2))
        else:
            anomaly_count = 0
        
        anomaly_percentage = (anomaly_count / len(clean_series)) * 100 if len(clean_series) > 0 else 0
        
        return StatisticalResult(
            parameter=param_name,
            mean=mean,
            std=std,
            max=max_val,
            min=min_val,
            median=median,
            q25=q25,
            q75=q75,
            iqr=iqr,
            skewness=skewness,
            kurtosis=kurtosis,
            trend_slope=trend_slope,
            trend_direction=trend_direction,
            anomaly_count=anomaly_count,
            anomaly_percentage=anomaly_percentage,
            percentile_90=percentile_90,
            percentile_10=percentile_10
        )
    
    def _calculate_trend(self, values: np.ndarray) -> float:
        """Calculate linear trend slope using least squares"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return float(slope)
    
    def _interpret_trend(self, slope: float) -> str:
        """Interpret trend direction"""
        # Normalize slope based on typical parameter ranges
        if abs(slope) < 0.1:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _empty_result(self, param_name: str) -> StatisticalResult:
        """Create empty result for no data"""
        return StatisticalResult(
            parameter=param_name,
            mean=0.0,
            std=0.0,
            max=0.0,
            min=0.0,
            median=0.0,
            q25=0.0,
            q75=0.0,
            iqr=0.0,
            skewness=0.0,
            kurtosis=0.0,
            trend_slope=0.0,
            trend_direction="stable",
            anomaly_count=0,
            anomaly_percentage=0.0,
            percentile_90=0.0,
            percentile_10=0.0,
        )
    
    def generate_narrative(self, results: Dict[str, StatisticalResult]) -> str:
        """Generate comprehensive statistical narrative"""
        
        text = """
╔══════════════════════════════════════════════════════════════╗
║           ANALISIS STATISTIK LANJUTAN                       ║
╚══════════════════════════════════════════════════════════════╝

"""
        
        for param, result in results.items():
            text += f"""
┌──────────────────────────────────────────────────────────────┐
│  📊 {param}
└──────────────────────────────────────────────────────────────┘

📈 Statistika Deskriptif:
   • Rata-rata   : {result.mean:.2f}
   • Median      : {result.median:.2f}
   • Std Dev     : {result.std:.2f}
   • Min - Max   : {result.min:.2f} - {result.max:.2f}
   • Q1 - Q3     : {result.q25:.2f} - {result.q75:.2f}
   • IQR         : {result.iqr:.2f}

📉 Distribusi:
   • Skewness    : {result.skewness:.3f} {'(Simetris)' if abs(result.skewness) < 0.5 else '(Miring)'}
   • Kurtosis    : {result.kurtosis:.3f} {'(Normal)' if abs(result.kurtosis) < 3 else '(Leptokurtik/Platikurtik)'}

📊 Persentil:
   • P10         : {result.percentile_10:.2f}
   • P90         : {result.percentile_90:.2f}

🔄 Tren:
   • Arah        : {result.trend_direction.upper()}
   • Slope       : {result.trend_slope:.4f}/hari
   • Interpretasi: {'Meningkat' if result.trend_direction == 'increasing' else 'Menurun' if result.trend_direction == 'decreasing' else 'Stabil'}

⚠️ Anomali:
   • Jumlah      : {result.anomaly_count} kejadian
   • Persentase  : {result.anomaly_percentage:.1f}%

"""
        
        # Summary
        text += """
┌──────────────────────────────────────────────────────────────┐
│  📋 RINGKASAN                                              │
└──────────────────────────────────────────────────────────────┘

"""
        
        # Find most variable parameter
        most_variable = max(results.values(), key=lambda x: x.std if x.mean != 0 else 0)
        most_anomalous = max(results.values(), key=lambda x: x.anomaly_count)
        
        text += f"""
• Parameter paling variabel: {most_variable.parameter} (std: {most_variable.std:.2f})
• Parameter dengan anomali tertinggi: {most_anomalous.parameter} ({most_anomalous.anomaly_count} kejadian)
• Total parameter dianalisis: {len(results)}

"""
        
        # Interpretation
        text += """
┌──────────────────────────────────────────────────────────────┐
│  💡 INTERPRETASI                                            │
└──────────────────────────────────────────────────────────────┘

Analisis ini menggunakan metode statistik untuk mengidentifikasi:
1. Variabilitas data melalui standar deviasi dan IQR
2. Tren waktu melalui regresi linear
3. Anomali melalui Z-score (|z| > 2)
4. Distribusi data melalui skewness dan kurtosis

Catatan: Anomali adalah nilai yang menyimpang lebih dari 2 standar
deviasi dari rata-rata, yang dapat mengindikasikan kondisi cuaca
yang tidak biasa atau kesalahan pengukuran.

══════════════════════════════════════════════════════════════════
Generated by BMKG Weather Intelligence Statistics Engine v2.0
══════════════════════════════════════════════════════════════════
"""
        
        return text
    
    def compare_periods(
        self, 
        df1: pd.DataFrame, 
        df2: pd.DataFrame, 
        param: str
    ) -> Dict[str, Any]:
        """
        Compare statistics between two periods
        
        Args:
            df1: First period data
            df2: Second period data
            param: Parameter to compare
            
        Returns:
            Comparison dictionary
        """
        
        if param not in df1.columns or param not in df2.columns:
            return {}
        
        stats1 = self._analyze_parameter(df1[param], f"{param}_P1")
        stats2 = self._analyze_parameter(df2[param], f"{param}_P2")
        
        return {
            "parameter": param,
            "period1": {
                "mean": stats1.mean,
                "max": stats1.max,
                "min": stats1.min,
            },
            "period2": {
                "mean": stats2.mean,
                "max": stats2.max,
                "min": stats2.min,
            },
            "change": {
                "mean_diff": stats2.mean - stats1.mean,
                "mean_pct_change": ((stats2.mean - stats1.mean) / stats1.mean * 100) if stats1.mean != 0 else 0,
                "max_diff": stats2.max - stats1.max,
                "min_diff": stats2.min - stats1.min,
            },
            "interpretation": self._interpret_comparison(stats1, stats2)
        }
    
    def _interpret_comparison(
        self, 
        stats1: StatisticalResult, 
        stats2: StatisticalResult
    ) -> str:
        """Interpret comparison between two periods"""
        
        mean_change = stats2.mean - stats1.mean
        
        if abs(mean_change) < stats1.std * 0.5:
            return "Perubahan tidak signifikan"
        elif mean_change > 0:
            return f"Peningkatan signifikan ({mean_change:.2f})"
        else:
            return f"Penurunan signifikan ({mean_change:.2f})"


# Export default engine instance
default_statistics_engine = StatisticsEngine()

