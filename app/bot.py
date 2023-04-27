import random

class RandomizerModel:
    def act(self, field):
        return random.choice([0, 1, 2, 3])

model = RandomizerModel()
