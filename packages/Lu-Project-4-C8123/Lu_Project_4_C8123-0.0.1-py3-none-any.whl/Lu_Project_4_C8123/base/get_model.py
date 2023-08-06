""" get model by name """

from torch.nn import Module
import torchvision.models as models

from .models import SampleNet, SampleNet_MNIST, ArgNet

model_dict = {
    "samplenet": SampleNet,
    "argnet": ArgNet,
    "samplenet_mnist": SampleNet_MNIST,
    "alexnet": models.alexnet,
    "resnet18": models.resnet18,
    "resnet34": models.resnet34,
    "resnet50": models.resnet50,
    "vgg11": models.vgg11,
    "vgg11_bn": models.vgg11_bn,
    "vgg13": models.vgg13,
    "vgg13_bn": models.vgg13_bn,
    "vgg16": models.vgg16,
    "vgg16_bn": models.vgg16_bn,
    "vgg19": models.vgg19,
    "vgg19_bn": models.vgg19_bn,
    "squeezenet1_0": models.squeezenet1_0,
    "squeezenet1_1": models.squeezenet1_1,
    "inception_v3": models.inception_v3,
    "densenet121": models.densenet121,
    "densenet161": models.densenet161,
    "densenet169": models.densenet169,
    "densenet201": models.densenet201,
}


def get_model(name: str, *args) -> Module:
    """ get model by name """
    if not isinstance(name, str):
        raise TypeError("The type of arg 'model' should be str. But get {}.".format(type(name)))

    if name.lower() not in model_dict:
        raise KeyError(f'{name} is not model name')

    model = model_dict[name.lower()](*args)
    return model
