def loadFromFile(filename):
    file = open(filename, 'r')
    data = file.read()
    data = data.split("\n")
    for index, row in enumerate(data):
        data[index] = row.split()

    for indexRow, row in enumerate(data):
        for indexCol, cell in enumerate(row):
            cell = cell.split(",")
            cell = (cell[1], cell[0], "")
            data[indexRow][indexCol] = cell

    return data



class BoardState:

    def __init__(self, state):
        self.state = []
        for row in state:
            temp = []
            for cell in row:
                temp.append(Tile(cell[1], cell[0], cell[2]))
            self.state.append(temp)

    def printState(self):
        for row in self.state:
            for cell in row:
                print(f"({cell.content}, {cell.color}, {cell.background}), ", end="")
            print("")

    def get(self, pos):
        return self.state[pos[0]][pos[1]]

    def set(self, pos, newItem):
        self.state[pos[0]][pos[1]] = Tile(newItem[1], newItem[0], newItem[2])

    def saveToFile(self, filename):
        file = open(filename, 'w')
        for row in self.state:
            for cell in row:
                file.write(f"{cell.content},{cell.color} ")
            file.write(f"\n")

    def __getitem__(self, item):
        return self.state[item]


class Tile:
    def __init__(self, content, color, background):
        self.items = [color, content, background]
        self.content = content
        self.color = color
        self.background = background

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self.items[1] = value
        self._content = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self.items[0] = value
        self._color = value

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self.items[2] = value
        self._background = value

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value