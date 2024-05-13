from torchvision import transforms
import torch
from PIL import Image


def predict_one(imgpath,modelpth):
    model=torch.load(modelpth)
    img=Image.open(imgpath).convert("RGB")
    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((40, 110))
    ])
    img_tensor=to_tensor(img)
    img_tensor=img_tensor.reshape(1,3,40,110)
    re=model(img_tensor)
    return re



def decode(code_tensor):
    # all_code = list('0123456789abcdefghijklmnopqrstuvwxyz')
    # f = code_tensor.view(4, 36)
    all_code = list('2345678abcdefgmnpwxy')
    f = code_tensor.view(4, 20)
    result = []
    for row in f:
        result.append(all_code[torch.argmax(row, dim=0)])
    result = ''.join(result)
    return result

if __name__ == '__main__':
    ...
    # re=decode(predict_one(r'code.png','verifycode_model.pth'))
    # print(re)
