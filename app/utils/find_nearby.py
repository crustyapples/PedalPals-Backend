from geopy.distance import geodesic

def find_nearby_coordinates(target, radius_km, coordinates):
    """
    Find all coordinates within a certain radius of a target coordinate.

    :param target: A tuple of (latitude, longitude) representing the target coordinate
    :param radius_km: The search radius in kilometers
    :param coordinates: A list of tuples, where each tuple represents a coordinate (latitude, longitude)
    :return: A list of coordinates (as tuples) that are within the search radius of the target coordinate
    """
    nearby_coords = []

    for coord in coordinates:
        distance = geodesic(target, coord).kilometers
        if distance <= radius_km:
            nearby_coords.append(coord)

    return nearby_coords


# target_coordinate = (40.748817, -73.985428)  # Example: The latitude and longitude for the Empire State Building
# search_radius_km = 5  # Search within 5 kilometers
# list_of_coordinates = [
#     (40.748817, -73.985428),  # Empire State Building
#     (40.758896, -73.985130),  # Times Square
#     (40.712776, -74.005974),  # Statue of Liberty
#     (1.3525545,103.6810534)
#     # Add more coordinates as needed
# ]

# nearby_coordinates = find_nearby_coordinates(target_coordinate, search_radius_km, list_of_coordinates)
# print(nearby_coordinates)
