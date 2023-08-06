import os
import numpy as np
from base.tool import flat
from matplotlib import pyplot as plt


base_folder = "../history/Norm cifar/"
un_folder = "../history/UN10+4 1-(T1-T2)/"

class DataPack:
    def __init__(self, loss_train, acc_train, loss_test, acc_test):
        self.loss_train = np.array(loss_train).T
        self.acc_train = np.array(acc_train).T
        self.loss_test = np.array(loss_test).T
        self.acc_test = np.array(acc_test).T


def main():
    draw_un_classic("MNIST, T2/T1, U14+R0")


def draw_un_classic(title):
    base = get_data(base_folder)
    our = get_data(un_folder)

    plt.figure(figsize=(6,8))
    plt.plot(base.acc_test, "g", alpha=0.2)
    plt.plot(our.acc_test, "r", alpha=0.2)
    plt.plot(np.mean(base.acc_test, axis=1), "g", label='classic')
    plt.plot(np.mean(our.acc_test, axis=1), "r", label='uncertainty')
    print(np.mean(base.acc_test, axis=1))
    print(np.mean(our.acc_test, axis=1))
    plt.title(title+" (acc)", fontsize=18)
    plt.xlabel("epoch", fontsize=16)
    plt.ylabel("acc", fontsize=16)
    plt.legend(fontsize=16)
    plt.show()

    plt.figure(figsize=(6,8))
    plt.plot(base.loss_test, "g", alpha=0.2)
    plt.plot(our.loss_test, "r", alpha=0.2)
    plt.plot(np.mean(base.loss_test, axis=1), "g", label='classic')
    plt.plot(np.mean(our.loss_test, axis=1), "r", label='uncertainty')

    plt.title(title+" (loss)", fontsize=18)
    plt.xlabel("epoch", fontsize=16)
    plt.ylabel("loss", fontsize=16)
    plt.legend(fontsize=16)
    plt.show()


def remove_repeat_label():
    handles, labels = plt.gca().get_legend_handles_labels()
    i = 1
    while i < len(labels):
        if labels[i] in labels[:i]:
            del labels[i]
            del handles[i]
        else:
            i += 1
    plt.legend(handles, labels)

def get_data(folder) -> DataPack:
    files = os.listdir(folder)
    files = [x for x in files if x.endswith("npy")]
    acc_train = []
    acc_test = []
    loss_train = []
    loss_test = []

    for file_name in files:
        file_path = os.path.join(folder, file_name)
        data = np.load(file_path,allow_pickle=True).item()

        losses_exam_test = []
        acc_exam_test = []
        losses_exam_train = []
        acc_exam_train = []

        for x in data["test"]:
            losses_exam_test.append(np.mean(x["losses"]))
            acc_exam_test.append(np.sum(x["correct"]) / len(x["correct"]))

        train_log = data["train"] if len(data["train_log"]) == 0 else data["train_log"]
        for x in train_log:

            loss = x["losses"]
            acc = x["correct"]
            if isinstance(loss[0], list):
                loss = flat(loss)
            if isinstance(acc[0], list):
                acc = flat(acc)

            losses_exam_train.append(np.mean(loss))
            acc_exam_train.append(np.sum(acc) / len(acc))

        loss_train.append(losses_exam_train)
        acc_train.append(acc_exam_train)
        loss_test.append(losses_exam_test)
        acc_test.append(acc_exam_test)
    return DataPack(loss_train, acc_train, loss_test, acc_test)


if __name__ == '__main__':
    main()
