class RoutePoint:
    def __init__(coordinates, pointType):
        self.coordinates = coordinates
        self.pointType = pointType

    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
