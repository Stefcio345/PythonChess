from pynput import keyboard

class Cursor:

    def __init__(self, maxX, maxY):
        self.x = 0
        self.y = 0
        self.maxX = maxX
        self.maxY = maxY
        self.selected = False
        self.selectedPos = (0, 0)

    def select(self):
        self.selectedPos = self.getPos()

    def isSelected(self):
        return self.selected

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

    def getPos(self):
        return self.x, self.y

    def move(self):
        with keyboard.Events() as events:
            event = events.get(1e6)
            if type(event) is keyboard.Events.Press:
                print("Something")
                try:
                    match event.key.char:
                        case 'w':
                            self.moveUp()
                        case 's':
                            self.moveDown()
                        case 'a':
                            self.moveLeft()
                        case 'd':
                            self.moveRight()

                except AttributeError:
                    match event.key:
                        case keyboard.Key.space:
                            self.select()
