"""Tests for price engine."""
import pytest
from app.services.price_engine import PriceEngine

@pytest.fixture
def engine():
    return PriceEngine()

def test_extract_iphone_13(engine):
    assert engine.extract_model("cuanto sale pantalla iphone 13") == "iphone_13"

def test_extract_samsung(engine):
    assert engine.extract_model("samsung a54 pantalla rota") == "samsung_a54"

def test_extract_galaxy(engine):
    assert engine.extract_model("galaxy s24") == "samsung_s24"

def test_extract_none(engine):
    assert engine.extract_model("hola buenos dias") is None

def test_detect_screen_service(engine):
    assert engine.detect_service_type("pantalla rota") == "screen_repair"

def test_detect_battery_service(engine):
    assert engine.detect_service_type("cambio de bateria") == "battery_replacement"
