import time

class FormatLog:
    def __init__(self,shared_data,funcNames:list):
        self.shared_data = shared_data
        self.shared_data["logsMap"] = {key: "" for key in funcNames}
        self.currentFuncName = ''
        self.currentcaseName = ''
    
    def change_funcName(self,funcName:str):
        self.currentFuncName = funcName
    
    def change_caseName(self,caseName:str):
        self.currentcaseName = caseName

    def writeLog(self,level:str,info:str):
        currentLog = f"【{level}】 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}   {info}\n"
        print(currentLog)
        self.shared_data["logsMap"][self.currentFuncName] += currentLog
        
    def writeStepLog(self,level:str,stepName:str,info:str):
        currentLog = f"【{level}】 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}  [{self.currentFuncName} / {self.currentcaseName} / {stepName}]   {info}\n"
        print(currentLog)
        self.shared_data["logsMap"][self.currentFuncName] += currentLog


