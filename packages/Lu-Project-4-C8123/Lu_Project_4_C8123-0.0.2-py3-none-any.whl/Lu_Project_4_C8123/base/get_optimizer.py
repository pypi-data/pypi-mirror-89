""" get optimizer by name """

from torch import optim

optimizers = ['Adadelta', 'Adagrad', 'Adam', 'Adamax', 'AdamW', 'ASGD',
              'LBFGS', 'RMSprop', 'Rprop', 'SGD', 'SparseAdam']

optimizer_dict = {
    "adadelta": optim.Adadelta,
    "adagrad": optim.Adagrad,
    "adam": optim.Adam,
    "adamax": optim.Adamax,
    "adamw": optim.AdamW,
    "asgd": optim.ASGD,
    "lbfgs": optim.LBFGS,
    "rmsprop": optim.RMSprop,
    "rprop": optim.Rprop,
    "sgd": optim.SGD,
    "sparseadam": optim.SparseAdam
}


def get_optimizer(name):
    """ get optimizer by name """
    if not isinstance(name, str):
        raise TypeError(f"The type of arg 'optim' should be str. But get {type(optim)}.")

    if name.lower() not in optimizer_dict:
        raise KeyError(f'{name} is not optimizer name.')

    return optimizer_dict[name.lower()]
