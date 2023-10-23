from app import mongo
from bson import ObjectId
from app.models.analytics import Analytics
from app.models.gamification import Gamification

class UserProfile:
    def __init__(self, user_id, name, telegram, instagram, email, pals, points, friends, analytics, gamification):
        self.id = None
        self.user_id = user_id
        self.name = name
        self.telegram = telegram
        self.instagram = instagram
        self.email = email
        self.pals = pals
        self.points = points
        self.friends = friends
        self.analytics = analytics
        self.gamification = gamification

    def save(self):
        user_profile_collection = mongo.db.User_Profile
        self.id = user_profile_collection.insert_one(self.__dict__).inserted_id
        return self.id

    def update_fields(self, fields):
        for field in fields:
            if field in self.__dict__:
                if field == 'analytics':
                    # get the analytics object from the database
                    analytics = Analytics.find_by_id(self.analytics)
                    # update the fields
                    analytics.update_fields(fields[field])
                    # update the analytics in the database
                    analytics.update(self.analytics)
                elif field == 'gamification':
                    # get the gamification object from the database
                    gamification = Gamification.find_by_id(self.gamification)
                    # update the fields
                    gamification.update_fields(fields[field])
                    # update the gamification in the database
                    gamification.update(self.gamification)
                else:
                    self.__dict__[field] = fields[field]

    def update(self, user_profile_id):
        user_profile_collection = mongo.db.User_Profile
        return user_profile_collection.update_one({"_id": ObjectId(user_profile_id)}, {"$set": self.__dict__})

    @classmethod
    def find_by_id(cls, profile_id):
        user_profile_collection = mongo.db.User_Profile
        profile = user_profile_collection.find_one({"_id": ObjectId(profile_id)})
        if profile:
            del profile['_id']
            del profile['id']
            return cls(**profile)
        return None
