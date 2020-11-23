# Authors: Greg Robson
# 000919616
# Version 3-27-18 v0.03


class Piece:

    def __init__(self, value):
        piece_type = {0: [[0, 0]],                                                      # Single square
         1: [[0, 0], [1, 0]],                                                           # Two across
         2: [[0, 0], [1, 0], [2, 0]],                                                   # Three across
         3: [[0, 0], [1, 0], [2, 0], [3, 0]],                                           # Four across
         4: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],                                   # Five across
         5: [[0, 0], [0, 1]],                                                           # Two down
         6: [[0, 0], [0, 1], [0, 2]],                                                   # Three down
         7: [[0, 0], [0, 1], [0, 2], [0, 3]],                                           # Four down
         8: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],                                   # Five down
         9: [[0, 0], [1, 0], [0, 1]],                                                   # Right s Gamma
         10: [[0, 0], [1, 0], [1, 1]],                                                  # Left s Gamma
         11: [[0, 0], [0, 1], [1, 1]],                                                  # Right s L
         12: [[1, 0], [0, 1], [1, 1]],                                                  # Left s L
         13: [[0, 0], [1, 0], [0, 1], [1, 1]],                                          # 2x2 box
         14: [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2]],                                  # Right b Gamma
         15: [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],                                  # Left b Gamma
         16: [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]],                                  # Right b L
         17: [[2, 0], [2, 1], [0, 2], [1, 2], [2, 2]],                                  # Left b L
         18: [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2]],  # 3x3 box
         19: []}                                                                        # Empty
        self.coords = piece_type[value]
        self.value = value

    def is_empty(self):
        size = 1
        if self.value == 19:
            size = 0
        return size

    def empty(self):
        self.value = 19
        self.coords = []
