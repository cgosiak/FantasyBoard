from Player import *


class FantasyBoard(object):

    def __init__(self, available_bank):

        self.available_bank = available_bank
        self.position_keys = []
        self.all_players = {}
        self.required_players = {}
        self.first_run = True
        self.flex = Player(None, None, None, None)

    def add_player(self, name, position, points, cost):

        if position not in self.position_keys:
            self.position_keys.append(position)
            self.all_players[position] = []
        else:
            self.all_players[position].append(Player(name, position, points, cost))

    def get_required(self):
        for key in self.position_keys:
            x = int(input("How Many Players Do You Need to Fill the Position " + key + ": "))
            self.required_players[key] = x

    def get_best(self, key):
        best_points = 0
        best_choice = Player(None, None, None, None)

        for player in self.all_players[key]:
            if (player.player_points() > best_points):
                if (not player.is_used()):
                    if (not player.dont_use_player()):
                        best_points = player.player_points()
                        best_choice = player

        best_choice.use_player()

        return best_choice

    def get_next_best(self, key):
        best_points = 0
        best_choice = Player(None, None, None, None)

        for player in self.all_players[key]:
            if (player.player_points() > best_points):
                if (not player.is_used()):
                    if (not player.dont_use_player()):
                        best_points = player.player_points()
                        best_choice = player

        return best_choice

    def print_best_choices(self):
        print("\n\n:::::: BEST CHOICES ::::::::::::::::::::::::::::::::::::")
        for key in self.position_keys:
            print("\nBest Choices for Position: " + key)
            for player in self.all_players[key]:
                if player.is_used():
                    print(key + " choice: " + player.name)

        print("\nBest Choices for Position: FLEX")
        print("FLEX choice: " + self.flex.name)

    def total_cost(self):
        tot_cost = 0
        for key in self.position_keys:
            for player in self.all_players[key]:
                if player.is_used():
                    tot_cost += player.cost

        tot_cost += self.flex.cost

        return tot_cost

    def total_points(self):
        tot_pts = 0
        for key in self.position_keys:
            for player in self.all_players[key]:
                if player.is_used():
                    tot_pts += player.player_points()

        tot_pts += self.flex.player_points()

        return tot_pts

    def make_flex_choice(self):
        keys = ["WR", "TE", "RB"]

        best_points = 0
        best_choice = Player(None, None, None, None)

        for key in keys:
            guess = self.get_next_best(key)
            if (guess.player_points() > best_points):
                best_choice = guess
                best_points = guess.player_points()

        best_choice.make_flex_choice()
        self.flex = best_choice

    def current_best_choice_for_replacement_in_position(self, key):
        # ROI is best locally

        used = []
        unused = []

        replace_this = Player(None, None, None, None)
        replace_with = Player(None, None, None, None)

        first_run_local = True
        min_change_roi = 0

        for player in self.all_players[key]:
            if player.is_used():
                used.append(player)
            else:
                unused.append(player)

        for player_used in used:
            for player_check in unused:
                if first_run_local:
                    replace_this = player_used
                    replace_with = player_check
                    min_change_roi = replace_this.return_on_investment() - replace_with.return_on_investment()
                    first_run_local = False
                else:
                    if (player_used.return_on_investment() - player_check.return_on_investment() < min_change_roi):
                        replace_this = player_used
                        replace_with = player_check
                        min_change_roi = replace_this.return_on_investment() - replace_with.return_on_investment()

        return min_change_roi, replace_this, replace_with

    def best_replacement(self):
        self.flex.no_longer_flex()
        replace_this = Player(None, None, None, None)
        replace_with = Player(None, None, None, None)

        first_run_local = True
        min_change_roi = 0

        for key in self.position_keys:
            if (first_run_local):
                min_change_roi, replace_this, replace_with = self.current_best_choice_for_replacement_in_position(key)
                first_run_local = False
            else:
                tmp_min_change_roi, tmp_replace_this, tmp_replace_with = self.current_best_choice_for_replacement_in_position(key)
                if (tmp_min_change_roi < min_change_roi):
                    min_change_roi = tmp_min_change_roi
                    replace_this = tmp_replace_this
                    replace_with = tmp_replace_with

        replace_this.dont_use_player()
        replace_with.use_player()

        self.make_flex_choice()


    def get_best_choices(self):
        if (self.first_run):
            for key in self.position_keys:
                for choice in range(self.required_players[key]):
                    new_choice = self.get_best(key)

            self.first_run = False
            self.make_flex_choice()
        else:
            self.best_replacement()

        if (self.total_cost() <= self.available_bank):
            self.print_best_choices()
            print("\nSpent " + str(self.total_cost()))
            print("Points " + str(self.total_points()))

        else:
            self.print_best_choices()
            print("Not Enough Bank! Trying to Spend " + str(self.total_cost()))
            self.get_best_choices()





