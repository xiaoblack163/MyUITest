from sqlmodel import  Session, select,text
from MyUITestDB.db import engine
from crud.m_tabel_model import FuncTest,CaseTest,StepData,Report,DetailReport




# 获取各表记录数
def get_record_count():
    RecordCount = {}
    with Session(engine) as session:
        RecordCount["funcTest"] = len(session.exec(select(FuncTest)).all())
    with Session(engine) as session:
        RecordCount["caseTest"] = len(session.exec(select(CaseTest)).all())
    with Session(engine) as session:
        RecordCount["stepData"] = len(session.exec(select(StepData)).all())
    with Session(engine) as session:
        RecordCount["report"] = len(session.exec(select(Report)).all())  
    return RecordCount

# 获取近期FAIL测试
def get_fail_detail_report_record():
    with Session(engine) as session:
        result = session.exec(select(DetailReport.detailReportID,DetailReport.reportID,DetailReport.stepName,DetailReport.result,DetailReport.execDate).where(DetailReport.result==False).order_by(DetailReport.execDate.desc()).limit(12)).mappings().all()
    return result

# 获取近期测试报告
def get_report_record():
    with Session(engine) as session:
        result = session.exec(select(Report.reportID,Report.version,Report.testDate,Report.activity,Report.result).order_by(Report.testDate.desc()).limit(7)).mappings().all()
    return result

# 获取近期测试趋势图
def get_report_trend_record():
    report_trend_record = {
        "testDateList":[],
        "passList":[],
        "failList":[]
    }
    with Session(engine) as session:
        # 手动执行SQL查询
        statement = text(f"""
        SELECT Report.testDate, DetailChart.reportID,DetailChart.passNumber,DetailChart.failNumber
            FROM Report
        JOIN DetailChart ON Report.reportID = DetailChart.reportID
        ORDER BY Report.testDate DESC
        LIMIT 7;
        """)
        result = session.exec(statement).all()
        for i in result:
            report_trend_record["testDateList"].append(i[0].split(" ")[0])
            report_trend_record["passList"].append(sum(eval(i[2]).values()))
            report_trend_record["failList"].append(sum(eval(i[3]).values()))
        report_trend_record["testDateList"].reverse()
        report_trend_record["passList"].reverse()
        report_trend_record["failList"].reverse()
    return report_trend_record
