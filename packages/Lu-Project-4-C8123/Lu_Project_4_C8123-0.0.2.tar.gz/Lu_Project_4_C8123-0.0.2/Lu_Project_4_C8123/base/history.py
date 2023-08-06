""" History for record metric """
import os
import pathlib
import numpy as np
from datetime import datetime


class History:
    """ data class, for record history2 in epochs"""
    def __init__(self, name="Experiment"):
        self.train = {
            "output": [],
            "losses": [],
            "predict": [],
            "correct": [],
            "uncertainty": [],
        }

        self.test = {
            "output": [],
            "losses": [],
            "predict": [],
            "correct": [],
            "uncertainty": [],
        }
        self.name = name
        self.model_state_dict = None


    def train_append(self, data: dict):
        self.train["output"].append(data["output"])
        self.train["losses"].append(data["losses"])
        self.train["predict"].append(data["predict"])
        self.train["correct"].append(data["correct"])
        self.train["uncertainty"].append(data["uncertainty"])

    def test_append(self, data: dict):
        self.test["output"].append(data["output"])
        self.test["losses"].append(data["losses"])
        self.test["predict"].append(data["predict"])
        self.test["correct"].append(data["correct"])
        self.test["uncertainty"].append(data["uncertainty"])


    def save(self, save_path, args=None):
        """ save the experiment history data"""
        p = pathlib.Path(save_path)
        p.mkdir(parents=True, exist_ok=True)

        data = {
            "train": self.train,
            "test": self.test,
            "name": self.name,
            "model_state_dict": self.model_state_dict,
            "args": args,
        }

        file_name = self.name + str(datetime.now().strftime("-%Y_%m_%d_%H_%M_%S"))
        file_path = os.path.join(save_path, file_name)
        np.save(file_path, data)


class HistoryEpoch:
    """ data class, for record history2
        TODO： 现在看起来HistoryEpoch很SHIT，需要改进。
    """
    def __init__(self):
        self.indices = []  # sample id(index in dataset)

        self.outputs = []  # model output, such as the result of softmax

        self.losses = []  # loss for every sample
        self.predict = []  # model predict, correct predict is target(label)

        self.correct = []  # the predict is right or not
        self.uncertainty = []  # the uncertainty of output

    def to_flatten_sorted(self):
        """ list[list] => list, and sort by index"""
        from base.tool import flat
        # flatten data
        self.indices = flat(self.indices)
        self.outputs = flat(self.outputs)
        self.losses = flat(self.losses)
        self.predict = flat(self.predict)
        self.correct = flat(self.correct)
        self.uncertainty = flat(self.uncertainty)

        # sort by sample index
        idx = self.indices.argsort()
        self.indices = self.indices[idx]
        if len(self.outputs) > 0:
            self.outputs = self.outputs[idx]
        self.losses = self.losses[idx]
        self.predict = self.predict[idx]
        self.correct = self.correct[idx]
        if len(self.uncertainty) > 0:
            self.uncertainty = self.uncertainty[idx]

    def to_dict(self):
        """ for storage, easy to save and parse """
        return {"indices": self.indices,
                "outputs": self.outputs,
                "losses": self.losses,
                "predict": self.predict,
                "correct": self.correct,
                "uncertainty": self.uncertainty}
