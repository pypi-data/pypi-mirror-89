""" 批量实验的主函数 """
from ..base.runners import batch_runner, BatchArgs


def main():
    """ main func """
    batch_runner(batch_args)
    batch_runner(batch_args_bn)


model_args = {
    "c1": [64, 56, 48, 40, 32],
    "c2": [64, 56, 48, 40, 32],
    "c_bn1": [False],
    "c_bn2": [False],
    "drop": [0, 0.1, 0.25]
}

model_args_bn = {
    "c1": [64, 56, 48, 40, 32],
    "c2": [64, 56, 48, 40, 32],
    "c_bn1": [True],
    "c_bn2": [True],
    "drop": [0, 0.1, 0.25]
}

batch_args_bn = {
    "name": "NORM",
    "dataset": "cifar10",
    "model": "ArgNet",
    "model_arg": list(BatchArgs(model_args_bn)),
    "_loss": 'nll_loss',
    'optim': 'Adam',
    "lr": [0.001],
    "epochs": 5,
    "batch_size": [512],
    "test_batch_size": 1500,
    "_metric": 'cls',
    # "seed": [42, 654, 114, 25, 759],
    "seed": [42],
    "_save_path": "E:/CifarCourseWork/",
    "_data_path": "E:/Code/Data/"
}


batch_args = {
    "name": "NORM",
    "dataset": "cifar10",
    "model": "ArgNet",
    "model_arg": list(BatchArgs(model_args)),
    "_loss": 'nll_loss',
    'optim': 'Adam',
    "lr": [0.001],
    "epochs": 5,
    "batch_size": [512],
    "test_batch_size": 1500,
    "_metric": 'cls',
    # "seed": [42, 654, 114, 25, 759],
    "seed": [42],
    "_save_path": "E:/CifarCourseWork/",
    "_data_path": "E:/Code/Data/"
}


if __name__ == '__main__':
    main()
