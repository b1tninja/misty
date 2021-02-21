# IF A TREE FALLS IN A FOREST DOES IT MAKE A SOUND IF YOU ARE NOT THERE TO HEAR IT --HISENBERG
# WALK THE PLANCK

class Grid:
    # GRID N**D grid, S(eed)
    # Example [8][8] or 64 (bits)
    N = 8  # LENGTH
    D = 2  # DIMMENSIONS
    S = 0  # SEED

    def __init__(self, n: int = N, d: int = D, s: int = S):
        """n**2/log(2)"""
        self.__value = int(s)
        self.n = n
        # assert 0 < d <= 3  # My mere human brain can not handle the 4th dimension, but conceptually tuple would work

    def peek(self, *pos, **kwargs) -> bool:
        assert len(pos) == self.d
        assert all([type(x) is int for x in pos])
        # TODO: convert *pos tuple into integer. (Like converting a number to binary [given a 2 dimensional grid]).
        # TODO: "peek log"

    def __hash__(self):
        return self.__value
        # TODO: finish psuedo
        v = 0
        for d in range(self.d):
            v += self.n ** d if bit else 0


class Battlegrid(Grid):

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


class Battleship:
    def __init__(self):
        players = 2
        self.grids = [Battlegrid() for player in range(players)]

    def play(self):
        while True:
            for g, grid in enumerate(self.grids):
                print(grid)


battleship = Battleship()
battleship.play()
