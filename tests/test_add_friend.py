import pytest
from flask_testing import TestCase
from app import app, mongo
import json

class TestAddFriend(TestCase):
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

    def test_add_friend(self):
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

        # get user id of testuser2
        user2 = mongo.db.User.find_one({"email": "testuser2@example.com"})
        user2_id = str(user2['_id'])

        # Send a POST request to the add-friend endpoint
        add_friend_response = self.client.post(f'/add-friend/{user2_id}', headers=headers)
        
        self.assertEqual(add_friend_response.status_code, 200)

if __name__ == '__main__':
    pytest.main()
