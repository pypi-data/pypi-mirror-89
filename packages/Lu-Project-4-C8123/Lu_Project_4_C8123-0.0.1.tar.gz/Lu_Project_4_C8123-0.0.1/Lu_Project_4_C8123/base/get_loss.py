""" support for get loss by name """
from typing import Callable
from torch.nn import functional as f

loss_dict = {"nll_loss": f.nll_loss}


def get_loss(name: str) -> Callable:
    """ get loss function by name
    :param name: loss function name
    :return: loss function
    """
    if not isinstance(name, str):
        raise TypeError("The type of arg 'name' should be str or Callable. But get {}.".format(type(name)))

    if name.lower() not in loss_dict:
        raise KeyError(f'{name} is not optimizer name, or not support now!')

    return loss_dict[name.lower()]
