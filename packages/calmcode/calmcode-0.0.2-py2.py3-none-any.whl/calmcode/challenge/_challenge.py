from abc import ABC, abstractmethod


class Challenge(ABC):
    @abstractmethod
    def score(self, solution):
        pass
