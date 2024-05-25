from typing import  Optional
from sqlmodel import SQLModel, Field

# 测试功能表
class FuncTest(SQLModel, table=True):
    funcID: str = Field(default=None, primary_key=True)
    funcName: str = Field(unique=True)

# 测试用例表
class CaseTest(SQLModel, table=True):
    caseID: str = Field(default=None, primary_key=True)
    caseName: str
    funcID: str

# 测试步骤表
class StepData(SQLModel, table=True):
    stepID: str = Field(default=None, primary_key=True)
    stepName: str
    locatMode: str
    locatValue: str
    yoloValue: str
    elementNumber: Optional[int] =Field(nullable=False)
    xValue: Optional[int] =Field(nullable=False)
    yValue: Optional[int] =Field(nullable=False)
    action: str
    AssertOrActionValue: str
    preSleep: Optional[int] =Field(nullable=False)
    stepInfo: str
    caseID: str 
    funcID: str 

# 测试报告表
class Report(SQLModel, table=True):
    reportID:  str = Field(default=None, primary_key=True)
    testEnv:str
    version: str
    testor:str
    testDate:str
    testFuncs: str
    activity: Optional[int] =Field(nullable=False)
    result:bool

# 详细报告图表
class DetailChart(SQLModel, table=True):
    reportID:  str = Field(default=None, primary_key=True)
    passNumber: str
    failNumber: str
    activity: str

# 详细报告表
class DetailReport(SQLModel, table=True):
    detailReportID: str = Field(default=None, primary_key=True)
    reportID:str
    execDate:str
    result:bool
    execInfo:str
    stepID: str
    stepName: str
    locatMode: str
    locatValue: str
    yoloValue: str
    elementNumber: Optional[int] =Field(nullable=False)
    xValue: Optional[int] =Field(nullable=False)
    yValue: Optional[int] =Field(nullable=False)
    action: str
    AssertOrActionValue: str
    preSleep: Optional[int] =Field(nullable=False)
    stepInfo: str
    caseID: str 
    funcID: str 
    caseName:str
    funcName:str

# 操作日志表
class OperationLog(SQLModel, table=True):
    operationID:  str = Field(default=None, primary_key=True)
    operationClass: str
    operationDate: str
    operationCrud: str
    operationName: str


# 测试环境表
class TestEnv(SQLModel, table=True):
    testEnvID:  str = Field(default=None, primary_key=True)
    testEnvIP: str = Field(unique=True)
    sendFlowHostName:str
    sendFlowUserName: str
    sendFlowPassWord: str

# 测试日志表
class TestLog(SQLModel, table=True):
    reportID:  str = Field(default=None, primary_key=True)
    testLog: str

# 测试文档表
class TestExcel(SQLModel, table=True):
    excelID:  str = Field(default=None, primary_key=True)
    excelName: str
    excelData: str

# 测试附件表
class TestFile(SQLModel, table=True):
    fileID:  str = Field(default=None, primary_key=True)
    fileName: str
