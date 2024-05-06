from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import OperationLog
import uuid


# 添加操作记录
def post_operation_log(operationClass:str,operationDate:str,operationCrud:str,operationName:str):
    operationLog = OperationLog(
        operationID=uuid.uuid4(),
        operationClass=operationClass,
        operationDate=operationDate,
        operationCrud=operationCrud,
        operationName=operationName
    )
    with Session(engine) as session:
        session.add(operationLog)
        session.commit()
        session.refresh(operationLog)


# 获取5条操作记录
def get_operation_logs():
    with Session(engine) as session:
        operationLogs = session.exec(select(OperationLog).order_by(OperationLog.operationDate.desc()).limit(5)).all()
        return operationLogs
