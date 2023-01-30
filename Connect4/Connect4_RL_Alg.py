import numpy as np
from numbers import Number

def game_reset():
    return np.zeros(shape=(7,6))

def game_update(board, col, player):
    forefit = False
    if not isinstance(col, Number):
        forefit = True
    

