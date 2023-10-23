import pytest
from flask_testing import TestCase
from app import app, mongo
import json

class TestUpdate(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb+srv://default:SCSX@a-train.pdzvpay.mongodb.net/PedalPals"  # use a separate test database
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_user_attributes(self):
        # User data for registration
        registration_data = {
            "username": "testuser",
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        # Send a POST request to the registration endpoint
        signup_response = self.client.post('/signup', data=json.dumps(registration_data), content_type='application/json')

        user_id = json.loads(signup_response.get_data(as_text=True))['user_id']

        # User data for login
        login_data = {
            "email": "testuser@example.com",
            "password": "securepassword123"
        }

        # Send a POST request to the login endpoint
        login_response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')

        # Get access token from login response
        response_data = json.loads(login_response.get_data(as_text=True))
        access_token = response_data['access_token']

        # User data for update
        update_data = {
            "username": "updateduser",
            "name": "Updated User",
            "email": "updateduser@example.com",
            "user_profile": {
                "telegram": "updatedtelegram",
                "gamification": {
                    "badge_count": 1,
                    "leadership_position": 5
                },
                "analytics": {
                    "avg_speed": 1,
                    "total_distance": 69
                }
            }
        }

        # Send a PUT request to the user update endpoint
        headers = {'Authorization': f'Bearer {access_token}'}
        update_response = self.client.put(f'/users/{user_id}', data=json.dumps(update_data), content_type='application/json', headers=headers)
        assert update_response.status_code == 200

        # Check if the user attributes in the database are updated
        with self.app.app_context():
            updated_user = mongo.db.User.find_one({"email": "updateduser@example.com"})
            assert updated_user is not None
            assert updated_user['username'] == 'updateduser'
            assert updated_user['name'] == 'Updated User'

if __name__ == '__main__':
    pytest.main()
