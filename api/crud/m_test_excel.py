from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import TestExcel


# 添加测试文档
def post_test_excel(test_excel:TestExcel):
    with Session(engine) as session:
        session.add(test_excel)
        session.commit()
        session.refresh(test_excel)
    return {"detail": "Success"}

# 获取测试文档列表
def get_test_excels():
    with Session(engine) as session:
        result = session.exec(select(TestExcel.excelID,TestExcel.excelName)).mappings().all()
        return result


# 获取单个测试文档
def get_test_excel(test_excel_id:str):
    with Session(engine) as session:
        result = session.exec(select(TestExcel).where(TestExcel.excelID == test_excel_id))
        db_test_excel = result.first()
        if not db_test_excel:
            db_test_excel = session.exec(select(TestExcel).limit(1)).one()
        return db_test_excel

# 修改测试环境
def put_test_excel(test_excel: TestExcel):
    with Session(engine) as session:
        db_test_excel_data = session.get(TestExcel, test_excel.excelID)
        if not db_test_excel_data:
            return {"detail": "不存在的测试文档 "+test_excel.excelID}
        db_test_excel_data_data = test_excel.model_dump(exclude_unset=True)
        db_test_excel_data.sqlmodel_update(db_test_excel_data_data)
        session.add(db_test_excel_data)
        session.commit()
        session.refresh(db_test_excel_data)
    return {"detail": "Success"}

# 删除测试附件
def delete_test_excel(test_excel_id: str):
    
    with Session(engine) as session:
        result = session.exec(select(TestExcel).where(TestExcel.excelID == test_excel_id))
        db_test_excel = result.first()
        if not db_test_excel:
            return {"detail": "不存在的测试文档 "+test_excel_id}
        session.delete(db_test_excel)
        session.commit()
    return {"detail": "Success"}





