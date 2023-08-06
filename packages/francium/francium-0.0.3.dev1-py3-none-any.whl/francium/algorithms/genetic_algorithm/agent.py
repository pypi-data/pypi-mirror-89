from typing import Tuple

from francium.algorithms.genetic_algorithm.environment import Environment
from francium.core import State, setup_logger, BaseAgent

import numpy as np

logger = setup_logger(__name__)


class Agent(BaseAgent):
    """Genetic Algorithm Agent"""

    def __init__(self):
        self.population = []
        self.initialized = False

    def init_agent(
        self,
        pop_size: int,
        x_bounds: Tuple[float, float],
        y_bounds: Tuple[float, float],
    ):
        x_min, x_max = x_bounds
        y_min, y_max = y_bounds

        population = []
        for _ in range(pop_size):
            individual = State(
                {
                    "x": np.random.uniform(x_min, x_max),
                    "y": np.random.uniform(y_min, y_max),
                }
            )

            population.append(individual)

        self.population = population

        self.initialized = True

    def sort_population_by_fitness(self, fitness_func):
        return sorted(self.population, key=fitness_func)

    @staticmethod
    def choice_by_roulette(sorted_population, fitness_sum, fitness_func):
        offset = 0
        normalized_fitness_sum = fitness_sum

        lowest_fitness = fitness_func(sorted_population[0])
        if lowest_fitness < 0:
            offset = -lowest_fitness
            normalized_fitness_sum += offset * len(sorted_population)

        draw = np.random.uniform(0, 1)

        accumulated = 0
        for individual in sorted_population:
            fitness = fitness_func(individual) + offset
            probability = fitness / normalized_fitness_sum
            accumulated += probability

            if draw <= accumulated:
                return individual

    @staticmethod
    def crossover(individual_a, individual_b):
        xa = individual_a["x"]
        ya = individual_a["y"]

        xb = individual_b["x"]
        yb = individual_b["y"]

        return {"x": (xa + xb) / 2, "y": (ya + yb) / 2}

    @staticmethod
    def mutate(individual, x_bounds, y_bounds):
        x_min, x_max = x_bounds
        y_min, y_max = y_bounds

        next_x = individual["x"] + np.random.uniform(-0.05, 0.05)
        next_y = individual["y"] + np.random.uniform(-0.05, 0.05)

        # Guarantee we keep inside boundaries
        next_x = min(max(next_x, x_min), x_max)
        next_y = min(max(next_y, y_min), y_max)

        return State({"x": next_x, "y": next_y})

    def act(self, env: Environment):

        if not self.initialized:
            logger.error(
                "=> initialize the agent: `agent.init_agent(pop_size, x_bounds, y_bounds)`"
            )
            raise Exception("Agent not Initialized")

        next_generation = []
        sorted_by_fitness_population = self.sort_population_by_fitness(env.fitness_func)
        population_size = len(self.population)
        fitness_sum = sum(
            env.fitness_func(individual) for individual in self.population
        )

        for i in range(population_size):
            first_choice = self.choice_by_roulette(
                sorted_by_fitness_population, fitness_sum, env.fitness_func
            )
            second_choice = self.choice_by_roulette(
                sorted_by_fitness_population, fitness_sum, env.fitness_func
            )

            individual = self.crossover(first_choice, second_choice)
            individual = self.mutate(individual, env.x_bounds, env.y_bounds)
            next_generation.append(individual)

        self.population = next_generation

        best_individual = self.sort_population_by_fitness(env.fitness_func)[-1]

        # best individual is the new state
        new_state = State({"x": best_individual["x"], "y": best_individual["y"]})

        return new_state
