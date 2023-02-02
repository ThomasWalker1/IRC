import numpy as np
import random

def game_reset():
    return np.zeros(shape=(7,6), dtype=int)

def game_update(board, col, player):
    for ix in range(len(board[col])):
        if board[col][ix]==0:
            board[col][ix]=player
            return board

def game_won(board):
    game_lists=[]
    for n in range(6):
        col_list = []
        for k in range(7):
            col_list.append(str(board[k][n]))
        game_lists.append(''.join(col_list))
    for n in range(7):
        row_list = []
        for dig in board[n]:
            row_list.append(str(dig))
        game_lists.append(''.join(row_list))
    game_lists.append(str(board[0][0])+str(board[1][1])+str(board[2][2])+str(board[3][3])+str(board[4][4])+str(board[5][5]))
    game_lists.append(str(board[0][1])+str(board[1][2])+str(board[2][3])+str(board[3][4])+str(board[4][5]))
    game_lists.append(str(board[0][2])+str(board[1][3])+str(board[2][4])+str(board[3][5]))
    game_lists.append(str(board[1][0])+str(board[2][1])+str(board[3][2])+str(board[4][3])+str(board[5][4])+str(board[6][5]))
    game_lists.append(str(board[2][0])+str(board[3][1])+str(board[4][2])+str(board[5][3])+str(board[6][4]))
    game_lists.append(str(board[3][0])+str(board[4][1])+str(board[5][2])+str(board[6][3]))

    game_lists.append(str(board[6][0])+str(board[5][1])+str(board[4][2])+str(board[3][3])+str(board[2][4])+str(board[1][5]))
    game_lists.append(str(board[6][1])+str(board[5][2])+str(board[4][3])+str(board[3][4])+str(board[2][5]))
    game_lists.append(str(board[6][2])+str(board[5][3])+str(board[4][4])+str(board[3][5]))
    game_lists.append(str(board[5][0])+str(board[4][1])+str(board[3][2])+str(board[2][3])+str(board[1][4])+str(board[0][5]))
    game_lists.append(str(board[4][0])+str(board[3][1])+str(board[2][2])+str(board[1][3])+str(board[0][4]))
    game_lists.append(str(board[3][0])+str(board[2][1])+str(board[1][2])+str(board[0][3]))
    def checker(string_list):
        for string in string_list:
            if '1111' in string:
                return 1
            elif '2222' in string:
                return 2
        return 0
    return checker(game_lists)

def game_play(board,player):
    columns_free_spots=[0,0,0,0,0,0,0]
    for i in range(7):
        for j in range(6):
            if board[i][j]==0:
                columns_free_spots[i]=6-j
                break
    columns_one_spot=[]
    for k in range(7):
        if columns_free_spots[k]>=1:
            columns_one_spot.append(k)
    for column in columns_one_spot:
        if game_won(game_update(board, column, player))==player:
            return column
    return random.randint(0,6)

print(game_play(game_reset(),1))