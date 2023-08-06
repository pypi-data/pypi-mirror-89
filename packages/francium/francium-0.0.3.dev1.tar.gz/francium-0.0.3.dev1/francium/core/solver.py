from abc import abstractmethod, ABC

from .agent import BaseAgent
from .environment import BaseEnvironment
from .memory import Memory
from .logger import setup_logger

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

sns.set()


logger = setup_logger(__name__)


class BaseSolver(ABC):
    def __init__(self, agent: BaseAgent, environment: BaseEnvironment, solver_type: str = None):
        self.agent: BaseAgent = agent
        self.env: BaseEnvironment = environment
        self.memory: Memory = Memory(retain_mem=True)
        self.initialized: bool = False
        self.solve_type = solver_type

    def plot_history(self):

        # plot the sphere_function and the search_space
        x_min, x_max = self.env.x_bounds
        y_min, y_max = self.env.y_bounds

        x = np.linspace(x_min, x_max, 50)
        y = np.linspace(y_min, y_max, 50)

        X, Y = np.meshgrid(x, y)

        Z = self.env.evaluation_func(X, Y)

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(25, 10))

        cp = ax1.contourf(X, Y, Z, 50, alpha=0.6, cmap=cm.bwr)
        fig.colorbar(cp)  # Add a colorbar to a plot

        x_states = [mem["x"] for mem in iter(self.memory)]
        y_states = [mem["y"] for mem in iter(self.memory)]

        ax1.plot(
            x_states,
            y_states,
            color="black",
            marker=".",
            alpha=0.5,
            linewidth=1,
            markersize=1,
        )
        ax1.plot(x_states[0], y_states[0], color="red", marker="o")
        ax1.plot(x_states[-1], y_states[-1], color="green", marker="o")

        ax1.set_xlabel("x")
        ax1.set_ylabel("y")

        ax1.legend(["search_path", "start_state", "end_state"])

        # plot the loss

        z_states = [mem["z"] for mem in iter(self.memory)]

        ax2.plot(z_states, marker=".")

        ax2.set_xlabel("iterations")
        ax2.set_ylabel("loss")

        ax2.legend(["loss"])

        if self.solve_type:
            fig.suptitle(self.solve_type, fontsize=20)

            plt.tight_layout()

            plt.subplots_adjust(top=0.95)

        plt.show()

    @abstractmethod
    def train_step(self) -> bool:
        raise NotImplementedError
