# Display:

padding = {"LEFT": 20, "RIGHT": 20, "TOP": 80, "BOTTOM": 20}  # Left/Right/Top/Bottom

class Dimension:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = x, y
        self.padded = padding["LEFT"] + x + padding["RIGHT"], padding["TOP"] + y + padding["BOTTOM"]

class GameMode:  # used to determine
    EASY = Dimension(16, 16)
    MEDIUM = Dimension(32, 32)
    HARD = Dimension(48, 48)

    @staticmethod
    def get_mines_from_difficulty(difficulty: Dimension) -> int:
        if difficulty == GameMode.EASY:
            return 40
        elif difficulty == GameMode.MEDIUM:
            return 120
        elif difficulty == GameMode.HARD:
            return 400


resolution = Dimension(800, 800)


# other
fps = 60
game_mode = GameMode.EASY
