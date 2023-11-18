from app.interfaces.route_planner_module import RoutePlanner

class AlternativePlanner(RoutePlanner):
    def calculate_route(self, start, end):
        """
        Retrieves the optimal route between two points using an alternative module.
        
        :param start: A string representing the starting coordinates of the route.
        :param end: A string representing the ending coordinates of the route.
        :return: A dictionary containing the route information.
        """
        
        pass