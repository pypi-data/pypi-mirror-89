from abc import abstractmethod, ABC
from typing import Tuple, Optional

from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from francium.core import State

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm

import seaborn as sns

from .eval_functions import *

sns.set()


class BaseEnvironment(ABC):
    def __init__(
        self,
        x_bounds: Tuple[float, float],
        y_bounds: Tuple[float, float],
        goal_val: Optional[State] = None,
        tolerance: Optional[float] = 1e-4,
        eval_func=convex_x_square,
    ):
        self.goal_val: State = goal_val
        self.tolerance: float = tolerance
        self.x_bounds: Tuple[float, float] = x_bounds
        self.y_bounds: Tuple[float, float] = y_bounds
        self.eval_func_ = eval_func

    def get_random_init_position(self) -> State:
        x_min, x_max = self.x_bounds
        y_min, y_max = self.y_bounds

        init_state: State = State(
            {
                "x": np.random.uniform(low=x_min, high=x_max),
                "y": np.random.uniform(low=y_min, high=y_max),
            }
        )

        z, _ = self.evaluate_state(init_state)

        init_state["z"] = z

        return init_state

    def plot_environment(self):
        x_min, x_max = self.x_bounds
        y_min, y_max = self.y_bounds

        fig = plt.figure(figsize=(25, 10))

        # plot the 3d sphere function

        ax1 = fig.add_subplot(1, 2, 1, projection="3d")

        x = np.linspace(x_min, x_max, 50)
        y = np.linspace(y_min, y_max, 50)

        X, Y = np.meshgrid(x, y)

        Z = self.evaluation_func(X, Y)

        z_min, z_max = np.min(Z), np.max(Z)

        ax1.plot_surface(
            X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none", alpha=0.7
        )
        cset = ax1.contour(X, Y, Z, zdir="z", offset=z_min, cmap=cm.coolwarm)
        cset = ax1.contour(X, Y, Z, zdir="x", offset=x_min, cmap=cm.coolwarm)
        cset = ax1.contour(X, Y, Z, zdir="y", offset=y_max, cmap=cm.coolwarm)
        ax1.view_init(60, 35)

        ax1.set_xlabel("X")
        ax1.set_xlim(x_min, x_max)

        ax1.set_ylabel("Y")
        ax1.set_ylim(y_min, y_max)

        ax1.set_zlabel("Z")
        ax1.set_zlim(z_min, z_max)

        # plot the contours
        ax2 = fig.add_subplot(1, 2, 2)

        cp = ax2.contourf(X, Y, Z, 50, alpha=0.6, cmap=cm.bwr)
        fig.colorbar(cp)  # Add a colorbar to a plot

        fig.suptitle("Environment", fontsize=20)

        plt.tight_layout()

        plt.subplots_adjust(top=0.95)

        plt.show()

    def fitness_func(self, state: State) -> float:
        eval_val = self.evaluation_func(state["x"], state["y"])
        return eval_val

    def evaluation_func(self, *args, **kwargs):
        return self.eval_func_(*args, **kwargs)

    @abstractmethod
    def evaluate_state(self, state: State) -> Tuple[float, bool]:
        raise NotImplementedError
