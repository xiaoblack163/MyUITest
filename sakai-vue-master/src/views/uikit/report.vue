<script setup>
import { ref, onBeforeMount } from 'vue';
import LogView from "./logView.vue";
import route from "@/router";
import { inject } from 'vue';
const utilss = inject('utilss');

const customer1 = ref([
       {
          "id":1000,
          "version":"888",
          "testor":"Benton, John B Jr",
          "date":"2015-09-13",
          "funcNames":["proposal","James"],
          "result":true,
          "activity":17
       },
       {
          "id":1001,
          "version":"888",
          "testor":"Chanay, Jeffrey A Esq",
          "date":"2019-02-09",
          "funcNames":["proposal","James"],
          "result":true,
          "activity":0
       }
]);

const reports = ref();

// 随机标签颜色
const getSeverity = () => {
    const items = ["danger", "success", "info","warning","secondary","help","contrast"];
    const randomIndex = Math.floor(Math.random() * items.length);
    return items[randomIndex];
};

// 跳转至详细报告界面
const toDetailReport = (reportID) => {
    localStorage.setItem("reportID",reportID)
    route.push('/uikit/detailReport')
}

////////////////////////////////////////////////////////////////////////////////////////////////
const visibleBottom = ref(false);
const test_log_id = ref("")
////////////////////////////////////////////////////////////////////////////////////////////////


onBeforeMount(async () => {
    reports.value = await utilss.GetReports()
    console.log("reports",reports.value)
    console.log("customer1",customer1.value)
});
</script>

<template>
    <Sidebar v-model:visible="visibleBottom"  position="bottom" style="height: auto">
        <LogView :logMode="test_log_id"/>
    </Sidebar>
    <div class="card">
        <h5>测试报告</h5>
        <DataTable :value="reports" :paginator="true" :rows="10" dataKey="id" :rowHover="true" showGridlines scrollable>
            <Column header="测试环境" field="testEnv" style="min-width: 7rem"></Column>
            <Column header="测试版本" field="version" style="min-width: 7rem"></Column>
            <Column header="测试人" field="testor" style="min-width: 7rem"> </Column>
            <Column header="测试时间" field="testDate" style="min-width: 15rem"></Column>
            <Column header="测试功能" field="testFuncs"  style="min-width: 32rem">
                <template #body="{ data }">
                    <Tag v-for="(testFunc,i) in data.testFuncs" :key="i" style="margin-right: 2px;" :severity="getSeverity()">{{ testFunc }}</Tag>
                </template>
            </Column>
            <Column field="activity" header="执行进度" style="min-width: 12rem">
                <template #body="{ data }">
                    <ProgressBar :value="data.activity" :showValue="false" style="height: 0.5rem"></ProgressBar>
                </template>
            </Column>
            <Column field="result" header="测试结果" dataType="boolean" bodyClass="text-center" style="min-width: 8rem">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'text-green-500 pi-check-circle': data.result, 'text-pink-500 pi-times-circle': !data.result }"></i>
                </template>
            </Column>
            <Column headerStyle="width: 10rem; text-align: center" frozen alignFrozen="right" bodyStyle="text-align: center; overflow: visible">
                <template #body="{ data }">
                    <Button @click="toDetailReport(data.reportID)" type="button" icon="pi pi-star" rounded />
                    <Button style="margin-left: 1rem;" @click="visibleBottom = true;test_log_id = data.reportID"  type="button" icon="pi pi-align-left" rounded />
                </template>
            </Column>
        </DataTable>
    </div>
</template>


