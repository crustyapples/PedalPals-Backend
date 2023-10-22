from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User:
    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.analytics = analytics
        self.gamification = gamification
        self.friends_list = []

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def add_friend(self, friend):
        if friend not in self.friends_list:
            self.friends_list.append(friend)

    def remove_friend(self, friend):
        if friend in self.friends_list:
            self.friends_list.remove(friend)

    def get_nearby_users(self, location):
        # Implementation depends on how users' locations are stored.
        # You would typically use geospatial querying.
        pass

    # ... define other methods ...
