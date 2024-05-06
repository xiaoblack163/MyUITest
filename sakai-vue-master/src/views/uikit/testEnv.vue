
<template>
    <Dialog v-model:visible="visible" modal header="测试配置" :style="{ width: '25rem' }">

        <span class="p-text-secondary block mb-5" >{{ currentCase.name }}</span>
        <div class="flex align-items-center gap-3 mb-3">
            <label for="selectedEnv" class="font-semibold w-6rem">选择环境</label>
            <Dropdown v-model="selectedEnv" :options="envOption" optionLabel="envIP" class="w-full md:w-14rem" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">用户</label>
            <InputText v-model="Tcpreplay"  id="Tcpreplay" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">密码</label>
            <InputText v-model="Tcpreplay"  id="Tcpreplay" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="Tcpreplay" class="font-semibold w-6rem">Tcpreplay</label>
            <InputText v-model="Tcpreplay"  id="Tcpreplay" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
            <Button type="button" label="Save" @click="visible = false;addTcpreplay()"></Button>
        </div>
    </Dialog>
    <div class="card">
        <h5>测试环境</h5>
        <TreeTable :value="treeTableValue">
            <Column field="name" header="名称" :expander="true"></Column>
            <Column field="id" header="ID"></Column>
            <Column field="type" header="类型"></Column>
            <Column header="用例设置" headerStyle="width: 10rem">
                <template #body="slotProps">
                    <div v-tooltip.left="'请选择测试用例'"  class="flex flex-wrap gap-2">
                        <Button :disabled="slotProps.node.data.type !== '测试用例'"  @click="addEnv(slotProps.node.data)" type="button" icon="pi pi-pencil" rounded />
                    </div>
                </template>
            </Column>
            <template #header>
                <div  class="flex justify-content-start">
                    <FloatLabel>
                        <InputText v-model="envIP" class="w-full md:w-14rem" />
                        <label>添加环境IP</label>
                    </FloatLabel>
                    <FloatLabel style="margin-left: 10px" >
                        <InputText v-model="envIP" class="w-full md:w-14rem" />
                        <label>发包环境</label>
                    </FloatLabel>
                    <FloatLabel style="margin-left: 10px" >
                        <InputText v-model="envIP" class="w-full md:w-14rem" />
                        <label>发包环境账户</label>
                    </FloatLabel>
                    <FloatLabel style="margin-left: 10px" >
                        <InputText v-model="envIP" class="w-full md:w-24rem" />
                        <label>发包命令</label>
                    </FloatLabel>
                    <Button style="margin-left: 10px" icon="pi pi-plus" label="添加环境" />
                    <Button style="margin-left: 10px" icon="pi pi-trash" label="删除环境" outlined />
                </div>
            </template>
        </TreeTable>
    </div>
</template>

<script setup>


import { ref, onMounted } from 'vue';

onMounted(() => {});

// 是否弹窗
const visible = ref(null);

// 环境IP
const envIP = ref(null);

// Tcpreplay命令
const Tcpreplay = ref(null);


// 环境选项
const envOption = ref([{ envIP: '10.0.0.200' }, { envIP: '10.0.200.101' }]);


// 当前选择环境
const selectedEnv = ref(null);

// 测试用例树
const treeTableValue = ref([
    {
        key: '测试功能_文件还原',
        data: {
            name: '文件还原',
            id: '2fd17c60-0557-427c-b9a5-55a58895e8ac',
            type: '测试功能'
        },
        children: [
            {
                key: '测试用例_HTTP',
                data: {
                    name: 'HTTP',
                    id: 'ydd17c60-0557-427c-b9a5-55a58895e8ac',
                    type: '测试用例'
                }
            },
            {
                key: '测试用例_FTP',
                data: {
                    name: 'FTP',
                    id: '2fd17c60-0557-427c-b9a5-55a58895e8ac',
                    type: '测试用例'
                }
            }
        ]
    },
    {
        key: '测试功能_全包溯源',
        data: {
            name: '全包溯源',
            id: 'nvd17c60-0557-427c-b9a5-55a58895e8ac',
            type: '测试功能'
        },
        children: [
            {
                key: '测试用例_空条件',
                data: {
                    name: '空条件',
                    id: '3sd17c60-0557-427c-b9a5-55a58895e8ac',
                    type: '测试用例'
                }
            },
            {
                key: '测试用例_有条件',
                data: {
                    name: '有条件',
                    id: 'bdr17c60-0557-427c-b9a5-55a58895e8ac',
                    type: '测试用例'
                }
            }
        ]
    }
]);

//当前选择的测试用例
const currentCase = ref(null)

// 添加测试配置
const addEnv = (data) => {
    console.log('addTcpreplay', data);
    if (data.type !== '测试用例') {
        console.log('请选择测试用例');
        return false;
    }
    currentCase.value = data
    visible.value = true
};

const addTcpreplay = () => {
    if (selectedEnv.value===null || Tcpreplay.value === null || Tcpreplay.value === ''){
        console.log('参数不能为空');
        return false;
    }
    console.log(selectedEnv.value)
    console.log(Tcpreplay.value)
    console.log(currentCase.value)
    // fetch
};



</script>
