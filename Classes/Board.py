import os

Colors = {
    #"BLACK": '\033[30m',
    "Black": '\033[90m',
    "Red": '\033[31m',
    "Green": '\033[32m',
    "Yellow": '\033[33m',
    "Blue": '\033[34m',
    "Magenta": '\033[35m',
    "Cyan": '\033[36m',
    "Light_Gray": '\033[37m',
    "Dark_Gray": '\033[90m',
    "Bright_Red": '\033[91m',
    "Bright_Green": '\033[92m',
    "Bright_Yellow": '\033[93m',
    "Bright_Blue": '\033[94m',
    "Bright_Magenta": '\033[95m',
    "Bright_Cyan": '\033[96m',
    "White": '\033[97m',
    "Reset": '\033[0m'}

class GraphicsNotSameSizeException(Exception):
    def __init__(self):
        super().__init__("All graphics are not the same size")


class GraphicsHandler:
    graphics = {}
    squareSizeVertical = 0
    squareSizeHorizontal = 0

    def __init__(self):
        self.squareSizeVertical, self.squareSizeHorizontal = self.loadSquareSizeFromFiles()
        self.normalizeGraphics(self.squareSizeHorizontal)
        self.loadGraphicsIntoMemory()

        # Add Hardcoded tiles
        self.graphics["None"] = [[" "] * self.squareSizeHorizontal for x in range(self.squareSizeVertical)]
        self.graphics["Missing"] = [["E"] * self.squareSizeHorizontal for x in range(self.squareSizeVertical)]

    def getGraphics(self, name):
        if name in self.graphics.keys():
            return self.graphics[name]
        else:
            return self.graphics["Missing"]

    def loadGraphicsIntoMemory(self, path="./Graphics"):
        for file in os.listdir(path):
            graphicsLoadedFromFile = []
            f = open(f"{path}/{file}", "r", encoding="utf-8", errors='ignore')
            for line in f:
                line = line.strip("\n")
                list = []
                for letter in [*line]:
                    list.append(letter)
                graphicsLoadedFromFile.append(list)

            self.graphics[file] = graphicsLoadedFromFile

    def loadSquareSizeFromFiles(self):
        nextSizeVertical = 0
        sizeHorizontal = 0
        sizeVertical = 0

        for index, file in enumerate(os.listdir("./Graphics")):
            sizeVertical = 0
            f = open(f"./Graphics/{file}", "r", encoding="utf-8", errors='ignore')
            for line in f:
                sizeVertical += 1
                # Check horizontal size
                line = line.rstrip()
                sizeHorizontal = sizeHorizontal if len(line) < sizeHorizontal else len(line)

            # Check if all graphics all same size
            if index > 0:
                if nextSizeVertical != sizeVertical:
                    raise GraphicsNotSameSizeException
            nextSizeVertical = sizeVertical

        return sizeVertical, sizeHorizontal

    def normalizeGraphics(self, maxHorizontalSize):
        for file in os.listdir("./Graphics"):
            newLetter = ""
            f = open(f"./Graphics/{file}", "r+", encoding="utf-8", errors='ignore')
            for line in f:
                line = line.rstrip()
                if len(line) < maxHorizontalSize:
                    newLetter += line + " " * (maxHorizontalSize - len(line)) + "\n"
                else:
                    newLetter += line + "\n"

            # Override nonNormalized letters
            f.seek(0)
            f.write(newLetter)
            f.truncate()
            f.close()


class Square:
    currentRow = 0
    loadedState = ""

    def __init__(self, graphicsHandler, background="None"):
        self.state = "Empty"
        self.color = "Reset"
        self.background = background
        self.graphicHandler = graphicsHandler

    def printRow(self):
        foreground = self.graphicHandler.getGraphics(self.state)
        bakcground = self.graphicHandler.getGraphics(self.background)

        for pixelForeground, pixelBackground in zip(foreground[self.currentRow], bakcground[self.currentRow]):
            if pixelForeground == " ":
                print(Colors["Reset"] + pixelBackground, end="")
            else:
                print(Colors[self.color] + pixelForeground, end="")
        if self.currentRow < len(foreground) - 1:
            self.currentRow += 1
        else:
            self.currentRow = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        value = value.split(" ")
        if len(value) == 1:
            self._state = value[0].title()
        else:
            self.color = value[0].title()
            self._state = value[1].title()


class Row:
    number = 0

    def __init__(self, rowSize, squareVerticalSize, graphicsHandler, verticalSpace=0):
        self.verticalSpace = verticalSpace
        self.size = rowSize
        self.row = [Square(graphicsHandler) for x in range(rowSize)]
        self.squareVerticalSize = squareVerticalSize

    def __iter__(self):
        self.number = 0
        return self

    def __next__(self):
        if self.number < self.size:
            self.number += 1
            return self.row[self.number - 1]
        else:
            raise StopIteration

    def printRow(self):
        for i in range(self.squareVerticalSize):
            for square in self.row:
                square.printRow()
                print(" "" " * self.verticalSpace, end="")
            print("")

    def getPos(self, index):
        return self.row[index]


class Board:

    def __init__(self, size, verticalSpaces=0, horizontalSpaces=0):
        self.graphicsHandler = GraphicsHandler()
        self.horizontalSpaces = horizontalSpaces
        # Prepare board
        self.boardState = [
            Row(size, self.graphicsHandler.squareSizeVertical, self.graphicsHandler, verticalSpaces) for x in
            range(size)]
        # Set Top of board
        number = 64
        for square in self.boardState[0]:
            square.state = chr(number)
            number += 1

        # Set side of board
        number = 0
        for row in self.boardState:
            row.getPos(0).state = "None" if number == 0 else str(number)
            number += 1

    def printBoardState(self):
        for row in self.boardState:
            for square in row:
                print(square.state + ", ", end="")
            print("")

    def printBoard(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.boardState:
            row.printRow()

            for i in range(self.horizontalSpaces):
                print("")


class ChessBoard(Board):
    def __init__(self, verticalSpaces=0, horizontalSpaces=0):
        super().__init__(9, verticalSpaces, horizontalSpaces)

        # Set Black pieces
        self.setPawn("Black", 2)
        self.setFigures("Black", 1)

        # Set white pieces
        self.setPawn("White", 7)
        self.setFigures("White", 8)

        self.colorBoard()

    def getBoardState(self):
        state = []
        for indexY, row in enumerate(self.boardState):
            if indexY != 0:
                temp = []
                for indexX, square in enumerate(row):
                    if indexX != 0:
                        temp.append((square.color, square.state))
                state.append(temp)

        return state


    def setBoardState(self, state):
        for selfRow, row in zip(self.boardState[1:], state):
            for index, square in enumerate(row):
                selfRow.getPos(index + 1).color = square[0]
                selfRow.getPos(index+1).state = square[1]


    def printBoardState(self):
        for indexY, row in enumerate(self.boardState):
            if indexY != 0:
                for indexX, square in enumerate(row):
                    if indexX != 0:
                        if square.color == "Reset":
                            print(square.state + ", ", end="")
                        else:
                            print(square.color + " " + square.state + ", ", end="")
                print("")

    def colorBoard(self):
        count = 0
        for indexY, row in enumerate(self.boardState):
            if indexY > 0:
                for indexX, square in enumerate(row):
                    if indexX > 0:
                        square.background = "EmptyWhite" if count % 2 == 0 else "EmptyBlack"
                    count += 1

    def setPawn(self, color, row):
        for square in self.boardState[row]:
            if square.state == "Empty":
                square.state = f"{color} Pawn"

    def setFigures(self, color, row):
        self.boardState[row].getPos(1).state = self.boardState[row].getPos(8).state = f"{color} Rook"
        self.boardState[row].getPos(2).state = self.boardState[row].getPos(7).state = f"{color} Knight"
        self.boardState[row].getPos(3).state = self.boardState[row].getPos(6).state = f"{color} Bishop"
        self.boardState[row].getPos(4).state = f"{color} Queen"
        self.boardState[row].getPos(5).state = f"{color} King"
