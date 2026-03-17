"""DashaCalculator computing Vimshottari Dasha periods."""
from __future__ import annotations
from datetime import datetime, timedelta
from ..models import Dasha, Graha, Nakshatra, Planet
from ..chart.planets import PlanetDatabase


NAKSHATRA_LIST = list(Nakshatra)

# Vimshottari dasha sequence and years
DASHA_SEQUENCE: list[tuple[Graha, float]] = [
    (Graha.KETU, 7), (Graha.SHUKRA, 20), (Graha.SURYA, 6),
    (Graha.CHANDRA, 10), (Graha.MANGAL, 7), (Graha.RAHU, 18),
    (Graha.GURU, 16), (Graha.SHANI, 19), (Graha.BUDHA, 17),
]
TOTAL_DASHA_YEARS = 120.0


class DashaCalculator:
    """Calculate Vimshottari Dasha periods from Moon's nakshatra position."""

    def __init__(self) -> None:
        self.planet_db = PlanetDatabase()

    def _get_dasha_lord_index(self, nakshatra_index: int) -> int:
        """Map nakshatra to starting dasha lord index in DASHA_SEQUENCE."""
        return nakshatra_index % 9

    def _nakshatra_balance(self, moon_longitude: float) -> float:
        """Calculate the remaining portion of the birth nakshatra.
        Returns fraction (0-1) of the nakshatra remaining.
        """
        nak_span = 360.0 / 27.0  # 13.333... degrees
        position_in_nak = moon_longitude % nak_span
        return 1.0 - (position_in_nak / nak_span)

    def calculate_mahadashas(self, moon: Planet, birth_dt: datetime) -> list[Dasha]:
        """Calculate Maha Dasha periods from Moon's position at birth."""
        nak_idx = NAKSHATRA_LIST.index(moon.nakshatra)
        start_lord_idx = self._get_dasha_lord_index(nak_idx)
        balance = self._nakshatra_balance(moon.longitude)

        dashas = []
        current_date = birth_dt

        # First dasha has balance remaining
        for i in range(9):
            lord_idx = (start_lord_idx + i) % 9
            graha, years = DASHA_SEQUENCE[lord_idx]
            if i == 0:
                actual_years = years * balance
            else:
                actual_years = years
            days = actual_years * 365.25
            end_date = current_date + timedelta(days=days)

            # Calculate sub-dashas (Antardashas)
            sub_dashas = self._calculate_antardashas(graha, current_date, actual_years)

            dashas.append(Dasha(
                planet=graha,
                start_date=current_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                duration_years=round(actual_years, 2),
                sub_dashas=sub_dashas,
            ))
            current_date = end_date

        return dashas

    def _calculate_antardashas(self, maha_lord: Graha, start: datetime, maha_years: float) -> list[Dasha]:
        """Calculate Antardasha (sub-periods) within a Mahadasha."""
        # Antardashas follow the same sequence starting from the maha lord
        maha_idx = next(i for i, (g, _) in enumerate(DASHA_SEQUENCE) if g == maha_lord)
        sub_dashas = []
        current = start

        for i in range(9):
            sub_idx = (maha_idx + i) % 9
            sub_graha, sub_base_years = DASHA_SEQUENCE[sub_idx]
            _, maha_base_years = DASHA_SEQUENCE[maha_idx]
            # Antardasha duration = (maha_years * sub_base_years) / total_dasha_years
            sub_years = (maha_years * sub_base_years) / TOTAL_DASHA_YEARS
            sub_days = sub_years * 365.25
            sub_end = current + timedelta(days=sub_days)

            sub_dashas.append(Dasha(
                planet=sub_graha,
                start_date=current.strftime("%Y-%m-%d"),
                end_date=sub_end.strftime("%Y-%m-%d"),
                duration_years=round(sub_years, 2),
            ))
            current = sub_end

        return sub_dashas

    def get_current_dasha(self, dashas: list[Dasha], current_date: datetime | None = None) -> Dasha | None:
        """Find the currently active Mahadasha."""
        if current_date is None:
            current_date = datetime.now()
        for d in dashas:
            start = datetime.strptime(d.start_date, "%Y-%m-%d")
            end = datetime.strptime(d.end_date, "%Y-%m-%d")
            if start <= current_date <= end:
                return d
        return None

    def get_current_antardasha(self, dasha: Dasha, current_date: datetime | None = None) -> Dasha | None:
        """Find the currently active Antardasha within a Mahadasha."""
        if current_date is None:
            current_date = datetime.now()
        for sd in dasha.sub_dashas:
            start = datetime.strptime(sd.start_date, "%Y-%m-%d")
            end = datetime.strptime(sd.end_date, "%Y-%m-%d")
            if start <= current_date <= end:
                return sd
        return None
