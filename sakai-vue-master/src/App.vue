<script setup>
import { provide } from "vue";
import storee from './service/storee.js'
import utilss from './service/utilss.js'

provide("storee", storee);
provide("utilss", utilss);

</script>

<template>
    <router-view />
</template>

<style scoped></style>
