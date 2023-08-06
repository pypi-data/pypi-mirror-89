import argparse
import os
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms

dataset_names = ('cifar10','cifar100','mnist')


train_transform = transforms.Compose([transforms.ToTensor()])
train_set = torchvision.datasets.FashionMNIST(root="../data", train=True, transform=train_transform)

# print(train_set.data.mean(axis=(0,1,2)) / 255)
# print(train_set.data.std(axis=(0,1,2)) / 255)

print(train_set.data.mean(axis=(0,1,2))/255)
print(train_set.data.std(axis=(0,1,2))/255)


