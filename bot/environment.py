import sys
sys.path.append('../')
import app.models

class Environment:

    def __init__(self, field_size=4, invalid_move_penalty=0):
        self.field = app.models.Field(n=field_size, invalid_move_penalty=invalid_move_penalty)
        self.reset()

    def reset(self):
        self.field.reset()
        return self.observation()

    def observation(self):
        return self.field.grid, self.field.score, self.field.is_over()

    def step(self, move: int):
        self.field.move(app.models.Direction(move))
        return self.observation()
