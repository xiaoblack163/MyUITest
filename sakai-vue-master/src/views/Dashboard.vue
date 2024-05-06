<script setup>
import { onBeforeMount, ref, watch } from 'vue';
import route from "@/router";
import { useLayout } from '@/layout/composables/layout';
import { inject } from 'vue';
const utilss = inject('utilss');
const storee = inject('storee');

const { isDarkTheme } = useLayout();

const FailDetailReportRecord = ref(null);
const RecordCount = ref({
    funcTest: 0,
    caseTest: 0,
    stepData: 0,
    report: 0
});
const ReportTrendRecord = ref({
    testDateList: [],
    passList: [],
    failList: []
});
const ReportRecord = ref();
const lineData = ref();

const OperationLog = ref([])


const setChartData = (testDateList, passList, failList) => {
    return {
        labels: testDateList,
        datasets: [
            {
                label: 'PASS',
                data: passList,
                fill: false,
                backgroundColor: '#00bb7e',
                borderColor: '#00bb7e',
                tension: 0.4
            },
            {
                label: 'FAIL',
                data: failList,
                fill: false,
                backgroundColor: '#FF8780',
                borderColor: '#FF8780',
                tension: 0.4
            }
        ]
    };
};


const lineOptions = ref(null);



const applyLightTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#495057'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            },
            y: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            }
        }
    };
};

const applyDarkTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#ebedef'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            },
            y: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            }
        }
    };
};

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);

// 跳转至详细报告界面
const toDetailReport = (reportID) => {
    console.log("saasd撒旦",reportID)
    localStorage.setItem("reportID",reportID)
    route.push('/uikit/detailReport')
}



onBeforeMount(async () => {
    FailDetailReportRecord.value = await utilss.GetFailDetailReportRecord();
    RecordCount.value = await utilss.GetRecordCount();
    ReportRecord.value = await utilss.GetReportRecord();
    ReportTrendRecord.value = await utilss.GetReportTrendRecord();
    lineData.value = setChartData(ReportTrendRecord.value.testDateList, ReportTrendRecord.value.passList, ReportTrendRecord.value.failList);
    OperationLog.value = await utilss.GetOperationLogs();
});
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-6 xl:col-3">
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">总功能数</span>
                        <div class="text-900 font-medium text-xl">{{ RecordCount.funcTest }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-th-large text-blue-500 text-xl"></i>
                    </div>
                </div>
                <span class="text-500">Recently New </span>
                <span class="text-green-500 font-medium"> 0 Record </span>
            </div>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">总用例数</span>
                        <div class="text-900 font-medium text-xl">{{ RecordCount.caseTest }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi  pi-star text-orange-500 text-xl"></i>
                    </div>
                </div>
                <span class="text-500">Recently New </span>
                <span class="text-green-500 font-medium"> 0 Record </span>
            </div>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">总步骤数</span>
                        <div class="text-900 font-medium text-xl">{{ RecordCount.stepData }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-cyan-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-inbox text-cyan-500 text-xl"></i>
                    </div>
                </div>
                <span class="text-500">Recently New </span>
                <span class="text-green-500 font-medium"> 0 Record </span>
            </div>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">测试报告数</span>
                        <div class="text-900 font-medium text-xl">{{ RecordCount.report }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-purple-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-calendar text-purple-500 text-xl"></i>
                    </div>
                </div>
                <span class="text-500">Recently New </span>
                <span class="text-green-500 font-medium"> 0 Record </span>
            </div>
        </div>

        <div class="col-12 xl:col-6">
            <div class="card">
                <h5>近期FAIL测试</h5>
                <DataTable :value="FailDetailReportRecord" :rows="5" :paginator="true" responsiveLayout="scroll">
                    <Column style="width: 15%">
                        <template #header>截图</template>
                        <template #body="slotProps">
                            <Image preview :src="storee.host + '/screenshot/' + slotProps.data.detailReportID + '.png'" alt="1" width="50" class="shadow-2" />
                        </template>
                    </Column>
                    <Column field="stepName" header="步骤名称" style="width: 50%"></Column>
                    <Column field="result" header="结果" style="width: 15%">
                        <template #body="{ data }">
                            <i class="pi" :class="{ 'text-green-500 pi-check-circle': data.result, 'text-pink-500 pi-times-circle': !data.result }"></i>
                        </template>
                    </Column>
                    <Column style="width: 10%">
                        <template #header>View</template>
                        <template #body="{ data }">
                            <Button @click="toDetailReport(data.reportID)"  icon="pi pi-search" type="button" class="p-button-text"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
            <div class="card">
                <div class="flex justify-content-between align-items-center mb-5">
                    <h5>近期测试报告</h5>
                </div>
                <DataTable :value="ReportRecord"  :rows="10" dataKey="id" :rowHover="true" size="large" >
                    <Column header="版本" field="version" style="width: 20%"></Column>
                    <Column header="测试时间" field="testDate"  style="width: 40%"></Column>
                    <Column field="result" header="结果" dataType="boolean" style="width: 15%">
                        <template #body="{ data }">
                            <i class="pi" :class="{ 'text-green-500 pi-check-circle': data.result, 'text-pink-500 pi-times-circle': !data.result }"></i>
                        </template>
                    </Column>
                    <Column field="activity" header="执行进度"  style="width: 25%">
                        <template #body="{ data }">
                            <ProgressBar :value="data.activity" :showValue="false" style="height: 0.5rem"></ProgressBar>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
        <div class="col-12 xl:col-6">
            <div class="card">
                <h5>近期测试趋势图</h5>
                <Chart type="line" :data="lineData" :options="lineOptions" />
            </div>
            <div class="card">
                <div class="flex align-items-center justify-content-between mb-4">
                    <h5>操作日志</h5>
                </div>
                <ul class="p-0 mx-0 mt-0 mb-4 list-none">
                    <li class="flex align-items-center py-2 border-bottom-1 surface-border" v-for="item in OperationLog" :key="item.operationID">
                        <div class="w-3rem h-3rem flex align-items-center justify-content-center bg-blue-100 border-circle mr-3 flex-shrink-0">
                            <i :class="item.operationClass"></i>
                        </div>
                        <span  class="text-blue-500 font-medium"> {{ item.operationDate }} <span class="text-700 line-height-3"> {{ item.operationCrud }} <span class="text-pink-500 font-medium"> {{ item.operationName }} </span></span></span>
                    </li>
                </ul>
            </div>
            <div
                class="px-4 py-5 shadow-2 flex flex-column md:flex-row md:align-items-center justify-content-between mb-3"
                style="border-radius: 1rem; background: linear-gradient(0deg, rgba(0, 123, 255, 0.5), rgba(0, 123, 255, 0.5)), linear-gradient(92.54deg, #1c80cf 47.88%, #ffffff 100.01%)"
            >
                <div>
                    <div class="text-blue-100 font-medium text-xl mt-2 mb-3">MACHLOOP</div>
                    <div class="text-white font-medium text-5xl">UI 自动化测试</div>
                </div>
                <div class="mt-4 mr-auto md:mt-0 md:mr-0">
                    <a href="javascript:;" class="p-button font-bold px-5 py-3 p-button-primary p-button-rounded p-button-raised"> README </a>
                </div>
            </div>
        </div>
    </div>
</template>