# Display:
class Dimension:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = x, y

class GameMode:  # used to determine
    EASY = Dimension(16, 16)
    MEDIUM = Dimension(32, 32)
    HARD = Dimension(64, 64)


resolution = Dimension(800, 800)
padding = {"LEFT": 20, "RIGHT": 20, "TOP": 20, "BOTTOM": 20}  # Left/Right/Top/Bottom


#
