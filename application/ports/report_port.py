"""
Report Port Interface
Abstract interface for report generation
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class ReportPort(ABC):
    """Abstract interface for report generation"""
    
    @abstractmethod
    def generate_risk_report(self, assessment: Dict[str, Any]) -> str:
        """Generate risk assessment report"""
        pass
    
    @abstractmethod
    def generate_statistics_report(self, stats: Dict[str, Any]) -> str:
        """Generate statistical analysis report"""
        pass

