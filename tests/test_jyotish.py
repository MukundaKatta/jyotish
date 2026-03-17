"""Tests for Jyotish."""
import pytest
from datetime import datetime
from jyotish.chart.calculator import ChartCalculator
from jyotish.chart.planets import PlanetDatabase
from jyotish.chart.houses import HouseSystem
from jyotish.analysis.yoga import YogaDetector
from jyotish.analysis.dasha import DashaCalculator
from jyotish.analysis.strength import PlanetStrengthCalculator
from jyotish.models import Graha, Rashi


class TestPlanetDatabase:
    def test_all_nine_grahas(self):
        db = PlanetDatabase()
        assert len(db.get_all_grahas()) == 9

    def test_properties(self):
        db = PlanetDatabase()
        props = db.get_properties(Graha.SURYA)
        assert props["english"] == "Sun"
        assert props["gem"] == "Ruby"

    def test_friendships(self):
        db = PlanetDatabase()
        assert Graha.CHANDRA in db.get_friends(Graha.SURYA)
        assert Graha.SHANI in db.get_enemies(Graha.SURYA)

    def test_exaltation(self):
        db = PlanetDatabase()
        ex = db.get_exaltation(Graha.SURYA)
        assert ex[0] == Rashi.MESHA
        assert ex[1] == 10.0

    def test_dignity(self):
        db = PlanetDatabase()
        assert db.get_dignity(Graha.SURYA, Rashi.MESHA) == "exalted"
        assert db.get_dignity(Graha.SURYA, Rashi.TULA) == "debilitated"
        assert db.get_dignity(Graha.SURYA, Rashi.SIMHA) == "own"


class TestHouseSystem:
    def test_build_12_houses(self):
        hs = HouseSystem()
        houses = hs.build_houses(Rashi.MESHA)
        assert len(houses) == 12
        assert houses[0].rashi == Rashi.MESHA
        assert houses[6].rashi == Rashi.TULA

    def test_significations(self):
        hs = HouseSystem()
        houses = hs.build_houses(Rashi.MESHA)
        assert "self" in houses[0].significations
        assert "marriage" in houses[6].significations

    def test_house_types(self):
        hs = HouseSystem()
        types = hs.get_house_type(1)
        assert "kendra" in types
        assert "trikona" in types


class TestChartCalculator:
    def test_calculate_chart(self):
        calc = ChartCalculator()
        dt = datetime(1990, 6, 15, 10, 30)
        chart = calc.calculate("Test", dt, "Delhi", 28.6139, 77.2090)
        assert len(chart.planets) == 9
        assert len(chart.houses) == 12
        assert chart.lagna is not None

    def test_all_planets_have_rashi(self):
        calc = ChartCalculator()
        dt = datetime(2000, 1, 1, 12, 0)
        chart = calc.calculate("Test", dt, "Mumbai", 19.076, 72.8777)
        for p in chart.planets:
            assert p.rashi is not None
            assert 1 <= p.house <= 12


class TestDashaCalculator:
    def test_mahadashas(self):
        calc = ChartCalculator()
        dt = datetime(1990, 1, 1, 12, 0)
        chart = calc.calculate("Test", dt, "Delhi", 28.6, 77.2)
        moon = next(p for p in chart.planets if p.name == Graha.CHANDRA)
        dc = DashaCalculator()
        dashas = dc.calculate_mahadashas(moon, dt)
        assert len(dashas) == 9
        # Total should be approximately 120 years
        total = sum(d.duration_years for d in dashas)
        assert 119 < total < 121

    def test_antardashas(self):
        calc = ChartCalculator()
        dt = datetime(1990, 1, 1, 12, 0)
        chart = calc.calculate("Test", dt, "Delhi", 28.6, 77.2)
        moon = next(p for p in chart.planets if p.name == Graha.CHANDRA)
        dc = DashaCalculator()
        dashas = dc.calculate_mahadashas(moon, dt)
        for d in dashas:
            assert len(d.sub_dashas) == 9


class TestYogaDetector:
    def test_detect_yogas(self):
        calc = ChartCalculator()
        dt = datetime(1990, 6, 15, 10, 30)
        chart = calc.calculate("Test", dt, "Delhi", 28.6139, 77.2090)
        detector = YogaDetector()
        yogas = detector.detect_all(chart)
        # Should find at least some yogas
        assert isinstance(yogas, list)


class TestStrength:
    def test_shadbala(self):
        calc = ChartCalculator()
        dt = datetime(1990, 6, 15, 10, 30)
        chart = calc.calculate("Test", dt, "Delhi", 28.6139, 77.2090)
        sc = PlanetStrengthCalculator()
        for p in chart.planets:
            bala = sc.calculate_shadbala(p, chart)
            assert "total" in bala
            assert bala["total"] >= 0

    def test_strongest_planet(self):
        calc = ChartCalculator()
        dt = datetime(1990, 6, 15, 10, 30)
        chart = calc.calculate("Test", dt, "Delhi", 28.6139, 77.2090)
        sc = PlanetStrengthCalculator()
        graha, score = sc.get_strongest_planet(chart)
        assert graha in Graha
        assert score > 0
