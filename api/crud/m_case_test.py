from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import CaseTest,FuncTest,StepData
from crud.m_step_data import delete_step_data
from crud.m_test_order import read_case_order,post_case_order,put_case_order,delete_case_order



# 添加测试用例
def post_case_test(case_test:CaseTest):
    # 判断测试功能是否存在
    with Session(engine) as session:
        result = session.exec(select(FuncTest).where(FuncTest.funcID == case_test.funcID))
        db_case_test = result.first()
        if not db_case_test:
            return {"detail": "添加失败,不存在的测试功能 "+case_test.funcID}
        
    # 判断测试用例是否已存在
    with Session(engine) as session:
        result = session.exec(select(CaseTest).where(CaseTest.caseName == case_test.caseName).where(CaseTest.funcID == case_test.funcID))
        db_case_test = result.all()
        if db_case_test:
            return {"detail": "添加失败 "+case_test.funcName+" 已存在: "+case_test.caseName}

    # 新建测试用例
    with Session(engine) as session:
        session.add(case_test)
        session.commit()
        session.refresh(case_test)

    # 新建测试用例排序
    post_case_order(case_test.funcID,case_test.caseID,case_test.caseName)

    return {"detail": "Success"}



# 获取所有测试用例
def get_case_tests():
    with Session(engine) as session:
        case_tests = session.exec(select(CaseTest)).all()
        return case_tests

# 获取对应测试功能的测试用例
def get_func_case_test(func_id:str):
    return read_case_order(func_id)

# 获取单个测试用例
def get_case_test(case_test_id:str):
    with Session(engine) as session:
        case_test = session.get(CaseTest, case_test_id)
        if not case_test:
            return {"detail": "不存在的测试用例 "+case_test_id}
        return case_test

# 修改测试用例名
def put_case_test(func_id:str,case_name: str, new_name: str):
    with Session(engine) as session:
        result = session.exec(select(CaseTest).where(CaseTest.caseName == case_name).where(CaseTest.funcID == func_id))
        db_case_test = result.first()
        if not db_case_test:
            return {"detail": "不存在的测试用例 "+case_name}
        # 更新case_name
        db_case_test.caseName = new_name
        session.add(db_case_test)
        session.commit()
        session.refresh(db_case_test)
    # 更新测试排序
    put_case_order(func_id,case_name,new_name)
    return {"detail": "Success"}    

# 删除测试用例
def delete_case_test(func_id:str,case_name: str,modify_order:bool):
    print("撒大大",func_id,case_name)
    with Session(engine) as session:
        result = session.exec(select(CaseTest).where(CaseTest.caseName == case_name).where(CaseTest.funcID == func_id))
        db_case_test = result.first()
        if not db_case_test:
            return {"detail": "不存在的测试用例 "+case_name}
        # 删除测试用例
        session.delete(db_case_test)
        session.commit()

    # 删除测试排序
    if modify_order:  
        delete_case_order(db_case_test.funcID,db_case_test.caseID)

    # 删除stepdata表
    with Session(engine) as session:
        # 使用caseID查询StepData表
        result = session.exec(select(StepData).where(StepData.caseID == db_case_test.caseID))
        db_case_tests = result.all()
        if not db_case_tests:
            print({"detail": "stepdata表不存在的测试用例 "+case_name})
        for db_case_test in db_case_tests:  
            # 删除步骤时不再删除步骤排序
            delete_step_data(db_case_test.stepID,modify_order=False)
    return {"detail": "Success"}
        










