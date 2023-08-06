"""
    models
"""
from torch import flatten
from torch.nn.functional import relu, max_pool2d
from torch.nn import Conv2d, Module, Dropout, Linear, BatchNorm2d


class ArgNet(Module):
    """
    model for Cifar10
    model have two layer CNN: Conv+BatchNorm+Conv+BatchNorm+Dropout+Linear
    model use Relu activation

    channels of each layer decided by args.
    args also control has BatchNorm layer or not,Dropout or not

    e.g.: arg = {'c1': 48, 'c_bn1': False, 'c2': 56, 'c_bn2': True, 'drop': 0.1}
          model = CNN(48) + CNN(56) + BatchNorm + Droupout(0.1)
    e.g.: arg = {'c1': 16, 'c_bn1': True, 'c2': 32, 'c_bn2': True, 'drop': 0}
          model = CNN(48) + BatchNorm + CNN(56) + BatchNorm

    Examples:
        >>> arg = {'c1': 48, 'c_bn1': False, 'c2': 56, 'c_bn2': False, 'drop': 0.1}
        >>> model = ArgNet(arg)
    """
    def __init__(self, args):
        super(ArgNet, self).__init__()
        self.need_bn1 = args['c_bn1']
        self.need_bn2 = args['c_bn2']
        conv_ch_1 = args['c1']
        conv_ch_2 = args['c2']
        drop = args['drop']

        self.conv1 = Conv2d(3, conv_ch_1, 3, 1)
        self.bn1 = BatchNorm2d(conv_ch_1)

        self.conv2 = Conv2d(conv_ch_1, conv_ch_2, 3, 1)
        self.bn2 = BatchNorm2d(conv_ch_2)

        self.dropout1 = Dropout(drop)
        self.fc1 = Linear(36 * conv_ch_2, 10)

    def forward(self, x):
        """ how model calc """
        x = self.conv1(x)

        if self.need_bn1:
            x = self.bn1(x)

        x = relu(x)
        x = max_pool2d(x, 2)

        x = self.conv2(x)
        if self.need_bn2:
            x = self.bn2(x)
        x = relu(x)
        x = max_pool2d(x, 2)

        x = self.dropout1(x)
        x = flatten(x, 1)
        # print(x.shape)
        output = self.fc1(x)

        return output


class SampleNet(Module):
    """ model for mnist 10 class """
    def __init__(self):
        super(SampleNet, self).__init__()
        self.conv1 = Conv2d(3, 64, 3, 1)
        self.bn1 = BatchNorm2d(64)

        self.conv2 = Conv2d(64, 64, 3, 1)
        self.bn2 = BatchNorm2d(64)

        self.dropout1 = Dropout(0.25)

        self.fc1 = Linear(36*64, 10)

    def forward(self, x):
        x = self.conv1(x)
        # x = self.bn1(x)
        x = relu(x)
        x = max_pool2d(x, 2)

        x = self.conv2(x)
        # x = self.bn2(x)
        x = relu(x)
        x = max_pool2d(x, 2)

        x = self.dropout1(x)
        x = flatten(x, 1)
        # print(x.shape)
        output = self.fc1(x)

        return output


class SampleNet_MNIST(Module):
    """ model for mnist 10 class """
    def __init__(self):
        super(SampleNet_MNIST, self).__init__()
        self.conv1 = Conv2d(1, 16, 3)
        self.conv2 = Conv2d(16, 16, 3)
        self.dropout1 = Dropout(0.25)
        self.fc1 = Linear(121*16, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = max_pool2d(x, 2)
        x = relu(x)

        x = self.conv2(x)
        x = relu(x)

        x = flatten(x, 1)
        # print(x.shape)
        x = self.dropout1(x)
        output = self.fc1(x)

        return output
