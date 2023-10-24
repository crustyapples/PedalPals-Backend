class Location:
    def __init__(self, gps_permission=None, coordinates=None):
        self.gps_permission = gps_permission
        self.coordinates = coordinates

    def to_dict(self):
        return {
            'gps_permission': self.gps_permission,
            'coordinates': self.coordinates
        }

    def has_gps_permission(self):
        return self.gps_permission

    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    # ... define other methods ...
