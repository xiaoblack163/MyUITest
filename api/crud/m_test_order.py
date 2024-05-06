import json
from typing import Dict,List,Any,Optional
from pydantic import BaseModel

TEST_ORDER_PATH = "MyUITestDB/test_order.json"

# 测试排序的pydandic模型(用于解析和验证JSON数据的模型)
class Step(BaseModel):
    stepID: str
    stepName: str
    caseID:str
    funcID:str

class Case(BaseModel):
    caseID: str
    caseName: str
    funcID:str
    grandchild: Optional[List[Step]] = None

class Function(BaseModel):
    funcID: str
    funcName: str
    children: Optional[List[Case]] = None

class TestOrderData(BaseModel):
    testOrderData: List[Function]

#读取数据库，format生成test_order.json(排序会丢失,脏数据时使用)
def init_test_order():
    #读取数据库，format生成test_order.json
    try:
        with open (TEST_ORDER_PATH,'r') as f:
            json.load(f)
    except:
        with open (TEST_ORDER_PATH,'w') as f:
            json.dump([],f)

# init_test_order()

# 读取测试排序
def read_test_order():
    with open (TEST_ORDER_PATH,'r',encoding='utf8') as f:
        return json.load(f)

# 更新测试排序
def write_test_order(content):
    # 验证pydantic模型
    TestOrderData(testOrderData=content)
    with open (TEST_ORDER_PATH,'w',encoding='utf8') as f:
        json.dump(content,f,ensure_ascii=False)


######################################################################################

# 读取功能排序
def read_func_order():
    return read_test_order()

# 添加功能排序
def post_func_order(func_ID:str,func_name:str):
    test_orders = read_test_order()
    test_orders.append({"funcID":func_ID,"funcName":func_name,"children":[]})
    write_test_order(test_orders)

# 修改排序功能名
def put_func_order(func_name:str,new_Name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcName"] == func_name:
            test_order["funcName"] = new_Name
            write_test_order(test_orders)
            return
    else:
        raise "修改排序功能名错误,不存在的测试功能"

# 删除功能排序   
def delete_func_order(func_name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcName"] == func_name:
            test_orders.remove(test_order)
            write_test_order(test_orders)
            return
    else:
        raise "删除排序功能错误,不存在的测试功能"

######################################################################################

# 读取用例排序
def read_case_order(func_ID:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            return test_order["children"]
    else:
        raise "获取对应测试功能的测试用例错误,不存在的测试功能"


# 添加用例排序
def post_case_order(func_ID:str,case_id:str,case_name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            test_order["children"].append({"funcID":func_ID,"caseID":case_id,"caseName":case_name,"grandchild":[]})
            write_test_order(test_orders)
            return
    else:
        raise "添加排序用例错误,不存在的测试功能"        
    
# 修改排序用例名
def put_case_order(func_ID:str,case_name:str,new_name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseName"] ==  case_name:
                    case_order["caseName"] = new_name
                    write_test_order(test_orders)
                    return
            else:
                print("修改排序用例名错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"])
                raise "修改排序用例名错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"]
    else:
        raise "修改排序用例名错误,不存在的测试功能"  

            
# 删除排序用例
def delete_case_order(func_ID:str,case_id:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseID"] ==  case_id:
                    test_order["children"].remove(case_order)
                    write_test_order(test_orders)
                    return
            else:
                raise "删除排序用例错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseID"]
    else:
        raise "删除排序用例错误,不存在的测试功能"  


######################################################################################

# 添加步骤排序
def post_step_order(func_ID:str,case_id:str,step_id:str,step_name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseID"] == case_id:
                    case_order["grandchild"].append({"funcID":func_ID,"caseID":case_id,"stepID":step_id,"stepName":step_name})
                    write_test_order(test_orders)
                    return
            else:
                raise "添加排序步骤错误,不存在的测试用例"
    else:
        raise "添加排序步骤错误,不存在的测试功能"        
    
# 修改步骤排序名
def put_step_order(func_ID:str,case_id:str,step_id:str,new_name:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseID"] ==  case_id:
                    for step_order in case_order["grandchild"]:
                        if step_order["stepID"] == step_id:
                            step_order["stepName"] = new_name
                            write_test_order(test_orders)
                            return
                    
                    else:
                        print("修改排序用步骤错误,测试用例:"+case_order["caseID"]+" 中不存在测试步骤:" + step_order["stepName"])
                        raise "修改排序用步骤错误,测试用例:"+case_order["caseID"]+" 中不存在测试步骤:" + step_order["stepName"]
            else:
                print("修改排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试步骤:" + case_order["caseName"])
                raise "修改排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试步骤:" + case_order["caseName"]
    else:
        raise "修改排序步骤名错误,不存在的测试功能"  

            
# 删除排序步骤
def delete_step_order(func_ID:str,case_id:str,step_id:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseID"] ==  case_id:
                    for step_order in case_order["grandchild"]:
                        if step_order["stepID"] == step_id:
                            case_order["grandchild"].remove(step_order)
                            write_test_order(test_orders)
                            return
                    
                    else:
                        print("删除排序用步骤错误,测试用例:"+case_order["caseID"]+" 中不存在测试步骤:" + step_order["stepName"])
                        raise "删除排序用步骤错误,测试用例:"+case_order["caseID"]+" 中不存在测试步骤:" + step_order["stepName"]
            else:
                print("删除排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"])
                raise "删除排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"]
    else:
        raise "删除排序步骤名错误,不存在的测试功能"   

######################################################################################

# 获取用例排序数据
def get_case_order(func_ID:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            return test_order["children"]
    else:
        raise "获取排序用例名错误,不存在的测试功能"  

# 获取步骤排序数据
def get_step_order(func_ID:str,case_id:str):
    test_orders = read_test_order()
    for test_order in test_orders:
        if test_order["funcID"] == func_ID:
            for case_order in test_order["children"]:
                if case_order["caseID"] ==  case_id:
                    return case_order["grandchild"]
            else:
                print("获取排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"])
                raise "获取排序用步骤错误,测试功能:"+test_order["funcID"]+" 中不存在测试用例:" + case_order["caseName"]
    else:
        raise "获取排序步骤名错误,不存在的测试功能"   

 ######################################################################################

def get_run_case_tree_data():
    tree_data = []
    test_orders = read_test_order()
    for test_order in test_orders:
        one_func_tree = {
                            "key": test_order["funcID"],
                            "data": {
                                "name": test_order["funcName"],
                                "id": test_order["funcID"],
                                "type": '测试功能'
                            },
                            "children": []
                        }
        for case_order in test_order["children"]:
            one_func_tree["children"].append({
                                                "key": f'{test_order["funcName"]}<->{test_order["funcID"]}<->{case_order["caseName"]}<->{case_order["caseID"]}',
                                                "data": {
                                                    "name": case_order["caseName"],
                                                    "id": case_order["caseID"],
                                                    "type": '测试用例'
                                                }
                                            })
        tree_data.append(one_func_tree)
    return tree_data

