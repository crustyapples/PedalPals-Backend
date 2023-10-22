class Location:
    def __init__(self, gps_permission, has_data):
        self.gps_permission = gps_permission
        self.has_data = has_data

    def has_gps_permission(self):
        return self.gps_permission

    # ... define other methods ...
