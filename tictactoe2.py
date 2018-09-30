# Tic Tac Toe
import random
import time

def drawBoard(board):
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
    if random.randint(0, 1) == 0:
        return ['O', 'X']
    else:
        return ['X', 'O']


def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer1'
    else:
        return 'computer2'

def isSpaceFree(board, move):
    # return true if the passed move is free on the passed board
    return board[move] == ' '

def getPlayerMove(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move?(1-9)')
        move = input()
    return int(move)

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(board, letter):
    return (
        (board[7] == letter and board[8] == letter and board[9] == letter) or # across the top
        (board[4] == letter and board[5] == letter and board[6] == letter) or # across the middle
        (board[1] == letter and board[2] == letter and board[3] == letter) or # across the bottom
        (board[7] == letter and board[4] == letter and board[1] == letter) or # down the left side
        (board[8] == letter and board[5] == letter and board[2] == letter) or # down the middle
        (board[9] == letter and board[6] == letter and board[3] == letter) or # down the right side
        (board[7] == letter and board[5] == letter and board[3] == letter) or # diagonal
        (board[9] == letter and board[5] == letter and board[1] == letter) # diagonal
    )

def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def getBoardCopy(board):
    dupBoard = []

    for i in board:
        dupBoard.append(i)

    return dupBoard

def chooseRandomMoveFromList(board, moveList):
    possibleMoves = []
    for i in moveList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    if isSpaceFree(board, 5):
        return 5

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def playAgain():
    print('Do you want to play again?(yes or no)')
    return input().lower().startswith('y')

#main
print('Welcome to Tic Tac Toe!')

while True:

    theBoard = [' '] * 10
    computer1Letter, computer2Letter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:

        if turn == 'computer1': # computer1's turn

            move = getComputerMove(theBoard, computer1Letter)
            makeMove(theBoard, computer1Letter, move)

            if isWinner(theBoard, computer1Letter):
                drawBoard(theBoard)
                print('The computer1 has won!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    drawBoard(theBoard)
                    turn = 'computer2'
                    print(turn + ' is thinking ...')
                    time.sleep(3)
        else: # computer2's turn

            move = getComputerMove(theBoard, computer2Letter)
            makeMove(theBoard, computer2Letter, move)

            if isWinner(theBoard, computer2Letter):
                drawBoard(theBoard)
                print('The computer2 has won!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    drawBoard(theBoard)
                    turn = 'computer1'
                    print(turn + ' is thinking ...')
                    time.sleep(3)

    if not playAgain():
        break