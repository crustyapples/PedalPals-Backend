import requests
from . import config
import pprint as pp

def get_access_token(email, password):
    url = "https://www.onemap.gov.sg/api/auth/post/getToken"

    payload = {
        "email": email,
        "password": password
    }

    # Make a POST request with JSON payload
    response = requests.post(url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful")
        # Parse the JSON response
        data = response.json()
        print(data)
        # Extract the access_token and expiry_timestamp
        access_token = data.get("access_token")
        expiry_timestamp = data.get("expiry_timestamp")

        return access_token, expiry_timestamp
    else:
        # Print an error message if the request was not successful
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.text)


        
# Function to make the API request
def get_route(start, end):
    url = f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start}&end={end}&routeType=cycle"

    token, expiry_timestamp = get_access_token(config.EMAIL, config.PASSWORD)
    print(token)
    print(expiry_timestamp)


    headers = {"Authorization": f"{token}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    return data

# # Coordinates for the route
# start_coords = "1.3541423,103.6855046"
# end_coords = "1.3466777,103.6782951"
# # Call the function to get the route information
# get_route(start_coords, end_coords)

