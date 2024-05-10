from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import OperationLog
import uuid,time


# 添加操作记录
def post_operation_log(operationCrud:str,operationName:str):
        if "添加" in operationCrud:
            operationClass = "pi pi-plus text-xl text-blue-500"
        elif "修改" in operationCrud:
            operationClass = "pi pi-eraser text-xl text-blue-500"
        elif "删除" in operationCrud:
            operationClass = "pi pi-trash text-xl text-blue-500"
        elif "执行" in operationCrud:
            operationClass = "pi pi-play text-xl text-blue-500"
        else:
            operationCrud = "pi pi-question text-xl text-blue-500"
        operationLog = OperationLog(
            operationID=str(uuid.uuid4()),
            operationClass=operationClass,
            operationDate=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            operationCrud=operationCrud,
            operationName=operationName
        )
        try:
            with Session(engine) as session:
                session.add(operationLog)
                session.commit()
                session.refresh(operationLog)
        except:
            print("添加操作日志失败")

# 获取5条操作记录
def get_operation_logs():
    with Session(engine) as session:
        operationLogs = session.exec(select(OperationLog).order_by(OperationLog.operationDate.desc()).limit(5)).all()
        return operationLogs
