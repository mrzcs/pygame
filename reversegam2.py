#reversegam.py
import random
import sys
import time

WIDTH = 19
HEIGHT = 19

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
    #print('  123456789012345')
    print('+' + '-'*WIDTH +'+')
    #print(' +--------+')
    for y in range(HEIGHT):
        print('|', end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|')

    print('+' + '-'*WIDTH +'+')
    #print('  123456789012345')

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
    temp = []
    for i in range(WIDTH):
        temp.append(i)
    #DIGITS1TO8 = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20'.split()
    DIGITS1TO8 = temp.remove(0)
    print(DIGITS1TO8)
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

def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnBoard(x, y):
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
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH -1 and y >=0 and y<= HEIGHT -1

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    coord = [[0, 1], [1, 1], [1, 0], [1, -1],
            [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    #for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
    for xdir, ydir in coord:
        x, y = xstart, ystart
        x += xdir
        y += ydir
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # Keep moving in this x & y direction.
            x += xdir
            y += ydir
            if isOnBoard(x, y) and board[x][y] == tile:

                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    if len(tilesToFlip) == 0:
        return False

    return tilesToFlip


def getValidMoves(board, tile):
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getBoardWithValidMoves(board, tile):
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '-'
    return boardCopy

def playGame(playerTile, computerTile):
    #showHints = False
    turn = whoGoesFirst()
    print('The %s will go first.' % (turn))

    board = getNewBoard()
    xcenter  = int(WIDTH/2)
    ycenter = int(HEIGHT/2)
    board[xcenter-1][ycenter-1] = 'X'
    board[xcenter-1][ycenter] = 'O'
    board[xcenter][ycenter-1] = 'O'
    board[xcenter][ycenter] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)
        #print(playerValidMoves)
        #print(computerValidMoves)
        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.
        elif turn == 'player':
            if playerValidMoves != []:
                #drawBoard(board)
                #printScore(board, playerTile, computerTile)

                #input('Press Enter to see the player\'s move.')
                move = getComputerMove(board, playerTile)
                makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'
        elif turn == 'computer':
            if computerValidMoves != []:
                #drawBoard(board)
                #printScore(board, playerTile, computerTile)

                #input('Press Enter to see the computer\'s move.')
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'
        #time.sleep(1)



#main
print('Welcome to Reversegam!')
playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)

    # Display the final score.
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored %s points. O scored %s points! Congras!' % (scores['X'], scores['O']))

    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points!' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    print('Do you want to play again?(yes or no)')
    if not input().lower().startswith('y'):
        break
