import {reactive} from "vue";
import stores from "./storee.js"



const Utilss=reactive({
    // 获取各表记录数
    async GetRecordCount(){
        try {
            const response = await fetch(stores.host + '/dash_board/get_record_count', {
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
            const response = await fetch(stores.host + '/dash_board/get_fail_detail_report_record', {
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
            const response = await fetch(stores.host + '/dash_board/get_report_record', {
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
            const response = await fetch(stores.host + '/dash_board/get_report_trend_record', {
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
            const response = await fetch(stores.host + '/dash_board/get_operation_logs', {
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
            const response = await fetch(stores.host + '/func_tests', {
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
        fetch(stores.host + '/func_test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"funcName":funcName,"funcID":crypto.randomUUID()})
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
        fetch(stores.host + '/func_test/'+funcName, {
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
        fetch(stores.host + '/func_test/'+funcName+'/'+newName, {
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
            const response = await fetch(stores.host + '/case_tests', {
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
            const response = await fetch(stores.host + '/case_order/'+func_id, {
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
        fetch(stores.host + '/case_test', {
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
        fetch(stores.host + '/case_test/'+funcID+'/'+caseName+'/'+newName, {
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
        fetch(stores.host + '/case_test/'+funcID+'/'+caseName, {
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
            const response = await fetch(stores.host + '/step_order/'+funcID+"/"+caseID, {
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
            const response = await fetch(stores.host + '/step_data/'+step_id, {
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
    uploadFile(toast,stepID,formData){
        fetch(stores.host+'/step_data/upload_file/' + stepID, {
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
        fetch(stores.host+'/step_data', {
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
        fetch(stores.host+'/step_data/'+stepID, {
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
            const response = await fetch(stores.host + '/init/step_data/locat_option', {
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
            const response = await fetch(stores.host + '/init/step_data/locatOption_actionOption', {
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
            const response = await fetch(stores.host + '/init/step_data/check_action_value', {
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
            const response = await fetch(stores.host + '/init/step_data/check_locat_value', {
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
            const response = await fetch(stores.host + '/init/step_data/yolo_option', {
                method: 'GET',
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.log('error', '获取目标检测选项错误!', error);
        }
    },
    //获取用例总览数据
    async GetCaseView(){
        try {
            const response = await fetch(stores.host + '/case_view', {
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
            const response = await fetch(stores.host + '/test_order', {
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
            const response = await fetch(stores.host + '/run_case', {
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
        fetch(stores.host+'/run_case', {
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
        fetch(stores.host+'/run_case', {
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
            const response = await fetch(stores.host + '/run_case/activity', {
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
            const response = await fetch(stores.host + '/report/reports', {
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
            const response = await fetch(stores.host + '/report/detail_chart/'+reportID, {
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
            const response = await fetch(stores.host + '/report/detail_reports/'+reportID, {
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
            const response = await fetch(stores.host + '/run_case/log', {
                method: 'GET',
            });
            return response.json()
        } catch (error) {
            console.log('error', '请求错误！', error);
        }
    },
})

export default Utilss


