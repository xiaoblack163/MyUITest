<script setup>
import { ref, computed } from 'vue';
import { inject } from 'vue';
const storee = inject('storee');


import { useLayout } from '@/layout/composables/layout';
const { layoutConfig } = useLayout();
const readmeUrl = computed(() => {
    return `/layout/images/${layoutConfig.darkTheme.value ? 'readme-dark' : 'readme-white'}.png`;
});
import AppMenuItem from './AppMenuItem.vue';
const model = ref([
    {
        label: '首页',
        items: [{ label: '仪表盘', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: '测试管理',
        items: [
            { label: '用例管理', icon: 'pi pi-fw pi-bookmark', to: '/uikit/caseManager' },
            { label: '用例总览', icon: 'pi pi-fw pi-bookmark', to: '/uikit/caseView'},
            { label: '测试顺序', icon: 'pi pi-fw pi-bookmark' ,to: '/uikit/testSort'},
            { label: '环境配置', icon: 'pi pi-fw pi-bookmark', to: '/uikit/testEnv'},
        ]
    },
    {
        label: '执行测试',
        items: [
            {
                label: '执行测试',
                icon: 'pi pi-fw pi-question',
                to: '/uikit/runCase'
            },
            {
                label: '运行日志',
                icon: 'pi pi-fw pi-pencil'
            }
        ]
    },
    {
        label: '测试报告',
        items: [
            {
                label: '测试报告',
                icon: 'pi pi-fw pi-question',
                to: '/uikit/report'
            },
            {
                label: '详细报告',
                icon: 'pi pi-fw pi-pencil',
                to: '/uikit/detailReport'
            }
            
        ]
    },
    {
        label: '录制',
        items: [{ label: '录制定位值', icon: 'pi pi-fw pi-home' }]
    },
    {
        label: '控制台',
        items: [
        { label: '测试文档', icon: 'pi pi-fw pi-bookmark'},
        { label: '测试附件', icon: 'pi pi-fw pi-bookmark'},
            { 
                label: '管理配置', 
                icon: 'pi pi-fw pi-home' 
            },
            {
                label: '接口文档',
                icon: 'pi pi-fw pi-pencil',
                url: storee.host + '/redoc',
                target: '_blank'
            }
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
        <li>
            <img :src="readmeUrl" alt="Prime Blocks" class="w-full mt-3" />
        </li>
    </ul>
</template>

<style lang="scss" scoped></style>
