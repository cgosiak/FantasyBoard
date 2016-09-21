from FantasyBoard import *


def Football():

    # my_file = str(input("INPUT FILE: "))
    my_file = "/home/caleb/Desktop/Py/players.csv"

    file = open(my_file, 'r')

    # Create global
    FB = FantasyBoard(50)

    for line in file:
        line = line.replace('\n', '')
        split = line.split(',')
        FB.add_player(str(split[0]), str(split[1]), int(split[2]), int(split[3]))

    # Get required amounts
    FB.get_required()

    FB.get_best_choices()


if __name__ == '__main__':
    Football()