from app import mongo
class SocialPost:
    def __init__(self, user, caption, route):
        self.user = user
        self.caption = caption
        self.route = route

    def save(self):
        social_post_collection = mongo.db.social_post
        return social_post_collection.insert_one(self.__dict__)

    @classmethod
    def find_by_id(cls, post_id):
        social_post_collection = mongo.db.social_post
        post = social_post_collection.find_one({"_id": post_id})
        if post:
            return cls(**post)
        return None
