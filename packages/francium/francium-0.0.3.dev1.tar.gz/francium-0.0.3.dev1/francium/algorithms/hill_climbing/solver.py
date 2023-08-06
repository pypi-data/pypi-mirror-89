from typing import Optional

from francium.algorithms.hill_climbing.agent import Agent
from francium.algorithms.hill_climbing.environment import Environment
from francium.core import BaseSolver, State, setup_logger

logger = setup_logger(__name__)


class Solver(BaseSolver):
    def __init__(self, agent: Agent, environment: Environment):
        BaseSolver.__init__(self, agent, environment, "Hill Climbing")
        self.initialized: bool = False

    def init_solver(self, init_state: Optional[State] = None):
        if init_state:
            self.memory.add_episode(init_state)
        else:
            init_state = self.env.get_random_init_position()

        logger.info(f"=> Initialized Solver with State: {init_state}")

        self.memory.add_episode(init_state)

        self.initialized = True

    def train_step(self) -> bool:

        if not self.initialized:
            logger.error("=> Solver not initialized !")
            raise Exception("Initialize the solver `solver.init_solver()`")

        curr_state = self.memory.get_curr_state()

        new_state = self.agent(curr_state, self.env)

        eval_val, is_done = self.env.evaluate_state(new_state)

        if is_done:
            logger.info(
                f"=> training is done ! best state: {self.memory.get_curr_state()}"
            )
            return False

        if eval_val < curr_state["z"]:
            # logger.info(f"z: f(x = {new_state['x']}, y = {new_state['y']}) = {eval_val}")
            new_state["z"] = eval_val
            self.memory.add_episode(new_state)

        return True
