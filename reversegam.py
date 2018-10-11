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
        return 'palyer'

def getNewBoard():
    board = []
    for i in range(WIDTH):
        board.append([' ']*8)
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

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print('The %s will go first.' % (turn))

    board = getNewBoard()

    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        palyerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if palyerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.
        elif turn == 'player':
            if palyerValidMoves != []:
                if showHints:
                    print('hint')
                else:
                    drawBoard(board)
            printScore(board, playerTile, computerTile)

            move = getPlayerMove(board, playerTile)

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH -1 and y >=0 and y<= HEIGHT -1

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != '' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    coord = [[0, 1], [1, 1], [1, 0], [1, -1],
            [0, -1], [-1, -1], [-1, 0], [-1, 1]]
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

#main
print('Welcome to Reversegam!')
playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)
