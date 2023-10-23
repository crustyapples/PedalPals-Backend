import pytest
from flask_testing import TestCase
from app import app, mongo
import json

class TestAuth(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb+srv://default:SCSX@a-train.pdzvpay.mongodb.net/PedalPals"  # use a separate test database
        return app

    def setUp(self):
        pass

    def tearDown(self):
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        # Send a POST request to the login endpoint
        login_response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        user_id = json.loads(login_response.get_data(as_text=True))['user_id']

        delete_response = self.client.delete(f'/users/{user_id}')
        assert delete_response.status_code == 200

    def test_user_registration_and_login(self):
        # User data for registration
        registration_data = {
            "username": "testuser",
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        # Send a POST request to the registration endpoint
        registration_response = self.client.post('/signup', data=json.dumps(registration_data), content_type='application/json')
        self.assertEqual(registration_response.status_code, 201)

        # Check if the user is in the database after registration
        user = mongo.db.User.find_one({"email": "testuser@example.com"})
        self.assertIsNotNone(user)

        # User data for login
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        # Send a POST request to the login endpoint
        login_response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(login_response.status_code, 200)

        # Check if the response contains an access token after login
        response_data = json.loads(login_response.get_data(as_text=True))
        self.assertIn('access_token', response_data)

if __name__ == '__main__':
    pytest.main()
