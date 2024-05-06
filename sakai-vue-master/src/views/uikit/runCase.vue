<script setup>
import { onMounted, ref } from 'vue';
import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast();
import { inject } from 'vue';
const utilss = inject('utilss');

// #####################################################################

// 测试用例tree
const treeTableValue = ref([]);
// 提交选测试运行数据
const runTestData = ref({
    selectedTreeTableValue:{},// 选择要执行的测试项
    testEnv:'', //测试环境
    testor:'', // 测试人
    version:'',// 测试版本
});


const showRunStatus = () => {
    if (runTestData.value.testEnv==='' || runTestData.value.testor==='' || runTestData.value.version==='' ){
        toast.add({ severity: 'warn', summary: '请输入测试参数', life: 3000 });
        return false
    }
    utilss.PostRunTestData(toast,runTestData.value)
};
const stopRunTest = () => {
    utilss.StopRunTest(toast)
};

// #####################################################################

// 测试进度
const MeterGroupvalue = ref([
    { label: '执行失败率', color1: '#fbbf24', color2: '#ef4444', value: 0, icon: 'pi pi-inbox' },
    { label: '断言失败率', color1: '#ef4444', color2: '#34d399', value: 0, icon: 'pi pi-image' },
    { label: '通过率', color1: '#34d399', color2: '#34d399', value: 0, icon: 'pi pi-table' }
]);

const MeterGroupvalue0 = ref([
    { label: '全部步骤', color1: '#0EA5E9', value: 0, icon: 'pi pi-table' },
    { label: '已测步骤', color1: '#F97316', value: 0, icon: 'pi pi-inbox' },
    { label: '未测步骤', color1: '#C0C1C0', value: 0, icon: 'pi pi-image' }
]);

const MeterGroupvalue00 = ref([
    { label: '功能数', color1: '#BEE399', value: 0, icon: 'pi pi-table' },
    { label: '用例数', color1: '#1ED6FB', value: 0, icon: 'pi pi-inbox' },
    { label: '步骤数', color1: '#F47A7A', value: 0, icon: 'pi pi-image' }
]);

// #####################################################################

// 测试图表
const chartData = ref();
const chartOptions = ref();

const setChartData = (funclist,passlist,faillist) => {
    const documentStyle = getComputedStyle(document.documentElement);
    return {
        labels: funclist,
        datasets: [
            {
                label: '通过步骤',
                backgroundColor: documentStyle.getPropertyValue('--cyan-500'),
                data: passlist
            },
            {
                label: '失败步骤',
                backgroundColor: documentStyle.getPropertyValue('--red-300'),
                data: faillist
            }
        ]
    };
};





const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        indexAxis: 'y',
        maintainAspectRatio: false,
        aspectRatio: 0.8,
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary,
                    font: {
                        weight: 500
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            }
        }
    };
};


// #####################################################################


const activity_chart = ref()
onMounted(async () => {

    treeTableValue.value = await utilss.GetRunCaseTreeData();

    activity_chart.value = await utilss.GetCaseActivity(toast);

    console.log("啊飒飒的",activity_chart.value)

    runTestData.value.testEnv = activity_chart.value.testEnv.testEnv
    runTestData.value.testor = activity_chart.value.testEnv.testor
    runTestData.value.version = activity_chart.value.testEnv.version

    MeterGroupvalue.value[0].value = (100*(activity_chart.value.activity.execFailNumber/activity_chart.value.activity.stepNumber)).toFixed(1)
    MeterGroupvalue.value[1].value = (100*(activity_chart.value.activity.assertpassNumber/activity_chart.value.activity.stepNumber)).toFixed(1)
    MeterGroupvalue.value[2].value = (100*(activity_chart.value.activity.passNumber/activity_chart.value.activity.stepNumber)).toFixed(1)

    MeterGroupvalue0.value[0].value = parseInt(activity_chart.value.activity.stepNumber)
    MeterGroupvalue0.value[1].value = parseInt(activity_chart.value.activity.testedNumber)
    MeterGroupvalue0.value[2].value = parseInt(activity_chart.value.activity.stepNumber-activity_chart.value.activity.testedNumber)

    MeterGroupvalue00.value[0].value = parseInt(activity_chart.value.activity.funcNumber)
    MeterGroupvalue00.value[1].value = parseInt(activity_chart.value.activity.caseNumber)
    MeterGroupvalue00.value[2].value = parseInt(activity_chart.value.activity.stepNumber)

    chartData.value = setChartData(Object.keys(activity_chart.value.funcChart.passNumber),Object.values(activity_chart.value.funcChart.passNumber),Object.values(activity_chart.value.funcChart.failNumber));
    chartOptions.value = setChartOptions();
});



</script>



<template>
    <div class="card">
        <h5>选择测试用例</h5>
        <TreeTable :value="treeTableValue" selectionMode="checkbox" v-model:selectionKeys="runTestData.selectedTreeTableValue">
            <Column field="name" header="名称" :expander="true"></Column>
            <Column field="id" header="ID"></Column>
            <Column field="type" header="类型"></Column>
        </TreeTable>
    </div>

    <div class="card">
        <h5>运行测试</h5>
        <div class="formgrid grid">
            <div class="field col-12 md:col-3">
                <label for="lastname1" class="p-sr-only">运行环境</label>
                <InputText v-model="runTestData.testEnv" style="width: 100%" type="text" placeholder="请输入运行环境" />
            </div>
            <div class="field col-12 md:col-3">
                <label for="lastname1" class="p-sr-only">测试版本</label>
                <InputText v-model="runTestData.version" style="width: 100%" type="text" placeholder="请输入测试版本" />
            </div>
            <div class="field col-12 md:col-3">
                <label for="lastname1" class="p-sr-only">测试人</label>
                <InputText v-model="runTestData.testor"  style="width: 100%" type="text" placeholder="请输入测试人" />
            </div>
            <div class="field col-12 md:col-3 flex justify-content-between">
                <Button label="运行测试" @click="showRunStatus" />
                <Button label="停止测试" @click="stopRunTest" outlined />
            </div>
        </div>
    </div>

    <div class="card">
        <MeterGroup :value="MeterGroupvalue" labelPosition="start">
            <template #label>
                <div class="flex flex-wrap gap-3">
                    <template v-for="(val, i) of MeterGroupvalue00" :key="i">
                        <Card class="flex-1">
                            <template #content>
                                <div class="flex justify-content-between gap-5">
                                    <div class="flex flex-column gap-1">
                                        <span class="text-secondary text-sm">{{ val.label }}</span>
                                        <span class="font-bold text-lg">{{ val.value }}</span>
                                    </div>
                                    <span class="w-2rem h-2rem border-circle inline-flex justify-content-center align-items-center text-center" :style="{ backgroundColor: `${val.color1}`, color: '#ffffff' }">
                                        <i :class="val.icon" />
                                    </span>
                                </div>
                            </template>
                        </Card>
                    </template>
                </div>

                <div class="flex flex-wrap gap-3">
                    <template v-for="(val, i) of MeterGroupvalue0" :key="i">
                        <Card class="flex-1">
                            <template #content>
                                <div class="flex justify-content-between gap-5">
                                    <div class="flex flex-column gap-1">
                                        <span class="text-secondary text-sm">{{ val.label }}</span>
                                        <span class="font-bold text-lg">{{ val.value }}</span>
                                    </div>
                                    <span class="w-2rem h-2rem border-circle inline-flex justify-content-center align-items-center text-center" :style="{ backgroundColor: `${val.color1}`, color: '#ffffff' }">
                                        <i :class="val.icon" />
                                    </span>
                                </div>
                            </template>
                        </Card>
                    </template>
                </div>

                <div class="flex flex-wrap gap-3">
                    <template v-for="(val, i) of MeterGroupvalue" :key="i">
                        <Card class="flex-1">
                            <template #content>
                                <div class="flex justify-content-between gap-5">
                                    <div class="flex flex-column gap-1">
                                        <span class="text-secondary text-sm">{{ val.label }}</span>
                                        <span class="font-bold text-lg">{{ val.value }}%</span>
                                    </div>
                                    <span class="w-2rem h-2rem border-circle inline-flex justify-content-center align-items-center text-center" :style="{ backgroundColor: `${val.color1}`, color: '#ffffff' }">
                                        <i :class="val.icon" />
                                    </span>
                                </div>
                            </template>
                        </Card>
                    </template>
                </div>
            </template>

            <template #meter="slotProps">
                <span :class="slotProps.class" :style="{ background: `linear-gradient(to right, ${slotProps.value.color1}, ${slotProps.value.color2})`, width: slotProps.size }" />
            </template>
            <template #start="{ totalPercent }">
                <div class="flex justify-content-between mt-3 mb-2 relative">
                    <span>测试进度</span>
                    <span :style="{ width: totalPercent + '%' }" class="absolute text-right"></span>
                </div>
            </template>
            <template #end> </template>
        </MeterGroup>
    </div>

    <div class="card">
        <Chart type="bar" :data="chartData" :options="chartOptions" class="h-30rem" />
    </div>
</template>
