from fastapi import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from MyUITestDB.db import create_db_and_tables


from crud import m_dash_board
from crud import m_operation_log
from crud import m_local_action_option
from crud import m_test_order
from crud import m_step_data
from crud import m_func_test
from crud import m_case_test
from crud import m_case_view
from crud import m_report
from crud import m_detail_chart
from crud import m_detail_report
from crud import m_test_env
from crud import m_test_set
from crud import m_test_log

from runTest import m_create_test_process

createTestExecutor = createTestExecutor =  m_create_test_process.Create_TestExecutor()
# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()
app.mount("/screenshot", StaticFiles(directory="screenshot"), name="screenshot")
app.mount("/screencast", StaticFiles(directory="screencast"), name="screencast")
app.mount("/yoloImages", StaticFiles(directory="yoloImages"), name="yoloImages")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# 第一次运行时创建数据库
@app.on_event("startup")
async def on_startup():
    return create_db_and_tables()



# 仪表盘数据
################################################################

# 获取各表记录数
@app.get("/dash_board/get_record_count")
async def get_record_count():
    return m_dash_board.get_record_count()

# 获取近期FAIL测试
@app.get("/dash_board/get_fail_detail_report_record")
async def get_fail_detail_report_record():
    return m_dash_board.get_fail_detail_report_record()


# 获取近期测试报告
@app.get("/dash_board/get_report_record")
async def get_report_record():
    return m_dash_board.get_report_record()


# 获取近期测试趋势图
@app.get("/dash_board/get_report_trend_record")
async def get_report_trend_record():
    return m_dash_board.get_report_trend_record()

# 获取5条操作记录
@app.get("/dash_board/get_operation_logs")
async def get_operation_logs():
    return m_operation_log.get_operation_logs()



#crud
################################################################

# 定位选项，传递给前端
@app.get("/init/step_data/locat_option")
async def locat_option():
    return m_local_action_option.locat_option

# 初始化定位与动作映射，传递给前端
@app.get("/init/step_data/locatOption_actionOption")
async def action_option():
    return m_local_action_option.locatOption_actionOption

# check操作值是否为空，传递给前端
@app.get("/init/step_data/check_action_value")
async def action_option():
    return m_local_action_option.checkActionValue

# check定位值是否为空，传递给前端
@app.get("/init/step_data/check_locat_value")
async def action_option():
    return m_local_action_option.checkLocatValue

# 目标检测选项，传递给前端
@app.get("/init/step_data/yolo_option")
async def action_option():
    return m_local_action_option.yoloOption


################################################################

# 添加测试功能数据
@app.post("/func_test")
async def post_func_test(func_test: m_func_test.FuncTest):
    return m_func_test.post_func_test(func_test)

# 获取所有测试功能数据
@app.get("/func_tests")
async def get_func_tests():
    return m_func_test.get_func_tests()

# 获取单个测试功能数据
@app.get("/func_test/{func_test_id}",response_model=m_func_test.FuncTest)
async def get_func_test(func_test_id:str):
    return m_func_test.get_func_test(func_test_id)

# 修改测试功能数据
@app.put("/func_test/{func_name}/{new_name}")
async def put_func_test(func_name:str,new_name: str):
    return m_func_test.put_func_test(func_name,new_name)

# 删除测试功能数据
@app.delete("/func_test/{func_name}")
async def delete_func_test(func_name:str):
    return m_func_test.delete_func_test(func_name)

################################################################

# 添加测试用例数据
@app.post("/case_test")
async def post_case_test(case_test: m_case_test.CaseTest):
    return m_case_test.post_case_test(case_test)

# 获取所有测试用例数据
@app.get("/case_tests")
async def get_case_tests():
    return m_case_test.get_case_tests()

# 获取对应测试功能的测试用例
@app.get("/case_test/{func_id}")
async def get_func_case_test(func_id:str):
    return m_case_test.get_func_case_test(func_id)

# 获取单个测试用例数据
@app.get("/case_test/{case_test_id}",response_model=m_case_test.CaseTest)
async def get_case_test(case_test_id:str):
    return m_case_test.get_case_test(case_test_id)

# 修改测试用例数据
@app.put("/case_test/{func_id}/{case_name}/{new_name}")
async def put_case_test(func_id:str,case_name:str,new_name: str):
    return m_case_test.put_case_test(func_id,case_name,new_name)

# 删除测试用例数据
@app.delete("/case_test/{func_id}/{case_name}")
async def delete_case_test(func_id:str,case_name:str):
    return m_case_test.delete_case_test(func_id,case_name,modify_order=True)

################################################################

# 添加测试步骤数据
@app.post("/step_data")
async def post_step_data(step_data: m_step_data.StepData):
    step_data.locatMode =  str(step_data.locatMode)
    step_data.action =  str(step_data.action)
    return m_step_data.post_step_data(step_data)

# 获取所有测试步骤数据
@app.get("/step_datas")
async def get_step_datas():
    return m_step_data.get_step_datas()

# 获取单个测试步骤数据
@app.get("/step_data/{step_data_id}",response_model=m_step_data.StepData)
async def get_step_data(step_data_id:str):
    return m_step_data.get_step_data(step_data_id)

# 修改测试步骤
@app.put("/step_data")
async def put_step_data(step_data: m_step_data.StepData):
    step_data.locatMode =  str(step_data.locatMode)
    step_data.action =  str(step_data.action)
    return m_step_data.put_step_data(step_data)

# 删除测试步骤
@app.delete("/step_data/{step_data_id}")
async def delete_step_data(step_data_id:str):
    return m_step_data.delete_step_data(step_data_id,modify_order=True)

# 上传定位图片
@app.post("/step_data/upload_file/{file_id}")
async def upload_file(file_id: str,file: UploadFile = File(...)):
    contents = await file.read()
    with open(f"locatImages/{file_id}.png",'wb') as f:
        f.write(contents)
    return {"detail":"Success"}

################################################################

# 获取所有用例总览数据
@app.get("/case_view")
async def get_case_view():
    return m_case_view.get_case_view()

################################################################

# 获取管理执行顺序数据
@app.get("/test_order")
async def get_test_order():
    return m_test_order.read_test_order()

# # 更新测试排序数据(直接解析json)
# @app.put("/test_order")
# async async def put_test_order(request: Request):
#     test_order_data = await request.json()
#     m_test_order.write_test_order(test_order_data)
#     return {"detail":"Success"}

# 更新测试排序数据(解析pydandic模型)
@app.put("/test_order")
async def put_test_order(testOrderData: m_test_order.TestOrderData):
    m_test_order.write_test_order(testOrderData.model_dump()["testOrderData"])
    return {"detail":"Success"}

################################################################

# 获取对应测试功能的测试用例排序数据
@app.get("/case_order/{funcID}")
async def get_case_order(funcID:str):
    return m_test_order.get_case_order(funcID)


# 获取对应测试用例的测试步骤排序数据
@app.get("/step_order/{funcID}/{caseID}")
async def get_step_data(funcID:str,caseID:str):
    return m_test_order.get_step_order(funcID,caseID)









#运行测试
################################################################运行测试

# 获取执行测试界面树形排序数据
@app.get("/run_case")
async def get_run_case_tree_data():
    return m_test_order.get_run_case_tree_data()


# 执行测试
@app.post("/run_case")
async  def post_run_test_data(run_test_data: m_create_test_process.RunTestData):
    run_test_data = run_test_data.model_dump()
    if run_test_data["selectedTreeTableValue"] == {}:
        return {"detail":[{"msg":"请选择测试项!"}]}
    if createTestExecutor.shared_data.get("run_status"):
        return {"detail":"已有测试任务正在执行中,请等待.."}
    else:
        createTestExecutor.create_worker(run_test_data)
    return {"detail":"开始执行测试.."}

# 停止测试执行
@app.put("/run_case")
async def stop_run_test():
    createTestExecutor.stop_event.set()
    return {"detail":"测试正在停止.."}

# 强制停止测试执行
@app.put("/run_case/force")
async def force_stop_run_test():
    createTestExecutor.stop_worker()
    return {"detail":"测试已停止.."}

# 获取执行进度
@app.get("/run_case/activity")
async def get_run_test_activity():
    return createTestExecutor.shared_data

# 获取执行日志
@app.get("/run_case/log")
async def get_run_test_log():
    return createTestExecutor.shared_data["logsMap"]


################################################################

# 获取所有测试报告
@app.get("/report/reports")
async def get_reports():
    return m_report.get_reports()

# 获取单个详细测试报告图表数据
@app.get("/report/detail_chart/{report_id}")
async def get_detail_chart(report_id:str):
    return m_detail_chart.get_detail_chart(report_id)

# 获取对应测试报告的详细测试数据
@app.get("/report/detail_reports/{report_id}")
async def get_detail_reports(report_id:str):
    return m_detail_report.get_detail_report(report_id)

################################################################

# 添加测试环境
@app.post("/test_env")
async def post_test_env(test_env:m_test_env.TestEnv):
    return m_test_env.post_test_env(test_env)


# 获取测试环境
@app.get("/test_envs")
async def get_test_envs():
    return m_test_env.get_test_envs()

# 获取单个测试环境
@app.get("/test_env/{test_env_ip}",response_model=m_test_env.TestEnv)
async def get_test_env(test_env_ip:str):
    return m_test_env.get_test_env(test_env_ip)

# 修改测试环境
@app.put("/test_env")
async def put_test_env(test_env:m_test_env.TestEnv):
    return m_test_env.put_test_env(test_env)

# 删除测试环境
@app.delete("/test_env/{test_env_ip}")
async def delete_test_env(test_env_ip:str):
    return m_test_env.delete_test_env(test_env_ip)


# 获取测试配置
@app.get("/test_set")
async def read_test_set():
    return m_test_set.read_test_set()


# 写入测试配置
@app.put("/test_set")
async def write_test_set(test_set_option:m_test_set.testSetAndOption):
    m_test_set.write_test_set(test_set_option)
    return {"detail":"success"}

########################################################################


# 获取测试日志
@app.get("/test_log/{test_log_ip}")
async def get_test_log(test_log_ip:str):
    return m_test_log.get_test_log(test_log_ip)


if __name__ == "__main__":
    import uvicorn
    # createTestExecutor =  m_create_test_process.Create_TestExecutor() #多进程必须放在在此执行
    uvicorn.run(app, host="127.0.0.1", port=58000)

    # pip install fastapi sqlmodel uvicorn
    # uvicorn main:app