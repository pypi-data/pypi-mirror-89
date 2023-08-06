from typing import List

from .state import State


class Memory:
    def __init__(self, retain_mem: bool = True):
        self.retain_mem = retain_mem
        self.memory: List[State] = []
        self.best_episode = None

    def __iter__(self):
        return MemoryIterator(self)

    def get_episode(self, episode: int) -> State:
        # return the state from `episode`
        return self.memory[episode]

    def add_episode(self, state: State) -> None:
        self.memory.append(state)

        if self.best_episode is None or state["z"] < self.best_episode["z"]:
            self.best_episode = state

    def get_curr_state(self) -> State:
        # return from the latest state
        return self.memory[-1]


class MemoryIterator:
    def __init__(self, memory):
        self.memory_ = memory
        self.index_ = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index_ < len(self.memory_.memory):
            result = self.memory_.memory[self.index_]
            self.index_ += 1
            return result
        raise StopIteration
