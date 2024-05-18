from torch.utils.data import DataLoader
from MyDataSet import My_DataSet
import torch
from torch import nn
from torch.optim import Adam
from Model import Model



class Train(object):
    Epoch = 30
    min_sum_loss = 100

    def __init__(self):
        super(Train, self).__init__()

    @staticmethod
    def train(model, optimizer, loss_func, train_dataloader):
        for epoch in range(Train.Epoch):
            sum_loss = 0
            print('第',epoch,'轮开始')
            for i, (data, label) in enumerate(train_dataloader):
                model.train()
                predict = model(data)
                # print(predict)
                loss = loss_func(predict, label.float())
                sum_loss += loss.item()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            print(f'轮次:{epoch}\t损失:{sum_loss}')
            if Train.min_sum_loss > sum_loss:
                print("更新最低损失模型 当前损失率:",sum_loss)
                torch.save(model,f'model_v2_min.pth')
                Train.min_sum_loss = sum_loss
        torch.save(model, 'model_v2.pth')


class Predict:
    @staticmethod
    def predict():
        correct = 0
        total = 0
        model = torch.load('model_v2.pth')
        test_dataset = My_DataSet('Dataset/TestData')
        test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True)
        for i, (image, label) in enumerate(test_dataloader):
            code = My_DataSet.decode(label)
            predict = model(image)
            pre_code = My_DataSet.decode(predict)
            if pre_code == code:
                correct += 1
            total += 1
        print(f'正确率:{correct / total:.4f}')

    @staticmethod
    def predict2(modelpth):
        correct = 0
        total = 0
        model = torch.load(modelpth)
        test_dataset = My_DataSet('Dataset/TestData')
        test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True)
        for i, (image, label) in enumerate(test_dataloader):
            code = My_DataSet.decode(label)
            predict = model(image)
            try:
                pre_code = My_DataSet.decode(predict)
            except:
                print("报错",i,"code ",code,"label ",label,"image ",image)
                raise
            if pre_code == code:
                correct += 1
            total += 1
        print(f'{modelpth}的正确率:{correct / total:.4f}')

if __name__ == '__main__':
    # MODEL = torch.load('verifycode_model_v2.pth') # 以现有模型开始训练
    # MODEL = Model() #重新训练
    # loss_function = nn.MultiLabelSoftMarginLoss()
    # opt = Adam(MODEL.parameters(), lr=0.001)
    # dataloader = DataLoader(My_DataSet('Dataset/TrainData'), batch_size=64, shuffle=True)
    # Train.train(MODEL, opt, loss_function, dataloader)
    # Predict.predict()

    Predict.predict2('model_v2.pth')
