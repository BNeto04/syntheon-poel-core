from poel.state import PoelState
from datetime import timedelta

def test_session_expiration():
    state = PoelState.create_new()

    # Mock tempo futuro
    state._data.created_at -= timedelta(hours=4)

    assert state.is_expired()

def test_turn_tracking():
    state = PoelState.create_new()

    state.add_user("olá")
    assert state.turn_id == 1

    state.add_assistant("oi")
    assert state.turn_id == 1  # mesmo turn

    state.add_user("tchau")
    assert state.turn_id == 2
