class Route:
    def __init__(self, distance, speed, start_coordinates, end_coordinates, start_time, end_time, route_status, traffic_info, weather_status, route_difficulty):
        self.distance = distance
        self.speed = speed
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates
        self.start_time = start_time
        self.end_time = end_time
        self.route_status = route_status
        self.traffic_info = traffic_info
        self.weather_status = weather_status
        self.route_difficulty = route_difficulty

    # Methods for manipulating route data

    def getDistance(self):
        return self.distance

    def setDistance(self, distance):
        self.distance = distance
    
    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getStartCoordinates(self):
        return self.start_coordinates

    def setStartCoordinates(self, start_coordinates):
        self.start_coordinates = start_coordinates
    
    def getEndCoordinates(self):
        return self.end_coordinates

    def setEndCoordinates(self, end_coordinates):
        self.end_coordinates = end_coordinates

    def getStartTime(self):
        return self.start_time

    def setStartTime(self, start_time):
        self.start_time = start_time

    def getEndTime(self):
        return self.end_time

    def setEndTime(self, end_time):
        self.end_time = end_time

    def getRouteStatus(self):
        return self.route_status

    def getTrafficInfo(self):
        return self.traffic_info

    def getWeatherStatus(self):
        return self.weather_status

    def getRouteDifficulty(self):
        return self.route_difficulty


