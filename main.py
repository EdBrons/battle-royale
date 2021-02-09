from sim import GameManager
from player import *
import random

def make_player(f, m):
    x = ( ThePleb, TheBuilder, TheAttacker )
    random.choice(x)(f, m)

if __name__ == "__main__":
    gm = GameManager()
    # add players
    for f in gm.map.factions: make_player(f, gm.map)
    while len(gm.map.factions) > 1:
        gm.update_map()
    print(f'winner: {gm.map.factions[0]}')
