import os
import sys


def set_mcp_state(state_name):
    """Helper function to set the mcp_fsm state."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    mcp_fsm = __import__("mcp_fsm")
    mcp_fsm.state = mcp_fsm.states[state_name]


def test_initial_state():
    """Test that initial state is CONNECTING."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state

    reset_state()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]


def test_connect_from_idle():
    """Test connecting from IDLE state."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, connect

    reset_state()
    set_mcp_state("IDLE")
    connect()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]


def test_connect_from_other_states():
    """Test that connect doesn't work from non-IDLE states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, connect

    reset_state()

    set_mcp_state("READY")
    connect()
    assert mcp_fsm.state == mcp_fsm.states["READY"]

    set_mcp_state("RUNNING")
    connect()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]

    set_mcp_state("STOPPED")
    connect()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]

    set_mcp_state("ERROR")
    connect()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_success_from_connecting():
    """Test success transitions from CONNECTING to READY."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, success

    reset_state()
    set_mcp_state("CONNECTING")
    success()
    assert mcp_fsm.state == mcp_fsm.states["READY"]


def test_success_from_other_states():
    """Test that success doesn't work from non-CONNECTING states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, success

    reset_state()

    set_mcp_state("IDLE")
    success()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("READY")
    success()
    assert mcp_fsm.state == mcp_fsm.states["READY"]

    set_mcp_state("RUNNING")
    success()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]

    set_mcp_state("STOPPED")
    success()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]

    set_mcp_state("ERROR")
    success()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_error_from_connecting():
    """Test error transitions from CONNECTING to ERROR."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, error

    reset_state()
    set_mcp_state("CONNECTING")
    error()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_error_from_ready():
    """Test error transitions from READY to ERROR."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, error

    reset_state()
    set_mcp_state("READY")
    error()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_error_from_running():
    """Test error transitions from RUNNING to ERROR."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, error

    reset_state()
    set_mcp_state("RUNNING")
    error()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_error_from_other_states():
    """Test that error doesn't work from non-CONNECTING, READY, or RUNNING states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, error

    reset_state()

    set_mcp_state("IDLE")
    error()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("STOPPED")
    error()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]


def test_recover_from_error():
    """Test recover transitions from ERROR to READY."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, recover

    reset_state()
    set_mcp_state("ERROR")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["READY"]


def test_recover_from_other_states():
    """Test that recover doesn't work from non-ERROR states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, recover

    reset_state()

    set_mcp_state("CONNECTING")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]

    set_mcp_state("IDLE")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("READY")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["READY"]

    set_mcp_state("RUNNING")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]

    set_mcp_state("STOPPED")
    recover()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]


def test_reset_from_error():
    """Test reset transitions from ERROR to IDLE."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, reset

    reset_state()
    set_mcp_state("ERROR")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]


def test_reset_from_stopped():
    """Test reset transitions from STOPPED to IDLE."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, reset

    reset_state()
    set_mcp_state("STOPPED")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]


def test_reset_from_other_states():
    """Test that reset doesn't work from non-ERROR or STOPPED states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, reset

    reset_state()

    set_mcp_state("CONNECTING")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]

    set_mcp_state("IDLE")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("READY")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["READY"]

    set_mcp_state("RUNNING")
    reset()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]


def test_start_from_ready():
    """Test start transitions from READY to RUNNING."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, start

    reset_state()
    set_mcp_state("READY")
    start()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]


def test_start_from_stopped():
    """Test start transitions from STOPPED to READY."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, start

    reset_state()
    set_mcp_state("STOPPED")
    start()
    assert mcp_fsm.state == mcp_fsm.states["READY"]


def test_start_from_other_states():
    """Test that start doesn't work from non-READY or STOPPED states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, start

    reset_state()

    set_mcp_state("CONNECTING")
    start()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]

    set_mcp_state("IDLE")
    start()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("RUNNING")
    start()
    assert mcp_fsm.state == mcp_fsm.states["RUNNING"]

    set_mcp_state("ERROR")
    start()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_stop_from_ready():
    """Test stop transitions from READY to STOPPED."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, stop

    reset_state()
    set_mcp_state("READY")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]


def test_stop_from_running():
    """Test stop transitions from RUNNING to STOPPED."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, stop

    reset_state()
    set_mcp_state("RUNNING")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]


def test_stop_from_other_states():
    """Test that stop doesn't work from non-READY or RUNNING states."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import reset_state, stop

    reset_state()

    set_mcp_state("CONNECTING")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["CONNECTING"]

    set_mcp_state("IDLE")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["IDLE"]

    set_mcp_state("STOPPED")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["STOPPED"]

    set_mcp_state("ERROR")
    stop()
    assert mcp_fsm.state == mcp_fsm.states["ERROR"]


def test_all_states_have_correct_values():
    """Test that all states have unique integer values."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    from mcp_fsm import states

    values = list(states.values())
    assert len(values) == len(set(values)), "All states should have unique values"


def test_state_dict_keys():
    """Test that state dict has all expected state names."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    from mcp_fsm import states

    expected_states = ["CONNECTING", "ERROR", "IDLE", "READY", "RUNNING", "STOPPED"]
    assert set(states.keys()) == set(expected_states), "State dict should have all expected states"


def test_state_transitions_complete():
    """Test all possible state transitions based on the bead definition."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    import mcp_fsm
    from mcp_fsm import (
        connect,
        error,
        recover,
        reset,
        reset_state,
        start,
        stop,
        success,
    )

    def execute_transition(from_state, event):
        """Helper to execute a state transition and return the result."""
        mcp_fsm.state = mcp_fsm.states[from_state]
        event_handlers = {
            "connect": connect,
            "success": success,
            "error": error,
            "recover": recover,
            "reset": reset,
            "start": start,
            "stop": stop,
        }
        handler = event_handlers.get(event)
        if handler:
            handler()
        return mcp_fsm.state

    reset_state()

    transitions = {
        "IDLE": {"connect": "CONNECTING"},
        "CONNECTING": {"success": "READY", "error": "ERROR"},
        "READY": {"start": "RUNNING", "stop": "STOPPED", "error": "ERROR"},
        "RUNNING": {"stop": "STOPPED", "error": "ERROR"},
        "STOPPED": {"start": "READY", "reset": "IDLE"},
        "ERROR": {"reset": "IDLE", "recover": "READY"},
    }

    for from_state, transitions_dict in transitions.items():
        for event, to_state in transitions_dict.items():
            result = execute_transition(from_state, event)
            assert result == mcp_fsm.states[to_state], f"Failed transition: {from_state} {event} -> {to_state}"


def test_state_values_are_integers():
    """Test that all state values are integers."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beads"))
    from mcp_fsm import states

    for value in states.values():
        assert isinstance(value, int), "State values should be integers"
