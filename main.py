#!/usr/bin/env python3
__author__ = 'Tingting Yu'
import sys
import random
import time
import math
import copy

# initial setting
pits1 = [4, 4, 4, 4, 4, 4, 0]
pits2 = [4, 4, 4, 4, 4, 4, 0]
# state[0] is player1's state and state[1] is player2's state at the beginning
state = [pits1, pits2]
is_new_turn = 0
current_player = 'p1'


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_board(s):
    """
    print game board at the current state
    s: state
    s[1]: player 2 's board data, which is the opponent
    """
    s[1].reverse()
    print("                 6     5     4     3     2     1")
    print("        --------------------------------------------")
    print("player2", end='')
    print('   '+str(s[1][0])+' '+'-'+' '+'|', end='')
    for i in range(1, 6):
        print(str(s[1][i]).rjust(3), "||", end='')
    print(str(s[1][6]).rjust(3), "|", end='')
    print("\n---------------------------------------------------------------")
    print("             ", "|", end='')
    for i in range(0, 5):
        print(str(s[0][i]).rjust(3), "||", end='')
    print(str(s[0][5]).rjust(3), "|", end='')
    print(" -", str(s[0][6]), end='')
    print("     player1", end='')
    print("\n        --------------------------------------------")
    print("                 1     2     3     4     5     6")

    s[1].reverse()


def initialize():
    """
    initialize the board when first come in
    :return strlist the user entered in
    """
    print("please choose 2 modes from 'human, random, minimax and alphabeta', sperated with a Space,ended with Enter")
    tempargs = input()
    strlist = tempargs.split()
    if strlist[0] in ['human', 'random', 'minimax', 'alphabeta'] and strlist[1] in ['human', 'random', 'minimax', 'alphabeta']:
        print_board(state)
        return strlist
    else:
        eprint("Invalid input. Please check your input and try again")


def find_a_not_empty_pit(board_state, Current_Player):
    """
    find the valid pit according to the board_state and who's turn
    :return a move
    """
    Choice = []
    if Current_Player == 'p1':
        for i in range(0, 6):
            if board_state[0][i] != 0:
                Choice.append(i+1)
    else:
        for i in range(0, 6):
            if board_state[1][i] != 0:
                Choice.append(1+i)

    return Choice


def is_the_move_legal(board_state, chosen_pit, Current_Player):
    """
    Test the chosen_pit is legal or not
    :param Current_Player: who is playing the game
    :return: True for is legal, False for not
    """
    Choice = find_a_not_empty_pit(board_state, Current_Player)
    flag = 0
    temp = len(Choice)
    for i in range(0, temp):
        if Choice[i] == chosen_pit:
            flag = 1
    if flag:
        return True
    else:
        eprint("Illegal move. Please try again\n Choose a pit with stones\n")
        return False


def one_move(board_state, Current_Player, chosen_pit):
    """
    This is the move rule of all modes
    return: the state after one move
    """
    global is_new_turn
    is_new_turn = 0
    if Current_Player == 'p1':
        stones = board_state[0][chosen_pit - 1]
        board_state[0][chosen_pit - 1] = 0
        # the most general situation
        if (stones + chosen_pit) < 7:
            temp = stones
            while stones > 0:
                board_state[0][chosen_pit + temp - stones] += 1
                stones -= 1
            # if p1 captured
            if board_state[0][chosen_pit + temp - 1] == 1:
                eaten = board_state[1][6-chosen_pit-temp]
                board_state[0][chosen_pit + temp - 1] = 0
                board_state[1][6 - chosen_pit - temp] = 0
                board_state[0][6] = board_state[0][6] + 1 + eaten

        # when the last stone fell into the store
        # Start a new turn for this player
        elif (stones + chosen_pit) == 7:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            is_new_turn = 1
            return board_state

        elif 7 < (stones + chosen_pit) < 14:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            temp = stones - (7-chosen_pit)
            for i in range(0, temp):
                board_state[1][i] += 1

        elif 14 <= (stones + chosen_pit) < 20:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            for i in range(0, 6):
                board_state[1][i] += 1
            temp = stones + chosen_pit - 13
            for i in range(0, temp):
                board_state[0][i] += 1
            # if p1 captured
            if board_state[0][temp - 1] == 1:
                eaten = board_state[1][6-temp]
                board_state[0][temp-1] = 0
                board_state[1][6-temp] = 0
                board_state[0][6] = board_state[0][6] + 1 + eaten

        # when the last stone fell into the store
        # Start a new turn for this player
        elif (stones + chosen_pit) == 20:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            for i in range(0, 6):
                board_state[1][i] += 1
            for i in range(0, 7):
                board_state[0][i] += 1
            is_new_turn = 1
            return board_state

        elif 20 < (stones + chosen_pit) <= 26:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            for i in range(0, 6):
                board_state[1][i] += 1
            for i in range(0, 7):
                board_state[0][i] += 1
            temp = stones +chosen_pit - 20
            for i in range(0, temp):
                board_state[1][i] += 1
        else:
            for i in range(chosen_pit, 7):
                board_state[0][i] += 1
            for i in range(0, 6):
                board_state[1][i] += 1
            for i in range(0, 7):
                board_state[0][i] += 1
            for i in range(0, 7):
                board_state[1][i] += 1
            temp = stones + chosen_pit - 26
            for i in range(0, temp):
                board_state[0][i] += 1
            if board_state[0][temp-1] == 1:
                eaten = board_state[1][6-temp]
                board_state[0][6] = board_state[0][6] + 1 + eaten
                board_state[0][temp-1] = 0
                board_state[1][6-temp] = 0

    else:
        stones = board_state[1][chosen_pit - 1]
        board_state[1][chosen_pit - 1] = 0
        # the most general situation
        if (stones + chosen_pit) < 7:
            temp = stones
            while stones > 0:
                board_state[1][chosen_pit + temp - stones] += 1
                stones -= 1
            # if p2 captured
            if board_state[1][chosen_pit + temp - 1] == 1:
                eaten = board_state[0][6 - chosen_pit - temp]
                board_state[1][chosen_pit + temp - 1] = 0
                board_state[0][6 - chosen_pit - temp] = 0
                board_state[1][6] = board_state[1][6] + 1 + eaten

        # when the last stone fell into the store
        # Start a new turn for this player
        elif (stones + chosen_pit) == 7:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            is_new_turn = 1
            return board_state

        elif 7 < (stones + chosen_pit) < 14:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            temp = stones - (7 - chosen_pit)
            for i in range(0, temp):
                board_state[0][i] += 1

        elif 14 <= (stones + chosen_pit) < 20:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            for i in range(0, 6):
                board_state[0][i] += 1
            temp = stones + chosen_pit - 13
            for i in range(0, temp):
                board_state[1][i] += 1
            # if p2 captured
            if board_state[1][temp - 1] == 1:
                eaten = board_state[0][6 - temp]
                board_state[1][temp - 1] = 0
                board_state[0][6 - temp] = 0
                board_state[1][6] = board_state[1][6] + 1 + eaten

        # when the last stone fell into the store
        # Start a new turn for this player
        elif (stones + chosen_pit) == 20:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            for i in range(0, 6):
                board_state[0][i] += 1
            for i in range(0, 7):
                board_state[1][i] += 1
            is_new_turn = 1
            return board_state

        elif 20 < (stones + chosen_pit) <= 26:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            for i in range(0, 6):
                board_state[0][i] += 1
            for i in range(0, 7):
                board_state[1][i] += 1
            temp = stones + chosen_pit - 20
            for i in range(0, temp):
                board_state[0][i] += 1
        else:
            for i in range(chosen_pit, 7):
                board_state[1][i] += 1
            for i in range(0, 6):
                board_state[0][i] += 1
            for i in range(0, 7):
                board_state[1][i] += 1
            for i in range(0, 7):
                board_state[0][i] += 1
            temp = stones + chosen_pit - 26
            for i in range(0, temp):
                board_state[1][i] += 1
            if board_state[1][temp - 1] == 1:
                eaten = board_state[0][6 - temp]
                board_state[1][6] = board_state[1][6] + 1 + eaten
                board_state[1][temp - 1] = 0
                board_state[0][6 - temp] = 0

    return board_state


def check_game_over(board_state):
    """
    Check if the game is over
    :return: True for over, False for not
    """
    p1_total = 0
    p2_total = 0
    for i in range(0, 6):
        p1_total += board_state[0][i]
        p2_total += board_state[1][i]
    if p1_total != 0 and p2_total != 0:
        return False
    else:
        return True


def check_score(board_state):
    """
    Check who is the winner
    :param board_state:
    :return: the winner of the game
    """
    if board_state[0][6] > board_state[1][6]:
        return "Player1"
    elif board_state[0][6] == board_state[1][6]:
        return "draw"
    else:
        return "Player2"


# From Line 314 to 322 is how to choose a random move
def random_algorithm(board_state, Current_Player):
    """
    Pick an random move for who's playing
    :return: a chosen move
    """
    Choice = find_a_not_empty_pit(board_state, Current_Player)
    return random.choice(Choice)


def utility_function(player, board_state):
    """
    The heuristic function for minimax and alphabeta algorithms
    :return: the utility value of specified node
    """
    if player == "p1":
        return board_state[0][6] - board_state[1][6]
    else:
        return board_state[1][6] - board_state[0][6]


# From Line 337 to 428 is how to choose a minimax move

# if this is a max node
def minimax_max_score(board_state, current_turn, depth):
    """
    Find the maximum value for current_turn's side at the specified depth
    :param board_state:
    :param current_turn: who calls this function
    :return: the max value
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)

    if depth == 5 or check_game_over(temp_state):
        # important! the global variable current_player
        if current_player == "p1":
            return utility_function("p1", temp_state)
        else:
            return utility_function("p2", temp_state)

    bestValue = -math.inf

    for each in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p1", each)
            v = minimax_min_score(s, "p2", depth+1)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p2", each)
            v = minimax_min_score(s, "p1", depth + 1)
        temp = max(bestValue, v)
        bestValue = temp
    return bestValue


# if this is a min node
def minimax_min_score(board_state, current_turn, depth):
    """
    Find the minimum value for current_turn's side at the specified depth in minimax algorithm
    :param current_turn: who calls this function
    :return: the min value
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)

    if depth == 5 or check_game_over(temp_state):
        # important! This is the global variable "current_player"
        if current_player == "p1":
            return utility_function("p1", temp_state)
        else:
            return utility_function("p2", temp_state)

    bestValue = math.inf

    for each in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p1", each)
            v = minimax_max_score(s, "p2", depth + 1)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p2", each)
            v = minimax_max_score(s, "p1", depth + 1)
        temp = min(bestValue, v)
        bestValue = temp
    return bestValue


def minimax_algorithm(board_state, current_turn, depth):
    """
    Find the minimax move from the side of current_turn, a.k.a the global var "current_player"
    :param current_turn: equals to the value of global var "current_player"
    :return: a chosen move
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)
    chosen_pit = -1
    score = -math.inf

    for move in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p1", move)
            temp_score = minimax_min_score(s, "p2", depth + 1)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p2", move)
            temp_score = minimax_min_score(s, "p1", depth + 1)
        if temp_score > score:
            score = temp_score
            chosen_pit = move
        if temp_score == score:
            chosen_pit = random.choice([move, chosen_pit])
    return chosen_pit


# From Line 434 to 542 is how to choose a alphabeta pruning move

# if this is a max node
def alphabeta_max_value(board_state, current_turn, depth, a, b):
    """
    Find the max value for current_turn's side at the specified depth in alphabeta algorithm
    And update a
    :param board_state:
    :param current_turn: who calls this function
    :param a: the low bound of this node
    :param b: the high bound of this node
    :return: the max value of this node
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)

    if depth == 5 or check_game_over(temp_state):
        # important! This is the global variable "current_player"
        if current_player == "p1":
            return utility_function("p1", temp_state)
        else:
            return utility_function("p2", temp_state)

    bestValue = -math.inf

    for child in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p1", child)
            score = alphabeta_min_value(s, "p2", depth+1, a, b)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p2", child)
            score = alphabeta_min_value(s, "p1", depth + 1, a, b)
        bestValue = max(bestValue, score)
        if bestValue >= b:
            return bestValue
        a = max(a, bestValue)
    return bestValue


# if this is a min node
def alphabeta_min_value(board_state, current_turn, depth, a, b):
    """
    Find the min value for current_turn's side at the specified depth in alphabeta algorithm
    And update b
    :param board_state:
    :param current_turn: who calls this function
    :param a: the low bound of this node
    :param b: the high bound of this node
    :return: the min value of this node
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)
    if depth == 5 or check_game_over(temp_state):
        # important! This is the global variable "current_player"
        if current_player == "p1":
            return utility_function("p1", temp_state)
        else:
            return utility_function("p2", temp_state)

    bestValue = math.inf
    for child in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p1", child)
            score = alphabeta_max_value(s, "p2", depth+1, a, b)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, "p2", child)
            score = alphabeta_max_value(s, "p1", depth + 1, a, b)
        bestValue = min(bestValue, score)
        if bestValue <= a:
            return bestValue
        b = min(b, bestValue)
    return bestValue


# the one who use alphabeta_pruning_algorithm is definitely wants to win
# in other words, it must be a max node
def alphabata_pruning_algorithm(board_state, current_turn, depth):
    """
    Find the alphabeta pruning move from the side of current_turn, a.k.a the global var "current_player"
    :param current_turn: equals to the value of global var "current_player"
    :return: a chosen move
    """
    temp_state = copy.deepcopy(board_state)
    children = find_a_not_empty_pit(temp_state, current_turn)
    a = -math.inf
    b = math.inf
    chosen_pit = -1
    bestValue = -math.inf

    for child in children:
        if current_turn == "p1":
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, current_turn, child)
            score = alphabeta_min_value(s, "p2", depth + 1, a, b)
        else:
            temp_state = copy.deepcopy(board_state)
            s = one_move(temp_state, current_turn, child)
            score = alphabeta_min_value(s, "p1", depth + 1, a, b)
        if bestValue < score:
            chosen_pit = child
            bestValue = score

        elif bestValue == score:
            chosen_pit = random.choice([chosen_pit, child])

        #a = max(bestValue, a)

    return chosen_pit


# From Line 546 to 683 are the experiment functions
def rate_calculation():
    """
    Find the win rate between the 2 modes that user entered
    :return: the win rate of this 2 modes
    """
    print("Please choose 2 modes from【random, minimax and alphabeta 】that you want to test and times")
    print("Seperated with space, ended with Enter")
    print("e.g: minimax random 50")
    print("means you want to test minimax and random, for 50 times")
    in_str = input()
    in_str = in_str.split()
    player1 = in_str[0]
    player2 = in_str[1]
    times = int(in_str[2])
    in_str.pop()

    win = 0
    loss = 0
    draw = 0
    n = 1
    while n <= times:
        print("\n===============================================================")
        print("This is round %d between %s and %s" % (n, player1, player2))
        PITS1 = [4, 4, 4, 4, 4, 4, 0]
        PITS2 = [4, 4, 4, 4, 4, 4, 0]
        s = [PITS1, PITS2]
        winner = start_with_only_result(s, in_str)
        if winner == "Player1":
            print("%s wins!" % player1)
            win += 1
        elif winner == "Player2":
            print("%s wins!" % player2)
            loss += 1
        else:
            print("Draw.")
            draw += 1
        n += 1

    p1_win_rate = win/times
    p2_win_rate = loss/times
    draw_rate = draw/times

    print("\nConclusion:")
    print("After running the game between %s and %s %d times," % (player1, player2, times))
    print("%s wins %d times, its win rate is %.4f" % (player1, win, p1_win_rate))
    print("%s wins %d times, its win rate is %.4f" % (player2, loss, p2_win_rate))
    print("Draw rate between %s and %s is %.4f" % (player1, player2, draw_rate))


def time_calculation():
    """
    find the total time and average time for running 2 modes at specified times
    :return: total time and average time
    """
    print("Please choose 2 modes from【random, minimax and alphabeta 】that you want to test and times")
    print("Seperated with space, ended with Enter")
    print("e.g: minimax random 50")
    print("means you want to test minimax and random, for 50 times")
    in_str = input()
    in_str = in_str.split()
    player1 = in_str[0]
    player2 = in_str[1]
    times = int(in_str[2])
    in_str.pop()
    n = 1

    time_start = time.process_time()
    while n <= times:
        print("\n===============================================================")
        print("This is round %d between %s and %s" % (n, player1, player2))
        PITS1 = [4, 4, 4, 4, 4, 4, 0]
        PITS2 = [4, 4, 4, 4, 4, 4, 0]
        s = [PITS1, PITS2]
        winner = start_with_only_result(s, in_str)
        if winner == "Player1":
            print("%s wins!" % player1)
        elif winner == "Player2":
            print("%s wins!" % player2)
        else:
            print("Draw.")
        n += 1

    time_end = time.process_time()
    time_spend = time_end - time_start
    average_time = time_spend / times
    print("\nConclusion:")
    print("After running the game between %s and %s %d times," % (player1, player2, times))
    print("The total time cost is %.4f seconds" % time_spend)
    print("The average time cost is %.4f seconds" % average_time)


def start_with_only_result(board_state, input_str):
    """
    concise version of the start function, which is the main function in this field
    use to check only the winner of 1 round game
    :param input_str: players that comes from user
    :return: the winner
    """
    global current_player

    while True:
        is_end = check_game_over(board_state)
        if is_end:
            break
        if current_player == "p1":

            if input_str[0] == "random":
                selected_pit = random_algorithm(board_state, "p1")
            elif input_str[0] == "minimax":
                selected_pit = minimax_algorithm(board_state, "p1", 0)
            elif input_str[0] == "alphabeta":
                selected_pit = alphabata_pruning_algorithm(board_state, "p1", 0)

            is_legal = is_the_move_legal(board_state, selected_pit, "p1")
            if is_legal:
                board_state = one_move(board_state, "p1", selected_pit)

                if is_new_turn == 0:
                    current_player = "p2"

        else:

            if input_str[1] == "random":
                selected_pit = random_algorithm(board_state, "p2")
            elif input_str[1] == "minimax":
                selected_pit = minimax_algorithm(board_state, "p2", 0)
            elif input_str[1] == "alphabeta":
                selected_pit = alphabata_pruning_algorithm(board_state, "p2", 0)

            is_legal = is_the_move_legal(board_state, selected_pit, "p2")
            if is_legal:
                board_state = one_move(board_state, "p2", selected_pit)
                if is_new_turn == 0:
                    current_player = "p1"

    print_board(board_state)
    winner = check_score(board_state)
    return winner


def start(board_state, input_str):
    """
    Main funtion in this field. Print every pit that chosen by players
    and prints the chess board after 1 player choose its move
    :param input_str: the player chosen by the mode
    """
    global current_player

    while True:
        is_end = check_game_over(board_state)
        if is_end:
            break
        if current_player == "p1":
            if input_str[0] == "human":
                print(" ")
                print("Player1, please choose a pit with stones")
                selected_pit = int(input())

            elif input_str[0] == "random":
                selected_pit = random_algorithm(board_state, "p1")
            elif input_str[0] == "minimax":
                selected_pit = minimax_algorithm(board_state, "p1", 0)
            elif input_str[0] == "alphabeta":
                selected_pit = alphabata_pruning_algorithm(board_state, "p1", 0)

            is_legal = is_the_move_legal(board_state, selected_pit, "p1")
            if is_legal:
                time.sleep(1)
                print(" ")
                print("Player1 choose the %dth pit:" % selected_pit)
                board_state = one_move(board_state, "p1", selected_pit)
                time.sleep(1)
                print(" ")
                print_board(board_state)
                print("\n===============================================================")
                if is_new_turn == 0:
                    current_player = "p2"
                else:
                    print("player1 another turn!")
                    time.sleep(0.5)
        else:
            if input_str[1] == "human":
                print(" ")
                print("Player2, please choose a pit with stones")
                selected_pit = int(input())
            elif input_str[1] == "random":
                selected_pit = random_algorithm(board_state, "p2")
            elif input_str[1] == "minimax":
                selected_pit = minimax_algorithm(board_state, "p2", 0)
            elif input_str[1] == "alphabeta":
                selected_pit = alphabata_pruning_algorithm(board_state, "p2", 0)

            is_legal = is_the_move_legal(board_state, selected_pit, "p2")
            if is_legal:
                time.sleep(1)
                print(" ")
                print("Player2 choose the %dth pit:" % selected_pit)
                board_state = one_move(board_state, "p2", selected_pit)
                time.sleep(1)
                print(" ")
                print_board(board_state)
                if is_new_turn == 0:
                    current_player = "p1"
                else:
                    print("player2 another turn!")
                    time.sleep(0.5)
        time.sleep(0.5)
    winner = check_score(board_state)
    if winner == "draw":
        print("Draw.")
    else:
        print("%s wins!" % winner)


if __name__ == "__main__":
    board_state = state
    input_str = initialize()
    start(board_state, input_str)

"""
 if you want to test win rates among [alphabeta, random, minimax], 
 comment line 760 - 763 and uncomment rate_calculation()
 if you want to test time consuming among [alphabeta, random, minimax],
 comment line 760 - 763 and uncomment time_calculation()
"""
# rate_calculation()
# time_calculation()





























