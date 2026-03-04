"""
Analyze Risk Use Case
"""
from typing import Optional
import pandas as pd

from ...domain.services.risk_engine import RiskEngine
from ...domain.entities.risk_assessment import RiskAssessment


class AnalyzeRiskUseCase:
    """Use case for risk analysis"""
    
    def __init__(self, risk_engine: Optional[RiskEngine] = None):
        self.risk_engine = risk_engine or RiskEngine()
    
    def execute(
        self,
        df: pd.DataFrame,
        station: str,
        use_adaptive: bool = True
    ) -> RiskAssessment:
        """
        Perform risk analysis on weather data
        
        Args:
            df: Weather DataFrame
            station: Station name
            use_adaptive: Use adaptive scoring
            
        Returns:
            RiskAssessment result
        """
        
        return self.risk_engine.calculate_risk(
            df=df,
            station=station,
            use_adaptive=use_adaptive
        )
    
    def get_risk_level_description(self, level: str) -> str:
        """Get description for risk level"""
        
        descriptions = {
            'NORMAL': 'Kondisi atmosfer relatif stabil',
            'WATCH': 'Perlu pemantauan berkala',
            'WARNING': 'Adanya variabilitas cuaca signifikan',
            'ALERT': 'Dinamika atmosfer signifikan - monitoring intensif',
            'CRITICAL': 'Potensi kejadian cuaca ekstrem tinggi'
        }
        
        return descriptions.get(level.upper(), 'Unknown')

