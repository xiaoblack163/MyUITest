from sqlmodel import Session, select,text
from MyUITestDB.db import engine
from crud.m_tabel_model import StepData
from crud.m_test_order import put_step_order,post_step_order,delete_step_order
from crud.m_operation_log import post_operation_log

# 添加测试步骤
def post_step_data(step_data:StepData):
    try:
        # 添加测试步骤
        with Session(engine) as session:
            session.add(step_data)
            session.commit()
            session.refresh(step_data)
            
        # 添加测试步骤排序
        post_step_order(step_data.funcID,step_data.caseID,step_data.stepID,step_data.stepName)
        
        # 添加操作日志
        post_operation_log("添加了测试步骤",step_data.stepName)
        return {"detail": "Success"}
        
    except Exception as e:
        # 如果stepID唯一索引报错则切换为更新数据
        if "UNIQUE constraint failed: stepdata.stepID" in str(e):
            print( {"detail": "测试步骤已创建"})
            return put_step_data(step_data)
        else:
            raise e

# 获取所有测试步骤
def get_step_datas():
    with Session(engine) as session:
        step_data = session.exec(select(StepData)).all()
        return step_data

# 获取单个测试步骤 
def get_step_data(step_data_id:str):
    with Session(engine) as session:
        step_data = session.get(StepData, step_data_id)
        if not step_data:
            return {"detail": "不存在的测试步骤 "+step_data_id}
        return step_data

# 修改测试步骤
def put_step_data(step_data:StepData):
    with Session(engine) as session:
        db_step_data = session.get(StepData, step_data.stepID)
        if not db_step_data:
            return {"detail": "不存在的测试步骤 "+step_data.stepID}
        step_data_data = step_data.model_dump(exclude_unset=True)
        db_step_data.sqlmodel_update(step_data_data)
        session.add(db_step_data)
        session.commit()
        session.refresh(db_step_data)

    # 更新测试步骤排序(主要更新测试步骤名称)
    put_step_order(step_data.funcID,step_data.caseID,step_data.stepID,step_data.stepName)            
    
    # 添加操作日志
    post_operation_log("修改了测试步骤",step_data.stepName)
    return {"detail": "Success"}

# 删除测试步骤
def delete_step_data(step_data_id:str,modify_order:bool):
    with Session(engine) as session:
        db_step_data = session.get(StepData, step_data_id)
        if not db_step_data:
            return {"detail": "不存在的测试步骤 "+step_data_id}
        # 删除测试步骤
        session.delete(db_step_data)
        session.commit()

    # 更新测试步骤排序(主要删除测试步骤)
    if modify_order:
        delete_step_order(db_step_data.funcID,db_step_data.caseID,db_step_data.stepID)
        # 添加操作日志
        post_operation_log("删除了测试步骤",db_step_data.stepName)

    return {"detail": "Success"}

def get_step_data_join(step_id:str):
    with Session(engine) as session:
        # 手动执行SQL查询
        statement = text(f"""
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
            StepData.caseID,
            StepData.funcID,
            CaseTest.caseName,
            FuncTest.funcName
        FROM
            StepData
        INNER JOIN
            CaseTest ON StepData.caseID = CaseTest.caseID
        INNER JOIN
            FuncTest ON StepData.funcID = FuncTest.funcID
        WHERE
            StepData.stepID = '{step_id}';
        """)
        result = dict(session.exec(statement).mappings().one())
        result["locatMode"] = eval(result["locatMode"])["value"]
        result["action"] = eval(result["action"])["value"]
        return result