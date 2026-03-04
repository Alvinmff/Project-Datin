"""
Generate Report Use Case
"""
from typing import Optional, Dict, Any
import pandas as pd

from ...domain.services.statistics_engine import StatisticsEngine
from ...domain.entities.risk_assessment import RiskAssessment


class GenerateReportUseCase:
    """Use case for generating reports"""
    
    def __init__(self, stats_engine: Optional[StatisticsEngine] = None):
        self.stats_engine = stats_engine or StatisticsEngine()
    
    def execute_risk_report(self, assessment: RiskAssessment) -> str:
        """
        Generate risk assessment report
        
        Args:
            assessment: RiskAssessment object
            
        Returns:
            Formatted report text
        """
        
        return assessment.to_report_text()
    
    def execute_statistics_report(self, df: pd.DataFrame) -> str:
        """
        Generate statistical analysis report
        
        Args:
            df: Weather DataFrame
            
        Returns:
            Formatted report text
        """
        
        stats = self.stats_engine.analyze(df)
        return self.stats_engine.generate_narrative(stats)
    
    def execute_summary(
        self,
        df: pd.DataFrame,
        station: str,
        risk_assessment: Optional[RiskAssessment] = None
    ) -> Dict[str, Any]:
        """
        Generate summary data
        
        Args:
            df: Weather DataFrame
            station: Station name
            risk_assessment: Optional risk assessment
            
        Returns:
            Summary dictionary
        """
        
        summary = {
            'station': station,
            'data_points': len(df),
            'date_range': {
                'start': df['Tanggal_DT'].min().strftime('%Y-%m-%d'),
                'end': df['Tanggal_DT'].max().strftime('%Y-%m-%d')
            },
            'temperature': {
                'avg': df['T_Avg'].mean(),
                'max': df['T_Max'].max(),
                'min': df['T_Min'].min()
            },
            'rainfall': {
                'total': df['Rain'].sum(),
                'max': df['Rain'].max()
            },
            'humidity': {
                'avg': df['RH_Avg'].mean()
            },
            'wind': {
                'max': df['WS_Max'].max()
            }
        }
        
        if risk_assessment:
            summary['risk'] = {
                'score': risk_assessment.risk_score,
                'level': risk_assessment.risk_level.value,
                'dominant_factors': risk_assessment.dominant_factors
            }
        
        return summary

