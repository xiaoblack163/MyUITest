<script setup>
import { onMounted, ref } from 'vue';


// app.component('MeterGroup', MeterGroup);

// 选择测试用例
const treeTableValue = ref([
    {
        key: '测试功能_文件还原',
        data: {
            name: '文件还原',
            id: '100kb',
            type: '测试功能'
        },
        children: [
            {
                key: '测试用例_HTTP',
                data: {
                    name: 'HTTP',
                    id: '25kb',
                    type: '测试用例'
                }
            },
            {
                key: '测试用例_FTP',
                data: {
                    name: 'FTP',
                    id: '25kb',
                    type: '测试用例'
                }
            }
        ]
    },
    {
        key: '测试功能_全包溯源',
        data: {
            name: '全包溯源',
            id: '100kb',
            type: '测试功能'
        },
        children: [
            {
                key: '测试用例_空条件',
                data: {
                    name: '空条件',
                    id: '25kb',
                    type: '测试用例'
                }
            },
            {
                key: '测试用例_有条件',
                data: {
                    name: '有条件',
                    id: '25kb',
                    type: '测试用例'
                }
            }
        ]
    }
]);
const selectedTreeTableValue = ref(null);

// 测试进度
const MeterGroupvalue = ref([
    { label: '通过', color1: '#34d399', color2: '#ef4444', value: 75, icon: 'pi pi-table' },
    { label: '断言失败', color1: '#ef4444', color2: '#fbbf24', value: 20, icon: 'pi pi-image' },
    { label: '执行失败', color1: '#fbbf24', color2: '#fbbf24', value: 1, icon: 'pi pi-inbox' }
]);

const MeterGroupvalue0 = ref([
    { label: '全部步骤', color1: '#0EA5E9', value: 625, icon: 'pi pi-table' },
    { label: '已试步骤', color1: '#F97316', value: 115, icon: 'pi pi-inbox' },
    { label: '未测步骤', color1: '#F1F5F9', value: 420, icon: 'pi pi-image' }
]);

// 测试图表
onMounted(() => {
    chartData.value = setChartData();
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const setChartData = () => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
        labels: ['文件还原', '全包溯源', 'IP画像', '业务告警', '第三方外发', '流量分析', '安全分析'],
        datasets: [
            {
                label: '通过步骤',
                backgroundColor: documentStyle.getPropertyValue('--cyan-500'),
                data: [65, 0, 80, 81, 56, 55, 40]
            },
            {
                label: '失败步骤',
                backgroundColor: documentStyle.getPropertyValue('--red-300'),
                data: [28, 48, 40, 19, 86, 27, 90]
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
</script>

<template>
    <div class="card">
        <h5>选择测试用例</h5>
        <TreeTable :value="treeTableValue" selectionMode="checkbox" v-model:selectionKeys="selectedTreeTableValue">
            <Column field="name" header="名称" :expander="true"></Column>
            <Column field="id" header="ID"></Column>
            <Column field="type" header="类型"></Column>
        </TreeTable>
        <div class="flex justify-content-between mt-3">
            <Button label="运行测试" size="small" />
            <Button label="停止测试" outlined size="small" />
        </div>
    </div>

    <div class="card">
        <MeterGroup :value="MeterGroupvalue" labelPosition="start">
            <template #label="{ value }">
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
                    <span :style="{ width: totalPercent + '%' }" class="absolute text-right">{{ totalPercent }}%</span>
                </div>
            </template>
            <template #end> </template>
        </MeterGroup>
    </div>

    <div class="card">
        <Chart type="bar" :data="chartData" :options="chartOptions" class="h-30rem" />
    </div>
</template>
