
from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import FuncTest,CaseTest
from crud.m_case_test import delete_case_test
from crud.m_test_order import read_func_order,post_func_order,put_func_order,delete_func_order



# 添加测试功能
def post_func_test(func_test:FuncTest):
    with Session(engine) as session:
        session.add(func_test)
        session.commit()
        session.refresh(func_test)

    # 添加测试排序
    post_func_order(func_test.funcID,func_test.funcName)
    return {"detail": "Success"}

# 获取所有测试功能
def get_func_tests():
    return read_func_order()

# 获取单个测试功能
def get_func_test(func_test_id:str):
    with Session(engine) as session:
        func_test = session.get(FuncTest, func_test_id)
        if not func_test:
            return {"detail": "不存在的测试功能 "+func_test_id}
        return func_test

# 修改测试功能名
def put_func_test(func_name: str, new_name: str):
    # 更新functest表
    with Session(engine) as session:
        result = session.exec(select(FuncTest).where(FuncTest.funcName == func_name))
        db_func_test = result.first()
        if not db_func_test:
            return {"detail": "不存在的测试功能 "+func_name}
        # 更新funcName
        db_func_test.funcName = new_name
        session.add(db_func_test)
        session.commit()
        session.refresh(db_func_test)

    # 更新测试排序
    put_func_order(func_name,new_name)
    return {"detail": "Success"}

# 删除测试功能
def delete_func_test(func_name: str):
    # 删除functest表
    with Session(engine) as session:
        # 使用funcName查询
        result = session.exec(select(FuncTest).where(FuncTest.funcName == func_name))
        db_func_test = result.first()
        if not db_func_test:
            return {"detail": "不存在的测试功能 "+func_name}
        session.delete(db_func_test)
        session.commit()

    # 删除测试排序
    delete_func_order(func_name)


    # 删除casetest表
    with Session(engine) as session:
        # 使用funcID查询CaseTest表
        result = session.exec(select(CaseTest).where(CaseTest.funcID == db_func_test.funcID))
        db_func_tests = result.all()
        if not db_func_tests:
            print({"detail": "casetest表不存在的测试功能 "+func_name})
        for db_func_test in db_func_tests:  
            # 删除用例时不再删除用例排序
            delete_case_test(db_func_test.funcID,db_func_test.caseName,modify_order=False)



    return {"detail": "Success"}






