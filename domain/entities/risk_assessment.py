"""
Risk Assessment Entity
Model for risk assessment results
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk Level Enumeration"""
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    ALERT = "ALERT"
    CRITICAL = "CRITICAL"
    
    @classmethod
    def from_score(cls, score: float) -> 'RiskLevel':
        """Determine risk level from score"""
        if score >= 85:
            return cls.CRITICAL
        elif score >= 70:
            return cls.ALERT
        elif score >= 50:
            return cls.WARNING
        elif score >= 30:
            return cls.WATCH
        else:
            return cls.NORMAL
    
    def get_color(self) -> str:
        """Get color for risk level"""
        colors = {
            self.NORMAL: "#00ff9d",
            self.WATCH: "#58a6ff",
            self.WARNING: "#ffa500",
            self.ALERT: "#ff6b35",
            self.CRITICAL: "#ff3366"
        }
        return colors.get(self, "#00ff9d")
    
    def get_emoji(self) -> str:
        """Get emoji for risk level"""
        emojis = {
            self.NORMAL: "🟢",
            self.WATCH: "🔵",
            self.WARNING: "🟡",
            self.ALERT: "🟠",
            self.CRITICAL: "🔴"
        }
        return emojis.get(self, "🟢")
    
    def get_description(self) -> str:
        """Get description for risk level"""
        descriptions = {
            self.NORMAL: "Kondisi atmosfer relatif stabil",
            self.WATCH: "Perlu pemantauan berkala",
            self.WARNING: "Adanya variabilitas cuaca signifikan",
            self.ALERT: "Dinamika atmosfer signifikan - monitoring intensif",
            self.CRITICAL: "Potensi kejadian cuaca ekstrem tinggi"
        }
        return descriptions.get(self, "Normal")


class RiskFactor(BaseModel):
    """Individual risk factor"""
    name: str
    value: float
    threshold: float
    contribution: float
    normalized_score: float
    
    
class RiskAssessment(BaseModel):
    """Risk Assessment Result Model"""
    
    # Identification
    station: str
    period_start: datetime
    period_end: datetime
    assessment_date: datetime = Field(default_factory=datetime.now)
    
    # Overall Score
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel = Field(default_factory=RiskLevel.NORMAL)
    
    # Factor Scores
    rainfall_score: float = 0.0
    temperature_score: float = 0.0
    wind_score: float = 0.0
    pressure_score: float = 0.0
    humidity_score: float = 0.0
    
    # Factor Details
    factors: List[RiskFactor] = Field(default_factory=list)
    
    # Statistics
    data_points: int = 0
    anomaly_count: int = 0
    
    # Dominant factors
    dominant_factors: List[str] = Field(default_factory=list)
    
    # Recommendation
    recommendation: str = ""
    
    def __init__(self, **data):
        """Initialize and calculate risk level"""
        super().__init__(**data)
        if self.risk_level == RiskLevel.NORMAL:
            self.risk_level = RiskLevel.from_score(self.risk_score)
    
    @classmethod
    def calculate(
        cls,
        station: str,
        period_start: datetime,
        period_end: datetime,
        risk_score: float,
        rainfall_score: float = 0.0,
        temperature_score: float = 0.0,
        wind_score: float = 0.0,
        pressure_score: float = 0.0,
        humidity_score: float = 0.0,
        factors: Optional[List[RiskFactor]] = None,
        data_points: int = 0,
        anomaly_count: int = 0,
        dominant_factors: Optional[List[str]] = None,
    ) -> 'RiskAssessment':
        """Factory method to create and calculate risk assessment"""
        
        # Determine risk level
        risk_level = RiskLevel.from_score(risk_score)
        
        # Generate recommendation based on level
        recommendation = cls._generate_recommendation(risk_level, dominant_factors or [])
        
        return cls(
            station=station,
            period_start=period_start,
            period_end=period_end,
            risk_score=risk_score,
            risk_level=risk_level,
            rainfall_score=rainfall_score,
            temperature_score=temperature_score,
            wind_score=wind_score,
            pressure_score=pressure_score,
            humidity_score=humidity_score,
            factors=factors or [],
            data_points=data_points,
            anomaly_count=anomaly_count,
            dominant_factors=dominant_factors or [],
            recommendation=recommendation,
        )
    
    @staticmethod
    def _generate_recommendation(level: RiskLevel, dominant_factors: List[str]) -> str:
        """Generate recommendation based on risk level"""
        
        base_recommendations = {
            RiskLevel.NORMAL: "Kondisi normal. Tetap lakukan monitoring rutin.",
            RiskLevel.WATCH: "Pantau perkembangan cuaca secara berkala.",
            RiskLevel.WARNING: "Siaga terhadap potensi perubahan cuaca. Perbarui informasi cuaca secara intensif.",
            RiskLevel.ALERT: "Monitoring intensif diperlukan. Siapkan langkah mitigasi.",
            RiskLevel.CRITICAL: "KEJADIAN LUAR BIASA. Segera lakukan tindakan evakuasi jika diperlukan."
        }
        
        base = base_recommendations.get(level, "")
        
        # Add specific factor recommendations
        if dominant_factors:
            factor_recs = []
            if any("hujan" in f.lower() for f in dominant_factors):
                factor_recs.append("Perhatikan potensi banjir dan tanah longsor.")
            if any("suhu" in f.lower() or "panas" in f.lower() for f in dominant_factors):
                factor_recs.append("Pencegahan heatstroke diperlukan.")
            if any("angin" in f.lower() for f in dominant_factors):
                factor_recs.append("Siaga terhadap angin kencang.")
            
            if factor_recs:
                base += " " + " ".join(factor_recs)
        
        return base
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "station": self.station,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "risk_level_color": self.risk_level.get_color(),
            "risk_level_emoji": self.risk_level.get_emoji(),
            "factor_scores": {
                "rainfall": self.rainfall_score,
                "temperature": self.temperature_score,
                "wind": self.wind_score,
                "pressure": self.pressure_score,
                "humidity": self.humidity_score,
            },
            "dominant_factors": self.dominant_factors,
            "recommendation": self.recommendation,
            "data_points": self.data_points,
            "anomaly_count": self.anomaly_count,
        }
    
    def to_report_text(self) -> str:
        """Generate text report"""
        level = self.risk_level
        
        return f"""
LAPORAN PENILAIAN RISIKO CUACA
UPT: {self.station}
Periode Analisis: {self.period_start.strftime('%d %B %Y')} - {self.period_end.strftime('%d %B %Y')}
Tanggal Assessment: {self.assessment_date.strftime('%d %B %Y %H:%M')}

{'='*50}
INDIKATOR RISIKO CUACA
{'='*50}
Risk Index: {self.risk_score:.1f}/100
Kategori Risiko: {level.get_emoji()} {level.value}

Deskripsi: {level.get_description()}

{'='*50}
SKOR FAKTOR RISIKO
{'='*50}
• Curah Hujan:    {self.rainfall_score:.1f}/25
• Suhu:           {self.temperature_score:.1f}/20
• Angin:          {self.wind_score:.1f}/20
• Tekanan:        {self.pressure_score:.1f}/15
• Kelembapan:     {self.humidity_score:.1f}/20

{'='*50}
FAKTOR DOMINAN
{'='*50}
{', '.join(self.dominant_factors) if self.dominant_factors else 'Tidak ada faktor dominan signifikan'}

{'='*50}
STATISTIK
{'='*50}
• Jumlah Data: {self.data_points} hari
• Jumlah Anomali: {self.anomaly_count} kejadian

{'='*50}
REKOMENDASI
{'='*50}
{self.recommendation}

{'='*50}
Generated by BMKG Weather Intelligence AI System v2.0
{'='*50}
"""

