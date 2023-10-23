from bson import ObjectId
from app import mongo
class Gamification:
    def __init__(self, user, badgeCount, leadership_position, badges):
        self.user = user
        self.badgeCount = badgeCount
        self.leadership_position = leadership_position
        self.badges = badges

    def save(self):
        gamification_collection = mongo.db.Gamification
        return gamification_collection.insert_one(self.__dict__).inserted_id

    def update_fields(self, fields):
        for field in fields:
            if field in self.__dict__:
                self.__dict__[field] = fields[field]
            

    def update(self, gamification_id):
        gamification_collection = mongo.db.Gamification
        return gamification_collection.update_one({"_id": ObjectId(gamification_id)}, {"$set": self.__dict__})

    @classmethod
    def find_by_id(cls, gamification_id):
        gamification_collection = mongo.db.Gamification
        gamification = gamification_collection.find_one({"_id": ObjectId(gamification_id)})
        if gamification:
            del gamification['_id']
            return cls(**gamification)
        return None
