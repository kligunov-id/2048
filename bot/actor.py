import torch
from network import PolicyNetwork
from torch.distributions import Categorical

def preprocessing(observed_grid, num_classes = 15):
    grid_tensor = torch.tensor(observed_grid)
    grid_tensor[grid_tensor == 0] = 1
    classes = torch.log2(grid_tensor).long()
    one_hot = torch.nn.functional.one_hot(classes, num_classes).flatten()
    return torch.unsqueeze(one_hot.flatten(), dim=0).float()


class Actor:

    def __init__(self, lr, save_path="./results/model_scripted.pt"):
        self.save_path = save_path
        self.lr = lr

        self.model = PolicyNetwork()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

    @torch.no_grad()
    def act(self, x):
        self.model.eval()
        probs = self.model.forward(x)
        return Categorical(probs).sample().numpy()[0]

    def learn_game(self, state_batch, action_batch, norm_reward):
        self.model.train()
        self.optimizer.zero_grad()
        probs_batch = self.model.forward(state_batch)
        dist_batch = Categorical(probs_batch)
        loss = - dist_batch.log_prob(action_batch) * norm_reward
        loss.sum().backward()
        self.optimizer.step()

    def save_scripted(self):
        torch.jit.script(self.model).save(self.save_path)
