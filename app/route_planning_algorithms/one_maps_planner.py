from app.interfaces.route_planner_module import RoutePlanner
from app.utils.one_maps import get_route
from app.utils.data_gov import get_nearest_pm25_and_weather

class OneMapsPlanner(RoutePlanner):
    def calculate_route(self, start, end):
        """
        Retrieves the optimal route between two points using the get_route function from the one_maps module.
        
        :param start: A string representing the starting coordinates of the route.
        :param end: A string representing the ending coordinates of the route.
        :return: A dictionary containing the route information.
        """
        result = get_route(start, end)
        route_instructions = result.get('route_instructions')
        route_start_coordinates = route_instructions[0][3]
        route_end_coordinates = route_instructions[-1][3]
        latitude, longitude = route_start_coordinates.split(',')
        
        try:
            pm25, weather = get_nearest_pm25_and_weather(latitude=float(latitude), longitude=float(longitude))
            # add the pm25 and weather data to the result
            weather = {
                "PM25": pm25,
                "weather": weather
            }
            result.update(weather)
        except:
            pass
        
        return result