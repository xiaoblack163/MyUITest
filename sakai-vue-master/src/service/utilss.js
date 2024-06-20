import {reactive} from "vue";
import storee from "./storee.js"
import { v4 as uuidv4 } from 'uuid';


const Utilss=reactive({
    // 获取各表记录数
    async GetRecordCount(){
        try {
            const response = await fetch(storee.host + '/dash_board/get_record_count', {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取近期FAIL测试
    async GetFailDetailReportRecord(){
        try {
            const response = await fetch(storee.host + '/dash_board/get_fail_detail_report_record', {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取近期测试报告
    async GetReportRecord(){
        try {
            const response = await fetch(storee.host + '/dash_board/get_report_record', {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 获取近期测试趋势图
    async GetReportTrendRecord(){
        try {
            const response = await fetch(storee.host + '/dash_board/get_report_trend_record', {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 获取5条操作记录
    async GetOperationLogs(){
        try {
            const response = await fetch(storee.host + '/dash_board/get_operation_logs', {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取功能列表
    async GetFuncTest(toast){
        try {
            const response = await fetch(storee.host + '/func_tests', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '获取功能列表错误!', life: 3000 });
            console.log('error', '获取功能列表错误', error);
        }
    },
    // 新增测试功能
    PostFuncTest(toast,funcName){
        fetch(storee.host + '/func_test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"funcName":funcName,"funcID":uuidv4()})
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '添加测试功能', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '添加测试功能', detail: '无法添加此功能!', life: 3000 });
            });
    },
    // 删除测试功能
    DeleteFuncTest(toast,funcName){
        fetch(storee.host + '/func_test/'+funcName, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '删除测试功能', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除测试功能', detail: '无法删除此功能!', life: 3000 });
            });
    },
    // 重命名测试功能
    PutFuncTest(toast,funcName,newName){
        fetch(storee.host + '/func_test/'+funcName+'/'+newName, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '重命名测试功能', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '重命名测试功能', detail: '无法重命名此功能!', life: 3000 });
            });
    },
    //获取所有测试用例
    async GetCaseTests(toast){
        try {
            const response = await fetch(storee.host + '/case_tests', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '获取测试用例错误!', life: 3000 });
            console.log('error', '获取测试用例错误', error);
        }
    },
    //获取对应测试功能的测试用例排序数据
    async GetFuncCaseTest(toast,func_id){
        try {
            const response = await fetch(storee.host + '/case_order/'+func_id, {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '获取 '+func_name+' 测试用例错误!', life: 3000 });
            console.log('error', '获取 '+func_name+' 测试用例错误!', error);
        }
    },
    // 新增测试用例
    PostCaseTest(toast,funcID,caseName,caseID){
        fetch(storee.host + '/case_test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"funcID":funcID,"caseName":caseName,"caseID":caseID})
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '添加测试用例', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '添加测试用例', detail: '无法添加此用例!', life: 3000 });
            });
    },
    // 重命名测试用例
    PutCaseTest(toast,funcID,caseName,newName){
        fetch(storee.host + '/case_test/'+funcID+'/'+caseName+'/'+newName, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '重命名测试用例', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '重命名测试用例', detail: '无法重命名此用例!', life: 3000 });
            });
    },
    // 删除测试用例
    DeleteCaseTest(toast,funcID,caseName){
        fetch(storee.host + '/case_test/'+funcID+'/'+caseName, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '删除测试用例', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除测试用例', detail: '无法删除此用例!', life: 3000 });
            });
    },
    //获取对应测试用例的测试步骤排序数据
    async GetStepOrder(toast,funcID,caseID){
        try {
            const response = await fetch(storee.host + '/step_order/'+funcID+"/"+caseID, {
                method: 'GET',
            });
            const data = await response.json();
            return data
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '获取测试步骤排序数据!', life: 3000 });
            console.log('error', '获取测试步骤排序数据!', error);
        }
    },
    //获取单个测试步骤数据
    async GetCaseStepTest(toast,step_id){
        try {
            const response = await fetch(storee.host + '/step_data/'+step_id, {
                method: 'GET',
            });
            const stepdata = await response.json();
            stepdata.locatMode = JSON.parse(stepdata.locatMode.replace(/'/g, '"'));
            stepdata.action = JSON.parse(stepdata.action.replace(/'/g, '"'));
            return stepdata;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '获取测试步骤错误!', life: 3000 });
            console.log('error', '获取测试步骤错误!', error);
        }
    },
    // 上传定位图像
    uploadStepImg(toast,stepID,formData){
        fetch(storee.host+'/step_data/upload_img/' + stepID, {
            method: 'POST',
            body: formData
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '上传图片', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                toast.add({ severity: 'error', summary: '上传图片', detail: "错误", life: 3000 });
                console.log('error', '请求错误！', error);
            });
    },
    // 提交步骤数据
    PostStepData(toast,saveStepMode,stepData){
        fetch(storee.host+'/step_data', {
            method: saveStepMode,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stepData)
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '提交步骤数据', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '提交步骤数据', detail: "错误", life: 3000 });
            });
    },
    // 删除步骤数据
    DeleteStepData(toast,stepID){
        fetch(storee.host+'/step_data/'+stepID, {
            method: 'DELETE',
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '删除步骤数据', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除步骤数据', detail: "错误", life: 3000 });
            });
    },
    // 初始化定位方式
    async initLocation(toast){
        try {
            const response = await fetch(storee.host + '/init/step_data/locat_option', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '初始化定位方式错误!', life: 3000 });
            console.log('error', '初始化定位方式错误！', error);
        }
    },
    // 初始化定位与动作映射
    async initAction(toast){
        try {
            const response = await fetch(storee.host + '/init/step_data/locatOption_actionOption', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '初始化动作错误!', life: 3000 });
            console.log('error', '初始化动作错误', error);
        }
    },
    // check操作值是否为空
    async checkActionValue(toast){
        try {
            const response = await fetch(storee.host + '/init/step_data/check_action_value', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '初始化校验动作!', life: 3000 });
            console.log('error', '初始化动作错误', error);
        }
    },
    // check定位值是否为空
    async checkLocatValue(toast){
        try {
            const response = await fetch(storee.host + '/init/step_data/check_locat_value', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            toast.add({ severity: 'error', summary: '错误', detail: '初始化校验定位!', life: 3000 });
            console.log('error', '初始化动作错误', error);
        }
    },
    //获取目标检测选项
    async GetYoloOption(){
        try {
            const response = await fetch(storee.host + '/init/step_data/yolo_option', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取目标检测选项错误!', error);
        }
    },
    //获取键盘按键选项
    async GetKeyOption(){
        try {
            const response = await fetch(storee.host + '/init/step_data/key_option', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取键盘按键选项错误!', error);
        }
    },
    //获取用例总览数据
    async GetCaseView(){
        try {
            const response = await fetch(storee.host + '/case_view', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取用例总览数据!', error);
        }
    },
    //获取管理执行顺序数据
    async GetTestOrder(){
        try {
            const response = await fetch(storee.host + '/test_order', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取管理执行顺序数据!', error);
        }
    },
    //获取执行测试界面树形排序数据
    async GetRunCaseTreeData(){
        try {
            const response = await fetch(storee.host + '/run_case', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取执行测试界面树形排序数据!', error);
        }
    },
    // 提交测试执行数据
    PostRunTestData(toast,runTestData){
        fetch(storee.host+'/run_case', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(runTestData)
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                if (data.detail[0].msg){
                    toast.add({ severity: 'warn', summary: '提交测试执行数据', detail: data.detail[0].msg, life: 6000 });
                    return 
                }
                toast.add({ severity: 'info', summary: '提交测试执行数据', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '提交测试执行数据', detail: "错误", life: 3000 });
            });
    },
    // 提交测试执行数据
    StopRunTest(toast){
        fetch(storee.host+'/run_case', {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '停止测试', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '停止测试', detail: "错误", life: 3000 });
            });
    },
    //获取执行测试过程进度数据
    async GetCaseActivity(toast){
        try {
            const response = await fetch(storee.host + '/run_case/activity', {
                method: 'GET',
            });
            const data = await response.json();
            if (data.run_status===true){
                toast.add({ severity: 'info', summary: '测试执行中..', detail: "请勿最小化或者关闭测试浏览器\n可置顶其他应用窗口",life: 6000 });
            }else{
                toast.add({ severity: 'info', summary: '暂无测试任务执行', detail: "",life: 3000 });
            }
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取所有测试报告数据
    async GetReports(){
        try {
            const response = await fetch(storee.host + '/report/reports', {
                method: 'GET',
            });
            const data = await response.json();
            for(let i=0;i<data.length;i++){
                data[i].testFuncs = JSON.parse(data[i].testFuncs)
            }
            return data;
        } catch (error) {
            console.log('error', '获取所有测试报告数据!', error);
        }
    },
    //获取单个详细测试报告图表数据
    async GetDetaiChart(reportID){
        try {
            const response = await fetch(storee.host + '/report/detail_chart/'+reportID, {
                method: 'GET',
            });
            const data = await response.json();
            data.passNumber = JSON.parse(data.passNumber.replace(/'/g, '"'))
            data.failNumber = JSON.parse(data.failNumber.replace(/'/g, '"'))
            data.activity = JSON.parse(data.activity.replace(/'/g, '"'))
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取对应测试报告的详细测试数据
    async GetDetaiReports(reportID){
        try {
            const response = await fetch(storee.host + '/report/detail_reports/'+reportID, {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data)
            return data
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取对执行日志
    async GetRunLog(){
        try {
            const response = await fetch(storee.host + '/run_case/log', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取所有测试环境数据
    async GetTestEnvs(){
        try {
            const response = await fetch(storee.host + '/test_envs', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取单个测试环境数据（未使用）
    async GetTestEnv(testEnvIP){
        try {
            const response = await fetch(storee.host + '/test_env/'+ testEnvIP, {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 提交测试执行数据
    PostTestEnv(toast,testEnvData){
        fetch(storee.host+'/test_env', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(testEnvData)
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '提交测试环境数据', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '提交测试环境数据', detail: "错误", life: 3000 });
            });
    },
    // 修改测试执行数据
    PutTestEnv(toast,testEnvData){
        fetch(storee.host+'/test_env', {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(testEnvData)
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '修改测试环境数据', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '修改测试环境数据', detail: "错误", life: 3000 });
            });
    },
    // 删除测试环境数据
    DeleteTestEnv(toast,testEnvIP){
        console.log("啊啊啊",testEnvIP)
        fetch(storee.host+'/test_env/'+testEnvIP, {
            method: "DELETE",
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '删除测试环境', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除测试环境', detail: "错误", life: 3000 });
            });
    },
    //获取测试配置
    async GetTestSet(){
        try {
            const response = await fetch(storee.host + '/test_set', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 修改测试设置数据
    PutTestSet(toast,testSetData){
        fetch(storee.host+'/test_set', {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(testSetData)
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '更新测试配置', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '更新测试配置', detail: "错误", life: 3000 });
            });
    },
    //获取测试配置
    async GetTestLog(test_log_id){
        try {
            const response = await fetch(storee.host + '/test_log/'+test_log_id, {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取测试文档列表
    async GetExcelDatas(){
        try {
            const response = await fetch(storee.host + '/test_excels', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    //获取测试文档
    async GetExcelData(excelID){
        try {
            const response = await fetch(storee.host + '/test_excel/' + excelID, {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 添加测试文档
    PostExcelData(toast,ExcelData){
        fetch(storee.host+'/test_excel', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ExcelData)
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '添加测试文档', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '添加测试文档', detail: "错误", life: 3000 });
            });
    },
    // 修改测试文档
    PutExcelData(toast,ExcelData){
        fetch(storee.host+'/test_excel', {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ExcelData)
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '修改测试文档', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '修改测试文档', detail: "错误", life: 3000 });
            });
    },
    // 删除测试文档
    DeleteExcelData(toast,ExcelID){
        fetch(storee.host+'/test_excel/'+ExcelID, {
            method: "DELETE",
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '删除测试文档', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除测试文档', detail: "错误", life: 3000 });
            });
    },
    // 上传测试附件
    uploadTestFile(toast,formData){
        fetch(storee.host+'/test_file', {
            method: 'POST',
            body: formData
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                toast.add({ severity: 'info', summary: '上传附件', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                toast.add({ severity: 'error', summary: '上传附件', detail: "错误", life: 3000 });
                console.log('error', '请求错误！', error);
            });
    },
    //获取测试附件列表
    async GetTestFiles(){
        try {
            const response = await fetch(storee.host + '/test_file', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
    // 删除测试附件
    DeleteTestFile(toast,fileID){
        fetch(storee.host+'/test_file/'+fileID, {
            method: "DELETE",
        })
            .then((response) => response.json())
            .then((data) => {
                toast.add({ severity: 'info', summary: '删除测试附件', detail: data.detail, life: 3000 });
            })
            .catch((error) => {
                console.log('error', '请求错误！', error);
                toast.add({ severity: 'error', summary: '删除测试附件', detail: "错误", life: 3000 });
            });
    },
})

export default Utilss


