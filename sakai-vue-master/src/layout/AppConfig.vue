<script setup>
import { ref,onBeforeMount } from 'vue';
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '@/layout/composables/layout';

defineProps({
    simple: {
        type: Boolean,
        default: false
    }
});

const $primevue = usePrimeVue();

const visible = ref(false);

const compactMaterial = ref(false);

const { layoutConfig } = useLayout();

const onConfigButtonClick = () => {
    visible.value = !visible.value;
};
const onChangeTheme = (theme, mode) => {
    localStorage.setItem("theme",theme)
    localStorage.setItem("mode",mode)
    $primevue.changeTheme(layoutConfig.theme.value, theme, 'theme-css', () => {
        layoutConfig.theme.value = theme;
        layoutConfig.darkTheme.value = mode;
    });

};



const onDarkModeChange = (value) => {
    const newThemeName = value ? layoutConfig.theme.value.replace('light', 'dark') : layoutConfig.theme.value.replace('dark', 'light');
    layoutConfig.darkTheme.value = value;
    onChangeTheme(newThemeName, value);
};

const changeTheme = (theme, color) => {
    let newTheme, dark;
    newTheme = theme + '-' + (layoutConfig.darkTheme.value ? 'dark' : 'light');
    if (color) {
        newTheme += '-' + color;
    }

    if (newTheme.startsWith('md-') && compactMaterial.value) {
        newTheme = newTheme.replace('md-', 'mdc-');
    }

    dark = layoutConfig.darkTheme.value;
    onChangeTheme(newTheme, dark);
};

const isThemeActive = (themeFamily, color) => {
    let themeName;
    let themePrefix = themeFamily === 'md' && compactMaterial.value ? 'mdc' : themeFamily;

    themeName = themePrefix + (layoutConfig.darkTheme.value ? '-dark' : '-light');

    if (color) {
        themeName += '-' + color;
    }
    return layoutConfig.theme.value === themeName;
};

onBeforeMount(() => {
    let theme = localStorage.getItem("theme")
    let mode = localStorage.getItem("mode")
    if (theme!==null && mode!=null) {
        onChangeTheme(theme, mode)
    }else{
        onChangeTheme('aura-light-noir', false)
    }

});


</script>

<template>
    <button  class="layout-config-button p-link" type="button" @click="onConfigButtonClick()">
        <i  class="pi pi-cog"></i>
    </button>
    <Sidebar v-model:visible="visible" position="right" class="layout-config-sidebar w-26rem" pt:closeButton="ml-auto">
        <div class="p-2">

            <section class="py-4 flex align-items-center justify-content-between border-bottom-1 surface-border">
                <span :class="['text-xl font-semibold']">暗黑模式</span>
                <InputSwitch :modelValue="layoutConfig.darkTheme.value" @update:modelValue="onDarkModeChange" />
            </section>

            <section class="py-4 border-bottom-1 surface-border">
                <div class="text-xl font-semibold mb-3">主题</div>

                <div class="flex align-items-center justify-content-between gap-3 mb-3">
                    <button
                        :class="[
                            'bg-transparent border-1 cursor-pointer p-2 w-3 flex align-items-center justify-content-center transition-all transition-duration-200',
                            { 'border-primary': isThemeActive('aura', 'noir'), 'hover:border-500 surface-border': !isThemeActive('aura', 'noir') }
                        ]"
                        style="border-radius: 30px"
                        @click="changeTheme('aura', 'noir')"
                    >
                        <span class="block h-1rem w-full" style="border-radius: 30px; background: linear-gradient(180deg, #0f172a 0%, rgba(0, 0, 0, 0.5) 100%)"></span>
                    </button>
                    <button
                        :class="[
                            'bg-transparent border-1 cursor-pointer p-2 w-3 flex align-items-center justify-content-center transition-all transition-duration-200',
                            { 'border-primary': isThemeActive('aura', 'amber'), 'hover:border-500 surface-border': !isThemeActive('aura', 'amber') }
                        ]"
                        style="border-radius: 30px"
                        @click="changeTheme('aura', 'amber')"
                    >
                        <span class="block h-1rem w-full" style="border-radius: 30px; background: linear-gradient(180deg, #f59e0b 0%, rgba(245, 158, 11, 0.5) 100%)"></span>
                    </button>
                    <button
                        :class="[
                            'bg-transparent border-1 cursor-pointer p-2 w-3 flex align-items-center justify-content-center transition-all transition-duration-200',
                            { 'border-primary': isThemeActive('aura', 'blue'), 'hover:border-500 surface-border': !isThemeActive('aura', 'blue') }
                        ]"
                        style="border-radius: 30px"
                        @click="changeTheme('aura', 'blue')"
                    >
                        <span class="block h-1rem w-full" style="border-radius: 30px; background: linear-gradient(180deg, #4378e6 0%, rgba(67, 120, 230, 0.5) 100%)"></span>
                    </button>
                    <button
                        :class="[
                            'bg-transparent border-1 cursor-pointer p-2 w-3 flex align-items-center justify-content-center transition-all transition-duration-200',
                            { 'border-primary': isThemeActive('aura', 'pink'), 'hover:border-500 surface-border': !isThemeActive('aura', 'pink') }
                        ]"
                        style="border-radius: 30px"
                        @click="changeTheme('aura', 'pink')"
                    >
                        <span class="block h-1rem w-full" style="border-radius: 30px; background: linear-gradient(180deg, #ec4899 0%, rgba(236, 72, 153, 0.5) 100%)"></span>
                    </button>
                </div>
            </section>
        </div>
    </Sidebar>
</template>

<style lang="scss" scoped></style>
