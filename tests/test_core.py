"""Tests for Jyotish."""
from src.core import Jyotish
def test_init(): assert Jyotish().get_stats()["ops"] == 0
def test_op(): c = Jyotish(); c.track(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Jyotish(); [c.track() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Jyotish(); c.track(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Jyotish(); r = c.track(); assert r["service"] == "jyotish"
