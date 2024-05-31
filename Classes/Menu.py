import os

from .Cursor import Cursor


class MenuItem:

    def __init__(self, value, text):
        self.value = value
        self.text = text

    def __str__(self):
        return self.text


class Menu:

    def __init__(self, title):
        self.title = title
        self.items = []
        self.cursor = Cursor(0, -1)

        self.maxLength = 0
        for line in self.title.split("\n"):
            if len(line) > self.maxLength:
                self.maxLength = len(line)

    def add_item(self, menuItem: MenuItem):
        self.cursor.maxY += 1
        self.items.append(menuItem)

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.title + "\n")
        for indexY, item in enumerate(self.items):
            if self.cursor.y == indexY:
                print(self.centerHighlight(item.text))
            else:
                print(self.center(item.text))

    def select(self):
        self.display()
        while self.cursor.selectedPos is None:
            if self.cursor.move():
                if self.cursor.selectedPos is not None:
                    selectedPos = self.cursor.selectedPos[0]
                    self.cursor.reset()
                    return self.items[selectedPos].value
                self.display()

    def center(self, text):
        if len(text) <= self.maxLength:
            return int((self.maxLength-len(text))/2)*" " + text + " "*int((self.maxLength-len(text))/2)
        else:
            return text


    def centerHighlight(self, text):
        if len(text) <= self.maxLength:
            return int((self.maxLength-len(text))/2)*" " + '\033[1m\033[47m' + text + '\033[0m' + " "*int((self.maxLength-len(text))/2)
        else:
            return '\033[1m\033[47m' + text + '\033[0m'
