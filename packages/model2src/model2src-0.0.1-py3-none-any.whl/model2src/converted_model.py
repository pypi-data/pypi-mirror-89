
import torch
import torch.nn as nn

class Bottleneck(nn.Module):
    def __init__(self):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(64, 64, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 256, kernel_size=1, stride=1, bias=False)
        self.bn3 = nn.BatchNorm2d(256)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = nn.Sequential()
        self.downsample.add_module('0', nn.Conv2d(64, 256, kernel_size=1, stride=1, bias=False))
        self.downsample.add_module('1', nn.BatchNorm2d(256))


    def forward(self, x):
        return x

class ResNet(nn.Module):
    def __init__(self):
        super(ResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=(7, 7), stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
        self.layer1 = nn.Sequential()
        self.layer1.add_module('0', Bottleneck())
        self.layer1.add_module('1', Bottleneck())
        self.layer1.add_module('2', Bottleneck())

        self.layer2 = nn.Sequential()
        self.layer2.add_module('0', Bottleneck())
        self.layer2.add_module('1', Bottleneck())
        self.layer2.add_module('2', Bottleneck())
        self.layer2.add_module('3', Bottleneck())

        self.layer3 = nn.Sequential()
        self.layer3.add_module('0', Bottleneck())
        self.layer3.add_module('1', Bottleneck())
        self.layer3.add_module('2', Bottleneck())
        self.layer3.add_module('3', Bottleneck())
        self.layer3.add_module('4', Bottleneck())
        self.layer3.add_module('5', Bottleneck())

        self.layer4 = nn.Sequential()
        self.layer4.add_module('0', Bottleneck())
        self.layer4.add_module('1', Bottleneck())
        self.layer4.add_module('2', Bottleneck())

        self.avgpool = nn.AdaptiveAvgPool2d(output_size=1)
        self.fc = nn.Linear(in_features=2048, out_features=1000, bias=True)

    def forward(self, x):
        return x

if __name__ == '__main__':
    model = ResNet()
    print(model)
