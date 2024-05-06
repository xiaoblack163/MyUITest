from sqlmodel import  SQLModel, create_engine

sqlite_file_name = "MyUITest.db"
sqlite_url = f"sqlite:///MyUITestDB/{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 手动执行sql2
# from sqlmodel import Session,text

# def get_case_view():
#     # 创建一个新会话
#     with Session(engine) as session:
#         # 手动执行SQL查询
#         statement = text("""
#         SELECT
#             StepData.stepID,
#             StepData.stepName,
#             StepData.locatMode,
#             StepData.locatValue,
#             StepData.elementNumber,
#             StepData.xyValue,
#             StepData.action,
#             StepData.AssertOrActionValue,
#             StepData.stepInfo,
#             CaseTest.caseID,
#             CaseTest.caseName,
#             FuncTest.funcName
#         FROM
#             StepData
#         INNER JOIN
#             CaseTest ON StepData.caseID = CaseTest.caseID
#         INNER JOIN
#             FuncTest ON CaseTest.funcID = FuncTest.funcID;
#         """)
#         result = session.exec(statement).mappings().all()
#     return result


# 手动执行sql
# with engine.connect() as conn:
#     xx = conn.connection.cursor().execute("select * from hero;")
#     for row in xx:
#         print("结果:",row)