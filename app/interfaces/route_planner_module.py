from abc import ABC, abstractmethod
from app.interfaces import route_planner_module as RoutePlanner
from app.utils.one_maps import get_route
from app.utils.data_gov import get_nearest_pm25_and_weather

class RoutePlanner(ABC):
        @abstractmethod
        def calculate_route(self, start, end):
            pass
