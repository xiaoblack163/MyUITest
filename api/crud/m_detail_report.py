from sqlmodel import  Session,select
from MyUITestDB.db import engine
from crud.m_tabel_model import DetailReport


# 添加详细步骤报告
def post_detail_report(detail_report:DetailReport):
    with Session(engine) as session:
        session.add(detail_report)
        session.commit()
        session.refresh(detail_report)



# 获取对应测试报告的详细测试数据
def get_detail_report(report_id:str):
    with Session(engine) as session:
        detail_reports = session.exec(select(DetailReport).where(DetailReport.reportID == report_id)).all()
        return detail_reports