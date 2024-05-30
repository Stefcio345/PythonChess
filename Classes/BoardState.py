class BoardState:

    def __init__(self, state):
        self.state = state

    def get(self, pos):
        return self.state[pos[0]][pos[1]]

    def set(self, pos, newItem):
        self.state[pos[0]][pos[1]] = newItem

    def __getitem__(self, item):
        return self.state[item]