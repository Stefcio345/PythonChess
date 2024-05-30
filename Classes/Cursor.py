from pynput import keyboard


class Cursor:

    def __init__(self, maxX, maxY):
        self.x = 0
        self.y = 0
        self.maxX = maxX
        self.maxY = maxY
        self.selected = False
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
                            return True
                        case 's':
                            self.moveDown()
                            return True
                        case 'a':
                            self.moveLeft()
                            return True
                        case 'd':
                            self.moveRight()
                            return True
                        case _:
                            return False

                except AttributeError:
                    match event.key:
                        case keyboard.Key.space:
                            self.select()
                            return True
                        case keyboard.Key.up:
                            self.moveUp()
                            return True
                        case keyboard.Key.space.down:
                            self.moveDown()
                            return True
                        case keyboard.Key.left:
                            self.moveLeft()
                            return True
                        case keyboard.Key.right:
                            self.moveRight()
                            return True
                        case _:
                            return False
