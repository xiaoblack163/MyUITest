import os
import torch
from torchvision import transforms
from torch.utils.data import Dataset
from PIL import Image

class My_DataSet(Dataset):
    def __init__(self,root_path):
        super(My_DataSet, self).__init__()
        self.img_path=[os.path.join(root_path,i) for i in os.listdir(root_path)]
        self.to_tensor=transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((40,110))
        ])
        # print(self.img_path)

    def __len__(self):
        return self.img_path.__len__()

    def __getitem__(self, index):
        img_tensor=self.to_tensor(Image.open(self.img_path[index]).convert('RGB'))
        code=self.img_path[index].split('\\')[-1].split('.')[0]
        # if len(code)!=4:
        #     print(code)
        #     os.remove(self.img_path[index])
        encoded=self.encode(code)
        return img_tensor,encoded

    @staticmethod
    def encode(code):
        all_code = list('2345678abcdefgmnpwxy')
        encoded=torch.zeros(len(code),len(all_code))
        for i in range(len(code)):
            encoded[i][all_code.index(code[i])]=1
        encoded =torch.flatten(encoded)
        return encoded

    @staticmethod
    def decode(code_tensor):
        all_code = list('2345678abcdefgmnpwxy')
        f = code_tensor.view(4, 20)
        result = []
        for row in f:
            result.append(all_code[torch.argmax(row, dim=0)])
        result = ''.join(result)
        return result

if __name__ == '__main__':
    mydata=My_DataSet('DataSet\TestData')
    # print(mydata.__len__())
    img,label=mydata[0]
    print(img,label)
    print(img.shape)
    print(label.shape)
    # print(My_DataSet.decode(label))
