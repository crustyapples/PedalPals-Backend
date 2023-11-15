from abc import ABC, abstractmethod

# RewardsStrategy base class
class RewardsStrategy(ABC):

    @abstractmethod
    def calculate_difficulty(self, route_distance):
        pass
    
    @abstractmethod
    def calculate_points(self, route_distance):
        pass


    @abstractmethod
    def calculate_badges(self, route_distance):
        pass


