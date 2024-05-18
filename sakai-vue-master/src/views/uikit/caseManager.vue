<script setup>
import { ref, onBeforeMount, watch } from 'vue';
import { useConfirm } from 'primevue/useconfirm';
const confirm = useConfirm();
import { inject } from 'vue';
const storee = inject('storee');
const utilss = inject('utilss');

import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast(); // 弹出提示

// #################################################################################

const op2 = ref(); // 弹窗2
const funcNameID = ref(null); // 功能名及code,绑定 功能选择
const selectedFuncs = ref(); // 功能列表
const caselistValue = ref(); // 用例列表

// 弹窗并加载功能列表
const toggle2 = async (event) => {
    // 弹窗
    op2.value.toggle(event);

    //获取功能列表
    selectedFuncs.value = await utilss.GetFuncTest(toast);
};

// 选择功能后加载测试用例
const selectFunc = async (funcNameID2) => {
    if (funcNameID2 === null) {
        //选择相同功能时重置为全部功能(暂时解决报错问题)
        funcNameID2 = { funcName: '全部功能', funcID: '全部功能' };
        funcNameID.value = { funcName: '全部功能', funcID: '全部功能' };
        // 加载所有测试用例
        caselistValue.value = await utilss.GetCaseTests(toast);
    } else {
        // 加载对应功能测试用例
        caselistValue.value = await utilss.GetFuncCaseTest(toast, funcNameID2.funcID);
    }
    op2.value.toggle();
};

// #################################################################################

// crud功能和用例弹窗相关

const FuncID = ref(null); // 功能ID
const showDig = ref(false); //弹窗标题
const ActionDig = ref(null); //crud动作
const modeName = ref(null); //展示名称
const DigInput1 = ref(null); // 输入框1
const DigInput2 = ref(null); // 输入框2

// 测试功能选项
const casefuncs = [
    {
        label: '添加测试用例',
        icon: 'pi pi-plus',
        command: () => {
            if (event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[0] === '全部功能') {
                toast.add({ severity: 'info', summary: '信息', detail: '请选择具体测试功能!', life: 3000 });
                return false;
            }
            // console.log("Update",event.target.getAttribute("id"))
            showDig.value = true;
            modeName.value = '用例';
            ActionDig.value = '添加测试用例';
            FuncID.value = event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[1];
        }
    },
    {
        label: '删除测试用例',
        icon: 'pi pi-trash',
        command: () => {
            if (event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[0] === '全部功能') {
                toast.add({ severity: 'info', summary: '信息', detail: '请选择具体测试功能!', life: 3000 });
                return false;
            }
            showDig.value = true;
            modeName.value = '用例';
            ActionDig.value = '删除测试用例';
            // console.log('删除测试用例', event.target.__vueParentComponent.attrs.id.split('_')[0]);
            FuncID.value = event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[1];
        }
    },
    {
        label: '重命名测试用例',
        icon: 'pi pi-eraser',
        command: () => {
            if (event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[0] === '全部功能') {
                toast.add({ severity: 'info', summary: '信息', detail: '请选择具体测试功能!', life: 3000 });
                return false;
            }
            showDig.value = true;
            modeName.value = '用例';
            ActionDig.value = '重命名测试用例';
            // console.log('重命名用例', event.target.__vueParentComponent.attrs.id.split('_')[0]);
            FuncID.value = event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[1];
        }
    }
];

// crud功能或者用例
const crudFuncOrCase = async () => {
    if (!DigInput1.value) {
        toast.add({ severity: 'info', summary: '信息', detail: '输入值不能为空!', life: 3000 });
        return false;
    }
    switch (ActionDig.value) {
        case '添加测试用例':
            let tmpcaseID = crypto.randomUUID();
            console.log('添加测试用例', FuncID.value, '输入值:', DigInput1.value);
            utilss.PostCaseTest(toast, FuncID.value, DigInput1.value, tmpcaseID);
            // utilss.PostStepOrder(toast,tmpcaseID)
            // 刷新对应功能测试用例
            setTimeout(async () => {
                caselistValue.value = await utilss.GetFuncCaseTest(toast, FuncID.value);
            }, 500);
            break;
        case '删除测试用例':
            console.log('删除测试用例', FuncID.value, '输入值:', DigInput1.value);
            utilss.DeleteCaseTest(toast, FuncID.value, DigInput1.value);
            // 刷新对应功能测试用例
            setTimeout(async () => {
                caselistValue.value = await utilss.GetFuncCaseTest(toast, FuncID.value);
            }, 500);
            break;
        case '重命名测试用例':
            if (!DigInput2.value) {
                toast.add({ severity: 'info', summary: '信息', detail: '输入值不能为空!', life: 3000 });
                console.log('输入值不能为空');
                return false;
            }
            console.log('重命名测试用例', FuncID.value, '输入值1:', DigInput1.value, '输入值2:', DigInput2.value);
            utilss.PutCaseTest(toast, FuncID.value, DigInput1.value, DigInput2.value);
            // 刷新对应功能测试用例
            setTimeout(async () => {
                caselistValue.value = await utilss.GetFuncCaseTest(toast, FuncID.value);
            }, 500);
            break;
        case '新增功能':
            console.log('新增功能', '输入值:', DigInput1.value);
            if (DigInput1.value === '全部功能') {
                toast.add({ severity: 'info', summary: '信息', detail: '无法添加此功能!', life: 3000 });
                return false;
            }
            utilss.PostFuncTest(toast, DigInput1.value);
            break;
        case '删除功能':
            console.log('删除功能', '输入值:', DigInput1.value);
            utilss.DeleteFuncTest(toast, DigInput1.value);
            caselistValue.value = await utilss.GetCaseTests(toast); // 重新获取测试用例数据
            break;
        case '重命名功能':
            if (!DigInput2.value) {
                toast.add({ severity: 'info', summary: '信息', detail: '输入值不能为空!', life: 3000 });
                console.log('输入值不能为空');
                return false;
            }
            console.log('重命名功能', '输入值1:', DigInput1.value, '输入值2:', DigInput2.value);
            utilss.PutFuncTest(toast, DigInput1.value, DigInput2.value);
            break;
    }
};

// 用例用例选项
const saveStepMode = ref(null); // 保存步骤时为post还是put
const stepfuncs = [
    {
        label: '添加测试步骤',
        icon: 'pi pi-plus',
        command: () => {
            stepData.value = {
                stepID: crypto.randomUUID(),
                stepName: '',
                locatMode: '',
                locatValue: '',
                yoloValue:'',
                elementNumber: 1,
                xValue: 0,
                yValue: 0,
                action: '',
                AssertOrActionValue: '',
                preSleep:0,
                stepInfo: '',
                caseID: event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[1],
                caseName: event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[0],
                funcID: event.target.__vueParentComponent.attrs.id.split('_')[0].split('<->')[2]
            };
            saveStepMode.value = 'POST';
            console.log('添加测试步骤', stepData);
        }
    }
];

// #################################################################################

// 步骤数据
const stepData = ref({
    stepID: '',
    stepName: '',
    locatMode: '',
    locatValue: '',
    yoloValue:'',
    elementNumber: 1,
    xValue: 0,
    yValue: 0,
    action: '',
    AssertOrActionValue: '',
    preSleep: 0,
    stepInfo: '',
    caseID: '',
    funcID: ''
});

// 切换定位方式模式,获取步骤时watch不重置操作与断言值
const locatModeChangeMode = ref('');

// 选择定位方式
const locatOption = ref(null);

// 操作与断言
const actionOption = ref(null);

// 定位与操作映射
const locatOption_actionOption = ref('');

// 定位值
const locatMode = ref('');

// 校验定位值
const checkLocatValue = ref('');

// 校验操作值
const checkActionValue = ref('');

// #################################################################################

// 打开步骤列表，获取步骤列表数据
const op = ref();
const selectedSteps = ref([]);
const selecteStepData = ref([]);
const toggle = async (event, funcID, caseID) => {
    op.value.toggle(event);
    selectedSteps.value = await utilss.GetStepOrder(toast, funcID, caseID);
};

// #################################################################################

// 获取步骤数据
const getStepData = async (selecteStepData) => {
    stepData.value = await utilss.GetCaseStepTest(toast, selecteStepData.stepID);
    locatModeChangeMode.value = '获取步骤数据';
    locatMode.value = stepData.value.locatMode;

    saveStepMode.value = 'PUT';
    toast.add({ severity: 'info', summary: '切换步骤', detail: selecteStepData.stepName, life: 3000 });
    op.value.toggle();
    selecteStepData.value = null;
};

// #################################################################################

// 提交步骤数据
const saveData = () => {
    stepData.value.locatMode = locatMode;
    if (stepData.value.stepID === '' || stepData.value.stepID === null) {
        toast.add({ severity: 'error', summary: '错误', detail: '步骤ID不能为空!', life: 3000 });
        return false;
    } else if (stepData.value.caseID === '' || stepData.value.caseID === null) {
        toast.add({ severity: 'error', summary: '错误', detail: '用例ID不能为空!', life: 3000 });
        return false;
    } else if (stepData.value.funcID === '' || stepData.value.funcID === null) {
        toast.add({ severity: 'error', summary: '错误', detail: '功能ID不能为空!', life: 3000 });
        return false;
    } else if (stepData.value.stepName === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '步骤名称不能为空!', life: 3000 });
        return false;
    } else if (stepData.value.locatMode === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '请选择定位方式!', life: 3000 });
        return false;
    } else if (checkLocatValue.value.includes(stepData.value.locatMode.value) && stepData.value.locatValue === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '请输入定位值!', life: 3000 });
        return false;
    } else if (stepData.value.locatMode.value === '目标检测' && stepData.value.yoloValue === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '请选择检测目标!', life: 3000 });
        return false;
    } else if (stepData.value.action === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '请选择操作或者断言!', life: 3000 });
        return false;
    } else if (Object.keys(checkActionValue.value).includes(stepData.value.action.value) && stepData.value.AssertOrActionValue === '') {
        toast.add({ severity: 'warn', summary: '警告', detail: '请输入操作或断言参数!\n' + checkActionValue.value[stepData.value.action.value], life: 3000 });
        return false;
    } else if (stepData.value.locatMode.value === '绝对坐标' && stepData.value.xValue === 0 && stepData.value.xValue === 0) {
        toast.add({ severity: 'warn', summary: '警告', detail: '绝对坐标错误!', life: 3000 });
        return false;
    }
    utilss.PostStepData(toast, saveStepMode.value, stepData.value);
};

// 选择文件时立即上传
const uploadFile = async (event) => {
    if (stepData.value.stepID === '' || stepData.value.stepID === null) {
        toast.add({ severity: 'warn', summary: '警告', detail: '步骤ID不能为空!', life: 3000 });
        return false;
    } else {
        const formData = new FormData();
        formData.append('file', event.files[0]);
        console.log(event.files[0]);
        utilss.uploadFile(toast, stepData.value.stepID, formData);
    }
};

// #################################################################################

// 删除步骤
const DeleteStepData = () => {
    if (stepData.value.stepID === '' || stepData.value.stepID === null) {
        toast.add({ severity: 'warn', summary: '警告', detail: '步骤ID不能为空!', life: 3000 });
        return false;
    } else {
        utilss.DeleteStepData(toast, stepData.value.stepID);
    }
};

const confirm2 = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: '删除步骤?',
        icon: 'pi pi-info-circle',
        rejectClass: 'p-button-secondary p-button-outlined p-button-sm',
        acceptClass: 'p-button-danger p-button-sm',
        rejectLabel: '取消',
        acceptLabel: '确认',
        accept: () => {
            DeleteStepData();
        },
        reject: () => {
            console.log('取消');
        }
    });
};

// #################################################################################

const locatValue_active = ref(false);// 是否禁用请输入定位值选择框
// 目标检测相关
const yolo = ref(false);//当前定位方式是否为目标检测
const yoloOption = ref([]);
// #################################################################################
watch(locatMode, (newValue) => {
    // 只有切换定位方式时清空数据,获取步骤时不清空
    if (locatModeChangeMode.value === '切换定位方式') {
        stepData.value.action = '';
        stepData.value.AssertOrActionValue = '';
        stepData.value.locatValue = '';
        stepData.value.yoloValue = '';
    }
    if (newValue.value === '无需定位') {
        actionOption.value = locatOption_actionOption.value['无需定位'];
        locatValue_active.value = true;
        yolo.value = false;
    } else if (['文本', 'ID', 'XPATH', 'CSS', '自定义'].includes(newValue.value)) {
        actionOption.value = locatOption_actionOption.value['标签定位'];
        locatValue_active.value = false;
        yolo.value = false;
    } else if (newValue.value === '文字识别') {
        actionOption.value = locatOption_actionOption.value['坐标定位'];
        locatValue_active.value = false;
        yolo.value = false;
    } else if (['绝对坐标', '图像识别'].includes(newValue.value)) {
        actionOption.value = locatOption_actionOption.value['坐标定位'];
        locatValue_active.value = true;
        yolo.value = false;
    } else if (newValue.value === '目标检测') {
        actionOption.value = locatOption_actionOption.value['坐标定位'];
        locatValue_active.value = true;
        yolo.value = true;
    } else {
        actionOption.value = '';
        locatValue_active.value = false;
        yolo.value = false;
    }
});

// #################################################################################

onBeforeMount(async () => {
    // 初始化功能
    funcNameID.value = { funcName: '全部功能', funcID: '全部功能' };

    // 初始化测试用例列表
    caselistValue.value = await utilss.GetCaseTests(toast);

    // 初始化定位方式
    locatOption.value = await utilss.initLocation(toast);

    // 初始化操作与断言
    locatOption_actionOption.value = await utilss.initAction(toast);

    // check操作值是否为空
    checkActionValue.value = await utilss.checkActionValue(toast);

    // check定位值是否为空
    checkLocatValue.value = await utilss.checkLocatValue(toast);

    // 获取目标检测选项
    yoloOption.value = await utilss.GetYoloOption()
});
</script>

<template>
    <!-- 删除确认框 -->
    <ConfirmPopup></ConfirmPopup>
    <!-- 功能与用例crud弹窗 -->
    <Dialog v-model:visible="showDig" modal :header="ActionDig" :style="{ width: '25rem' }">
        <div class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ modeName }}名</label>
            <InputText v-model="DigInput1" class="flex-auto" autocomplete="off" />
        </div>
        <div v-if="ActionDig === '重命名测试用例' || ActionDig === '重命名功能'" class="flex align-items-center gap-3 mb-5">
            <label class="font-semibold w-6rem">新{{ modeName }}名</label>
            <InputText v-model="DigInput2" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button
                type="button"
                label="确认"
                @click="
                    crudFuncOrCase();
                    showDig = false;
                "
            ></Button>
        </div>
    </Dialog>

    <!-- 步骤弹窗 -->
    <OverlayPanel ref="op">
        <Listbox v-model="selecteStepData" @change="getStepData(selecteStepData)" filter :options="selectedSteps" optionLabel="stepName" class="w-full md:w-14rem" />
    </OverlayPanel>

    <!-- 选择功能弹窗 -->
    <OverlayPanel ref="op2">
        <Listbox v-model="funcNameID" @change="selectFunc(funcNameID)" filter :options="selectedFuncs" optionLabel="funcName" class="w-full md:w-14rem" />
    </OverlayPanel>

    <div class="grid">
        <div class="col-12 md:col-3">
            <div class="card p-fluid">
                <h5>测试功能列表</h5>
                <div class="field">
                    <ButtonGroup>
                        <Button
                            @click="
                                showDig = true;
                                ActionDig = '新增功能';
                                modeName = '功能';
                            "
                            text
                            icon="pi pi-plus"
                        />
                        <Button
                            @click="
                                showDig = true;
                                ActionDig = '删除功能';
                                modeName = '功能';
                            "
                            text
                            icon="pi pi-trash"
                        />
                        <Button
                            @click="
                                showDig = true;
                                ActionDig = '重命名功能';
                                modeName = '功能';
                            "
                            text
                            icon="pi pi-eraser"
                        />
                    </ButtonGroup>
                </div>
                <div class="field">
                    <SplitButton :model="casefuncs" @click="toggle2($event)" :key="funcNameID.funcID" :id="funcNameID.funcName + '<->' + funcNameID.funcID">
                        <span class="flex align-items-center font-bold">
                            <i class="pi pi-th-large" style="height: 1rem; margin-right: 0.5rem"></i>
                            <span>{{ funcNameID.funcName }}</span>
                        </span>
                    </SplitButton>
                </div>
            </div>
            <div class="card p-fluid">
                <h5>测试用例列表</h5>
                <div v-for="item in caselistValue" :key="item.caseID" :id="item.caseName + '<->' + item.caseID + '<->' + item.funcID" class="field">
                    <SplitButton :model="stepfuncs" @click="toggle($event, item.funcID, item.caseID)" :key="item.caseID" :id="item.caseName + '<->' + item.caseID + '<->' + item.funcID">
                        <span class="flex align-items-center font-bold">
                            <i class="pi pi-star" style="height: 1rem; margin-right: 0.5rem"></i>
                            <span>{{ item.caseName }}</span>
                        </span>
                    </SplitButton>
                </div>
            </div>
        </div>

        <div class="col-12 md:col-9">
            <div class="card p-fluid">
                <h5>步骤编号与名称</h5>
                <p class="text-color-secondary block mb-5">请输入步骤编号与名称.</p>
                <div class="formgrid grid">
                    <div class="field col-12 md:col-4">
                        <InputText disabled v-model="stepData.stepID" id="lastname1" style="width: 100%" type="text" placeholder="请输入步骤编号" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <InputText id="lastname1" v-model="stepData.stepName" style="width: 100%" type="text" placeholder="请输入步骤名称" />
                    </div>
                    <div class="field col-12 md:col-2">
                        <Button label="保存" @click="saveData" />
                    </div>
                    <div class="field col-12 md:col-2">
                        <Button @click="confirm2($event)" label="删除" outlined></Button>
                    </div>
                </div>
            </div>

            <div class="card p-fluid">
                <h5>定位方式与定位值</h5>
                <p class="text-color-secondary block mb-5">请选择定位方式并填写定位值.</p>
                <div class="formgrid grid">
                    <div class="field col-12 md:col-5">
                        <CascadeSelect
                            @change="locatModeChangeMode = '切换定位方式'"
                            v-model="locatMode"
                            :options="locatOption"
                            style="width: 100%"
                            optionLabel="value"
                            optionGroupLabel="value"
                            :optionGroupChildren="['states']"
                            placeholder="请选择定位方式"
                        />
                    </div>
                    <div v-if="!yolo" class="field col-12 md:col-5">
                        <InputText :disabled="locatValue_active" id="lastname1" v-model="stepData.locatValue" style="width: 100%" type="text" placeholder="请输入定位值" />
                    </div>
                    <div v-if="yolo" class="field col-12 md:col-5">
                        <Dropdown v-model="stepData.yoloValue" :options="yoloOption" placeholder="请选择检测目标">
                            <template #value="slotProps">
                                <div v-if="slotProps.value" class="flex align-items-center">
                                    <Image alt="Image" preview>
                                        <template #image>
                                            <img :src="storee.host+'/yoloImages/'+slotProps.value+'.jpg'" alt="" width="18" />
                                        </template>
                                        <template #preview>
                                            <img :src="storee.host+'/yoloImages/'+slotProps.value+'.jpg'" alt="" width="500"/>
                                        </template>
                                    </Image>
                                    <div>{{ slotProps.value }}</div>
                                </div>
                                <span v-else>
                                    {{ slotProps.placeholder }}
                                </span>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <img alt="" :src="storee.host+'/yoloImages/'+slotProps.option+'.jpg'"  style="width: 18px" />
                                    <div>{{ slotProps.option }}</div>
                                </div>
                            </template>
                        </Dropdown>
                    </div>
                    <div class="field col-12 md:col-2">
                        <InputNumber v-model="stepData.elementNumber" inputId="minmax-buttons" placeholder="元素序号" mode="decimal" showButtons :min="1" :max="100" />
                    </div>
                </div>
            </div>

            <div class="card p-fluid">
                <h5>操作与断言</h5>
                <p class="text-color-secondary block mb-5">请输入操作与断言.</p>
                <div class="formgrid grid">
                    <div class="field col-12  md:col-5">
                        <CascadeSelect v-model="stepData.action" :options="actionOption" style="width: 100%" optionLabel="value" optionGroupLabel="value" :optionGroupChildren="['states']" placeholder="请选择操作与断言" />
                    </div>
                    <div class="field col-12  md:col-5">
                        <InputText id="lastname1" v-model="stepData.AssertOrActionValue" style="width: 100%" type="text" placeholder="请输入操作或断言参数" />
                    </div>
                    <div class="field col-12  md:col-2">
                        <InputNumber v-model="stepData.preSleep" inputId="minmax-buttons" placeholder="执行前置等待" mode="decimal" showButtons :min="0" :max="100" />
                    </div>
                </div>
            </div>

            <div class="card p-fluid">
                <div class="formgrid grid">
                    <div class="col-12 md:col-6">
                        <div class="card p-fluid">
                            <h5>绝对坐标</h5>
                            <div class="formgrid grid">
                                <div class="field col">
                                    <p class="text-color-secondary block mb-5">请输入绝对定位坐标.</p>

                                    <div class="formgrid grid">
                                        <div class="field col">
                                            <InputNumber v-model="stepData.xValue" placeholder="请输入x坐标" :min="-1920" :max="1920" />
                                        </div>
                                        <div class="field col">
                                            <InputNumber v-model="stepData.yValue" placeholder="请输入y坐标" :min="-1080" :max="1080" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 md:col-6">
                        <div class="card p-fluid">
                            <h5>上传定位图片</h5>
                            <FileUpload name="demo[]" :showCancelButton="false" :showUploadButton="false" :fileLimit="1" @select="uploadFile($event)" accept="image/*" :maxFileSize="1000000" customUpload />
                            <!-- <FileUpload  name="demo[]" :multiple="false" accept="image/*" :maxFileSize="1000000" customUpload /> -->
                        </div>
                    </div>
                </div>
            </div>
            <div class="card p-fluid">
                <h5>步骤说明</h5>
                <p class="text-color-secondary block mb-5">请输入步骤说明.</p>
                <Textarea v-model="stepData.stepInfo" id="address" rows="4" />
            </div>
        </div>
    </div>
</template>




