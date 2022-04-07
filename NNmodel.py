import torch
from config import args

class Fit_model(torch.nn.Module):
    def __init__(self):
        super(Fit_model, self).__init__()
        self.linear1 = torch.nn.Linear(5, 32)
        self.relu = torch.nn.LeakyReLU()
        self.linear2 = torch.nn.Linear(32, 64)
        self.linear3 = torch.nn.Linear(64, 1)
        # torch.nn.
        self.sigmoid=torch.nn.Sigmoid()
        self.criterion = torch.nn.MSELoss()
        self.lr=0.00001
        self.opt = torch.optim.SGD(self.parameters(), lr=args.lr)

    def forward(self, input):
        y = self.linear1(input)
        y = self.sigmoid(y)
        y = self.linear2(y)
        y = self.sigmoid(y)
        y = self.linear3(y)
        y=self.relu(y)
        return y
