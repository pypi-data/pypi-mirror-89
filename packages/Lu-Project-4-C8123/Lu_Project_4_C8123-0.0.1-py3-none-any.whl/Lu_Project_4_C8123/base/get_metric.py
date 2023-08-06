""" support for get metric by name """
from .metrics import BaseMetric
from .metrics import ClassificationMetric as ClassificationMetric


def get_metric(name: str = None) -> BaseMetric:
    """ get metric by name """
    if name is None:
        return ClassificationMetric()

    loss_dict = {
        "cls": ClassificationMetric,
        "classification": ClassificationMetric
    }

    if name.lower() not in loss_dict:
        raise KeyError(f'{name} is not metric name, or not support now!')

    return loss_dict[name.lower()]()
