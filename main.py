import time

from Classes.Board import ChessBoard
from Classes.ChessEngine import ChessEngine
from Classes.Cursor import Cursor

def highlightPossibleMoves(possibleMoves, boardState):
    for move in possibleMoves:
        boardState[move[0]][move[1]][2] = "greenbg"
def clearBoardState(boardState):
    for row in boardState:
        for cell in row:
            cell[2] = ""


testState = [[["Reset","Empty",""],["Reset","Empty",""],["Black","Bishop",""],["Black","Queen",""],["Reset","Empty",""],["Black","Bishop",""],["Black","Knight",""],["Black","Rook",""]],
[["Black","Pawn",""],["Black","Pawn",""],["Black","Pawn",""],["Black","Pawn",""],["Reset","Empty",""],["Black","Pawn",""],["Black","Pawn",""],["Black","Pawn",""]],
[["White","Pawn",""],["Reset","Empty",""],["Black","Knight",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Black","Pawn",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["White","Queen",""],["White","Pawn",""],["Black","King",""],["White","Bishop",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Black","Rook",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["White","Pawn",""],["White","Pawn",""],["White","Pawn",""],["Reset","Empty",""],["White","Pawn",""],["White","Pawn",""],["White","Pawn",""],["Reset","Empty",""]],
[["White","Rook",""],["White","Knight",""],["Reset","Empty",""],["Reset","Empty",""],["White","King",""],["White","Bishop",""],["White","Knight",""],["White","Rook",""]]]

board = ChessBoard()
board.setBoardState(testState)
chessEngine = ChessEngine()
possibleMoves = []
boardCursor = Cursor(7, 7)

#GameLoopssssssds
while True:
    #board.printBoard()

    #Move cursor
    prevCursorPos = boardCursor.getPos()
    prevSelectedPos = boardCursor.selectedPos
    boardCursor.move()
    cursorPos = boardCursor.getPos()
    testState[prevCursorPos[1]][prevCursorPos[0]][2] = ""
    clearBoardState(testState)

    selectedPos = boardCursor.selectedPos
    possibleMoves = chessEngine.getMoves(selectedPos[1], selectedPos[0], testState)

    #If piece was selected
    if len(possibleMoves) > 0:
        highlightPossibleMoves(possibleMoves, testState)
        if (selectedPos[1], selectedPos[0]) in possibleMoves:
            print("TREUEIEVNWEIUNEWOINFRUIEHJOPWBYUFIVJFEJKBHFIWEKJVUIWERHFPOEWFHUI")

    # Color board
    testState[cursorPos[1]][cursorPos[0]][2] = "whiteBG"

    board.setBoardState(testState)









