from app import mongo
class SocialPost:
    def __init__(self, user, user_id, caption, timestamp, route):
        self.user = user
        self.user_id = user_id
        self.caption = caption
        self.timestamp = timestamp
        self.route = route
        self.likes = []
        self.comments = []

    def save(self):
        social_post_collection = mongo.db.Post
        social_post_collection.insert_one(self.__dict__)

    def update(self, route_id):
        social_post_collection = mongo.db.Post
        return social_post_collection.update_one({"_id": ObjectId(route_id)}, {"$set": self.__dict__})

    def update_fields(self, fields):
        for field in fields:
            if field in self.__dict__:
                self.__dict__[field] = fields[field]

    @classmethod
    def find_by_id(cls, post_id):
        social_post_collection = mongo.db.Post
        post = social_post_collection.find_one({"_id": post_id})
        if post:
            return cls(**post)
        return None
