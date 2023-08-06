""" get dataset """
from torchvision import datasets
from torch.utils.data.dataset import Dataset
from torchvision.transforms import Compose, ToTensor, Normalize


class IndexDataSet(Dataset):
    """
        Dataset with sample index
        带数据索引的Dataset。获取数据时，还返回数据的Index。

        example:
            mnist = datasets.MNIST(...)
            dataset = IndexDataSet(mnist)  # use IndexDataSet like this
            loader = DataLoader(dataset, ...)
            for data, target, index in train_loader:  # original loader only have 'data' and 'target'
                ...
    """
    def __init__(self, dataset, max_num=None):
        self.dataset = dataset
        self.max_num = max_num

    def __len__(self):
        if self.max_num is not None:
            return self.max_num
        return len(self.dataset)

    def __getitem__(self, index):
        data, target = self.dataset[index]
        return data, target, index


def get_dataset(name: str, root: str) -> (Dataset, Dataset):
    """ get dataset by name. return train and test dataset
    :param name: dataset name. only support torchvision.datasets
    :param root: dataset root path
    :return : train_set, test_set
    """
    dataset_dic = {
        'mnist': (datasets.MNIST, (0.2860,), (0.3530,)),
        'fashionmnist': (datasets.FashionMNIST, (0.1307,), (0.3081,)),
        'cifar10': (datasets.CIFAR10, (0.4914, 0.4822, 0.4465), (0.2470, 0.2434, 0.2615))
    }

    if name.lower() not in dataset_dic:
        raise ValueError(f"get_dataset_args not support {name} yet!")

    set_cls, mean, std = dataset_dic[name.lower()]

    transform = Compose([ToTensor(), Normalize(mean, std)])

    train: Dataset = set_cls(root, train=True, transform=transform, download=True)
    test: Dataset = set_cls(root, train=False, transform=transform)

    return train, test
