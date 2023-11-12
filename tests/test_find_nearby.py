import pytest
from flask_testing import TestCase
from app import app, mongo
import json

class TestFindNearbyCyclists(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb+srv://default:SCSX@a-train.pdzvpay.mongodb.net/PedalPals"  # use a separate test database
        return app

    def setUp(self):
        self.user_data = [
            {
                "username": "testuser1",
                "name": "Test User 1",
                "email": "testuser1@example.com",
                "password": "securepassword123",
                "location": {"coordinates": "40.758896,-73.985130"}  
            },
            {
                "username": "testuser2",
                "name": "Test User 2",
                "email": "testuser2@example.com",
                "password": "securepassword123",
                "location": {"coordinates": "40.748817,-73.985428"}  
            },
            {
                "username": "testuser3",
                "name": "Test User 3",
                "email": "testuser3@example.com",
                "password": "securepassword123",
                "location": {"coordinates": "1.3525545,103.6810534"}  
            }
        ]

        for user in self.user_data:
            self.client.post('/signup', data=json.dumps(user), content_type='application/json')

    def tearDown(self):
        for user in self.user_data:
            user_in_db = mongo.db.User.find_one({"email": user['email']})
            if user_in_db:
                user_id = str(user_in_db['_id'])
                self.client.delete(f'/users/{user_id}')

    def test_find_nearby_cyclists(self):
        # You might want to modify this depending on how you are obtaining and sending tokens
        login_data = {
            "email": "testuser1@example.com",
            "password": "securepassword123"
        }
        login_response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        access_token = json.loads(login_response.get_data(as_text=True))['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Send a GET request to the find-nearby-cyclists endpoint
        find_cyclists_data = {
            "radius": 5  # in km or miles, depending on your application's settings
        }
        find_cyclists_response = self.client.post('/find-nearby-cyclists', data=json.dumps(find_cyclists_data), content_type='application/json', headers=headers)
        
        self.assertEqual(find_cyclists_response.status_code, 200)

        # Check if the response contains the expected nearby users
        response_data = json.loads(find_cyclists_response.get_data(as_text=True))
        self.assertIn('nearby_users', response_data)
        self.assertEqual(len(response_data['nearby_users']), 1)  # Expecting 1 nearby user
        self.assertIn('testuser2', response_data['nearby_users'][0]['username'])

if __name__ == '__main__':
    pytest.main()
