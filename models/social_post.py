class SocialPost:
    def __init__(self, post_id, caption, date_time, comments=[]):
        self.post_id = post_id
        self.caption = caption
        self.timestamp = datetime.datetime.now()
        self.comments = comments

    # Methods related to social posts here
