"""
Weather Data Entity
Pydantic model for weather data with validation
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class WeatherData(BaseModel):
    """Weather Data Model with validation"""
    
    # Identification
    station: str
    date: datetime
    
    # Temperature (°C)
    t07: Optional[float] = None
    t13: Optional[float] = None
    t18: Optional[float] = None
    t_avg: Optional[float] = None
    t_max: Optional[float] = None
    t_min: Optional[float] = None
    
    # Rainfall (mm)
    rain: float = 0.0
    
    # Sunshine (%)
    sun: Optional[float] = None
    
    # Pressure (mb)
    pressure: Optional[float] = None
    
    # Humidity (%)
    rh07: Optional[float] = None
    rh13: Optional[float] = None
    rh18: Optional[float] = None
    rh_avg: Optional[float] = None
    
    # Wind
    ws_avg: Optional[float] = None
    ws_max: Optional[float] = None
    wd_most: Optional[float] = None
    wd_max: Optional[float] = None
    
    # Metadata
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    
    # Additional fields for processing
    is_valid: bool = True
    
    @field_validator('rain')
    @classmethod
    def validate_rain(cls, v: float) -> float:
        """Validate rainfall is non-negative"""
        if v < 0:
            return 0.0
        return v
    
    @field_validator('t_max', 't_min', 't_avg')
    @classmethod
    def validate_temperature(cls, v: Optional[float]) -> Optional[float]:
        """Validate temperature is within reasonable range"""
        if v is not None:
            if v < -50 or v > 60:
                return None
        return v
    
    @field_validator('pressure')
    @classmethod
    def validate_pressure(cls, v: Optional[float]) -> Optional[float]:
        """Validate pressure is within reasonable range"""
        if v is not None:
            if v < 800 or v > 1100:
                return None
        return v
    
    @field_validator('rh_avg', 'rh07', 'rh13', 'rh18')
    @classmethod
    def validate_humidity(cls, v: Optional[float]) -> Optional[float]:
        """Validate humidity is within 0-100%"""
        if v is not None:
            if v < 0:
                return 0.0
            if v > 100:
                return 100.0
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()
    
    @classmethod
    def from_dataframe_row(cls, row: Dict[str, Any], station: str) -> 'WeatherData':
        """Create WeatherData from dataframe row"""
        return cls(
            station=station,
            date=row.get('Tanggal_DT', datetime.now()),
            t07=row.get('T07'),
            t13=row.get('T13'),
            t18=row.get('T18'),
            t_avg=row.get('T_Avg'),
            t_max=row.get('T_Max'),
            t_min=row.get('T_Min'),
            rain=row.get('Rain', 0.0),
            sun=row.get('Sun'),
            pressure=row.get('Pressure'),
            rh07=row.get('RH07'),
            rh13=row.get('RH13'),
            rh18=row.get('RH18'),
            rh_avg=row.get('RH_Avg'),
            ws_avg=row.get('WS_Avg'),
            ws_max=row.get('WS_Max'),
            wd_most=row.get('WD_Most'),
            wd_max=row.get('WD_Max'),
            year=row.get('year'),
            month=row.get('month'),
            day=row.get('day'),
        )

