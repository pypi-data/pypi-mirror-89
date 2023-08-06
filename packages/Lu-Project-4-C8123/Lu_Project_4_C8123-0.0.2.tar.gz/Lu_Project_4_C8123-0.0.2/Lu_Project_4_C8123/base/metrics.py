""" metric class """
import numpy as np
import torch
from torch import Tensor
from torch.nn.functional import nll_loss

from ..other.uncertain_metrics import uncertain


class BaseMetric:
    """ Abstract metric class, for record history data.
        define the interface for all metric classes.
        every subclass should implement 'record'.
    """
    def __init__(self, need_output=False):
        self._history = {
            "output": [],
            "losses": [],
            "predict": [],
            "correct": [],
            "uncertainty": [],
        }
        self.need_output = need_output

    def record(self, output: Tensor, target: Tensor) -> float:
        """ record info to self._history for every batch
        :param output: Tensor, model output, after softmax
        :param target: Tensor, label for samples
        :param indices: Tensor, index(id) for samples
        :return loss: float, batch loss, until now
        """
        raise NotImplementedError

    def result(self) -> dict:
        """ get and clear history """

        history = self._history
        self._history = {
            "output": [],
            "losses": [],
            "predict": [],
            "correct": [],
            "uncertainty": [],
        }

        return history


class ClassificationMetric(BaseMetric):
    """ Metric for Classification.
        TODO： 应该拆分Metric到多个，不然修改指标必然要改动History，Metric
    """
    def __init__(self, need_output=False):
        super(ClassificationMetric, self).__init__(need_output)

    def record(self, output: Tensor, target: Tensor):
        """ record metric: acc loss predict, correct, uncertainty
        :param output: Tensor, model output, after softmax
        :param target: Tensor, label for samples
        :param indices: Tensor, index(id) for samples
        """
        with torch.no_grad():

            if self.need_output:
                self._history["outputs"].append(output.tolist())

            losses = nll_loss(output, target, reduction='none')
            self._history["losses"] += losses.tolist()

            predict = output.argmax(dim=1)
            self._history["predict"] += predict.tolist()

            correct = target.eq(predict.view_as(target))
            self._history["correct"] += correct.tolist()

            uncertainty = uncertain(output.cpu().numpy())
            self._history["uncertainty"] += uncertainty.tolist()

            # cal loss,acc
            epoch_loss = np.mean(self._history["losses"])
            tmp_correct = self._history["correct"]
            epoch_acc = np.sum(tmp_correct) / len(tmp_correct)
            return epoch_loss, epoch_acc
