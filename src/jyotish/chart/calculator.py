"""ChartCalculator computing planetary positions from birth data."""
from __future__ import annotations
import numpy as np
from datetime import datetime
from ..models import BirthChart, Planet, Graha, Rashi, Nakshatra, House
from .planets import PlanetDatabase
from .houses import HouseSystem, RASHIS, RASHI_LORDS


NAKSHATRAS = list(Nakshatra)


class ChartCalculator:
    """Calculate Vedic birth chart from birth date, time and place.

    Uses simplified mean-longitude calculations for demonstration.
    Real Vedic astrology uses Swiss Ephemeris or similar for precision.
    """

    def __init__(self) -> None:
        self.planet_db = PlanetDatabase()
        self.house_system = HouseSystem()

    def _julian_day(self, dt: datetime) -> float:
        """Compute approximate Julian Day Number."""
        y = dt.year
        m = dt.month
        d = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24.0
        if m <= 2:
            y -= 1
            m += 12
        A = int(y / 100)
        B = 2 - A + int(A / 4)
        return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5

    def _mean_longitude(self, jd: float, graha: Graha) -> float:
        """Compute simplified mean longitude for a planet in degrees."""
        T = (jd - 2451545.0) / 36525.0  # centuries from J2000
        # Mean daily motion rates (approximate, in degrees per century)
        rates = {
            Graha.SURYA: 36000.7698,
            Graha.CHANDRA: 481267.8834,
            Graha.MANGAL: 19140.2993,
            Graha.BUDHA: 54810.3054,
            Graha.GURU: 3034.9057,
            Graha.SHUKRA: 21071.5882,
            Graha.SHANI: 1222.1138,
            Graha.RAHU: -6962.1,   # retrograde
            Graha.KETU: -6962.1 + 180 * 36525 / 6798.38,  # opposite Rahu
        }
        base = {
            Graha.SURYA: 280.4665,
            Graha.CHANDRA: 218.3165,
            Graha.MANGAL: 355.4330,
            Graha.BUDHA: 252.2509,
            Graha.GURU: 34.3515,
            Graha.SHUKRA: 181.9798,
            Graha.SHANI: 49.9429,
            Graha.RAHU: 125.0445,
            Graha.KETU: 305.0445,
        }
        lon = base.get(graha, 0) + rates.get(graha, 0) * T
        return lon % 360

    def _apply_ayanamsa(self, tropical_lon: float, ayanamsa: float) -> float:
        """Convert tropical to sidereal longitude."""
        return (tropical_lon - ayanamsa) % 360

    def _longitude_to_rashi(self, sidereal_lon: float) -> Rashi:
        idx = int(sidereal_lon / 30) % 12
        return RASHIS[idx]

    def _longitude_to_nakshatra(self, sidereal_lon: float) -> tuple[Nakshatra, int]:
        nak_idx = int(sidereal_lon / (360 / 27)) % 27
        pada = int((sidereal_lon % (360 / 27)) / (360 / 108)) + 1
        return NAKSHATRAS[nak_idx], min(pada, 4)

    def _compute_lagna(self, jd: float, latitude: float, longitude_deg: float, ayanamsa: float) -> tuple[Rashi, float]:
        """Compute approximate Lagna (Ascendant)."""
        # Simplified: use local sidereal time
        T = (jd - 2451545.0) / 36525.0
        gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T
        lst = (gmst + longitude_deg) % 360
        # Simplified lagna calculation
        lagna_tropical = (lst + 90) % 360  # Very rough approximation
        lagna_sidereal = self._apply_ayanamsa(lagna_tropical, ayanamsa)
        return self._longitude_to_rashi(lagna_sidereal), lagna_sidereal % 30

    def calculate(self, name: str, birth_dt: datetime, place: str,
                  latitude: float, longitude: float, ayanamsa: float = 23.85) -> BirthChart:
        """Calculate a complete Vedic birth chart."""
        jd = self._julian_day(birth_dt)

        # Compute Lagna
        lagna_rashi, lagna_degree = self._compute_lagna(jd, latitude, longitude, ayanamsa)

        # Compute planet positions
        planets = []
        for graha in Graha:
            trop_lon = self._mean_longitude(jd, graha)
            sid_lon = self._apply_ayanamsa(trop_lon, ayanamsa)
            rashi = self._longitude_to_rashi(sid_lon)
            nakshatra, pada = self._longitude_to_nakshatra(sid_lon)

            # Determine house
            lagna_idx = RASHIS.index(lagna_rashi)
            planet_idx = RASHIS.index(rashi)
            house_num = ((planet_idx - lagna_idx) % 12) + 1

            dignity = self.planet_db.get_dignity(graha, rashi)
            is_retro = graha in (Graha.RAHU, Graha.KETU)  # simplified

            planets.append(Planet(
                name=graha, longitude=sid_lon, rashi=rashi,
                nakshatra=nakshatra, nakshatra_pada=pada,
                house=house_num, is_retrograde=is_retro, dignity=dignity,
            ))

        # Build houses
        houses = self.house_system.build_houses(lagna_rashi)
        # Place planets in houses
        for planet in planets:
            for house in houses:
                if house.number == planet.house:
                    house.planets.append(planet.name)

        return BirthChart(
            name=name, birth_datetime=birth_dt, birth_place=place,
            latitude=latitude, longitude=longitude, ayanamsa=ayanamsa,
            lagna=lagna_rashi, lagna_degree=lagna_degree,
            planets=planets, houses=houses,
        )
