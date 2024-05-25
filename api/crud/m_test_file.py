from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import TestFile
import uuid
import os


# 添加测试附件
def post_test_file(filename,contents):
    with open("testFile/"+filename ,"wb") as f:
        f.write(contents)
    test_file = TestFile(
        fileName = filename,
        fileID = str(uuid.uuid4())
    )
    with Session(engine) as session:
        session.add(test_file)
        session.commit()
        session.refresh(test_file)
    return {"detail": "Success"}

# 获取测试附件列表
def get_test_files():
    with Session(engine) as session:
        result = session.exec(select(TestFile)).all()
        return result


# 删除测试附件
def delete_test_file(test_file_id: str):
    with Session(engine) as session:
        result = session.exec(select(TestFile).where(TestFile.fileID == test_file_id))
        db_test_file = result.first()
        if not db_test_file:
            return {"detail": "不存在的测试附件 "+test_file_id}
        os.remove("testFile/"+db_test_file.fileName)
        session.delete(db_test_file)
        session.commit()
    return {"detail": "Success"}





