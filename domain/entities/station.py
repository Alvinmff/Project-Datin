"""
Station Entity
Model for weather station information
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class Station(BaseModel):
    """Weather Station Model"""
    
    name: str = Field(..., description="Station name")
    code: Optional[str] = Field(None, description="Station code")
    region: Optional[str] = Field(None, description="Region/Province")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    elevation: Optional[float] = Field(None, description="Elevation (m)")
    station_type: Optional[str] = Field(None, description="Station type (Tretes, Stamet, etc)")
    
    # Climatological normals (calculated from historical data)
    climatology: Optional[dict] = Field(None, description="Climatological normal values")
    
    class Config:
        """Pydantic config"""
        extra = "allow"


class StationManager:
    """Manages station information and data"""
    
    DEFAULT_STATIONS: List[str] = [
        "Stageof Tretes",
        "Stamet Kalianget",
        "Stamet Tuban", 
        "Staklim Malang",
        "Stamet Banyuwangi",
        "Stamet Juanda",
        "Stamet Bawean",
        "Stageof Karang Kates",
        "Stamet Perak 1",
        "Stamar Perak 2",
        "Stageof Nganjuk"
    ]
    
    @classmethod
    def get_station_type(cls, station_name: str) -> str:
        """Get station type from name"""
        if station_name.startswith("Stageof"):
            return "Stageof"
        elif station_name.startswith("Stamet"):
            return "Stamet"
        elif station_name.startswith("Staklim"):
            return "Staklim"
        elif station_name.startswith("Stamar"):
            return "Stamar"
        else:
            return "Unknown"
    
    @classmethod
    def get_all_stations(cls) -> List[str]:
        """Get list of all available stations"""
        return cls.DEFAULT_STATIONS.copy()
    
    @classmethod
    def get_station_codes(cls) -> dict:
        """Get station name to code mapping"""
        return {
            "Stageof Tretes": "TRT",
            "Stamet Kalianget": "KLT",
            "Stamet Tuban": "TBN",
            "Staklim Malang": "MLG",
            "Stamet Banyuwangi": "BWI",
            "Stamet Juanda": "JUA",
            "Stamet Bawean": "BWN",
            "Stageof Karang Kates": "KRK",
            "Stamet Perak 1": "PRK1",
            "Stamar Perak 2": "PRK2",
            "Stageof Nganjuk": "NGJ",
        }

