from flask_bcrypt import Bcrypt
from bson import ObjectId
from .user_profile import UserProfile
from .analytics import Analytics
from .gamification import Gamification
from app import mongo 

bcrypt = Bcrypt()

class User:
    def __init__(self, name, email, username, user_profile, password=None, friends_list=None):
        self.id = None
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.user_profile = user_profile
        self.friends_list = friends_list if friends_list is not None else []

    def save(self):
        user_collection = mongo.db.User
        self.id = user_collection.insert_one(self.__dict__).inserted_id
        return self.id

    def update_fields(self, fields):
        for field in fields:
            if field in self.__dict__:
                if field == 'user_profile':
                    # get the user_profile object from the database
                    user_profile = UserProfile.find_by_id(self.user_profile)
                    # update the fields
                    user_profile.update_fields(fields[field])
                    # update the user_profile in the database
                    user_profile.update(self.user_profile)
                else: 
                    self.__dict__[field] = fields[field]
                
    def update(self, user_id):
        user_collection = mongo.db.User
        return user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": self.__dict__})

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        user_collection = mongo.db.User
        user = user_collection.find_one({"email": email})
        if user:
            return cls(**user)
        return None

    @classmethod
    def find_by_id(cls, user_id):
        user_collection = mongo.db.User
        
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        # remove the unexpected _id field
        if user:
            del user['_id']
            del user['id']
            return cls(**user)
        
        return None