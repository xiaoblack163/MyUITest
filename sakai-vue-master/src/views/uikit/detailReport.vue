<script setup>
import { ref, onMounted } from 'vue';
import { inject } from 'vue';
const utilss = inject('utilss');
const storee = inject('storee');

const stepReports = ref([]);

// 随机标签颜色
const getSeverity = () => {
    const items = ["danger", "success", "info","warning","secondary","help","contrast"];
    const randomIndex = Math.floor(Math.random() * items.length);
    return items[randomIndex];
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



const visible = ref(false)
const sidebarTitle = ref(' ')
const imgvideopath = ref('')
const displaymode = ref('')
const getScreen = (displaymode2,sidebarTitle2,ID2) => {
    visible.value = true
    displaymode.value = displaymode2
    sidebarTitle.value = sidebarTitle2
    if (displaymode2 === 'video' ){
        imgvideopath.value = storee.host+"/screencast/"+ID2+".webm"
    }else{
        imgvideopath.value = storee.host+"/screenshot/"+ID2+".png"
    }  
}


// #####################################################################

const activity_chart = ref()
onMounted(async () => {
    const reportID = localStorage.getItem("reportID")

    stepReports.value = await utilss.GetDetaiReports(reportID);

    activity_chart.value = await utilss.GetDetaiChart(reportID);

    MeterGroupvalue.value[0].value = (100*(activity_chart.value.activity.execFailNumber/activity_chart.value.activity.stepNumber)).toFixed(1)
    MeterGroupvalue.value[1].value = (100*(activity_chart.value.activity.assertFailNumber/activity_chart.value.activity.stepNumber)).toFixed(1)
    MeterGroupvalue.value[2].value = (100*(activity_chart.value.activity.passNumber/activity_chart.value.activity.stepNumber)).toFixed(1)

    MeterGroupvalue0.value[0].value = parseInt(activity_chart.value.activity.stepNumber)
    MeterGroupvalue0.value[1].value = parseInt(activity_chart.value.activity.testedNumber)
    MeterGroupvalue0.value[2].value = parseInt(activity_chart.value.activity.stepNumber-activity_chart.value.activity.testedNumber)

    MeterGroupvalue00.value[0].value = parseInt(activity_chart.value.activity.funcNumber)
    MeterGroupvalue00.value[1].value = parseInt(activity_chart.value.activity.caseNumber)
    MeterGroupvalue00.value[2].value = parseInt(activity_chart.value.activity.stepNumber)

    chartData.value = setChartData(Object.keys(activity_chart.value.passNumber),Object.values(activity_chart.value.passNumber),Object.values(activity_chart.value.failNumber));
    chartOptions.value = setChartOptions();
    
});






</script>

<template>

    <Sidebar v-model:visible="visible" :header="sidebarTitle" position="full">
        <div class="card">
            <video v-if="displaymode === 'video'" controls width="80%" >
                <source :src="imgvideopath" type="video/webm" />
            </video>
            <Image v-if="displaymode === 'img'" :src="imgvideopath" alt="Image" width="80%" />
        </div>
    </Sidebar>


     <div class="card">
        <MeterGroup :value="MeterGroupvalue" labelPosition="start">
            <template #label="{ value }">
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
                    <template v-for="(val, i) of value" :key="i">
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

    <div class="card">
        <h5>测试报告</h5>
        <DataTable :value="stepReports" showGridlines rowGroupMode="subheader" groupRowsBy="caseID" sortMode="single" selectionMode="single" sortField="caseID" :sortOrder="1" scrollable scrollHeight="48vh">
            <Column headerStyle="width: 5rem; text-align: center"  bodyStyle="text-align: center; overflow: visible">
                <template #body="{ data }">
                    <Button  @click="getScreen('img',data.stepName,data.detailReportID)"  type="button" icon="pi pi-image" rounded />
                </template>
            </Column>
            <Column field="caseID" header="caseID" ></Column>
            <Column field="stepName" header="步骤" style="min-width: 300px" class="font-bold"></Column>
            <Column field="execDate" header="测试时间" style="min-width: 200px"></Column>
            <Column field="action" header="动作" style="min-width: 200px"></Column>
            <Column field="AssertOrActionValue" header="输入参数" style="min-width: 200px"></Column>
            <Column field="locatMode" header="定位方式" style="min-width: 120px">
                <template #body="slotProps">
                    <Tag :severity="getSeverity(slotProps.data.locatMode)">{{ slotProps.data.locatMode.toUpperCase() }}</Tag>
                </template>
            </Column>
            <Column field="locatValue" header="定位值" style="min-width: 200px"></Column>
            <Column field="yoloValue" header="目标检测元素" style="min-width: 200px"></Column>
            <Column field="elementNumber" header="元素序号" style="min-width: 100px"></Column>
            <Column field="xValue" header="x坐标" style="min-width: 100px"></Column>
            <Column field="yValue" header="y坐标" style="min-width: 100px"></Column>
            <Column field="stepInfo" header="步骤说明" style="min-width: 200px"></Column>
            <Column field="execInfo" header="步骤执行信息" style="min-width: 200px"></Column>
            <Column field="result" header="测试结果"  frozen alignFrozen="right"  style="min-width: 100px">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'text-green-500 pi-check-circle': data.result, 'text-pink-500 pi-times-circle': !data.result }"></i>
                </template>
            </Column>

            <template #groupheader="slotProps">
                <div class="flex align-items-center gap-2"  style="color: #0D8ADB;">
                    <Button @click="getScreen('video',slotProps.data.caseName,slotProps.data.reportID + slotProps.data.caseID)"  type="button" icon="pi pi-youtube" rounded style="margin-right: 1.5rem"/>
                    <i class="pi pi-th-large" style="height: 1rem; margin-right: 0.5rem"></i>
                    <td style="text-align: right" class="text-bold pr-6">测试功能: {{ slotProps.data.funcName }}</td>
                    <i class="pi pi-star" style="height: 1rem; margin-right: 0.5rem"></i>
                    <td style="text-align: right" class="text-bold pr-6">测试用例: {{ slotProps.data.caseName }}</td>
                </div>
            </template>
        </DataTable>
    </div>
</template>
