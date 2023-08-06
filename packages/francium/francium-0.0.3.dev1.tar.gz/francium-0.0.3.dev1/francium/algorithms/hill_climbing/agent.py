from francium.algorithms.hill_climbing.environment import Environment
from francium.core import BaseAgent, State, BaseEnvironment

import numpy as np


class Agent(BaseAgent):
    """Hill Climbing AI Agent"""

    def __init__(self, step_size: float = 1e-2):
        self.step_size = step_size

    def act(self, state: State, env: Environment):
        # get the current state, act upon it and give a new state
        new_state = State({"x": state["x"], "y": state["y"]})
        new_state["x"] += np.random.randn() * self.step_size
        new_state["y"] += np.random.randn() * self.step_size

        # check if you are in bounds of the environment
        new_state["x"] = min(max(new_state["x"], env.x_bounds[0]), env.x_bounds[1])
        new_state["y"] = min(max(new_state["y"], env.y_bounds[0]), env.y_bounds[1])

        return new_state
