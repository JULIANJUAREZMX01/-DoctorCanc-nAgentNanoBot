"""Tests for conversation state machine."""
from app.core.state_machine import StateManager, LeadStatus

def test_create_state():
    sm = StateManager()
    state = sm.get_state("test_123")
    assert state.session_id == "test_123"
    assert state.lead_status == LeadStatus.NEW

def test_state_persistence():
    sm = StateManager()
    s1 = sm.get_state("test_123")
    s1.lead_status = "LEAD_INTERESADO"
    s2 = sm.get_state("test_123")
    assert s2.lead_status == "LEAD_INTERESADO"

def test_interaction_count():
    sm = StateManager()
    sm.get_state("test_123")
    sm.get_state("test_123")
    s = sm.get_state("test_123")
    assert s.interaction_count == 3
