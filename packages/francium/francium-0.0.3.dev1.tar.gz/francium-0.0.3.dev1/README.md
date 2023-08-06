<h1 align="center">Projekt Francium</h1>

<div align="center">
<img src="https://raw.githubusercontent.com/satyajitghana/ProjektFrancium/master/logo.png">
</div>

---

A package to test out AI Algorithms in Python

## Install

```shell script
pip install git+https://github.com/satyajitghana/ProjektFrancium
```

## [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/satyajitghana/ProjektFrancium/blob/master/FranciumColab.ipynb)

## Example Usage

```python
import francium.algorithms.hill_climbing as hc
import francium.core.eval_functions as eval_functions
from francium.core import State

agent = hc.Agent(step_size=1e-1)
env = hc.Environment(x_bounds=(-5.0, 5.0), y_bounds=(-5.0, 5.0), eval_func=eval_functions.sinx_plus_x)
solver = hc.Solver(agent=agent, environment=env)

solver.init_solver(
    init_state=State({
        'x': 4.0,
        'y': 2.0,
        'z': env.evaluation_func(4.0, 2.0)
    })
)

for episode in range(1000):
    trainable = solver.train_step()
    if not trainable:
        break

solver.plot_history()

env.plot_environment()

```

see `notebooks` for more examples

---

<h3 align="center">Made with 💘 by shadowleaf</h3>
