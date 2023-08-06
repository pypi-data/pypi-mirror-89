""" experiment process tool """
import time

import torch
from torch.nn import Module
from torch.optim import Optimizer

from torch.utils.data.dataloader import DataLoader

from .history import History
from .get_metric import get_metric
from .get_loss import get_loss
from .get_model import get_model
from .get_optimizer import get_optimizer
from .metrics import BaseMetric


class Experiment:
    """ An Experiment, easy to do a experiment with little code. """
    model: Module  # nn model
    optim: Optimizer  # optimizer for model
    lr: float  # learning rate
    loss_fn: callable  # loss function

    save_path: str = "../history"  # path to save the his or model file
    metric: BaseMetric

    def __init__(self, model_name: str, model_arg, optim_name: str, lr: float, loss_name: str, metric_name: str, use_cuda=True):
        # use cuda if available and use_cuda=True
        self.device = torch.device("cuda" if torch.cuda.is_available() and use_cuda else "cpu")

        self.lr = lr  # learning rate
        self.loss_fn = get_loss(loss_name)  # loss function
        self.model = get_model(model_name, model_arg)  # check and set model
        print(model_arg)
        self.model.to(self.device)

        optim_cls = get_optimizer(optim_name)
        self.optim = optim_cls(self.model.parameters(), lr=lr)
        self.metric = get_metric(metric_name)

    def run(self, loaders, epochs: int, record_name: str):
        """ control train/test process and record metric history"""
        loader, loader_test = loaders

        history = History(record_name)

        for epoch_id in range(epochs):
            print("epoch {}/{}: ".format(epoch_id + 1, epochs))

            start = time.time()
            train_his: dict = self.train(loader)
            history.train_append(train_his)
            end = time.time()
            print(" ", round(end - start, 4), "s")

            start = time.time()
            test_his: dict = self.test(loader_test)
            history.test_append(test_his)
            end = time.time()
            print(" ", round(end - start, 4), "s")

        return history

    def train(self, loader: DataLoader):
        """ train epoch """
        self.model.train()  # set model mode

        batch_num = len(loader)
        for batch_id, (data, label) in enumerate(loader):
            data, label = data.to(self.device), label.to(self.device)

            # train step
            self.optim.zero_grad()
            output = self.model(data)
            output = torch.log_softmax(output, dim=1)
            loss = self.loss_fn(output, label)
            loss.backward()
            self.optim.step()

            with torch.no_grad():
                epoch_loss, epoch_acc = self.metric.record(output, label)  # record info

                print("\r  train {}/{}, loss: {:.4f}, acc: {:.4f}"
                      .format(batch_id + 1, batch_num, epoch_loss, epoch_acc), end="")

        self.model.eval()  # set model mode
        # print(" done.")
        epoch_history: dict = self.metric.result()  # get epoch history
        return epoch_history

    def test(self, loader: DataLoader):
        """ evaluate by dataloader """
        self.model.eval()
        with torch.no_grad():
            batch_num = len(loader)
            for batch_id, (data, target) in enumerate(loader):
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                output = torch.log_softmax(output, dim=1)
                epoch_loss, epoch_acc = self.metric.record(output, target)  # record info
                print("\r  eval {}/{}, loss: {:.5f}, acc: {:.5f}"
                      .format(batch_id + 1, batch_num, epoch_loss, epoch_acc), end='')  # for display process

            epoch_history = self.metric.result()

        return epoch_history
