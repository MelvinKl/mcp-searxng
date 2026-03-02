states: dict = {
    "CONNECTING": 0,
    "ERROR": 1,
    "IDLE": 2,
    "READY": 3,
    "RUNNING": 4,
    "STOPPED": 5,
}


state: int = states["CONNECTING"]


def connect() -> None:
    global state
    if state == states["IDLE"]:
        state = states["CONNECTING"]


def error() -> None:
    global state
    if state == states["CONNECTING"]:
        state = states["ERROR"]
    elif state == states["READY"]:
        state = states["ERROR"]
    elif state == states["RUNNING"]:
        state = states["ERROR"]


def recover() -> None:
    global state
    if state == states["ERROR"]:
        state = states["READY"]


def reset() -> None:
    global state
    if state == states["ERROR"]:
        state = states["IDLE"]
    elif state == states["STOPPED"]:
        state = states["IDLE"]


def start() -> None:
    global state
    if state == states["READY"]:
        state = states["RUNNING"]
    elif state == states["STOPPED"]:
        state = states["READY"]


def stop() -> None:
    global state
    if state == states["READY"]:
        state = states["STOPPED"]
    elif state == states["RUNNING"]:
        state = states["STOPPED"]


def success() -> None:
    global state
    if state == states["CONNECTING"]:
        state = states["READY"]
