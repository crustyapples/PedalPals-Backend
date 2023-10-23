from app import mongo
from bson import ObjectId
class Analytics:
    def __init__(self, user, user_id, avg_speed, total_distance, routes):
        self.user = user
        self.user_id = user_id
        self.avg_speed = avg_speed
        self.total_distance = total_distance
        self.routes = routes

    def save(self):
        analytics_collection = mongo.db.Analytics
        return analytics_collection.insert_one(self.__dict__).inserted_id

    def update_fields(self, fields):
        for field in fields:
            if field in self.__dict__:
                self.__dict__[field] = fields[field]

    def update(self, analytics_id):
        analytics_collection = mongo.db.Analytics
        return analytics_collection.update_one({"_id": ObjectId(analytics_id)}, {"$set": self.__dict__})

    @classmethod
    def find_by_id(cls, analytics_id):
        analytics_collection = mongo.db.Analytics
        analytics = analytics_collection.find_one({"_id": ObjectId(analytics_id)})
        if analytics:
            del analytics['_id']
            return cls(**analytics)
        return None
