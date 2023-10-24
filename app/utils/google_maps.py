import requests
from . import config

# Replace 'YOUR_API_KEY' with your actual Google Places API key
API_KEY = config.GOOGLE_MAPS_API

def get_location_coordinates(place_id):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == "OK":
        # Extract latitude and longitude from the response
        location = data['result']['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        print("Unable to fetch coordinates for the selected place.")
        return None

def get_address_suggestions(input_address):
    base_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        "input": input_address,
        "location": "1.354174, 103.688160",
        "radius": 20000,
        "types": "address",
        "key": API_KEY
    }

    response = requests.get(base_url, params=params)

    data = response.json()
    print(data)

    suggestions = []

    if data['status'] == "OK":
        for prediction in data['predictions']:
            suggestion = prediction['description']
            place_id = prediction['place_id']
            suggestions.append((suggestion, place_id))

    return suggestions

    
# def main():
#     address = input("Enter an address: ")

#     suggestions = get_address_suggestions(address)

#     if not suggestions:
#         print("No suggestions found for the entered address.")
#         return

#     print("Suggestions:")
#     for i, (suggestion, _) in enumerate(suggestions, start=1):
#         print(f"{i}. {suggestion}")

#     choice = input("Select an address (enter the number): ")

#     try:
#         choice = int(choice)
#         if 1 <= choice <= len(suggestions):
#             selected_address, place_id = suggestions[choice - 1]
#             coordinates = get_location_coordinates(place_id)
#             if coordinates:
#                 latitude, longitude = coordinates
#                 print(f"Latitude: {latitude}, Longitude: {longitude}")
#             else:
#                 print("Could not fetch coordinates for the selected address.")
#         else:
#             print("Invalid choice. Please select a valid number.")
#     except ValueError:
#         print("Invalid input. Please enter a valid number.")

# if __name__ == "__main__":
#     main()
