import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/uikit/caseManager',
                    name: 'caseManager',
                    component: () => import('@/views/uikit/caseManager.vue')
                },
                {
                    path: '/uikit/caseView',
                    name: 'caseView',
                    component: () => import('@/views/uikit/caseView.vue')
                },
                {
                    path: '/uikit/detailReport',
                    name: 'detailReport',
                    component: () => import('@/views/uikit/detailReport.vue')
                },
                {
                    path: '/uikit/runCase',
                    name: 'runCase',
                    component: () => import('@/views/uikit/runCase.vue')
                },
                {
                    path: '/uikit/report',
                    name: 'report',
                    component: () => import('@/views/uikit/report.vue')
                },
                {
                    path: '/uikit/testEnv',
                    name: 'testEnv',
                    component: () => import('@/views/uikit/testEnv.vue')
                },
                {
                    path: '/uikit/testSort',
                    name: 'testSort',
                    component: () => import('@/views/uikit/testSort.vue')
                },
                {
                    path: '/uikit/runLog',
                    name: 'runLog',
                    component: () => import('@/views/uikit/runLog.vue')
                }
            ]
        },
    ]
});

export default router;
