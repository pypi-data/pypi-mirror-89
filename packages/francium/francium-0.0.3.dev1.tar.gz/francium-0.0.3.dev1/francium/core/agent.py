from abc import abstractmethod, ABC

from .state import State


class BaseAgent(ABC):
    @abstractmethod
    def act(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs) -> State:
        return self.act(*args, **kwargs)
