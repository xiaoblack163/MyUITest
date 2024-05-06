from multiprocessing import Process,Event,Manager
import time
from runTest.m_test_executor import TestExecutor 

# 创建一个多进程的测试执行对象(连接前端与执行测试的桥梁,共享内存,停止执行等)
class Create_TestExecutor:
    def __init__(self):
        self.stop_event = Event() #终止执行的信号
        self.manager = Manager()
        self.shared_data = self.manager.dict() #共享内存

    def reset(self):
        self.stop_event.clear()
        self.shared_data.clear()

    def create_worker(self,run_test_data):
        # 创建并启动子进程
        self.reset()
        testExecutor = TestExecutor(self.manager,self.stop_event,self.shared_data,run_test_data)
        self.process = Process(target=testExecutor.runTest, args=())
        self.process.start()

        
    def stop_worker(self):
        # 停止子进程
        print("捕捉到中断信号，正在停止子进程...")
        self.stop_event.set()
        self.process.join()  # 等待子进程结束
        time.sleep(30)
        if self.process.is_alive():
            print("子进程未正常退出，正在强制终止...")
            self.process.terminate()
        self.reset()


if __name__ == "__main__":
    ppp = {"selectedTreeTableValue":{"57d4898a-070d-4f1c-b86f-eb6dafbf2086":{"checked":True,"partialChecked":False},"测试webdriver<->57d4898a-070d-4f1c-b86f-eb6dafbf2086<->测试webdriver用例<->da7bd0c9-d403-4437-9df1-005d7e096fe5":{"checked":True,"partialChecked":False}},"testEnv":"1.1.1.1","testor":"3","version":"3"}
    xxx = Create_TestExecutor()
    xxx.create_worker(ppp)

