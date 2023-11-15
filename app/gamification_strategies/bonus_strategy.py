from app.interfaces.rewards_strategy import RewardsStrategy


# BonusPointsStrategy concrete class
class BonusPointsStrategy(RewardsStrategy):

    def calculate_difficulty(self, route_distance):
        # Implement bonus difficulty calculation logic
        if route_distance < 5:
            return 'Easy'
        elif route_distance < 10:
            return 'Medium'
        else:
            return 'Hard'

    def calculate_points(self, route_distance):
        # Implement bonus point calculation logic
        if self.calculate_difficulty(route_distance) == "Easy":
            return route_distance * 1 * 2
        elif self.calculate_difficulty(route_distance) == "Medium":
            return route_distance * 2 * 2
        else:
            return route_distance * 3 * 2


    def calculate_badges(self, route_distance):
    # Implement bonus badge calculation logic
        if self.calculate_difficulty(route_distance) == "Easy":
            return 'bronze'
        elif self.calculate_difficulty(route_distance) == "Medium":
            return 'silver'
        else:  
            return 'gold'