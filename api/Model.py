import torch
from torch import nn



class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=(3, 3), padding=1),#卷积
            nn.ReLU(),#激活函数，非线性
            nn.MaxPool2d(kernel_size=2)#池化
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer5 = nn.Sequential(
            nn.Flatten(),  # torch.Size([64, 6144]),降维
            nn.Linear(6144, 3072),#全连接层，线性层
            nn.Dropout(),
            nn.Linear(3072, 80)
        )

    def forward(self, x):
        x = self.layer1(x)  # torch.Size([64, 64, 20, 50])
        x = self.layer2(x)  # torch.Size([64, 128, 10, 25])
        x = self.layer3(x)  # torch.Size([64, 256, 5, 12])
        x = self.layer4(x)  # torch.Size([64, 512, 2, 6])
        x = self.layer5(x)  # torch.Size([64, 40])
        return x

if __name__ == '__main__':

    data=torch.ones([1, 3, 40, 110])
    print(data)
    m=Model()
    x=m(data)
    print(x)