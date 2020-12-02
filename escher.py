# first a simple representation
blocks = [
    'b', # solid cube
    's', # staircase
    '-', # air
]


# maybe later
class Block:
    def __init__(self, data):
        self.data = data

class Stair(Block):
    def __init__(self, orientation):
        # orientation stores the direction of the stairs.
        # ()
        self.orientation = orientation