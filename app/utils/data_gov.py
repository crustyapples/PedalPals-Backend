import requests
from math import sin, cos, sqrt, atan2, radians

def get_pm25_and_weather(date_time=None, date=None):
    # Define the endpoints
    base_url = "https://api.data.gov.sg/v1/environment/"
    pm25_endpoint = "pm25"
    weather_endpoint = "2-hour-weather-forecast"
    
    # Append the query parameters to the URLs as needed
    if date_time:
        pm25_url = f"{base_url}{pm25_endpoint}?date_time={date_time}"
        weather_url = f"{base_url}{weather_endpoint}?date_time={date_time}"
    elif date:
        pm25_url = f"{base_url}{pm25_endpoint}?date={date}"
        weather_url = f"{base_url}{weather_endpoint}?date={date}"
    else:
        # Default behavior if no date or date_time provided
        pm25_url = f"{base_url}{pm25_endpoint}"
        weather_url = f"{base_url}{weather_endpoint}"
    
    # Make the HTTP GET request to fetch PM2.5 data
    pm25_response = requests.get(pm25_url)
    if pm25_response.status_code != 200:
        return "Failed to fetch PM2.5 data", None
    
    # Make the HTTP GET request to fetch weather data
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        return "Failed to fetch weather data", None
    
    # Parse the JSON response
    pm25_data = pm25_response.json()
    weather_data = weather_response.json()
    
    return pm25_data, weather_data

def get_nearest_pm25_and_weather(latitude, longitude):
    # Call the get_pm25_and_weather function to fetch all the PM2.5 and weather data
    pm25_data, weather_data = get_pm25_and_weather()
    
    # Calculate the distance between the input coordinates and each of the regions in the PM2.5 data
    distances = []
    for region in pm25_data['region_metadata']:
        region_latitude = region['label_location']['latitude']
        region_longitude = region['label_location']['longitude']
        distance = calculate_distance(latitude, longitude, region_latitude, region_longitude)
        distances.append(distance)

    # Find the region with the smallest distance
    min_distance_index = distances.index(min(distances))
    nearest_region = pm25_data['region_metadata'][min_distance_index]['name']

    # Return the PM2.5 and weather data for the nearest region
    pm25_level = pm25_data['items'][0]['readings']['pm25_one_hourly'][nearest_region]

    # Calculate the distance between the input coordinates and each of the regions in the weather data
    distances = []
    for area in weather_data['area_metadata']:
        area_latitude = area['label_location']['latitude']
        area_longitude = area['label_location']['longitude']
        distance = calculate_distance(latitude, longitude, area_latitude, area_longitude)
        distances.append(distance)

    # Find the region with the smallest distance
    min_distance_index = distances.index(min(distances))
    nearest_area = weather_data['area_metadata'][min_distance_index]['name']

    # print(nearest_area)
    # print(weather_data)
    # Return the weather data for the nearest region
    for forecast in weather_data['items'][0]['forecasts']:
        if forecast['area'] == nearest_area:
            weather_forecast = forecast
    
    return pm25_level, weather_forecast

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

# # Call the function with a specific latitude and longitude and print the result
# pm25, weather = get_nearest_pm25_and_weather(latitude=1.35735, longitude=103.7)
# print("Nearest PM2.5 Level:", pm25)
# print("-"*50)
# print("Nearest Weather Forecast:", weather)
