
<template>
    <!-- 删除确认框 -->
    <ConfirmPopup></ConfirmPopup>
    <Dialog v-model:visible="visible" modal header="环境配置" :style="{ width: '25rem' }">
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">测试环境</label>
            <InputText disabled v-model="testEnvData.testEnvIP" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">发包环境</label>
            <InputText v-model="testEnvData.sendFlowHostName" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">用户</label>
            <InputText v-model="testEnvData.sendFlowUserName" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">密码</label>
            <InputText v-model="testEnvData.sendFlowPassWord" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
            <Button
                type="button"
                label="Save"
                @click="
                    visible = false;
                    editEnv();
                "
            ></Button>
        </div>
    </Dialog>
    <div class="card">
        <h5>测试环境</h5>
        <div class="flex justify-content-start">
            <Dropdown v-model="selectedEnv" editable :options="EnvOption" optionLabel="testEnvIP" placeholder="请选择测试环境" class="w-full md:w-14rem" />
            <Button @click="addEnv" style="margin-left: 10px" icon="pi pi-plus" label="添加环境" />
            <Button @click="openEditEnv" style="margin-left: 10px" icon="pi pi-plus" label="编辑发包环境" />
            <Button @click="confirm2($event)" style="margin-left: 10px" icon="pi pi-trash" label="删除环境" outlined />
        </div>
    </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import { useConfirm } from 'primevue/useconfirm';
const confirm = useConfirm();
import { inject } from 'vue';
const utilss = inject('utilss');
import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast(); // 弹出提示
import { v4 as uuidv4 } from 'uuid';
// 当前选择的测试环境
const selectedEnv = ref('');

// 测试环境选项
const EnvOption = ref();

// 是否弹窗
const visible = ref(null);

// 测试环境数据结构
const testEnvData = ref({
    testEnvID: '',
    testEnvIP: '',
    sendFlowHostName: '',
    sendFlowUserName: '',
    sendFlowPassWord: '',
});

// 添加测试环境
const addEnv = () => {
    console.log(selectedEnv.value);
    if (selectedEnv.value == '') {
        toast.add({ severity: 'info', summary: '信息', detail: '测试环境不能为空!', life: 3000 });
        return false;
    }
    if (selectedEnv.value.testEnvIP === undefined) {
        testEnvData.value = {
            testEnvID: uuidv4(),
            // testEnvID: crypto.randomUUID(),
            testEnvIP: selectedEnv.value,
            sendFlowHostName: '',
            sendFlowUserName: '',
            sendFlowPassWord: '',
        };
        // console.log(testEnvData.value)
        utilss.PostTestEnv(toast, testEnvData.value);
    } else {
        toast.add({ severity: 'info', summary: '信息', detail: '环境已存在!', life: 3000 });
        return false;
    }
};


// 删除测试环境
const deleteEnv = () => {
    if (selectedEnv.value === ''){
        return false;
    }
    else if (selectedEnv.value.testEnvIP === undefined) {
        utilss.DeleteTestEnv( toast,selectedEnv.value);
    } else {
        utilss.DeleteTestEnv(toast, selectedEnv.value.testEnvIP);
    }
};

const confirm2 = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: '删除环境?',
        icon: 'pi pi-info-circle',
        rejectClass: 'p-button-secondary p-button-outlined p-button-sm',
        acceptClass: 'p-button-danger p-button-sm',
        rejectLabel: '取消',
        acceptLabel: '确认',
        accept: () => {
            deleteEnv();
        },
        reject: () => {
            console.log('取消');
        }
    });
};

// 编辑测试弹窗
const openEditEnv = async () => {
    testEnvData.value = selectedEnv.value;
    visible.value = true;
};

// 编辑测试环境
const editEnv = () => {
    if (
        testEnvData.value.testEnv === '' ||
        testEnvData.value.testEnvID === '' ||
        testEnvData.value.sendFlowHostName === '' ||
        testEnvData.value.sendFlowUserName === '' ||
        testEnvData.value.sendFlowPassWord === ''
    ) {
        toast.add({ severity: 'info', summary: '信息', detail: '参数不能为空!', life: 3000 });
        return false;
    }
    utilss.PutTestEnv(toast, testEnvData.value);
};

onBeforeMount(async () => {
    EnvOption.value = await utilss.GetTestEnvs();
});
</script>
