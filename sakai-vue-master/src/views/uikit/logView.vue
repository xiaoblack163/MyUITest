<template>
    <div class="card flex justify-content-center">
        <Stepper style="flex-basis: 100rem">
            <StepperPanel v-for="(log, funcName) in runlog" :key="funcName" :header="funcName">
                <template #content="{ prevCallback, nextCallback }">
                    <div style="height: 60vh;" class="border-2 border-dashed surface-border border-round surface-ground flex-auto flex font-medium">
                        <ScrollPanel style="width: 100%;">
                            <div style="white-space: pre-wrap; margin: 10px" v-html="log"></div>
                        </ScrollPanel>
                    </div>
                    <div class="flex pt-4 justify-content-between">
                        <Button label="Back" severity="secondary" icon="pi pi-arrow-left" @click="prevCallback" />
                        <Button label="Next" icon="pi pi-arrow-right" iconPos="right" @click="nextCallback" />
                    </div>
                </template>
            </StepperPanel>
        </Stepper>
    </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
const logMode = defineProps( ["logMode"]);
import { inject } from 'vue';
const utilss = inject('utilss');

const runlog = ref({});

const formattedText = (text) => {
    // 定义颜色
    const colors = {
        INFO: '#00A4EF',
        ERROR: '#EC586C',
        FAIL: '#F25022',
        PASS: '#88C972',
        WARN: '#E2BF75'
    };

    // 使用正则表达式替换标记，并添加颜色
    const regex = /\【(PASS|FAIL|INFO|ERROR|WARN)\】/g;
    return text.replace(regex, (match, type) => {
        return `<br><span style="color: ${colors[type]};font-weight: bold;">${match} </span>`;
    });
};

onBeforeMount(async () => {
    if (logMode.logMode==='RunLog'){
        runlog.value = await utilss.GetRunLog();
    }else{
        runlog.value = await utilss.GetTestLog(logMode.logMode);
    }
    
    for (const key in runlog.value) {
        runlog.value[key] = formattedText(runlog.value[key]);
    }
});
</script>




