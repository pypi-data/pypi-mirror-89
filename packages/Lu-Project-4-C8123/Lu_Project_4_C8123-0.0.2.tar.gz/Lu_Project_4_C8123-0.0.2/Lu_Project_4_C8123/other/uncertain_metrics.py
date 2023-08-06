"""
    计算样本困难程度
"""
import numpy as np


def uncertain(data: np.ndarray):
    """ 评估模型对某样本输出的不确定性
        Evaluate the uncertainty of model predictions, only for classification
    """
    data = np.exp(data)
    data = np.sort(data)

    # 1-(T1-T2)
    # value = 1 - (data[:, -1] - data[:, -2])

    # T2 - T1
    value = data[:, -2] / data[:, -1]

    # (1-T1)/(n/n-1)
    # value = (1 - data[:, -1]) * (10.0 / 9)

    # entropy
    # log_probs = data * np.log(data)
    # raw_entropy = -np.sum(log_probs, axis=1)
    # value = raw_entropy / np.log2(len(data))
    return value

