from typing import Dict


class State:
    def __init__(self, init_state: Dict[str, float]):
        self.state_: Dict[str, float] = init_state

    def __repr__(self):
        return str(self.state_)

    def __str__(self):
        return str(self.state_)

    def __getitem__(self, key) -> float:
        return self.state_[key]

    def __setitem__(self, key, new_val):
        self.state_[key] = new_val
