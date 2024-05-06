from sqlmodel import  Session
from MyUITestDB.db import engine
from crud.m_tabel_model import DetailChart


# 添加详细报告图表
def post_detail_chart(detail_chart:DetailChart):
    with Session(engine) as session:
        session.add(detail_chart)
        session.commit()
        session.refresh(detail_chart)


# 获取单个详细报告图表
def get_detail_chart(report_id:str):
    with Session(engine) as session:
        detail_chart = session.get(DetailChart, report_id)
        if not detail_chart:
            return {"detail": "不存在的测试报告 "+report_id}
        return detail_chart
