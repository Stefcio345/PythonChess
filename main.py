import os

from Classes.Board import ChessBoard, setGraphics, setColors
from Classes.ChessEngine import ChessEngine
from Classes.Cursor import Cursor
from Classes.BoardState import BoardState, loadFromFile
from Classes.Menu import Menu, MenuItem

# Main menu
mainMenu = Menu("""+=======================================+
|  ____   _   _   _____   ____    ____  |
| / ___| | | | | | ____| / ___|  / ___| |
|| |     | |_| | |  _|   \___ \  \___ \ |
|| |___  |  _  | | |___   ___) |  ___) ||
| \____| |_| |_| |_____| |____/  |____/ |
+=======================================+""")
mainMenu.add_item(MenuItem("start_game", "2-Player Game"))
mainMenu.add_item(MenuItem("resume_game", "Resume Game"))
mainMenu.add_item(MenuItem("options", "Options"))
mainMenu.add_item(MenuItem("exit", "Exit"))

pauseMenu = Menu("""+=========================================+
| ____       _      _   _   ____    _____ |
||  _ \     / \    | | | | / ___|  | ____||
|| |_) |   / _ \   | | | | \___ \  |  _|  |
||  __/   / ___ \  | |_| |  ___) | | |___ |
||_|     /_/   \_\  \___/  |____/  |_____||
+=========================================+""")
pauseMenu.add_item(MenuItem("resume", "Resume Game"))
pauseMenu.add_item(MenuItem("save_and_exit", "Save and Exit"))
pauseMenu.add_item(MenuItem("exit", "Exit to Main Menu"))

optionsMenu = Menu("""+=====================================================+
|  ___    ____    _____   ___    ___    _   _   ____  |
| / _ \  |  _ \  |_   _| |_ _|  / _ \  | \ | | / ___| |
|| | | | | |_) |   | |    | |  | | | | |  \| | \___ \ |
|| |_| | |  __/    | |    | |  | |_| | | |\  |  ___) ||
| \___/  |_|       |_|   |___|  \___/  |_| \_| |____/ |
+=====================================================+""")
optionsMenu.add_item(MenuItem("main_menu", "Go Back to Main Menu"))
optionsMenu.add_item(MenuItem("change_graphics", "Change graphics"))
optionsMenu.add_item(MenuItem("change_color", "Change colors"))

noSaveMenu = Menu("""+=====================================================+
| _   _    ___      ____       _     __     __  _____ |
|| \ | |  / _ \    / ___|     / \    \ \   / / | ____||
||  \| | | | | |   \___ \    / _ \    \ \ / /  |  _|  |
|| |\  | | |_| |    ___) |  / ___ \    \ V /   | |___ |
||_| \_|  \___/    |____/  /_/   \_\    \_/    |_____||
+=====================================================+""")
noSaveMenu.add_item(MenuItem("exit", "Exit"))

#TODO Read items from file
#TODO Normalize graphics when changing
changeGraphics = Menu("""Choose graphics folder name""")
changeGraphics.add_item(MenuItem("defaultGraphics", "Default Graphics"))
changeGraphics.add_item(MenuItem("asciiGraphics", "Ascii Graphics"))
changeGraphics.add_item(MenuItem("exit", "Exit"))

changeColor = Menu("""Choose for what you want to change color""")
changeColor.add_item(MenuItem("black_pieces", "Black Pieces"))
changeColor.add_item(MenuItem("white_pieces", "White Pieces"))
#changeColor.add_item(MenuItem("highlight", "Highlight"))

chooseColor = Menu("""Choose which color""")
chooseColor.add_item(MenuItem("\033[90m", "\033[90m Black"))
chooseColor.add_item(MenuItem("\033[31m", "\033[31m Red"))
chooseColor.add_item(MenuItem("\033[32m", "\033[32m Green"))
chooseColor.add_item(MenuItem("\033[33m", "\033[33m Yellow"))
chooseColor.add_item(MenuItem("\033[34m", "\033[34m Blue"))
chooseColor.add_item(MenuItem("\033[35m", "\033[35m Magenta"))
chooseColor.add_item(MenuItem("\033[36m", "\033[36m Cyan"))
chooseColor.add_item(MenuItem("\033[37m", "\033[37m Light Gray"))
chooseColor.add_item(MenuItem("\033[90m", "\033[90m Dark Gray"))
chooseColor.add_item(MenuItem("\033[91m", "\033[91m Bright Red"))
chooseColor.add_item(MenuItem("\033[92m", "\033[92m Bright Green"))
chooseColor.add_item(MenuItem("\033[93m", "\033[93m Bright Yellow"))
chooseColor.add_item(MenuItem("\033[94m", "\033[94m Bright Blue"))
chooseColor.add_item(MenuItem("\033[95m", "\033[95m Bright Magenta"))
chooseColor.add_item(MenuItem("\033[96m", "\033[96m Bright Cyan"))
chooseColor.add_item(MenuItem("\033[97m", "\033[97m White"))


def startGame(customState=None):
    # Prepare board
    board = ChessBoard()
    if customState is None:
        state = BoardState(board.getBoardState())
    else:
        state = BoardState(customState)
        board.setBoardState(state)
    chessEngine = ChessEngine(state, "White")
    boardCursor = Cursor(7, 7)
    board.printBoard()

    # GameLoop
    while True:
        match boardCursor.move():
            case "Valid_key":
                cursorPos = boardCursor.getPos()

                # If second tile was selected
                if boardCursor.prevSelectedPos is not None:
                    # Try to make a move
                    if chessEngine.makeMove(boardCursor.prevSelectedPos, boardCursor.selectedPos, state):
                        boardCursor.unSelect()


                # Update board after move
                chessEngine.updateBoard(cursorPos, boardCursor.selectedPos, state)

                board.setBoardState(state)
                board.printBoard()

                if chessEngine.mate:
                    print(f"{ChessEngine.currentColor} WINS!!!! \n Press enter to exit")
                    boardCursor.move()
                    break
            case "Pause":
                match pauseMenu.select():
                    case "resume":
                        pass
                    case "save_and_exit":
                        state.saveToFile("save")
                        break
                    case "exit":
                        break
            case "Invalid_key":
                pass


if __name__ == "__main__":
    while True:
        match mainMenu.select():
            case "start_game":
                startGame()
            case "resume_game":
                if os.path.isfile("./save"):
                    state = loadFromFile("save")
                    startGame(state)
                else:
                    noSaveMenu.select()
            case "options":
                match optionsMenu.select():
                    case "main_menu":
                        pass
                    case "change_graphics":
                        new = changeGraphics.select()
                        match new:
                            case "exit":
                                pass
                            case _:
                                setGraphics(new)
                    case "change_color":
                        match changeColor.select():
                            case "black_pieces":
                                setColors("Black", chooseColor.select())
                            case "white_pieces":
                                setColors("White", chooseColor.select())
            case "exit":
                exit()
