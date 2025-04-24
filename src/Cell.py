from State import State


class Cell:

    def __init__(self, initial_status = State.DEAD):
        self.state: State = initial_status

    def __repr__(self):
        return f"{self.state.value}"
