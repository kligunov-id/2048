import torch.nn

class PolicyNetwork(torch.nn.Module):

    def __init__(self, feature_n=4*4*10, hidden_n=20, actions_n=4):
        super().__init__()

        self.feature_n = feature_n
        self.hidden_n = hidden_n
        self.actions_n = actions_n

        self.linear_1 = torch.nn.Linear(feature_n, hidden_n)
        self.activation = torch.nn.ReLU()
        self.linear_2 = torch.nn.Linear(hidden_n, actions_n)
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x = self.linear_1(x)
        x = self.activation(x)
        x = self.linear_2(x)
        x = self.softmax(x)
        return x
