from threading import Thread,Event
from runTest.m_test_executor import TestExecutor 
from pydantic import BaseModel
from ipaddress import IPv4Address
from typing import Dict

# 定义前后端交互的测试数据结构
class RunTestData(BaseModel):
    selectedTreeTableValue:Dict[str, Dict[str,bool]]
    testEnv:IPv4Address
    testor:str
    version: str


# 创建一个多进程的测试执行对象(连接前端与执行测试的桥梁,共享内存,停止执行等)
class Create_TestExecutor:
    def __init__(self):
        self.stop_event = Event()  # 创建停止信号
        self.shared_data  = {
            "run_status": False,
            "testEnv": {
                "testEnv": "",
                "testor": "",
                "version": ""
            },
            "activity": {
                "funcNumber": 0,
                "caseNumber": 0,
                "stepNumber": 0.1,
                "testedNumber": 0,
                "passNumber": 0,
                "execFailNumber": 0,
                "assertFailNumber": 0
            },
            "funcChart": {
                "passNumber": {},
                "failNumber": {}
            },
            "logsMap": {"暂无日志":""}
        }

    def reset(self):
        self.stop_event.clear()  # 重置停止信号
        self.shared_data.clear()
        self.shared_data  = {
            "run_status": False,
            "testEnv": {
                "testEnv": "",
                "testor": "",
                "version": ""
            },
            "activity": {
                "funcNumber": 0,
                "caseNumber": 0,
                "stepNumber": 0.1,
                "testedNumber": 0,
                "passNumber": 0,
                "execFailNumber": 0,
                "assertFailNumber": 0
            },
            "funcChart": {
                "passNumber": {},
                "failNumber": {}
            },
            "logsMap": {"暂无日志":""}
        }

    def create_worker(self,run_test_data):
        # 创建并启动子进程
        self.reset()
        testExecutor = TestExecutor(self.stop_event,self.shared_data,run_test_data)
        self.thread = Thread(target=testExecutor.runTest, args=())
        self.thread.start()

        
    def stop_worker(self):
        # 停止子进程
        print("捕捉到中断信号，正在停止子进程...")
        self.stop_event.set()
        self.thread.join()  # 等待子进程结束
        print("子线程已经结束")
        self.reset()


if __name__ == "__main__":
    ppp = {"selectedTreeTableValue":{"57d4898a-070d-4f1c-b86f-eb6dafbf2086":{"checked":True,"partialChecked":False},"测试webdriver<->57d4898a-070d-4f1c-b86f-eb6dafbf2086<->测试webdriver用例<->da7bd0c9-d403-4437-9df1-005d7e096fe5":{"checked":True,"partialChecked":False}},"testEnv":"1.1.1.1","testor":"3","version":"3"}
    xxx = Create_TestExecutor()
    xxx.create_worker(ppp)

