
<template>
    <testEnv />
    <div class="card">
        <h5>测试配置</h5>
        <div class="grid p-fluid">
            <div class="col-12 md:col-6">
                <h5>运行模式</h5>
                <SelectButton v-model="testSetAndOption.testSet.runMode" :options="testSetAndOption.runModeOption" aria-labelledby="basic" />
                <h5>是否录屏</h5>
                <SelectButton v-model="testSetAndOption.testSet.screencastValue" :options="testSetAndOption.boolOption" aria-labelledby="basic" />
                <h5>是否截屏</h5>
                <SelectButton v-model="testSetAndOption.testSet.screenshotValue" :options="testSetAndOption.boolOption" aria-labelledby="basic" />
                <h5>发包失败的动作</h5>
                <SelectButton v-model="testSetAndOption.testSet.sendFlowFailAction" :options="testSetAndOption.failAction" aria-labelledby="basic" />
                <h5>网页访问失败的动作</h5>
                <SelectButton v-model="testSetAndOption.testSet.getUrlFailAction" :options="testSetAndOption.failAction" aria-labelledby="basic" />
                <h5>登录失败的动作</h5>
                <SelectButton v-model="testSetAndOption.testSet.loginFailAction" :options="testSetAndOption.failAction" aria-labelledby="basic" />
                <h5>断言失败的动作</h5>
                <SelectButton v-model="testSetAndOption.testSet.assertFailAction" :options="testSetAndOption.failAction" aria-labelledby="basic" />
                <h5>执行失败的动作</h5>
                <SelectButton v-model="testSetAndOption.testSet.execFailAction" :options="testSetAndOption.failAction" aria-labelledby="basic" />
                <h5>文字识别模型版本</h5>
                <SelectButton v-model="testSetAndOption.testSet.ocrModel" :options="testSetAndOption.ocrModelOption" aria-labelledby="basic" />
            </div>
            <div class="col-12 md:col-6">    
                <h5>网页访问失败重试次数</h5>
                <InputNumber v-model="testSetAndOption.testSet.getUrlRetry" showButtons :min="1" :max="3" /> 
                <h5>登录失败重试次数</h5>
                <InputNumber v-model="testSetAndOption.testSet.loginRetry" showButtons :min="1" :max="5" /> 
                <h5>截图失败重试次数</h5>
                <InputNumber v-model="testSetAndOption.testSet.screenshotRetry" showButtons :min="1" :max="5" />    
                <h5>定位失败重试次数</h5>
                <InputNumber v-model="testSetAndOption.testSet.locatRetry" showButtons :min="1" :max="10" />
                <h5>文字识别置信度不低于</h5>
                <InputNumber v-model="testSetAndOption.testSet.ocrConfidence" prefix="%" showButtons :min="60" :max="100" />
                <h5>文字识别匹配度不低于</h5>
                <InputNumber v-model="testSetAndOption.testSet.ocrMatch"  showButtons :min="60" :max="100" />
                <h5>图像识别置信度不低于</h5>
                <InputNumber v-model="testSetAndOption.testSet.imgConfidence"  prefix="%" showButtons :min="60" :max="100" />
                <h5>目标检测置信度不低于</h5>
                <InputNumber v-model="testSetAndOption.testSet.yoloConfidence"  prefix="%" showButtons :min="60" :max="100" />
                <Button @click="UpdateTestSet" style="margin-top:65px;" label="提交"></Button>
            </div>
        </div>
        
    </div>
</template>

<script setup>
import testEnv from './testEnv.vue';
import { ref,onBeforeMount } from 'vue';
import { inject } from 'vue';
const utilss = inject('utilss');
import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast(); // 弹出提示


const testSetAndOption = ref({
    "runModeOption": ["正常模式", "无头模式"],
    "boolOption": ["是", "否"],
    "failAction": ["停止测试", "跳过用例", "继续执行"],
    "ocrModelOption": ["v2", "v3", "v4"],
    "testSet":{
        "runMode": "",
        "screencastValue": "",
        "screenshotValue": "",
        "sendFlowFailAction": "",
        "getUrlFailAction": "",
        "loginFailAction": "",
        "assertFailAction": "",
        "execFailAction": "",
        "ocrModel": "v4",
        "getUrlRetry": 0,
        "loginRetry": 0,
        "screenshotRetry": 0,
        "locatRetry": 0,
        "ocrConfidence": 0,
        "ocrMatch": 0,
        "imgConfidence": 0,
        "yoloConfidence": 0
    }
})

const UpdateTestSet = ( () => {
    utilss.PutTestSet(toast,testSetAndOption.value);
})

onBeforeMount(async () => {
    testSetAndOption.value = await utilss.GetTestSet();
});




</script>
