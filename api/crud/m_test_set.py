import json
from typing import List,Optional
from pydantic import BaseModel


TEST_SET_PATH = "MyUITestDB/test_set.json"

class testSet(BaseModel):
    runMode: str
    screencastValue: str
    screenshotValue: str
    sendFlowFailAction: str
    getUrlFailAction: str
    loginFailAction: str
    assertFailAction: str
    execFailAction: str
    ocrModel: str
    getUrlRetry: int
    loginRetry: int
    screenshotRetry: int
    locatRetry: int
    ocrConfidence: int
    ocrMatch: int
    imgConfidence: int
    yoloConfidence: int

class testSetAndOption(BaseModel):
    runModeOption:List[str]
    boolOption: List[str]
    failAction: List[str]
    ocrModelOption: List[str]
    testSet:testSet


# 读取测试配置
def read_test_set():
    with open (TEST_SET_PATH,'r',encoding='utf8') as f:
        setData = json.load(f)
    # 验证pydantic模型
    testSetAndOption(runModeOption=setData["runModeOption"],boolOption=setData["boolOption"],failAction=setData["failAction"],ocrModelOption=setData["ocrModelOption"],testSet=setData["testSet"])
    return setData

# 更新测试配置
def write_test_set(content:testSetAndOption):
    # 验证pydantic模型
    testSetAndOption(runModeOption=content.runModeOption,boolOption=content.boolOption,failAction=content.failAction,ocrModelOption=content.ocrModelOption,testSet=content.testSet)
    setData = read_test_set()
    setData["testSet"] = dict(content.testSet)
    print(setData)
    with open (TEST_SET_PATH,'w',encoding='utf8') as f:
        json.dump(setData,f,ensure_ascii=False)
    return True


# {
#     "runModeOption": ["正常模式", "无头模式"],
#     "boolOption": ["是", "否"],
#     "failAction": ["停止测试", "跳过用例", "继续执行"],
#     "ocrModelOption": ["v2", "v3", "v4"],
#     "testSet":{
#         "runMode": "无头模式",
#         "screencastValue": "是",
#         "screenshotValue": "是",
#         "sendFlowFailAction": "停止测试",
#         "getUrlFailAction": "停止测试",
#         "loginFailAction": "跳过用例",
#         "assertFailAction": "跳过用例",
#         "execFailAction": "跳过用例",
#         "ocrModel": "v4",
#         "getUrlRetry": 4,
#         "loginRetry": 4,
#         "screenshotRetry": 4,
#         "locatRetry": 4,
#         "ocrConfidence": 90,
#         "ocrMatch": 80,
#         "imgConfidence": 95,
#         "yoloConfidence": 80
#     }
# }