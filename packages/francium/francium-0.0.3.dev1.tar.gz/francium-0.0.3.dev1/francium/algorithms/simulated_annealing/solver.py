from typing import Optional

from francium.algorithms.simulated_annealing.agent import Agent
from francium.algorithms.simulated_annealing.environment import Environment
from francium.core import BaseSolver, setup_logger, State

import numpy as np

logger = setup_logger(__name__)


class Solver(BaseSolver):
    def __init__(
        self,
        agent: Agent,
        environment: Environment,
        initial_temp: float,
        final_temp: float,
        iters_per_temp: int = 100,
        temp_reduction: Optional[str] = None,
        alpha: float = 10.0,
        beta: float = 5.0,
    ):

        BaseSolver.__init__(self, agent, environment, "Simulated Annealing")
        self.initialized: bool = False
        self.curr_temp = initial_temp
        self.final_temp = final_temp
        self.iters_per_temp = iters_per_temp
        self.alpha = alpha
        self.beta = beta

        if temp_reduction == "linear":
            self.temp_decrement = self.linear_temp_reduction
        elif temp_reduction == "geometric":
            self.temp_decrement = self.geometric_temp_reduction
        elif temp_reduction == "slow_decrease":
            self.temp_decrement = self.slow_decrease_temp_reduction
        else:
            logger.info("=> Using linear_temp_reduction")
            self.temp_decrement = self.linear_temp_reduction

    def linear_temp_reduction(self):
        self.curr_temp -= self.alpha

    def geometric_temp_reduction(self):
        self.curr_temp *= 1 / self.alpha

    def slow_decrease_temp_reduction(self):
        self.curr_temp = self.curr_temp / (1 + self.beta * self.curr_temp)

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

        for iter in range(self.iters_per_temp):

            if self.curr_temp <= self.final_temp:
                logger.warning(
                    f"=> curr_temp {self.curr_temp} <= final_temp {self.final_temp} ! cannot anneal further"
                )
                return False

            curr_state: State = self.memory.get_curr_state()

            new_state: State = self.agent(curr_state, self.env)

            eval_val, is_done = self.env.evaluate_state(new_state)

            if is_done:
                logger.info(
                    f"=> training is done ! best state: {self.memory.get_curr_state()}"
                )
                return False

            cost: float = curr_state["z"] - eval_val

            # check if we can update state based on annealing temp.
            can_anneal: bool = np.random.uniform(0, 1) < np.exp(cost / self.curr_temp)

            if cost >= 0 or can_anneal:
                # logger.info(f"z: f(x = {new_state['x']}, y = {new_state['y']}) = {eval_val}")
                new_state["z"] = eval_val

                self.memory.add_episode(new_state)

        # reduce the temperature
        self.temp_decrement()

        return True
