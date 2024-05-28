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

def getOppositeColor(color):
    if color == "White":
        return "Black"
    else:
        return "White"

testState = [[["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["Black","Pawn",""],["Reset","Empty",""],["Reset","Empty",""],["Black","Pawn",""],["Reset","Empty",""],["Black","Pawn",""]],
[["White","Pawn",""],["Reset","Empty",""],["Black","Knight",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Black","Pawn",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["White","Queen",""],["White","Pawn",""],["Black","King",""],["White","Bishop",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["White","Pawn",""],["Reset","Empty",""],["White","Pawn",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]],
[["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""],["White","King",""],["Reset","Empty",""],["Reset","Empty",""],["Reset","Empty",""]]]

board = ChessBoard()
board.setBoardState(testState)
chessEngine = ChessEngine()
possibleMoves = []
boardCursor = Cursor(7, 7)
board.printBoard()
currentColor = "White"

# GameLoop
while True:
    prevCursorPos = boardCursor.getPos()
    prevSelectedPos = boardCursor.selectedPos
    if boardCursor.move():
        cursorPos = boardCursor.getPos()
        testState[prevCursorPos[1]][prevCursorPos[0]][2] = ""
        clearBoardState(testState)

        selectedPos = boardCursor.selectedPos

        if testState[selectedPos[1]][selectedPos[0]][0] == currentColor:
            possibleMoves = chessEngine.getMoves(selectedPos[1], selectedPos[0], testState)

        # If piece was selected
        if len(possibleMoves) > 0:
            if (selectedPos[1], selectedPos[0]) in possibleMoves:
                # Make move
                testState[selectedPos[1]][selectedPos[0]] = testState[prevSelectedPos[1]][prevSelectedPos[0]]
                testState[prevSelectedPos[1]][prevSelectedPos[0]] = ["Reset","Empty",""]
                currentColor = getOppositeColor(currentColor)
                possibleMoves = []
            else:
                if testState[selectedPos[1]][selectedPos[0]][0] == currentColor:
                    possibleMoves = chessEngine.getMoves(selectedPos[1], selectedPos[0], testState)
                else:
                    possibleMoves = []

        # Color board
        highlightPossibleMoves(possibleMoves, testState)
        testState[cursorPos[1]][cursorPos[0]][2] = "whiteBG"

        board.setBoardState(testState)
        board.printBoard()


