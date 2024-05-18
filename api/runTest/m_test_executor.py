from typing import Dict,Any
import copy,uuid,time,json
from crud.m_test_order import read_test_order
from crud.m_step_data import get_step_data_join
from crud.m_report import post_report,Report
from crud.m_detail_chart import post_detail_chart,DetailChart
from crud.m_detail_report import post_detail_report,DetailReport
from crud.m_test_log import post_test_log,TestLog
from crud.m_operation_log import post_operation_log
from crud.m_test_set import read_test_set
from crud.m_test_env import get_test_env

from runTest.m_action import WebDriver
from runTest.m_log import FormatLog





# 执行测试的对象(整理测试数据，写入测试结果)
class TestExecutor:
    def __init__(self,stop_event,shared_data,run_test_data:Dict[str, Any]) -> None:
        self.testID = str(uuid.uuid4()) # 测试报告ID
        self.testDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) # 测试时间
        self.stop_skip_event = {"stop_event":stop_event,"skipCase":False} # 停止测试或者跳过用例运行信号
        self.shared_data = shared_data # 进程间共享数据
        self.test_order_data = self.parseCase(run_test_data) # 解析测试数据
        self.init_shared_data(run_test_data) # 初始化共享数据
        self.testSet = read_test_set()["testSet"] # 读取测试配置
        self.testEnv = dict(get_test_env(str(run_test_data["testEnv"]))) # 读取测试环境(发包)
        self.webdriver = WebDriver(self.testEnv,self.testSet,self.stop_skip_event,self.formatLog) # 创建webdriver对象
        

    # 初始化共享数据
    def init_shared_data(self,run_test_data):
        # 测试状态
        self.shared_data["run_status"] = True

        # 测试环境
        self.shared_data["testEnv"] = {}
        self.shared_data["testEnv"]["testEnv"] = run_test_data["testEnv"]
        self.shared_data["testEnv"]["testor"] = run_test_data["testor"]
        self.shared_data["testEnv"]["version"] = run_test_data["version"]
        

        # 测试进度
        self.shared_data["activity"] = {}
        self.shared_data["activity"]["funcNumber"]=str(self.test_order_data).count("funcName") #功能数
        self.shared_data["activity"]["caseNumber"]=str(self.test_order_data).count("caseName")#用例总数
        self.shared_data["activity"]["stepNumber"]=str(self.test_order_data).count("stepName")#步骤总数
        self.shared_data["activity"]["testedNumber"]= 0 #已测步骤数
        self.shared_data["activity"]["passNumber"]=0 #通过数
        self.shared_data["activity"]["execFailNumber"]=0 #执行失败数
        self.shared_data["activity"]["assertFailNumber"]=0 #断言失败数

        # 测试进度图表
        self.shared_data["funcChart"] = {}
        self.shared_data["funcChart"]["passNumber"] = {}  # 测试功能通过数list
        self.shared_data["funcChart"]["failNumber"] = {}   # 测试功能失败数list
        for funcTest in self.test_order_data:
            self.shared_data["funcChart"]["passNumber"][funcTest["funcName"]] = 0
            self.shared_data["funcChart"]["failNumber"][funcTest["funcName"]] = 0
        #添加操作日志和运行日志
        self.formatLog = FormatLog(self.shared_data,list(self.shared_data["funcChart"]["passNumber"]))
        post_operation_log("执行了测试",str(list(self.shared_data["funcChart"]["passNumber"])).replace("[","").replace("]", "").replace("'", ""))

    # 解析测试数据
    def parseCase(self,run_test_data):
        selectedTreeTableValue = run_test_data["selectedTreeTableValue"]
        selectedTreeTableValue_bak = copy.deepcopy(selectedTreeTableValue)
        for k,v in selectedTreeTableValue.items():
            if "<->" not in k or (v["checked"] == False and v["partialChecked"] == False):
                selectedTreeTableValue_bak.pop(k)
        selectedTreeTableValue_str = str(selectedTreeTableValue_bak)
        test_order_data = read_test_order()
        test_order_data_bak = copy.deepcopy(test_order_data)
        for funcData in test_order_data:
            if funcData["funcID"] not in selectedTreeTableValue_str:
                print("移除功能",funcData["funcName"])
                test_order_data_bak.remove(funcData)
        test_order_data_bak_bak = copy.deepcopy(test_order_data_bak)
        for k,funcData in enumerate(test_order_data_bak):
            for caseData in funcData["children"]:
                if caseData["caseID"] not in selectedTreeTableValue_str:
                    print("移除用例",caseData["caseName"])
                    test_order_data_bak_bak[k]["children"].remove(caseData)
        print("测试项:\n",test_order_data_bak_bak)
        return test_order_data_bak_bak

    # 添加测试报告
    def writeReport(self):
        reportData = Report(
            reportID=self.testID,
            testEnv=str(self.shared_data["testEnv"]["testEnv"]),
            version=self.shared_data["testEnv"]["version"],
            testor=self.shared_data["testEnv"]["testor"],
            testDate=self.testDate,
            testFuncs=json.dumps([funcTest["funcName"] for funcTest in self.test_order_data],ensure_ascii=False),
            activity= int((self.shared_data["activity"]["testedNumber"]/self.shared_data["activity"]["stepNumber"])*100),
            result=bool(self.shared_data["activity"]["stepNumber"]==self.shared_data["activity"]["passNumber"])
        )
        post_report(reportData)

    # 添加详细报告图表
    def writeDetailChart(self):
        detailChartData = DetailChart(
            reportID=self.testID,
            passNumber = str(self.shared_data["funcChart"]["passNumber"]),
            failNumber = str(self.shared_data["funcChart"]["failNumber"]),
            activity=str(self.shared_data["activity"])
        )
        post_detail_chart(detailChartData)

    # 添加测试日志
    def writeTestLog(self):
        testLogData = TestLog(
            reportID=self.testID,
            testLog=json.dumps(self.shared_data["logsMap"],ensure_ascii=False)
        )
        post_test_log(testLogData)


    # 添加详细步骤报告
    def writeDetailReport(self,stepReportData):
        detailReporttData = DetailReport(
            detailReportID = stepReportData["detailReportID"],
            reportID = stepReportData["reportID"],
            execDate = stepReportData["execDate"],
            result = stepReportData["result"],
            execInfo = stepReportData["execInfo"],
            stepID = stepReportData["stepID"],
            stepName = stepReportData["stepName"],
            locatMode = stepReportData["locatMode"],
            locatValue = stepReportData["locatValue"],
            yoloValue = stepReportData["yoloValue"],
            elementNumber = stepReportData["elementNumber"],
            xValue = stepReportData["xValue"],
            yValue = stepReportData["yValue"],
            action = stepReportData["action"],
            AssertOrActionValue = stepReportData["AssertOrActionValue"],
            preSleep = stepReportData["preSleep"],
            stepInfo = stepReportData["stepInfo"],
            caseID = stepReportData["caseID"],
            funcID = stepReportData["funcID"],
            caseName = stepReportData["caseName"],
            funcName = stepReportData["funcName"]
        )
        post_detail_report(detailReporttData)


    # 执行测试
    def runTest(self):
        for funcTest in self.test_order_data:
            self.formatLog.change_funcName(funcTest["funcName"])
            self.formatLog.writeLog("INFO","测试功能开始执行")
            for caseTest in funcTest["children"]:
                self.stop_skip_event["skipCase"] = False # 跳过用例设置为False
                self.formatLog.change_caseName(caseTest["caseName"])
                self.formatLog.writeLog("INFO","测试用例开始执行")
                self.webdriver.start_screencast() # 开始录屏 测试用例为单位
                for StepTest in caseTest["grandchild"]:
                    if self.stop_skip_event["stop_event"].is_set():
                        self.webdriver.stop_screencast(self.testID+caseTest["caseID"]) # 停止录屏
                        self.done()
                        self.formatLog.writeLog("WARN","捕捉到停止信号，测试终止")
                        return 
                    if self.stop_skip_event["skipCase"]:
                        self.webdriver.stop_screencast(self.testID+caseTest["caseID"]) # 停止录屏
                        self.formatLog.writeLog("WARN","捕捉到跳过用例信号，测试用例跳过")
                        break 
                    self.formatLog.writeLog("INFO","测试步骤开始执行")
                    try:
                        self.shared_data["activity"]["testedNumber"] += 1 #已测步骤加1
                        stepdata = get_step_data_join(StepTest["stepID"]) # 读取步骤相关信息
                        stepdata["detailReportID"] = str(uuid.uuid4()) # 执行测试ID
                        stepdata["reportID"] = self.testID #报告ID
                        stepdata["execDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) # 步骤执行时间
                        if self.webdriver.start_step(stepdata): # 执行步骤操作
                            stepdata["result"] = True  # 步骤执行成功加1
                            stepdata["execInfo"] = "执行步骤成功"  #步骤执行成功信息
                            self.shared_data["activity"]["passNumber"] += 1 #通过数加1
                            self.shared_data["funcChart"]["passNumber"][funcTest["funcName"]] += 1# 测试功能通过数加1
                            self.formatLog.writeStepLog("PASS",StepTest["stepName"],"执行步骤成功")
                        else:
                            stepdata["result"] = False  #断言失败加1
                            stepdata["execInfo"] = "断言失败"  #断言失败信息
                            self.shared_data["activity"]["assertFailNumber"] += 1 #断言失败数加1
                            self.shared_data["funcChart"]["failNumber"][funcTest["funcName"]] += 1 # 测试功能失败数加1
                            self.formatLog.writeStepLog("FAIL",StepTest["stepName"],"断言失败")
                            self.webdriver.set_stop_skip_event("assertFailAction") # 设置停止或者跳过用例
                    except Exception as e:
                        stepdata["result"] = False  #步骤执行失败加1
                        stepdata["execInfo"] = "执行失败"  #步骤执行失败信息
                        self.shared_data["activity"]["execFailNumber"] += 1 #执行失败加1
                        self.shared_data["funcChart"]["failNumber"][funcTest["funcName"]] += 1 # 测试功能失败数加1
                        self.formatLog.writeStepLog("ERROR",StepTest["stepName"],"步骤执行失败"+str(e))
                        self.webdriver.set_stop_skip_event("execFailAction") # 设置停止或者跳过用例
                    finally:
                        ...
                        self.writeDetailReport(stepdata) #写入测试步骤结果
                        self.webdriver.start_screenshot(stepdata["detailReportID"]) # 步骤执行完截图
                self.webdriver.stop_screencast(self.testID+caseTest["caseID"]) # 停止录屏
        self.done()

    def done(self):
        self.writeReport()
        self.writeDetailChart()
        self.writeTestLog()
        self.webdriver.page.quit()
        self.shared_data["run_status"] = False
        self.formatLog.writeLog("INFO","测试执行完毕")
    

