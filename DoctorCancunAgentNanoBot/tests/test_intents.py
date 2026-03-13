"""Tests for intent detection engine."""
import pytest
from app.core.intent_router import IntentRouter

@pytest.fixture
def router():
    return IntentRouter()

def test_greeting(router):
    result = router.detect("hola buenas tardes")
    assert result.intent_name == "greeting"
    assert result.confidence > 0.5

def test_location(router):
    result = router.detect("donde estan ubicados")
    assert result.intent_name == "location"

def test_price_screen(router):
    result = router.detect("cuanto cuesta cambiar la pantalla de mi iphone")
    assert result.intent_name == "price_screen"

def test_water_damage(router):
    result = router.detect("se me cayo al agua mi celular")
    assert result.intent_name == "water_damage"

def test_english(router):
    result = router.detect("hello do you repair iphones")
    assert result.intent_name == "english"

def test_unknown(router):
    result = router.detect("asdfghjkl")
    assert result.confidence < 0.5
