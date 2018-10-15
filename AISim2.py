#reversegam.py
import random
import sys

WIDTH = 8
HEIGHT = 8

def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append([' '] * WIDTH)
        #board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def drawBoard(board):
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))

    print(' +--------+')
    print('  12345678')

def getBoardCopy(board):
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]
    return boardCopy

def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            elif board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore} #Return a dictionary with keys 'X' and 'O'.

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s points' % (scores[playerTile], scores[computerTile]))

def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, "quit" to end the game, or "hints" to goggle hints')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter the column (1-8) and then the row (1-8).')
    return x, y

def isOnCorner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Find the highest-scoring move possible.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestScore = score
            bestMove = [x, y]

    return bestMove

def makeMove(board, tile, xstart, ystart):
    # to place a tile on the board and flip the other tiles
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnBoard(x, y):
    # Return True if the coordinates are located on the board.(0-7)
    return x >= 0 and x <= WIDTH -1 and y >=0 and y<= HEIGHT -1

def isValidMove(board, tile, xstart, ystart):
    # Return False if the player's move on space xstart, ystart is invalid.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    # If it is a valid move, return a list of spaces that would become the player's if they made a move here.
    # for a move to be valid, it must be both on the board and next to one of the other player’s tiles
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = [] # contain the coordinates of all opponent’s tiles that would be flipped
    coord = [[0, 1], [1, 1], [1, 0], [1, -1],
            [0, -1], [-1, -1], [-1, 0], [-1, 1]] # eight directions to check
    #for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
    for xdir, ydir in coord:
        x, y = xstart, ystart
        x += xdir # First step in the x direction
        y += ydir # First step in the y direction
        while isOnBoard(x, y) and board[x][y] == otherTile: # mark the start of sandwich
            # Keep moving in this x & y direction.
            x += xdir
            y += ydir
            if isOnBoard(x, y) and board[x][y] == tile: # mark the end of the sandwich made by the player’s tiles surrounding the opponent’s tiles
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y]) # record the coordinates of all of the opponent’s tiles that should be flipped
    if len(tilesToFlip) == 0: # none of the eight directions ended up flipping at least one of the opponent’s tiles, not a valid move
        return False

    return tilesToFlip


def getValidMoves(board, tile):
    """
        return: a list of two-item lists which hold the coordinates for all valid moves
    """
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getBoardWithValidMoves(board, tile):
    """
        purpose: displays a board with all possible moves marked on it as hints
        return: a game board data structure that has periods (.) for all spaces that are valid moves:
    """
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    #print('The %s will go first.' % (turn))

    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)
        #print(playerValidMoves)
        #print(computerValidMoves)
        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.
        elif turn == 'player':
            if playerValidMoves != []:
                """ if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                    #print('hint')
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    #print('show hints')
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1]) """
                move = getComputerMove(board, playerTile)
                makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'
        elif turn == 'computer':
            if computerValidMoves != []:
                """ drawBoard(board)
                printScore(board, playerTile, computerTile)

                input('Press Enter to see the computer\'s move.') """
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'

#main
NUM_GAMES = 250
xWins = oWins = ties = 0
print('Welcome to Reversegam!')
#playerTile, computerTile = enterPlayerTile()
playerTile, computerTile = ['X', 'O']

#while True:
for i in range(NUM_GAMES):
    finalBoard = playGame(playerTile, computerTile)

    # Display the final score.
    #drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('#%s:X scored %s points. O scored %s points.' % (i + 1, scores['X'], scores['O']))

    if scores[playerTile] > scores[computerTile]:
        xWins += 1
        #print('You beat the computer by %s points!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        oWins += 1
        #print('You lost. The computer beat you by %s points!' % (scores[computerTile] - scores[playerTile]))
    else:
        ties += 1
        #print('The game was a tie!')

    """ print('Do you want to play again?(yes or no)')
    if not input().lower().startswith('y'):
        break """

print('X wins: %s (%s%%)' % (xWins, round(xWins / NUM_GAMES * 100, 1)))
print('O wins: %s (%s%%)' % (oWins, round(oWins / NUM_GAMES * 100, 1)))
print('Ties: %s (%s%%)' % (ties, round(ties / NUM_GAMES * 100, 1)))