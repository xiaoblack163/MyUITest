import pyautogui
from PIL import Image
import io


def get_image(img_binary,image_path,confidence,formatLog):
    try:
        # 使用io.BytesIO创建一个字节流
        image_stream = io.BytesIO(img_binary)
        # 使用Pillow的Image.open方法从字节流中加载图像
        # 当前步骤执行的截图
        image = Image.open(image_stream)
        # 定位到的box生成器
        locations = pyautogui.locateAll(needleImage=image_path, haystackImage=image,confidence=confidence,grayscale=False)
        return list(locations)
    except Exception as e:
        stre = str(e)
        if "highest confidence" in stre:
            formatLog.writeLog("ERROR","图像未识别:"+stre)
            return []
        elif "Failed to read" in stre:
            formatLog.writeLog("ERROR","图像不存在:"+stre)
            return []
        else:
            formatLog.writeLog("ERROR","未知错误:"+stre)
            return []

def locate_all(img_binary, image_path, confidence, formatLog,distance=10):
    try:
        distance = pow(distance, 2)
        elements = []
        locations = get_image(img_binary, image_path,confidence,formatLog)
        for element in locations:
            if all(map(lambda x: pow(element.left - x.left, 2) + pow(element.top - x.top, 2) > distance, elements)):
                elements.append(element)
        return elements
    except:
        formatLog.writeLog("ERROR","图像识别错误")
        return []

