"""
Data Port Interface
Abstract interface for data access
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import pandas as pd
from datetime import datetime


class DataPort(ABC):
    """Abstract interface for data access"""
    
    @abstractmethod
    def load_station_data(
        self, 
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> Optional[pd.DataFrame]:
        """Load weather data for a station"""
        pass
    
    @abstractmethod
    def get_available_years(self, station: str) -> List[int]:
        """Get available years for a station"""
        pass
    
    @abstractmethod
    def get_available_months(self, station: str, year: int) -> List[int]:
        """Get available months for a station and year"""
        pass
    
    @abstractmethod
    def get_date_range(self, station: str) -> Optional[tuple]:
        """Get date range of available data"""
        pass

