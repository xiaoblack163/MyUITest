from MyUITestDB.db import engine
from sqlmodel import Session,text

def get_case_view():
    # 创建一个新会话
    with Session(engine) as session:
        # 手动执行SQL查询
        statement = text("""
        SELECT
            StepData.stepID,
            StepData.stepName,
            StepData.locatMode,
            StepData.locatValue,
            StepData.elementNumber,
            StepData.xValue,
            StepData.yValue,
            StepData.action,
            StepData.AssertOrActionValue,
            StepData.stepInfo,
            CaseTest.caseID,
            CaseTest.caseName,
            FuncTest.funcName
        FROM
            StepData
        INNER JOIN
            CaseTest ON StepData.caseID = CaseTest.caseID
        INNER JOIN
            FuncTest ON CaseTest.funcID = FuncTest.funcID;
        """)
        result = session.exec(statement).mappings().all()
        return result