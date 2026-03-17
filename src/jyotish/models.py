"""Pydantic models for Jyotish."""
from __future__ import annotations
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class Graha(str, Enum):
    SURYA = "Surya"       # Sun
    CHANDRA = "Chandra"   # Moon
    MANGAL = "Mangal"     # Mars
    BUDHA = "Budha"       # Mercury
    GURU = "Guru"         # Jupiter
    SHUKRA = "Shukra"     # Venus
    SHANI = "Shani"       # Saturn
    RAHU = "Rahu"         # North Node
    KETU = "Ketu"         # South Node


class Rashi(str, Enum):
    MESHA = "Mesha"       # Aries
    VRISHABHA = "Vrishabha"  # Taurus
    MITHUNA = "Mithuna"   # Gemini
    KARKA = "Karka"       # Cancer
    SIMHA = "Simha"       # Leo
    KANYA = "Kanya"       # Virgo
    TULA = "Tula"         # Libra
    VRISHCHIKA = "Vrishchika"  # Scorpio
    DHANU = "Dhanu"       # Sagittarius
    MAKARA = "Makara"     # Capricorn
    KUMBHA = "Kumbha"     # Aquarius
    MEENA = "Meena"       # Pisces


class Nakshatra(str, Enum):
    ASHWINI = "Ashwini"
    BHARANI = "Bharani"
    KRITTIKA = "Krittika"
    ROHINI = "Rohini"
    MRIGASHIRA = "Mrigashira"
    ARDRA = "Ardra"
    PUNARVASU = "Punarvasu"
    PUSHYA = "Pushya"
    ASHLESHA = "Ashlesha"
    MAGHA = "Magha"
    PURVA_PHALGUNI = "Purva Phalguni"
    UTTARA_PHALGUNI = "Uttara Phalguni"
    HASTA = "Hasta"
    CHITRA = "Chitra"
    SWATI = "Swati"
    VISHAKHA = "Vishakha"
    ANURADHA = "Anuradha"
    JYESHTHA = "Jyeshtha"
    MOOLA = "Moola"
    PURVA_ASHADHA = "Purva Ashadha"
    UTTARA_ASHADHA = "Uttara Ashadha"
    SHRAVANA = "Shravana"
    DHANISHTHA = "Dhanishtha"
    SHATABHISHA = "Shatabhisha"
    PURVA_BHADRAPADA = "Purva Bhadrapada"
    UTTARA_BHADRAPADA = "Uttara Bhadrapada"
    REVATI = "Revati"


class Planet(BaseModel):
    name: Graha
    longitude: float = 0.0
    rashi: Rashi = Rashi.MESHA
    nakshatra: Nakshatra = Nakshatra.ASHWINI
    nakshatra_pada: int = 1
    house: int = 1
    is_retrograde: bool = False
    dignity: str = ""  # exalted, own, friend, neutral, enemy, debilitated


class House(BaseModel):
    number: int
    rashi: Rashi
    lord: Graha
    significations: list[str] = Field(default_factory=list)
    planets: list[Graha] = Field(default_factory=list)


class Dasha(BaseModel):
    planet: Graha
    start_date: str
    end_date: str
    duration_years: float
    sub_dashas: list["Dasha"] = Field(default_factory=list)


class Yoga(BaseModel):
    name: str
    description: str
    planets_involved: list[Graha] = Field(default_factory=list)
    houses_involved: list[int] = Field(default_factory=list)
    is_benefic: bool = True
    strength: str = "medium"


class BirthChart(BaseModel):
    name: str = ""
    birth_datetime: datetime = Field(default_factory=datetime.now)
    birth_place: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    ayanamsa: float = 23.85  # Lahiri ayanamsa approximate
    lagna: Rashi = Rashi.MESHA
    lagna_degree: float = 0.0
    planets: list[Planet] = Field(default_factory=list)
    houses: list[House] = Field(default_factory=list)
    dashas: list[Dasha] = Field(default_factory=list)
    yogas: list[Yoga] = Field(default_factory=list)
