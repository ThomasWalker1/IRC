import numpy as np
from numbers import Number

def game_reset():
    return np.zeros(shape=(7,6), dtype=int)

def game_forfeit(board, col):
    if not isinstance(col, Number) or (col>6 or col<0): 
        return True
    if board[col][-1]!=0:
        return True
    return False

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
    

def game_update(board, col, player):
    for ix in range(len(board[col])):
        if board[col][ix]==0:
            board[col][ix]=player
            return board

def game_state(board):
    state = []
    for k in range(7):
        for i in range(6):
            if board[k][i]==0:
                break
        if i==5:
            if board[k][i]==0:
                state.append((k, 4, board[k][4]))
            else:
                state.append((k, 5, board[k][5]))
        elif i==0:
            state.append((k, 0, board[k][0]))
        else:
            state.append((k, i-1, board[k][i-1]))
    return state

player=2
board=game_reset()
forfeit=False
while game_won(board)==0:
    if player==1:
        player=2
    else:
        player=1
    column = np.random.randint(0,7)
    if game_forfeit(board, column):
        print("Forfeit")
        print(board)
        print(column)
        break
    else:
        board = game_update(board, column, player)
print(board)
print(game_state(board))


