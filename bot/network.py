import torch.nn

class PolicyNetwork(torch.nn.Module):

    def __init__(self, feature_dim=4*4*15, hidden_1_dim=60, hidden_2_dim = 20, actions_dim=4):
        super().__init__()

        self.linear_1 = torch.nn.Linear(feature_dim, hidden_1_dim)
        self.activation_1 = torch.nn.ReLU()
        self.linear_2 = torch.nn.Linear(hidden_1_dim, hidden_2_dim)
        self.activation_2 = torch.nn.ReLU()
        self.linear_3 = torch.nn.Linear(hidden_2_dim, actions_dim)
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x = self.linear_1(x)
        x = self.activation_1(x)
        x = self.linear_2(x)
        x = self.activation_2(x)
        x = self.linear_3(x)
        x = self.softmax(x)
        return x
