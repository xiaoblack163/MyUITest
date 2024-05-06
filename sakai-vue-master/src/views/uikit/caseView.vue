<script setup>
import { ref, onBeforeMount } from 'vue';
import { inject } from 'vue';
const utilss = inject('utilss');

// const processSteps =  async () => {
    
// };
const customer3 = ref([]);
onBeforeMount(async () => {
    let data = await utilss.GetCaseView();
    customer3.value = data.map(step => {
            // 解析locatMode和action字段
            step.locatMode = JSON.parse(step.locatMode.replace(/'/g, '"')).value;
            step.action = JSON.parse(step.action.replace(/'/g, '"')).value;
            return step;
        });
});

// 随机标签颜色
const getSeverity = () => {
    const items = ["danger", "success", "info","warning","secondary","help","contrast"];
    const randomIndex = Math.floor(Math.random() * items.length);
    return items[randomIndex];
};



</script>

<template>
    <div class="card">
        <h5>用例总览</h5>
        <DataTable :value="customer3" rowGroupMode="subheader" groupRowsBy="caseID" sortMode="single" selectionMode="single" sortField="caseID" :sortOrder="1" scrollable scrollHeight="72vh">
            <Column field="caseID" header="caseID"></Column>
            <Column field="stepName" header="步骤名称" style="min-width: 200px" class="font-bold"></Column>
            <Column field="stepID" header="步骤ID" style="min-width: 400px"></Column>
            <Column field="locatMode" header="定位方式" style="min-width: 200px">
                <template #body="slotProps">
                    <Tag :severity="getSeverity(slotProps.data.locatMode)">{{ slotProps.data.locatMode.toUpperCase() }}</Tag>
                </template>
            </Column>
            <Column field="locatValue" header="定位值" style="min-width: 200px"></Column>
            <Column field="elementNumber" header="元素序号" style="min-width: 200px"></Column>
            <Column field="xyValue" header="绝对坐标" style="min-width: 200px"></Column>
            <Column field="action" header="动作" style="min-width: 200px"></Column>
            <Column field="AssertOrActionValue" header="输入值" style="min-width: 200px"></Column>
            <Column field="stepInfo" header="步骤说明" style="min-width: 200px"></Column>
            <template #groupheader="slotProps">
                <div class="flex align-items-center gap-2 " style="color: #0D8ADB;">
                    <i class="pi pi-th-large" style="height: 1rem; margin-right: 0.5rem"></i>
                    <td style="text-align: right;" class="text-bold pr-6">测试功能: {{ slotProps.data.funcName }}</td>
                    <i class="pi pi-star" style="height: 1rem; margin-right: 0.5rem"></i>
                    <td style="text-align: right" class="text-bold pr-6">测试用例: {{ slotProps.data.caseName }}</td>
                </div>
            </template>
        </DataTable>
    </div>
</template>

