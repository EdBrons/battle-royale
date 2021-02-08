import random
class Faction:
    def __init__(self, n):
        self.gold = 1
        self.name = n
class Tile:
    def __init__(self, x, y):
        self.owner = None
        self.x = x
        self.y = y
        self.gold = 1
        self.army = 1
    def __repr__(self):
        return "tile_" + str(x) + "," + str(y)
class Map:
    unit_cost = 1
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.tiles = []
        for y in range(h):
            for x in range(w):
                self.tiles.append(Tile(x, y))
        self.facs = [ Faction("faction_" + str(i)) for i in range(w) ]
        self.tiles[0].owner = self.facs[0]
    def get_adj_tiles(self, x, y):
        return [ t for t in [ self.get_tile(x+1, y), self.get_tile(x-1,y), self.get_tile(x,y+1), self.get_tile(x,y-1) ] if t is not None ]
    def is_adj(self, tile, other):
        return other in self.get_adj_tiles(tile)
    def in_bounds(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height
    def get_tile(self, x, y):
        return self.tiles[x + y * self.width] if self.in_bounds(x, y) else None
    def get_fac_tiles(self, f):
        return [ t for t in self.tiles if t.owner is f ]
    def do_update(self):
        # add gold
        for t in self.tiles:
            if t.owner is not None:
                t.owner.gold += t.gold
class MoveUnits:
    def __init__(self, m, f, s, d, a):
        self.m = m
        self.fac = f
        self.src = s
        self.dest = d
        self.amount = a
    def validate(self):
        return self.src.owner is self.fac and self.m.is_adj(self.src, self.dest) and self.src.army >= self.amount
    def execute(self):
        self.src.army -= self.amount
        if self.dest.owner is not self.fac:
            battle = TileBattle(m, s, d, a)
            battle.execute()
        else:
            print(self.fac.name + " moved " + self.amount + " units from " + self.src + " to " + self.dest)
            self.dest.army += self.amount
class TileBattle:
    def __init__(self, m, s, d, a):
        self.m = m
        self.att_src = s
        self.att_amnt = a
        self.dest = d
        self.dest_amnt = d.army
    def execute(self):
        if dest.owner is None:
            self.dest.owner = self.att_src.owner
            self.dest.army = self.att_amnt
        else:
            self.dest.army = abs(self.att_amnt - self.dest_amnt)
            if self.att_amnt > self.dest_amnt:
                self.dest.owner = self.att_src.owner
class BuildUnits:
    def __init__(self, m, f, s, a):
        self.m = m
        self.fac = f
        self.src = s
        self.amount = a
    def validate(self):
        return self.src.owner is self.fac and self.amount * self.m.unit_cost <= self.fac.gold
    def execute(self):
        self.fac.gold -= self.amount * self.m.unit_cost
        self.src.army += self.amount
class Player:
    def __init__(self, f):
        self.fac = f
    def update(self, m):
        units = int(self.fac.gold / m.unit_cost)
        build_tile = random.choice(m.get_fac_tiles(self.fac))
        build_move = BuildUnits(m, self.fac, build_tile, units)
        if build_move.validate(): build_move.execute()
m = Map(10, 10)
players = []
for f in m.facs:
    players.append(Player(f))
s = ""
while input(s) == "":
    m.do_update()
    for p in players:
        p.update(m)
