
from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import TestLog
import json

# 添加测试日志
def post_test_log(test_log:TestLog):
    with Session(engine) as session:
        session.add(test_log)
        session.commit()
        session.refresh(test_log)
    return {"detail": "Success"}


# 获取单个测试日志
def get_test_log(test_log_ip:str):
    with Session(engine) as session:
        # 使用funcName查询
        result = session.exec(select(TestLog.testLog).where(TestLog.reportID == test_log_ip))
        db_test_log = result.first()
        if not db_test_log:
            return {"detail": "不存在的测试日志 "+test_log_ip}
        return json.loads(db_test_log)
