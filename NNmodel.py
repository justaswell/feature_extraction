import torch

class Fit_model(torch.nn.Module):
    def __init__(self):
        super(Fit_model, self).__init__()
        self.linear1 = torch.nn.Linear(7, 32)
        self.relu = torch.nn.LeakyReLU()
        self.linear2 = torch.nn.Linear(32, 32)
        self.linear3 = torch.nn.Linear(32, 1)
        # torch.nn.

        self.criterion = torch.nn.MSELoss()
        self.opt = torch.optim.SGD(self.parameters(), lr=0.00001)

    def forward(self, input):
        y = self.linear1(input)
        y = self.relu(y)
        y = self.linear2(y)
        y = self.relu(y)
        y = self.linear3(y)
        return y