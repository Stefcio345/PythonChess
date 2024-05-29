class ChessEngine:

    def updateBoard(self, boardState):
        whiteKingPos = self.getKingPos(boardState, "White")
        blackKingPos = self.getKingPos(boardState, "Black")
        self.whitePins, self.whiteChecks = self.checkForPins(whiteKingPos[0], whiteKingPos[1], boardState)
        self.blackPins, self.blackChecks = self.checkForPins(blackKingPos[0], blackKingPos[1], boardState)

    def getMoves(self, row, col, boardState):
        piece = boardState[row][col][1]
        color = boardState[row][col][0]
        kingPos = self.getKingPos(boardState, color)
        checkSources = []
        check = False
        if color == "White":
            pins = self.whitePins
            checks = self.whiteChecks
        else:
            pins = self.blackPins
            checks = self.blackChecks

        # If pinned cannot move
        if (row, col) in pins:
            return []

        match piece:
            case "Pawn":
                moves = self.getPawnMoves(row, col, boardState)
            case "Rook":
                moves = self.getRookMoves(row, col, boardState)
            case "Bishop":
                moves = self.getBishopMoves(row, col, boardState)
            case "Knight":
                moves = self.getKnightMoves(row, col, boardState)
            case "Queen":
                moves = self.getQueenMoves(row, col, boardState)
            case "King":
                return self.getKingMoves(row, col, boardState)
            case _:
                return []

        if len(checks) > 0:
            check = True
            for source, direction in checks:
                # calculate line from king to check source
                currPos = kingPos
                while currPos != source:
                    currPos = (currPos[0] + direction[0], currPos[1] + direction[1])
                    checkSources.append(currPos)
                checkSources.append(source)

        if check:
            return set(moves) & set(checkSources)
        else:
            return moves

    def getAllMoves(self, boardState, color=""):
        allMoves = set()
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile[0] == color or color == "":
                    possibleMoves = self.getMoves(indexY, indexX, boardState)
                    if len(possibleMoves) > 0:
                        allMoves.update(possibleMoves)

        return allMoves

    def getPawnMoves(self, row, col, boardState):

        possibleMoves = []
        allyColor = boardState[row][col][0]

        #Check movement
        if allyColor == "White":
            endRow = row - 1
            if boardState[endRow][col][1] == "Empty" and 0 <= endRow <= 7:
                possibleMoves.append((endRow, col))
                endRow = endRow - 1
                if boardState[endRow][col][1] == "Empty" and row == 6:
                    possibleMoves.append((endRow, col))
        if allyColor == "Black":
            endRow = row + 1
            if boardState[endRow][col][1] == "Empty" and 0 <= endRow <= 7:
                possibleMoves.append((endRow, col))
                endRow = endRow + 1
                if boardState[endRow][col][1] == "Empty" and row == 1:
                    possibleMoves.append((endRow, col))

        #Check Attacks
        possibleBlackAttacks = ((1, -1), (1, 1))
        possibleWhiteAttacks = ((-1, -1), (-1, 1))

        if allyColor == "White":
            for move in possibleWhiteAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "Black":
                        possibleMoves.append((endRow, endCol))

        if allyColor == "Black":
            for move in possibleBlackAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "White":
                        possibleMoves.append((endRow, endCol))

        return possibleMoves

    def getPawnAttacks(self, row, col, boardState):

        possibleMoves = []
        allyColor = boardState[row][col][0]

        #Check Attacks
        possibleBlackAttacks = ((1, -1), (1, 1))
        possibleWhiteAttacks = ((-1, -1), (-1, 1))

        if allyColor == "White":
            for move in possibleWhiteAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    possibleMoves.append((endRow, endCol))

        if allyColor == "Black":
            for move in possibleBlackAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    possibleMoves.append((endRow, endCol))

        return possibleMoves

    def getKnightMoves(self, row, col, boardState):

        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        possibleMoves = []
        allyColor = boardState[row][col][0]

        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = boardState[endRow][endCol]
                if endPiece[0] != allyColor:  # so its either enemy piece or empty square
                    possibleMoves.append((endRow, endCol))

        return possibleMoves

    def getRookMoves(self, row, col, boardState):
        RookMoves = ((-1, 0), (1, 0), (0, -1), (0, 1))  # left, right, down, up
        return self.checkForContinousMoves(row, col, boardState, RookMoves)

    def getBishopMoves(self, row, col, boardState):
        BishopMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # left down, right down, left up, right up
        return self.checkForContinousMoves(row, col, boardState, BishopMoves)

    def getQueenMoves(self, row, col, boardState):
        QueenMoves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        return self.checkForContinousMoves(row, col, boardState, QueenMoves)

    def getKingMoves(self, row, col, boardState):

        kingMoves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        possibleMoves = []
        allyColor = boardState[row][col][0]

        for move in kingMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = boardState[endRow][endCol]
                if endPiece[0] != allyColor:
                    #Simulate king move, check for checks
                    memoryPiece = boardState[endRow][endCol]
                    boardState[endRow][endCol] = boardState[row][col]
                    boardState[row][col] = ["Reset", "Empty", ""]
                    pins, checks = self.checkForPins(endRow, endCol, boardState)
                    if len(checks) == 0:
                        possibleMoves.append((endRow, endCol))

                    #Revert board
                    boardState[row][col] = boardState[endRow][endCol]
                    boardState[endRow][endCol] = memoryPiece

        return possibleMoves

    def checkForPins(self, row, col, boardState):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        checks = []
        pins = []
        allyColor = boardState[row][col][0]
        enemyColor = "White" if allyColor == "Black" else "Black"

        for index, move in enumerate(directions):
            nextRow = row
            nextCol = col
            possiblePin = ()
            for distance in range(1, 8):
                nextRow += move[0]
                nextCol += move[1]
                if 0 <= nextRow <= 7 and 0 <= nextCol <= 7:
                    nextSquare = boardState[nextRow][nextCol]
                    if nextSquare[1] != "Empty":
                        if nextSquare[0] == allyColor:
                            if possiblePin == ():
                                # Found possible pin
                                possiblePin = (nextRow, nextCol)
                            else:
                                # Found second ally piece
                                break

                        elif nextSquare[0] == enemyColor:
                            enemy = nextSquare[1]
                            if ((0 <= index <= 3 and enemy == "Rook") or
                                    (4 <= index <= 7 and enemy == "Bishop") or
                                    (enemy == "Queen") or
                                    (distance == 1 and enemy == "King") or
                                    (distance == 1 and enemy == "Pawn" and (
                                            (enemyColor == "Black" and 4 <= index <= 5) or (
                                             enemyColor == "White" and 6 <= index <= 7)))):
                                if possiblePin == ():
                                    # Found check append, check source + direction
                                    checks.append(((nextRow, nextCol), move))
                                    break
                                else:
                                    # Found pin
                                    pins.append(possiblePin)
                                    break
                            else:
                                # Enemy piece blocking
                                break
                else:
                    break

        # Check for Knights
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))

        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = boardState[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "Knight":  # so its either enemy piece or empty square
                    checks.append((endRow, endCol))

        return pins, checks

    def checkForContinousMoves(self, row, col, boardState, setOfMoves):
        possibleMoves = []
        allyColor = boardState[row][col][0]
        enemyColor = "White" if allyColor == "Black" else "Black"

        for move in setOfMoves:
            nextRow = row
            nextCol = col
            while True:
                nextRow += move[0]
                nextCol += move[1]
                if 0 <= nextRow <= 7 and 0 <= nextCol <= 7:
                    nextSquare = boardState[nextRow][nextCol]
                    if nextSquare[0] == enemyColor:  # Its enemy piece
                        possibleMoves.append((nextRow, nextCol))
                        break
                    elif nextSquare[0] != allyColor:  # Its Empty square
                        possibleMoves.append((nextRow, nextCol))
                    else:
                        break
                else:
                    break

        return possibleMoves

    def getKingPos(self, boardState, color):
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile[0] == color and tile[1] == "King":
                    return indexY, indexX
