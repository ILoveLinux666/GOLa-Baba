from State import State


class Cell:

    def __init__(self):
        self.state: State = State.DEAD

    def __repr__(self):
        return f"{self.state}"
