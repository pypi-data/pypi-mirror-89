""" show Cifar Course Work """

import os
import numpy as np

from base.tool import flat

root = "E:/CifarCourseWork/bs756/"

for name in os.listdir(root):
    if not name.endswith(".npy"):
        continue
    full_path = root + name
    data = np.load(full_path, allow_pickle=True).item()

    if not isinstance(data, dict):
        raise ValueError()

    train_acc = np.sum(data["train"]["correct"][4]) / 50000.0
    test_acc = np.sum(data["test"]["correct"][4]) / 10000.0

    print(name, end="\t ")
    print(train_acc, end="\t ")
    print(test_acc)









