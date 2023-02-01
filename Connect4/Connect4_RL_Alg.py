import numpy as np
from numbers import Number
import matplotlib.pyplot as plt

def game_reset():
    return np.zeros(shape=(7,6), dtype=int)

def game_drawn(board):
    for i in range(7):
        for j in range(6):
            if board[i][j]==0:
                return False
    return True

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
    averages = []
    state=0
    for n in range(7):
        average = sum(board[n])/6
        if average==0:
            cat=0
        elif average<=0.35:
            cat = 1
        elif average<=0.85:
            cat = 2
        else:
            cat = 3
        state+= cat*4**n
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
        break
    else:
        board = game_update(board, column, player)

def game_ending(board):
    if game_drawn(board):
        return 0
    else:
        return game_won(board)

def game_play_random():
    states_observed = []
    actions = []
    board = game_reset()
    player=2
    while game_won(board)==0:
        if player==2:
            states_observed.append(game_state(board))
        if player==1:
            player=2
        else:
            player=1
        action = np.random.randint(0,7)
        if game_forfeit(board,action):
            break
        board = game_update(board, action, player)
        if player==1:
            actions.append(action)
    if len(states_observed)>len(actions):
        states_observed=states_observed[0:-1]
    return(board, states_observed, actions, game_ending(board))

def game_value(observations, result):
    if result==0:
        reward = 0
    elif result==1:
        reward = 1
    else:
        reward=-1
    value_list = []
    N=len(observations)
    for ix in range(N):
        value_list.append(0.95**(N-ix)*reward)
    return value_list

q_table = np.zeros(shape=(4**7+3, 7))

epochs=50000
for n in range(epochs):
    if n%100==0:
        print(n)
    b,s,a,r = game_play_random()
    values = game_value(s, r)
    s.append(4**7+r)
    
    for k in range(len(s)-1):
        next_max = np.max(q_table[s[k+1]])
        old_value = q_table[s[k]][a[k]]
        new_value = old_value+0.6*(values[k]+0.6*next_max-old_value)
        q_table[s[k]][a[k]]=new_value

def game_play_evaluate():
    board = game_reset()
    player=2
    while game_won(board)==0:
        if player==1:
            player=2
            action = np.random.randint(0,7)
        else:
            player=1
            action = np.argmax(q_table[game_state(board)])
            if q_table[game_state(board)][action]==0:
                action = np.random.randint(0,7)
        if game_forfeit(board,action):
            break
        board = game_update(board, action, player)
    return(board, game_ending(board))

drawn=0
won=0
lost = 0
no_games = 2000
for k in range(no_games):
    if k%100==0:
        print(k)
    b, r = game_play_evaluate()
    if r==0:
        drawn+=1
    elif r==1:
        won+=1
    else:
        lost+=1
print(f"Played: {no_games}\nWon: {won}\nLost: {lost}\nDrawn: {drawn}")