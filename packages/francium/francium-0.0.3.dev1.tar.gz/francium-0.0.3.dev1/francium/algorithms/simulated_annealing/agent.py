from francium.algorithms.hill_climbing.agent import Agent as HillAgent


class Agent(HillAgent):
    def __init__(self, *args, **kwargs):
        HillAgent.__init__(self, *args, **kwargs)
