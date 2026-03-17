"""PlanetStrengthCalculator with shadbala concepts."""
from __future__ import annotations
import numpy as np
from ..models import BirthChart, Planet, Graha, Rashi
from ..chart.planets import PlanetDatabase


class PlanetStrengthCalculator:
    """Calculate planetary strength using Shadbala (six-fold strength) concepts."""

    def __init__(self) -> None:
        self.planet_db = PlanetDatabase()

    def calculate_shadbala(self, planet: Planet, chart: BirthChart) -> dict[str, float]:
        """Calculate the six types of strength for a planet.

        Returns dict with each bala component and total (all 0-60 scale).
        """
        sthana = self._sthana_bala(planet)
        dig = self._dig_bala(planet)
        kaala = self._kaala_bala(planet, chart)
        cheshta = self._cheshta_bala(planet)
        naisargika = self._naisargika_bala(planet)
        drik = self._drik_bala(planet, chart)

        total = sthana + dig + kaala + cheshta + naisargika + drik
        return {
            "sthana_bala": round(sthana, 2),
            "dig_bala": round(dig, 2),
            "kaala_bala": round(kaala, 2),
            "cheshta_bala": round(cheshta, 2),
            "naisargika_bala": round(naisargika, 2),
            "drik_bala": round(drik, 2),
            "total": round(total, 2),
        }

    def _sthana_bala(self, planet: Planet) -> float:
        """Positional strength based on dignity."""
        dignity_scores = {
            "exalted": 60.0,
            "own": 45.0,
            "friend": 30.0,
            "neutral": 15.0,
            "enemy": 7.5,
            "debilitated": 0.0,
        }
        return dignity_scores.get(planet.dignity, 15.0)

    def _dig_bala(self, planet: Planet) -> float:
        """Directional strength based on house placement."""
        # Planets get dig bala in specific houses
        dig_houses = {
            Graha.SURYA: 10, Graha.MANGAL: 10,     # Strong in 10th
            Graha.GURU: 1, Graha.BUDHA: 1,          # Strong in 1st
            Graha.CHANDRA: 4, Graha.SHUKRA: 4,      # Strong in 4th
            Graha.SHANI: 7,                          # Strong in 7th
        }
        ideal_house = dig_houses.get(planet.name)
        if ideal_house is None:
            return 30.0  # Rahu/Ketu get neutral
        diff = abs(planet.house - ideal_house)
        if diff > 6:
            diff = 12 - diff
        return max(0, 60.0 - diff * 10.0)

    def _kaala_bala(self, planet: Planet, chart: BirthChart) -> float:
        """Temporal strength (simplified)."""
        hour = chart.birth_datetime.hour
        # Day planets (Sun, Jupiter, Venus) strong during day
        # Night planets (Moon, Mars, Saturn) strong at night
        is_day = 6 <= hour <= 18
        day_planets = {Graha.SURYA, Graha.GURU, Graha.SHUKRA}
        night_planets = {Graha.CHANDRA, Graha.MANGAL, Graha.SHANI}
        if planet.name in day_planets:
            return 45.0 if is_day else 15.0
        elif planet.name in night_planets:
            return 45.0 if not is_day else 15.0
        return 30.0  # Mercury, Rahu, Ketu

    def _cheshta_bala(self, planet: Planet) -> float:
        """Motional strength (simplified - retrograde planets get more strength)."""
        if planet.is_retrograde:
            return 45.0
        return 30.0

    def _naisargika_bala(self, planet: Planet) -> float:
        """Natural strength - inherent to each planet."""
        natural_strength = {
            Graha.SURYA: 60.0,
            Graha.CHANDRA: 51.4,
            Graha.MANGAL: 17.1,
            Graha.BUDHA: 25.7,
            Graha.GURU: 34.3,
            Graha.SHUKRA: 42.9,
            Graha.SHANI: 8.6,
            Graha.RAHU: 12.0,
            Graha.KETU: 6.0,
        }
        return natural_strength.get(planet.name, 10.0)

    def _drik_bala(self, planet: Planet, chart: BirthChart) -> float:
        """Aspectual strength (simplified)."""
        # Count benefic and malefic aspects
        benefics = {Graha.GURU, Graha.SHUKRA, Graha.BUDHA, Graha.CHANDRA}
        score = 30.0
        for other in chart.planets:
            if other.name == planet.name:
                continue
            diff = abs(other.house - planet.house) % 12
            is_aspecting = diff in (6,)  # 7th aspect (simplified)
            if planet.name == Graha.MANGAL:
                is_aspecting = is_aspecting or diff in (3, 7)  # 4th and 8th
            elif planet.name == Graha.GURU:
                is_aspecting = is_aspecting or diff in (4, 8)  # 5th and 9th
            elif planet.name == Graha.SHANI:
                is_aspecting = is_aspecting or diff in (2, 9)  # 3rd and 10th
            if is_aspecting:
                if other.name in benefics:
                    score += 5
                else:
                    score -= 5
        return max(0, min(60, score))

    def get_strongest_planet(self, chart: BirthChart) -> tuple[Graha, float]:
        """Find the strongest planet in the chart."""
        best_graha = chart.planets[0].name
        best_score = 0.0
        for planet in chart.planets:
            bala = self.calculate_shadbala(planet, chart)
            if bala["total"] > best_score:
                best_score = bala["total"]
                best_graha = planet.name
        return best_graha, best_score

    def get_weakest_planet(self, chart: BirthChart) -> tuple[Graha, float]:
        """Find the weakest planet in the chart."""
        worst_graha = chart.planets[0].name
        worst_score = float("inf")
        for planet in chart.planets:
            bala = self.calculate_shadbala(planet, chart)
            if bala["total"] < worst_score:
                worst_score = bala["total"]
                worst_graha = planet.name
        return worst_graha, worst_score
