import argparse

parser = argparse.ArgumentParser(description='NNmodel_argument')

parser.add_argument('--lr', type=float, default=0.0001, metavar='LR',help='learning rate (default: 0.00001)')

args = parser.parse_args()

