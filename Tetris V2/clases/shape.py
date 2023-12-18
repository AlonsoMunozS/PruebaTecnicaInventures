from constants import SHAPE_COLORS

class Shape:
    SHAPES = [
        [[1, 1, 1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 1, 1], [0, 1, 0]],
    ]

    def __init__(self, type):
        self.type = type
        self.color = SHAPE_COLORS[self.type]
        self.original_shape = self.SHAPES[self.type]
        self.current_state = self.original_shape
    
    def set_current_state(self, state):
        self.current_state = state