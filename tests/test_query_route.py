import pytest
from flask_testing import TestCase
from app import app, mongo
import json

class TestCyclingRoute(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb+srv://default:SCSX@a-train.pdzvpay.mongodb.net/PedalPals"  # use a separate test database
        return app

    def test_cycling_route(self):
        # 1. Use address_autocomplete for a start and end address and take the first suggestion of both
        start_address_data = {"input_address": "Nanyang Crescent"}
        end_address_data = {"input_address": "Bedok South Avenue 1"}

        start_suggestions_response = self.client.get('/address-autocomplete', data=json.dumps(start_address_data), content_type='application/json')
        end_suggestions_response = self.client.get('/address-autocomplete', data=json.dumps(end_address_data), content_type='application/json')

        start_suggestions = json.loads(start_suggestions_response.get_data(as_text=True))
        end_suggestions = json.loads(end_suggestions_response.get_data(as_text=True))

        start_place_id = start_suggestions[0][1]
        end_place_id = end_suggestions[0][1]

        # 2. Use reverse_geocode to get the place_id of both
        start_location_response = self.client.get('/reverse-geocode', data=json.dumps({"place_id": start_place_id}), content_type='application/json')
        end_location_response = self.client.get('/reverse-geocode', data=json.dumps({"place_id": end_place_id}), content_type='application/json')

        # for start_location and end_location which returns a tuple of the coordinates, convert them to a string and strip any white space
        start_location = str(start_location_response.get_data(as_text=True)).strip()
        end_location = str(end_location_response.get_data(as_text=True)).strip()

        # 3. Use the coordinates to fetch the route using get_cycling_path
        cycling_route_data = {
            "start_address": start_location[1:-1],
            "end_address": end_location[1:-1]
        }

        print(cycling_route_data)

        cycling_route_response = self.client.get('/get_cycling_route', data=json.dumps(cycling_route_data), content_type='application/json')
        cycling_route = json.loads(cycling_route_response.get_data(as_text=True))

        self.assertEqual(cycling_route_response.status_code, 200)
        self.assertIn('status_message', cycling_route)

if __name__ == '__main__':
    pytest.main()
