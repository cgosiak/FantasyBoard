class Player(object):

    def __init__(self, name, position, projected_points, cost):
        self.name = name
        self.position = position
        self.projected_points = projected_points
        self.cost = cost
        self.used = False
        self.can_be_used = True
        self.is_flex = False

    def is_used(self):
        return self.used

    def can_be_used(self):
        return self.can_be_used

    def dont_use_player(self):
        self.used = False
        self.can_be_used = False

    def is_flex_choice(self):
        return self.is_flex

    def no_longer_flex(self):
        self.is_flex = False

    def make_flex_choice(self):
        self.is_flex = True

    def use_player(self):
        self.used = True

    def return_on_investment(self):
        roi = float(self.projected_points/self.cost)
        return roi

    def player_points(self):
        return self.projected_points

    def name(self):
        return self.name

    def cost(self):
        return self.cost

    def position(self):
        return self.position