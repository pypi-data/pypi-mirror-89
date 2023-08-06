from francium.algorithms.hill_climbing.environment import Environment as HillEnv


class Environment(HillEnv):
    def __init__(self, *args, **kwargs):
        HillEnv.__init__(self, *args, **kwargs)
