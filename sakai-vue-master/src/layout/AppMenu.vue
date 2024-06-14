<script setup>
import { ref, computed } from 'vue';
import { useConfirm } from 'primevue/useconfirm';
const confirm = useConfirm();
// 测试附件
import { inject } from 'vue';
const storee = inject('storee');
const utilss = inject('utilss');
import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast(); // 弹出提示

const visible = ref(false);
const visible2 = ref(false);
const fileList = ref([]);

// 选择文件时立即上传
const uploadFile = async (event) => {
    const formData = new FormData();
    formData.append('file', event.files[0]);
    utilss.uploadTestFile(toast, formData);
    getFiles();
};

// 获取附件列表
const getFiles = async () => {
    fileList.value = await utilss.GetTestFiles();
};

// 删除文件
const deleteFile = (fileID) => {
    utilss.DeleteTestFile(toast, fileID);
    getFiles();
};
// 删除确认框
const confirm2 = (event,fileID) => {
    confirm.require({
        target: event.currentTarget,
        message: '删除附件?',
        icon: 'pi pi-info-circle',
        rejectClass: 'p-button-secondary p-button-outlined p-button-sm',
        acceptClass: 'p-button-danger p-button-sm',
        rejectLabel: '取消',
        acceptLabel: '确认',
        accept: () => {
            deleteFile(fileID);
        },
        reject: () => {
            console.log('取消');
        }
    });
};
////////////////////////////////////////////////////////////////////////////

// 导航栏
import { useLayout } from '@/layout/composables/layout';
const { layoutConfig } = useLayout();
const uitestUrl = computed(() => {
    return `/layout/images/${layoutConfig.darkTheme.value ? 'uitest-dark' : 'uitest-white'}.png`;
});
import AppMenuItem from './AppMenuItem.vue';
const model = ref([
    {
        label: '首页',
        items: [{ label: '仪表盘', icon: 'pi pi-fw pi-chart-bar', to: '/' }]
    },
    {
        label: '测试管理',
        items: [
            { label: '用例管理', icon: 'pi pi-fw pi-th-large', to: '/uikit/caseManager' },
            { label: '用例总览', icon: 'pi pi-fw pi-flag', to: '/uikit/caseView' },
            { label: '测试顺序', icon: 'pi pi-fw pi-sitemap', to: '/uikit/testSort' },
            { label: '环境配置', icon: 'pi pi-fw pi-sliders-h', to: '/uikit/testSet' }
        ]
    },
    {
        label: '执行测试',
        items: [
            {
                label: '执行测试',
                icon: 'pi pi-fw pi-forward',
                to: '/uikit/runCase'
            },
            {
                label: '运行日志',
                icon: 'pi pi-fw pi-align-left',
                to: '/uikit/runLog'
            }
        ]
    },
    {
        label: '测试报告',
        items: [
            {
                label: '测试报告',
                icon: 'pi pi-fw pi-external-link',
                to: '/uikit/report'
            },
            {
                label: '详细报告',
                icon: 'pi pi-fw pi-star',
                to: '/uikit/detailReport'
            }
        ]
    },
    {
        label: '控制台',
        items: [
            {
                label: '测试文档',
                icon: 'pi pi-fw pi-tags',
                to: '/uikit/MyExcel'
            },
            {
                label: '测试附件',
                icon: 'pi pi-fw pi-wallet',
                command: () => {
                    getFiles();
                    visible.value = true;
                }
            }
        ]
    },
    {
        label: '外部系统',
        items: [
            {
                label: '交付系统',
                icon: 'pi pi-fw pi-link',
                url: 'http://10.0.0.101:65432',
                target: '_blank'
            },
            {
                label: '接口自动化',
                icon: 'pi pi-fw pi-link',
                url: 'http://10.0.146.102:58080',
                target: '_blank'
            }
        ]
    }
]);
</script>

<template>
    <!-- 删除确认框 -->
    <ConfirmPopup></ConfirmPopup>
    <!-- 测试附件 -->
    <div>
        <Dialog v-model:visible="visible" modal header="测试附件" style="width: 35rem">
            <div style="height: 20em">
                <div v-for="cItem2 in fileList" :key="cItem2.fileID">
                    <a target="_blank" :href="storee.host + '/testFile/'+cItem2.fileName" download>
                        <Button text style="width: 80%; height: 2.5em">{{ cItem2.fileName }}</Button>
                    </a>
                    <Button @click="confirm2($event,cItem2.fileID)"  text style="width: 20%; height: 2.5em">删除</Button>
                </div>
            </div>
            <div class="flex justify-content-end gap-2" style="position: absolute; bottom: 1%; right: 10%">
                <Button type="button" label="添加附件" @click="visible2 = true"></Button>
            </div>
        </Dialog>
        <Dialog v-model:visible="visible2" modal header="添加附件" style="width: 20rem">
            <FileUpload name="demo[]" :showCancelButton="false" :showUploadButton="false" :fileLimit="1" @select="uploadFile($event)" customUpload />
        </Dialog>
    </div>

    <!-- 导航栏 -->
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item :item="item" :index="i"></app-menu-item>
        </template>
        <li>
            <a target="_blank" href="/">
                <img :src="uitestUrl" alt="Prime Blocks" class="w-full mt-3" />
            </a>
        </li>
    </ul>
</template>

<style lang="scss" scoped>
</style>
