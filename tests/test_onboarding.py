"""Tests for owner onboarding engine."""
from app.core.onboarding import OnboardingEngine

def test_start_session():
    engine = OnboardingEngine()
    msg = engine.start_session("owner_123")
    assert "setup de DocBot" in msg
    assert engine.is_onboarding("owner_123")

def test_process_first_answer():
    engine = OnboardingEngine()
    engine.start_session("owner_123")
    response = engine.process_answer("owner_123", "iDoctor Cancún")
    assert "DATOS DEL NEGOCIO" in response or "PRECIOS" in response or "%" in response

def test_skip_question():
    engine = OnboardingEngine()
    engine.start_session("owner_123")
    response = engine.process_answer("owner_123", "/skip")
    assert "%" in response  # Progress bar should show

def test_done_command():
    engine = OnboardingEngine()
    engine.start_session("owner_123")
    engine.process_answer("owner_123", "iDoctor Cancún")
    response = engine.process_answer("owner_123", "/done")
    assert "completado" in response.lower()
    assert not engine.is_onboarding("owner_123")

def test_not_onboarding():
    engine = OnboardingEngine()
    assert not engine.is_onboarding("random_user")
