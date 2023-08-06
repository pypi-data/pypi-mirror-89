""" some tool function """
import torch
import random
import numpy as np
import operator
import functools
from torch.backends import cudnn


def flat(data: list) -> np.ndarray:
    """ list[list] -> list """
    result = functools.reduce(operator.iconcat, data, [])
    return np.array(result)


def get_record_name(args: dict):
    """ gen name from args """
    name = "E"
    for k, v in args.items():
        if not k.startswith("_"):
            if isinstance(v, dict):
                v = [x for x in v.values()]
            name += "-" + str(v)
    return name


def set_random(seed: int, cudnn_benchmark=False, cudnn_deterministic=False, np_seed: int = None):
    """ control randomness

    Args:
        seed (int): random seed
        cudnn_benchmark (bool):
        cudnn_deterministic (bool): config. avoid using nondeterministic algorithms for some operations.
        np_seed (int): Optional, set numpy random seed independently

    Examples:
        >>> set_random(seed=42)
        >>> set_random(42, cudnn_deterministic=True)
        >>> set_random(-42, False, True, np_seed=42)
    """

    if np_seed is None:
        np_seed = seed

    random.seed(seed)

    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # set seed for all gpus

    cudnn.benchmark = cudnn_benchmark
    cudnn.deterministic = cudnn_deterministic

    if 0 <= np_seed <= 2 ** 32 - 1:
        np.random.seed(np_seed)
    else:
        raise ValueError(f"numpy seed range should from 0 to 2^32-1, but get np_seed={seed}")


if __name__ == '__main__':
    print(cudnn.benchmark)
    print(cudnn.deterministic)