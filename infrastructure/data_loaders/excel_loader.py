"""
Excel Weather Data Loader
Loads and processes weather data from Excel files
"""
import os
import pandas as pd
from typing import Optional, List
from pathlib import Path

from config import get_settings


class ExcelWeatherLoader:
    """
    Loads weather data from Excel files
    
    Expected columns:
    - Tanggal (Date)
    - T '07.00, T '13.00, T '18.00 (Temperature)
    - TRata2 (Average Temperature)
    - TMax, TMin (Max/Min Temperature)
    - Curah Hujan (mm) (Rainfall)
    - SS (%) (Sunshine)
    - Tekanan Udara (mb) (Pressure)
    - RH07.00, RH13.00, RH18.00 (Relative Humidity)
    - RHRata2 (Average RH)
    - Kec Rata2 (Average Wind Speed)
    - Arah Terbanyak (Most Frequent Wind Direction)
    - Kec,Max (Max Wind Speed)
    - Arah (Wind Direction)
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.settings = get_settings()
        self.data_dir = Path(data_dir) if data_dir else self.settings.data_dir
        
        # Column mappings (original -> standardized)
        self.column_mappings = self.settings.column_mappings
        
        # Invalid values to clean
        self.invalid_values = self.settings.invalid_values
    
    def load(self, station_name: str) -> Optional[pd.DataFrame]:
        """
        Load weather data for a specific station
        
        Args:
            station_name: Name of the weather station
            
        Returns:
            Processed DataFrame or None if file not found
        """
        
        # Try different extensions
        for ext in ['.xlsx', '.xls']:
            file_path = self.data_dir / f"{station_name}{ext}"
            
            if file_path.exists():
                try:
                    df = pd.read_excel(file_path)
                    return self._process(df)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    return None
        
        return None
    
    def load_all(self, stations: Optional[List[str]] = None) -> dict:
        """
        Load data for all stations
        
        Args:
            stations: List of station names (default: all from settings)
            
        Returns:
            Dictionary mapping station name to DataFrame
        """
        
        if stations is None:
            stations = self.settings.stations
        
        data = {}
        for station in stations:
            df = self.load(station)
            if df is not None:
                data[station] = df
        
        return data
    
    def _process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean the raw DataFrame
        
        Args:
            df: Raw DataFrame from Excel
            
        Returns:
            Processed DataFrame
        """
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Rename columns to standardized names
        df = df.rename(columns=self.column_mappings)
        
        # Parse date
        if 'Tanggal' in df.columns:
            df['Tanggal_DT'] = pd.to_datetime(
                df['Tanggal'], 
                dayfirst=True, 
                errors='coerce'
            )
            
            # Extract year, month, day
            df['year'] = df['Tanggal_DT'].dt.year
            df['month'] = df['Tanggal_DT'].dt.month
            df['day'] = df['Tanggal_DT'].dt.day
        
        # Clean numeric columns
        numeric_cols = [
            'T07', 'T13', 'T18', 'T_Avg', 'T_Max', 'T_Min',
            'Rain', 'Sun', 'Pressure', 
            'RH07', 'RH13', 'RH18', 'RH_Avg',
            'WS_Avg', 'WD_Most', 'WS_Max', 'WD_Max'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].apply(self._clean_value)
        
        # Drop rows with invalid dates
        if 'Tanggal_DT' in df.columns:
            df = df.dropna(subset=['Tanggal_DT'])
        
        return df
    
    def _clean_value(self, value) -> float:
        """
        Clean a single value
        
        Args:
            value: Raw value
            
        Returns:
            Cleaned float value
        """
        
        # Handle NaN
        if pd.isna(value):
            return 0.0
        
        # Handle string values
        if isinstance(value, str):
            value = value.strip()
            
            # Check for invalid values
            if value in self.invalid_values:
                return 0.0
            
            # Replace comma with dot (Indonesian decimal format)
            value = value.replace(',', '.')
        
        # Try to convert to float
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def get_available_files(self) -> List[str]:
        """Get list of available Excel files in data directory"""
        
        files = []
        for ext in ['*.xlsx', '*.xls']:
            files.extend(self.data_dir.glob(ext))
        
        return [f.stem for f in files if f.is_file()]
    
    def validate_data(self, df: pd.DataFrame) -> dict:
        """
        Validate loaded data
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Validation results dictionary
        """
        
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }
        
        # Check required columns
        required_cols = ['Tanggal_DT', 'T_Avg', 'Rain']
        for col in required_cols:
            if col not in df.columns:
                results['valid'] = False
                results['errors'].append(f"Missing required column: {col}")
        
        # Check data range
        if 'T_Avg' in df.columns:
            temp_outliers = df[(df['T_Avg'] < -10) | (df['T_Avg'] > 50)]
            if len(temp_outliers) > 0:
                results['warnings'].append(
                    f"Found {len(temp_outliers)} temperature values out of range"
                )
        
        if 'Rain' in df.columns:
            negative_rain = df[df['Rain'] < 0]
            if len(negative_rain) > 0:
                results['warnings'].append(
                    f"Found {len(negative_rain)} negative rainfall values"
                )
        
        # Basic stats
        results['stats'] = {
            'row_count': len(df),
            'date_range': (
                df['Tanggal_DT'].min().strftime('%Y-%m-%d') if 'Tanggal_DT' in df.columns and not df.empty else None,
                df['Tanggal_DT'].max().strftime('%Y-%m-%d') if 'Tanggal_DT' in df.columns and not df.empty else None
            ),
            'columns': list(df.columns)
        }
        
        return results


# Export default loader
default_loader = ExcelWeatherLoader()

