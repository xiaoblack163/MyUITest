from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import Report

# 添加测试报告
def post_report(report:Report):
    with Session(engine) as session:
        session.add(report)
        session.commit()
        session.refresh(report)


# 获取所有测试报告
def get_reports():
    with Session(engine) as session:
        reports = session.exec(select(Report).order_by(Report.testDate.desc())).all()
        return reports