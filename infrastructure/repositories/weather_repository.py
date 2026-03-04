"""
Weather Repository
Provides data access interface using repository pattern
"""
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..data_loaders.excel_loader import ExcelWeatherLoader
from config import get_settings


class WeatherRepository:
    """
    Repository for weather data access
    
    Provides a clean interface for data retrieval,
    with caching and filtering capabilities
    """
    
    def __init__(self, loader: Optional[ExcelWeatherLoader] = None):
        self.settings = get_settings()
        self.loader = loader or ExcelWeatherLoader()
        self._cache: Dict[str, pd.DataFrame] = {}
    
    def get_station_data(
        self,
        station: str,
        use_cache: bool = True,
        force_refresh: bool = False
    ) -> Optional[pd.DataFrame]:
        """
        Get weather data for a specific station
        
        Args:
            station: Station name
            use_cache: Whether to use cached data
            force_refresh: Force reload from file
            
        Returns:
            DataFrame with weather data
        """
        
        cache_key = station
        
        # Check cache
        if use_cache and not force_refresh and cache_key in self._cache:
            return self._cache[cache_key].copy()
        
        # Load from file
        df = self.loader.load(station)
        
        # Cache the result
        if df is not None:
            self._cache[cache_key] = df.copy()
        
        return df
    
    def get_filtered_data(
        self,
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[List[int]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        use_cache: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        Get filtered weather data
        
        Args:
            station: Station name
            year: Filter by year
            month: Filter by month
            day: Filter by days
            start_date: Start date for range filter
            end_date: End date for range filter
            use_cache: Use cached data
            
        Returns:
            Filtered DataFrame
        """
        
        # Get base data
        df = self.get_station_data(station, use_cache=use_cache)
        
        if df is None or df.empty:
            return None
        
        # Apply filters
        df_filtered = df.copy()
        
        # Date range filter (highest priority)
        if start_date is not None and end_date is not None:
            df_filtered = df_filtered[
                (df_filtered['Tanggal_DT'] >= pd.to_datetime(start_date)) &
                (df_filtered['Tanggal_DT'] <= pd.to_datetime(end_date))
            ]
        else:
            # Year filter
            if year is not None:
                df_filtered = df_filtered[df_filtered['year'] == year]
            
            # Month filter
            if month is not None:
                df_filtered = df_filtered[df_filtered['month'] == month]
            
            # Day filter
            if day:
                df_filtered = df_filtered[df_filtered['day'].isin(day)]
        
        return df_filtered
    
    def get_available_years(self, station: str) -> List[int]:
        """
        Get list of available years for a station
        
        Args:
            station: Station name
            
        Returns:
            List of years (sorted ascending)
        """
        
        df = self.get_station_data(station)
        
        if df is None or 'year' not in df.columns:
            return []
        
        years = df['year'].dropna().unique()
        return sorted([int(y) for y in years if pd.notna(y)])
    
    def get_available_months(self, station: str, year: int) -> List[int]:
        """
        Get list of available months for a station and year
        
        Args:
            station: Station name
            year: Year
            
        Returns:
            List of months (sorted)
        """
        
        df = self.get_station_data(station)
        
        if df is None:
            return []
        
        # Filter by year
        df_year = df[df['year'] == year]
        
        if 'month' not in df_year.columns:
            return []
        
        months = df_year['month'].dropna().unique()
        return sorted([int(m) for m in months if pd.notna(m)])
    
    def get_available_days(self, station: str, year: int, month: int) -> List[int]:
        """
        Get list of available days for a station, year and month
        
        Args:
            station: Station name
            year: Year
            month: Month
            
        Returns:
            List of days (sorted)
        """
        
        df = self.get_station_data(station)
        
        if df is None:
            return []
        
        # Filter by year and month
        df_period = df[(df['year'] == year) & (df['month'] == month)]
        
        if 'day' not in df_period.columns:
            return []
        
        days = df_period['day'].dropna().unique()
        return sorted([int(d) for d in days if pd.notna(d)])
    
    def get_date_range(self, station: str) -> Optional[tuple]:
        """
        Get the date range of available data
        
        Args:
            station: Station name
            
        Returns:
            Tuple of (min_date, max_date) or None
        """
        
        df = self.get_station_data(station)
        
        if df is None or 'Tanggal_DT' not in df.columns:
            return None
        
        min_date = df['Tanggal_DT'].min()
        max_date = df['Tanggal_DT'].max()
        
        if pd.isna(min_date) or pd.isna(max_date):
            return None
        
        return (min_date, max_date)
    
    def clear_cache(self, station: Optional[str] = None):
        """
        Clear cached data
        
        Args:
            station: Specific station to clear (or all if None)
        """
        
        if station is None:
            self._cache.clear()
        elif station in self._cache:
            del self._cache[station]
    
    def get_all_stations_data(self) -> Dict[str, pd.DataFrame]:
        """
        Get data for all stations
        
        Returns:
            Dictionary mapping station name to DataFrame
        """
        
        return self.loader.load_all()
    
    def get_summary_stats(self, station: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get summary statistics for a station
        
        Args:
            station: Station name
            year: Optional year filter
            
        Returns:
            Dictionary with summary statistics
        """
        
        if year:
            df = self.get_filtered_data(station, year=year)
        else:
            df = self.get_station_data(station)
        
        if df is None or df.empty:
            return {}
        
        stats = {
            'station': station,
            'total_records': len(df),
            'date_range': {
                'start': df['Tanggal_DT'].min().strftime('%Y-%m-%d') if 'Tanggal_DT' in df.columns else None,
                'end': df['Tanggal_DT'].max().strftime('%Y-%m-%d') if 'Tanggal_DT' in df.columns else None
            },
            'temperature': {
                'avg': float(df['T_Avg'].mean()) if 'T_Avg' in df.columns else None,
                'max': float(df['T_Max'].max()) if 'T_Max' in df.columns else None,
                'min': float(df['T_Min'].min()) if 'T_Min' in df.columns else None
            },
            'rainfall': {
                'total': float(df['Rain'].sum()) if 'Rain' in df.columns else None,
                'max': float(df['Rain'].max()) if 'Rain' in df.columns else None,
                'rainy_days': int(len(df[df['Rain'] > 0])) if 'Rain' in df.columns else 0
            },
            'humidity': {
                'avg': float(df['RH_Avg'].mean()) if 'RH_Avg' in df.columns else None
            },
            'wind': {
                'max': float(df['WS_Max'].max()) if 'WS_Max' in df.columns else None,
                'avg': float(df['WS_Avg'].mean()) if 'WS_Avg' in df.columns else None
            }
        }
        
        return stats


# Export default repository
default_repository = WeatherRepository()

