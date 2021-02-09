from math import sqrt
import random

# stolen from stack overflow
def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def shift(self, x, y):
        self.x += x
        self.y += y
    def length(self):
        return sqrt(self.x**2 + self.y**2)
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def __repr__(self):
        return f'({self.x}, {self.y})'

# geometry stuff
def distance(p1, p2):
    return (p1 - p2).length()
def is_adj(p1, p2):
    return (p1 - p2).length() == 1
def get_adjs(p):
    return [ Point(p.x + 1, p.y), Point(p.x - 1, p.y), Point(p.x, p.y + 1), Point(p.x, p.y - 1) ]

class MoveArmy:
    def __init__(self, f, s, d, v):
        self.fac = f
        self.src = s
        self.dest = d
        self.val = v
    def is_valid(self):
        return self.src.owner is self.fac and is_adj(self.src.pos, self.dest.pos) and self.src.army >= self.val
    def execute(self):
        self.src.army -= self.val
        if self.dest.owner is None:
            # claiming unowned province
            self.dest.army += self.val
            self.owner = self.fac
            return f'[RESOLUTION]: [CAPTURE]'
        elif self.dest.owner is not self.fac:
            def_str = self.dest.defense + self.dest.army
            att_str = self.val
            if def_str >= att_str:
                # def wins
                self.dest.army -= max(att_str - self.dest.defense, 0)
                return f'[RESOLUTION]: [FAILED]'
            else:
                # att wins
                self.dest.owner = self.fac
                self.dest.army = self.val - def_str
                return f'[RESOLUTION]: [CAPTURE]'
        else:
            self.dest.army += self.val
    def __repr__(self):
        return f'[MOVE]: [MoveArmy] [FACTION]: [{self.fac}] [SRC]: [{self.src}] [DEST]: [{self.dest}] [VAL]: [{self.val}]'
class BuildArmy:
    def __init__(self, f, s, v):
        self.fac = f
        self.src = s
        self.val = v
    def is_valid(self):
        return self.src.owner is self.fac and self.fac.gold >= self.val and self.src.army < 1000
    def execute(self):
        self.fac.gold -= self.val
        self.src.army += self.val
        return '[RESOLUTION]: [BUILT]'
    def __repr__(self):
        return f'[MOVE]: [BuildArmy] [FACTION]: [{self.fac}] [SRC]: [{self.src}] [VAL]: [{self.val}]'
class BuildDefenses:
    def __init__(self, f, s, v):
        self.fac = f
        self.src = s
        self.val = v
    def is_valid(self):
        return self.src.owner is self.fac and self.fac.gold >= self.val and self.src.defense < 1000
    def execute(self):
        self.fac.gold -= self.val
        self.src.defense += self.val
        return '[RESOLUTION]: [BUILT]'
    def __repr__(self):
        return f'[MOVE]: [BuildDefenses] [FACTION]: [{self.fac}] [SRC]: [{self.src}] [VAL]: [{self.val}]'

class Faction:
    def __init__(self, name, player=None):
        self.name = name
        self.player = None
        self.gold = 1
    # all factions should have a player
    def get_moves(self, m):
        return self.player.get_moves(m)
    def __repr__(self):
        return f'f_{self.name}'

class Tile:
    def __init__(self, pos):
        self.pos = pos
        self.owner = None
        self.gold = 1
        self.army = 1
        self.defense = 1
    def __repr__(self):
        return f't_{self.pos}'

class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.tiles = []
        self.factions = []
        for y in range(h):
            for x in range(w):
                self.tiles.append(Tile(Point(x, y)))
    def in_bounds(self, p):
        return p.x >= 0 and p.y >= 0 and p.x < self.width and p.y < self.height
    def get_tile(self, p):
        return self.tiles[p.x + p.y * self.width] if self.in_bounds(p) else None
    def get_fac_tiles(self, f):
        return [ t for t in self.tiles if t.owner is f  ]
    def get_adjs(self, p):
        return [ self.get_tile(a) for a in get_adjs(p) if self.in_bounds(a) ]

class GameManager:
    def __init__(self):
        self.map = Map(3, 3)
        # add factions
        for t in self.map.tiles:
            f = Faction(str(len(self.map.factions)))
            t.owner = f
            self.map.factions.append(f)
    def scrub_map(self, f):
        # TODO: add vision and hidden info
        return self.map
    def update_map(self):
        # update faction gold
        for t in self.map.tiles:
            if t.owner is not None:
                t.owner.gold += t.gold
        # get moves and shuffle them
        moves = [ f.get_moves(self.scrub_map(f)) for f in self.map.factions ]
        moves = flatten(moves)
        random.shuffle(moves)
        for m in moves:
            # execute move
            print(m)
            if m.is_valid(): print(m.execute())
        self.map.factions = [ f for f in self.map.factions if len(self.map.get_fac_tiles(f)) > 0 ]
