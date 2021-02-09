from sim import *
import random

# chooses moves randomly
class ThePleb:
    def __init__(self, f, m):
        self.fac = f
        self.fac.player = self
        self.fac.name += "(ThePleb)"
    def get_moves(self, m):
        moves = []
        # movement moves
        for t in m.get_fac_tiles(self.fac):
            for a in m.get_adjs(t.pos):
                moves.append(MoveArmy(self.fac, t, a, t.army / 2))
        # build moves
        for t in m.get_fac_tiles(self.fac):
            moves.append(BuildArmy(self.fac, t, self.fac.gold / 2))
        return random.choice(moves)

# he only builds...
class TheBuilder:
    def __init__(self, f, m):
        self.fac = f
        self.fac.player = self
        self.fac.name += "(TheBuilder)"
        # store ref to home tile
        self.capital = m.get_fac_tiles(f)[0]
    def get_moves(self, m):
        return [ BuildArmy(self.fac, self.capital, self.fac.gold) ]

# he attacks his neighbors if he has troops
# else he builds troops
class TheAttacker:
    def __init__(self, f, m):
        self.fac = f
        self.fac.player = self
        self.fac.name += "(TheAttacker)"
    def get_moves(self, m):
        moves = []
        # look for the largest imbalance of troops
        max_diff = -1
        src = None
        dest = None
        for t in m.get_fac_tiles(self.fac):
            # loop through my tiles
            for a in m.get_adjs(t.pos):
                if a.owner is self.fac: continue
                diff = t.army - a.army
                if diff > max_diff or src is None:
                    max_diff = diff
                    src = t
                    dest = a
        if max_diff < 0:
            # build units
            return [ BuildArmy(self.fac, src, self.fac.gold) ]
        else:
            return [ MoveArmy(self.fac, src, dest, src.army)  ]
        return moves
