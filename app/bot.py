import random
import torch

def preprocessing(observed_grid, num_classes = 15):
    grid_tensor = torch.tensor(observed_grid)
    grid_tensor[grid_tensor == 0] = 1
    classes = torch.log2(grid_tensor).long()
    one_hot = torch.nn.functional.one_hot(classes, num_classes).flatten()
    return torch.unsqueeze(one_hot.flatten(), dim=0).float()

class TrainedModel:
    def __init__(self):
        self.model = torch.jit.load('./bot/model_scripted.pt')

    def act(self, x):
        probs = self.model.forward(preprocessing(x))
        return torch.distributions.Categorical(probs).sample().numpy()[0]

class RandomizerModel:
    def act(self, field):
        return random.choice([0, 1, 2, 3])

model = TrainedModel()
