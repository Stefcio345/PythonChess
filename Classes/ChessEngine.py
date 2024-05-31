class ChessEngine:
    currentColor = None

    def __init__(self, state, colorToMove):
        self.updateStates(state)
        self.currentColor = colorToMove
        self.mate = False

    def makeMove(self, startingPos, endPos, boardState):
        #TODO Bandaidfix check this later
        if boardState.get(startingPos).color == self.currentColor:
            if endPos in self.getMoves(startingPos, boardState):
                boardState.set(endPos, boardState.get(startingPos))
                boardState.set(startingPos, ["Reset", "Empty", ""])
                self.updateStates(boardState)
                self.mate = self.checkIfMate(boardState)
                return True
        return False

    def updateBoard(self, cursorPos, selectedPos, boardState):
        self.clearHighlights(boardState)
        self.highlightChecks(boardState)

        if selectedPos is not None:
            if boardState.get(selectedPos).color == self.currentColor:
                moves = self.getMoves(selectedPos, boardState)
                if len(moves) > 0:
                    self.highlightPossibleMoves(moves, boardState)

        boardState.get(cursorPos).background = "whiteBG"

    def updateStates(self, boardState):
        self.whiteKingPos = self.getKingPos(boardState, "White")
        self.blackKingPos = self.getKingPos(boardState, "Black")
        self.whitePins, self.whiteChecks = self.checkForPins(self.whiteKingPos, boardState)
        self.blackPins, self.blackChecks = self.checkForPins(self.blackKingPos, boardState)
        self.currentColor = self.getOppositeColor(self.currentColor)

    def getMoves(self, pos, boardState):
        piece = boardState.get(pos).content
        color = boardState.get(pos).color
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
        if pos in pins:
            return []

        match piece:
            case "Pawn":
                moves = self.getPawnMoves(pos, boardState)
            case "Rook":
                moves = self.getRookMoves(pos, boardState)
            case "Bishop":
                moves = self.getBishopMoves(pos, boardState)
            case "Knight":
                moves = self.getKnightMoves(pos, boardState)
            case "Queen":
                moves = self.getQueenMoves(pos, boardState)
            case "King":
                return self.getKingMoves(pos, boardState)
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
                if tile.color == color or color == "":
                    #TODO Check pos
                    possibleMoves = self.getMoves((indexY, indexX), boardState)
                    if len(possibleMoves) > 0:
                        allMoves.update(possibleMoves)

        return allMoves

    def getPawnMoves(self, pos, boardState):

        possibleMoves = []
        allyColor = boardState.get(pos).color

        #Check movement
        if allyColor == "White":
            endMove = (pos[0] - 1, pos[1])
            if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                if boardState.get(endMove).content == "Empty":
                    possibleMoves.append(endMove)
                    endMove = (endMove[0] - 1, endMove[1])
                    if pos[0] == 6:
                        if boardState.get(endMove).content == "Empty":
                            possibleMoves.append(endMove)
        if allyColor == "Black":
            endMove = (pos[0] + 1, pos[1])
            if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                if boardState.get(endMove).content == "Empty":
                    possibleMoves.append(endMove)
                    endMove = (endMove[0] + 1, endMove[1])
                    if pos[0] == 1:
                        if boardState.get(endMove).content == "Empty":
                            possibleMoves.append(endMove)

        #Check Attacks
        possibleBlackAttacks = ((1, -1), (1, 1))
        possibleWhiteAttacks = ((-1, -1), (-1, 1))

        if allyColor == "White":
            for move in possibleWhiteAttacks:
                endMove = (pos[0] + move[0], pos[1] + move[1])
                if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                    if boardState.get(endMove).color == "Black":
                        possibleMoves.append(endMove)

        if allyColor == "Black":
            for move in possibleBlackAttacks:
                endMove = (pos[0] + move[0], pos[1] + move[1])
                if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                    if boardState.get(endMove).color == "White":
                        possibleMoves.append(endMove)

        return possibleMoves

    def getKnightMoves(self, pos, boardState):

        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        possibleMoves = []
        allyColor = boardState.get(pos).color

        for move in knightMoves:
            endMove = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                endPiece = boardState.get(endMove)
                if endPiece.color != allyColor:  # so its either enemy piece or empty square
                    possibleMoves.append(endMove)

        return possibleMoves

    def getRookMoves(self, pos, boardState):
        RookMoves = ((-1, 0), (1, 0), (0, -1), (0, 1))  # left, right, down, up
        return self.checkForContinousMoves(pos, boardState, RookMoves)

    def getBishopMoves(self, pos, boardState):
        BishopMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # left down, right down, left up, right up
        return self.checkForContinousMoves(pos, boardState, BishopMoves)

    def getQueenMoves(self, pos, boardState):
        QueenMoves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        return self.checkForContinousMoves(pos, boardState, QueenMoves)

    def getKingMoves(self, pos, boardState):

        kingMoves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        possibleMoves = []
        allyColor = boardState.get(pos).color

        for move in kingMoves:
            endMove = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= endMove[0] <= 7 and 0 <= endMove[1] <= 7:
                endPiece = boardState.get(endMove)
                if endPiece.color != allyColor:
                    #Simulate king move, check for checks
                    memoryPiece = boardState.get(endMove)
                    boardState.set(endMove, boardState.get(pos))
                    boardState.set(pos, ["Reset", "Empty", ""])
                    pins, checks = self.checkForPins(endMove, boardState)
                    if len(checks) == 0:
                        possibleMoves.append(endMove)

                    #Revert board
                    boardState.set(pos, boardState.get(endMove))
                    boardState.set(endMove, memoryPiece)

        return possibleMoves

    def checkForPins(self, pos, boardState):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        checks = []
        pins = []
        allyColor = boardState.get(pos).color
        enemyColor = "White" if allyColor == "Black" else "Black"

        for index, move in enumerate(directions):
            nextMove = pos
            possiblePin = ()
            for distance in range(1, 8):
                nextMove = (nextMove[0] + move[0], nextMove[1] + move[1])
                if 0 <= nextMove[0] <= 7 and 0 <= nextMove[1] <= 7:
                    nextSquare = boardState.get(nextMove)
                    if nextSquare.content != "Empty":
                        if nextSquare.color == allyColor:
                            if possiblePin == ():
                                # Found possible pin
                                possiblePin = nextMove
                            else:
                                # Found second ally piece
                                break

                        elif nextSquare.color == enemyColor:
                            enemy = nextSquare.content
                            if ((0 <= index <= 3 and enemy == "Rook") or
                                    (4 <= index <= 7 and enemy == "Bishop") or
                                    (enemy == "Queen") or
                                    (distance == 1 and enemy == "King") or
                                    (distance == 1 and enemy == "Pawn" and (
                                            (enemyColor == "Black" and 4 <= index <= 5) or (
                                            enemyColor == "White" and 6 <= index <= 7)))):
                                if possiblePin == ():
                                    # Found check append, check source + direction
                                    checks.append((nextMove, move))
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
            nextMove = (pos[0] + move[0], pos[1] + move[1])
            if 0 <= nextMove[0] <= 7 and 0 <= nextMove[1] <= 7:
                endPiece = boardState.get(nextMove)
                if endPiece.color == enemyColor and endPiece.content == "Knight":
                    checks.append((nextMove, move))

        return pins, checks

    def checkForContinousMoves(self, pos, boardState, setOfMoves):
        possibleMoves = []
        allyColor = boardState.get(pos).color
        enemyColor = "White" if allyColor == "Black" else "Black"

        for move in setOfMoves:
            nextMove = pos
            while True:
                nextMove = (nextMove[0] + move[0], nextMove[1] + move[1])
                if 0 <= nextMove[0] <= 7 and 0 <= nextMove[1] <= 7:
                    nextSquare = boardState.get(nextMove)
                    if nextSquare[0] == enemyColor:  # Its enemy piece
                        possibleMoves.append(nextMove)
                        break
                    elif nextSquare[0] != allyColor:  # Its Empty square
                        possibleMoves.append(nextMove)
                    else:
                        break
                else:
                    break

        return possibleMoves

    def getKingPos(self, boardState, color):
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile.color == color and tile.content == "King":
                    return indexY, indexX

    def checkIfMate(self, boardState):
        if len(self.whiteChecks) > 0:
            if len(self.getAllMoves(boardState, "White")) == 0:
                return True
        elif len(self.blackChecks) > 0:
            if len(self.getAllMoves(boardState, "Black")) == 0:
                return True
        else:
            return False

    def highlightChecks(self, boardState):
        if len(self.whiteChecks) > 0:
            boardState.get(self.whiteKingPos).background = "Redbg"
        if len(self.blackChecks) > 0:
            boardState.get(self.blackKingPos).background = "Redbg"

    def clearHighlights(self, boardState):
        for row in boardState:
            for cell in row:
                cell[2] = ""

    def highlightPossibleMoves(self, possibleMoves, boardState):
        for move in possibleMoves:
            boardState.get(move).background = "greenbg"

    def getOppositeColor(self, color):
        if color == "White":
            return "Black"
        else:
            return "White"
