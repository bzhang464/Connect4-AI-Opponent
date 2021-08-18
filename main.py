import numpy as np

grid = np.zeros((6, 7))


def drop_token(player):
    valid_col = None
    while True:
        col = int(input("Please enter a column 0-6 "))
        if col < 0 or col > 6:
            continue
        if grid[0][col] == 0:
            valid_col = col
            break
        else:
            print("This column is full!")
    for x in range(6):
        if grid[5-x][valid_col] == 0:
            grid[5-x][valid_col] = player
            break


def check_winner(board):
    for x in range(6):
        for y in range(7):
            if board[x][y] == 1:
                if x < 3:
                    if board[x+1][y] == 1 and board[x+2][y] == 1 and board[x+3][y] == 1:
                        return 1
                    if y < 4:
                        if board[x+1][y+1] == 1 and board[x+2][y+2] == 1 and board[x+3][y+3] == 1:
                            return 1
                    if y > 2:
                        if board[x+1][y-1] == 1 and board[x+2][y-2] == 1 and board[x+3][y-3] == 1:
                            return 1
                if y < 4:
                    if board[x][y+1] == 1 and board[x][y+2] == 1 and board[x][y+3] == 1:
                        return 1
                if y > 2:
                    if board[x][y-1] == 1 and board[x][y-2] == 1 and board[x][y-3] == 1:
                        return 1
            if board[x][y] == 2:
                if x < 3:
                    if board[x+1][y] == 2 and board[x+2][y] == 2 and board[x+3][y] == 2:
                        return 2
                    if y < 4:
                        if board[x+1][y+1] == 2 and board[x+2][y+2] == 2 and board[x+3][y+3] == 2:
                            return 2
                    if y > 2:
                        if board[x+1][y-1] == 2 and board[x+2][y-2] == 2 and board[x+3][y-3] == 2:
                            return 2
                if y < 4:
                    if board[x][y+1] == 2 and board[x][y+2] == 2 and board[x][y+3] == 2:
                        return 2
                if y > 2:
                    if board[x][y-1] == 2 and board[x][y-2] == 2 and board[x][y-3] == 2:
                        return 2
    return 0


def window_score(goods, bads, empties):
    result = 0
    if goods == 4:
        result += 1000
    elif goods == 3 and empties == 1:
        result += 5
    elif goods == 2 and empties == 2:
        result += 1
    elif bads == 3 and empties == 1:
        result -= 10
    elif bads == 4:
        result -= 1000
    return result


def board_score(board, player):
    score = 0
    opponent = switch_player(player)
    for x in range(6):
        row = board[x].tolist()
        for y in range(4):
            goods = row[y:y+4].count(player)
            bads = row[y:y+4].count(opponent)
            empties = row[y:y+4].count(0)
            score += window_score(goods, bads, empties)
    for x in range(7):
        column = board[:, x].tolist()
        for y in range(3):
            goods = column[y:y+4].count(player)
            bads = column[y:y+4].count(opponent)
            empties = column[y:y+4].count(0)
            score += window_score(goods, bads, empties)
    for x in range(3):
        for y in range(4):
            diagonal = [board[x][y], board[x+1][y+1], board[x+2][y+2], board[x+3][y+3]]
            goods = diagonal.count(player)
            bads = diagonal.count(opponent)
            empties = diagonal.count(0)
            score += window_score(goods, bads, empties)
    for x in range(3):
        for y in range(4):
            diagonal = [board[x][6-y], board[x+1][5-y], board[x+2][4-y], board[x+3][3-y]]
            goods = diagonal.count(player)
            bads = diagonal.count(opponent)
            empties = diagonal.count(0)
            score += window_score(goods, bads, empties)
    middle = board[:, 3].tolist()
    left = board[:, 2].tolist()
    right = board[:, 4].tolist()
    score += (middle.count(player))*4
    score += (left.count(player))*2
    score += (right.count(player))*2
    return score


def is_terminal(board):
    if check_winner(board) != 0:
        return True
    elif 0 not in board[0].tolist():
        return True
    else:
        return False


def child_boards(board, player):
    top_row = board[0].tolist()
    board_list = []
    for x in range(7):
        if top_row[x] != 0:
            continue
        new_board = board.copy()
        y = 0
        while new_board[5-y][x] != 0:
            y += 1
        new_board[5-y][x] = player
        board_list.append((x, new_board))
    return board_list


def switch_player(player):
    if player == 1:
        return 2
    else:
        return 1


def minimax(board, depth, player, maximizing):
    if depth == 0 or is_terminal(board):
        return None, board_score(board, player)
    if maximizing:
        biggest = None, -10000000
        for tup in child_boards(board, player):
            score = minimax(tup[1], depth - 1, player, False)[1]
            if score > biggest[1]:
                biggest = tup[0], score
        return biggest
    else:
        smallest = None, 10000000
        for tup in child_boards(board, switch_player(player)):
            score = minimax(tup[1], depth - 1, player, True)[1]
            if score < smallest[1]:
                smallest = tup[0], score
        return smallest


turn = 1
human = 0
while human != 1 and human != 2:
    human = int(input("Would you like to play as Player 1 or 2? 1/2 "))
AI = switch_player(human)
while not is_terminal(grid):
    if turn == AI:
        best_move = minimax(grid, 4, AI, True)[0]
        for x in range(6):
            if grid[5 - x][best_move] == 0:
                grid[5 - x][best_move] = AI
                break
    else:
        drop_token(human)
    print(grid)
    turn = switch_player(turn)

print("Game over!")
if check_winner(grid) != 0:
    print("Player {} wins!".format(check_winner(grid)))
else:
    print("No winners!")
print("Thank you for playing!")
