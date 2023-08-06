import os
import math
import torch
from torch.utils.data.dataloader import DataLoader

from .experiment import Experiment
from .get_dataset import get_dataset
from .tool import get_record_name, set_random


class BatchArgs:
    """tool for experiment in batches"""

    def __init__(self, args: dict):
        self.args = args

    def __len__(self):
        """ number of experiment """
        num = 1
        for v in self.args.values():
            if isinstance(v, list):
                num *= len(v)
        return num-1

    def __getitem__(self, index):
        """ get arg by experiment index. """
        if index > len(self):
            raise IndexError("experiment index out of index!")

        _arg = {}
        for k, v in self.args.items():
            if not isinstance(v, list):
                _arg[k] = v
            else:
                v_len = len(v)
                v_idx = index % v_len
                index = math.floor(index / v_len)
                _arg[k] = v[v_idx]

        return _arg


def batch_runner(args):
    """ run batch experiment by batch arg """
    for arg in BatchArgs(args):
        if need_run(arg):
            runner(arg)


def get_dataloader(dataset, batch_size, test_batch, dataset_root: str = "../data"):
    """ get dataloader"""
    train_dataset, test_dataset = get_dataset(dataset, dataset_root)

    loader = DataLoader(train_dataset, batch_size, shuffle=True, pin_memory=True)
    loader_test = DataLoader(test_dataset, test_batch, pin_memory=True)
    return loader, loader_test


def runner(arg: dict, skip_exist=False):
    """ run a experiment by a arg """

    if skip_exist and not need_run(arg):
        print("skip: ", get_record_name(arg))
    else:
        print("running: ", get_record_name(arg))

    torch.cuda.empty_cache()
    print(f"New Train in seed {arg['seed']}")
    set_random(arg["seed"])  # allows experiment can Recurring

    exam = Experiment(arg["model"], arg["model_arg"], arg["optim"], arg["lr"], arg["_loss"], arg["_metric"])

    loader, loader_test = get_dataloader(arg["dataset"], arg["batch_size"], arg["test_batch_size"], arg["_data_path"])
    history = exam.run((loader, loader_test), arg["epochs"], get_record_name(arg))

    if "_save_path" in arg:
        history.save(arg["_save_path"], args=arg)


def need_run(arg):
    """ check is arg have history file """
    record_name = get_record_name(arg)
    not_exist = True
    for name in os.listdir(arg["_save_path"]):
        if name.startswith(record_name):
            not_exist = False
    return not_exist
