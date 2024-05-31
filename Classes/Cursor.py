from pynput import keyboard


class Cursor:

    def __init__(self, maxX, maxY):
        self.x = 0
        self.y = 0
        self.maxX = maxX
        self.maxY = maxY
        self.selectedPos = None
        self.prevSelectedPos = None

    def select(self):
        self.prevSelectedPos = self.selectedPos
        self.selectedPos = self.getPos()
        if self.prevSelectedPos == self.selectedPos:
            self.unSelect()

    def unSelect(self):
        self.selectedPos = None
        self.prevSelectedPos = None

    def reset(self):
        self.unSelect()
        self.x = 0
        self.y = 0

    def getPos(self):
        return self.y, self.x

    def moveUp(self):
        if self.y > 0:
            self.y -= 1

    def moveDown(self):
        if self.y < self.maxY:
            self.y += 1

    def moveLeft(self):
        if self.x > 0:
            self.x -= 1

    def moveRight(self):
        if self.x < self.maxX:
            self.x += 1

    def move(self):
        with keyboard.Events() as events:
            event = events.get(1e6)
            if type(event) is keyboard.Events.Press:
                try:
                    key = event.key.char
                    match key:
                        case 'w':
                            self.moveUp()
                            return "Valid_key"
                        case 's':
                            self.moveDown()
                            return "Valid_key"
                        case 'a':
                            self.moveLeft()
                            return "Valid_key"
                        case 'd':
                            self.moveRight()
                            return "Valid_key"
                        case _:
                            return "Invalid_key"

                except AttributeError:
                    match event.key:
                        case keyboard.Key.esc:
                            return "Pause"
                        case keyboard.Key.space:
                            self.select()
                            return "Valid_key"
                        case keyboard.Key.enter:
                            self.select()
                            return "Valid_key"
                        case keyboard.Key.up:
                            self.moveUp()
                            return "Valid_key"
                        case keyboard.Key.down:
                            self.moveDown()
                            return "Valid_key"
                        case keyboard.Key.left:
                            self.moveLeft()
                            return "Valid_key"
                        case keyboard.Key.right:
                            self.moveRight()
                            return "Valid_key"
                        case _:
                            return "Invalid_key"
