"""
Load Weather Data Use Case
"""
from typing import Optional, List, Dict, Any
import pandas as pd

from ...infrastructure.repositories.weather_repository import WeatherRepository


class LoadWeatherDataUseCase:
    """Use case for loading weather data"""
    
    def __init__(self, repository: Optional[WeatherRepository] = None):
        self.repository = repository or WeatherRepository()
    
    def execute(
        self,
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[List[int]] = None,
        start_date: Optional[pd.Timestamp] = None,
        end_date: Optional[pd.Timestamp] = None
    ) -> Optional[pd.DataFrame]:
        """
        Load weather data with filters
        
        Args:
            station: Station name
            year: Year filter
            month: Month filter
            day: Day filter
            start_date: Start date for range
            end_date: End date for range
            
        Returns:
            Filtered DataFrame or None
        """
        
        return self.repository.get_filtered_data(
            station=station,
            year=year,
            month=month,
            day=day,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_available_periods(self, station: str) -> Dict[str, Any]:
        """Get available time periods for a station"""
        
        return {
            'years': self.repository.get_available_years(station),
            'date_range': self.repository.get_date_range(station)
        }

