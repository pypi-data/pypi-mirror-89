from francium.algorithms.genetic_algorithm.agent import Agent
from francium.algorithms.genetic_algorithm.environment import Environment
from francium.core import BaseSolver, setup_logger

logger = setup_logger(__name__)


class Solver(BaseSolver):
    def __init__(self, agent: Agent, environment: Environment, pop_size: int = 100):
        BaseSolver.__init__(self, agent=agent, environment=environment, solver_type="Genetic Algorithm")
        self.initialized: bool = False
        self.pop_size = pop_size

    def init_solver(self):
        self.agent.init_agent(self.pop_size, self.env.x_bounds, self.env.y_bounds)

        logger.info(f"=> Initialized Agent !")

        self.initialized = True

    def train_step(self) -> bool:

        if not self.initialized:
            logger.error("=> Solver not initialized !")
            raise Exception("Initialize the solver `solver.init_solver()`")

        new_state = self.agent(self.env)

        eval_val, is_done = self.env.evaluate_state(new_state)

        if is_done:
            logger.info(
                f"=> training is done ! best state: {self.memory.get_curr_state()}"
            )
            return False

        # logger.info(f"z: f(x = {new_state['x']}, y = {new_state['y']}) = {eval_val}")
        new_state["z"] = eval_val
        self.memory.add_episode(new_state)

        return True
