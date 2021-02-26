# IF A TREE FALLS IN A FOREST DOES IT MAKE A SOUND IF YOU ARE NOT THERE TO HEAR IT --HISENBERG
# WALK THE PLANCK
# IS SPACE HALF EMPTY? OR HALF FULL?
# PRESERVE THE BITS (POPULATION) AND SHUFFLE ON EXAMINATION? [4th dimmension]
# 5th dimmension hides the state of the 4th
# TODO: HAMMING CODES (jk)
# TDIL, well, yesterday, of Jan Amb

class Grid:
    # GRID N**D grid, S(eed)
    # Example [8][8] or 64 (bits)
    N: int
    D: int
    S: int

    def __init__(self, n: int = N, d: int = D, s: int = S):
        """n**d/log(2)"""
        self.__value = int(s)
        self.n = n
        # assert 0 < d <= 3  # My mere human brain can not handle the 4th dimension, but conceptually tuple would work

    def peek(self, *pos, **kwargs) -> bool:
        assert len(pos) == self.d
        assert all([type(x) is int for x in pos])
        # TODO: convert *pos tuple into integer. (Like converting a number to binary [given a 2 dimensional grid]).
        # TODO: "peek log"

    def flip(self, *pos, **kwargs):
        self.__value ^= sum([self.n ** d if bit else 0 for d in range(self.d)])

    def __hash__(self):
        return self.__value
        # TODO: finish psuedo


class Point(Grid):
    N = 0
    D = 0


class Field(Grid):
    D = 2


class BattleField(Field):
    def __str__(self):
        pass
        return """        
#########  BATTLE SHIP  #########
# # # A # B # C # D # E # F # G #
#################################
# 1 #   #   #   #   #   #   #   #
# 2 #   #   #   #   #   #   #   #
# 3 #   #   #   #   #   #   #   #
# 4 #   #   #   #   #   #   #   #
# 5 #   #   #   #   #   #   #   #
# 6 #   #   #   #   #   #   #   #
# 7 #   #   #   #   #   #   #   #
# 8 #   #   #   #   #   #   #   #
#################################
"""


class BattleShip:
    def __init__(self):
        players = 2
        self.grids = [BattleField() for player in range(players)]

    def play(self):
        while True:
            user_input = input()
            args = user_input.split()
            for g, grid in enumerate(self.grids):
                print(grid)

    def fire(self, x, y):
        if self.grids[0].peek(x, y):
            print("hit!")
        else:
            print("miss.")


battleship = BattleShip()
battleship.play()
