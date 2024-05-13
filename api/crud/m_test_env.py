
from sqlmodel import  Session, select
from MyUITestDB.db import engine
from crud.m_tabel_model import TestEnv
from ipaddress import IPv4Address

# 添加测试环境
def post_test_env(test_env:TestEnv):
    try:
        IPv4Address(test_env.testEnvIP)
    except:
        return {"detail": "环境IP地址有误"}
    try:
        with Session(engine) as session:
            session.add(test_env)
            session.commit()
            session.refresh(test_env)
    except Exception as e:
        if "UNIQUE constraint failed:" in str(e):
            return {"detail": "已存在的测试环境"}
        else:
            raise e
    return {"detail": "Success"}

# 获取所有测试环境
def get_test_envs():
    with Session(engine) as session:
        test_env = session.exec(select(TestEnv)).all()
        return test_env

# 获取单个测试功能
def get_test_env(test_env_ip:str):
    with Session(engine) as session:
        # 使用funcName查询
        result = session.exec(select(TestEnv).where(TestEnv.testEnvIP == test_env_ip))
        db_test_env = result.first()
        if not db_test_env:
            return {"detail": "不存在的测试环境 "+test_env_ip}
        return db_test_env

# 修改测试环境
def put_test_env(test_env: TestEnv):
    try:
        IPv4Address(test_env.testEnvIP)
    except:
        return {"detail": "环境IP地址有误"}
    try:
        IPv4Address(test_env.sendFlowHostName)
    except:
        return {"detail": "发包IP地址有误"}
    with Session(engine) as session:
        db_test_env_data = session.get(TestEnv, test_env.testEnvID)
        if not db_test_env_data:
            return {"detail": "不存在的测试环境 "+test_env.testEnvID}
        db_test_env_data_data = test_env.model_dump(exclude_unset=True)
        db_test_env_data.sqlmodel_update(db_test_env_data_data)
        session.add(db_test_env_data)
        session.commit()
        session.refresh(db_test_env_data)
    return {"detail": "Success"}

# 删除测试环境
def delete_test_env(test_env_ip: str):
    
    with Session(engine) as session:
        # 使用funcName查询
        result = session.exec(select(TestEnv).where(TestEnv.testEnvIP == test_env_ip))
        db_test_env = result.first()
        if not db_test_env:
            return {"detail": "不存在的测试环境 "+test_env_ip}
        session.delete(db_test_env)
        session.commit()
    return {"detail": "Success"}





