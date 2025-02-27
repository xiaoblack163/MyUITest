<template>
  <div ref="container" class="univer-container"></div>
</template>

<script setup>
import "@univerjs/design/lib/index.css";
import "@univerjs/ui/lib/index.css";
import "@univerjs/sheets-ui/lib/index.css";
import "@univerjs/sheets-formula/lib/index.css";

import { Univer } from "@univerjs/core";
import { defaultTheme } from "@univerjs/design";
import { UniverDocsPlugin } from "@univerjs/docs";
import { UniverDocsUIPlugin } from "@univerjs/docs-ui";
import { UniverFormulaEnginePlugin } from "@univerjs/engine-formula";
import { UniverRenderEnginePlugin } from "@univerjs/engine-render";
import { UniverSheetsPlugin } from "@univerjs/sheets";
import { UniverSheetsFormulaPlugin } from "@univerjs/sheets-formula";
import { UniverSheetsUIPlugin } from "@univerjs/sheets-ui";
import { UniverUIPlugin } from "@univerjs/ui";
import { onBeforeUnmount, onMounted, ref } from "vue";


// const {data} = defineProps({
  // workbook data
  // data: {
  //   type: Object,
  //   default: () => ({}),
  // },
// });

const univer = ref(null);
const workbook = ref(null);
const container = ref(null);

// onMounted(() => {
//   console.log("onMounted")
//   init(data);
// });

onBeforeUnmount(() => {
  destroyUniver();
});


/**
 * Initialize univer instance and workbook instance
 * @param data {IWorkbookData} document see https://univer.work/api/core/interfaces/IWorkbookData.html
 */

const init = (data = {}) => {
  const univer = new Univer({
    theme: defaultTheme,
  });
  univer.value = univer;



  // core plugins
  univer.registerPlugin(UniverRenderEnginePlugin);
  univer.registerPlugin(UniverFormulaEnginePlugin);
  univer.registerPlugin(UniverUIPlugin, {
    container: container.value,
    header: true,
    toolbar: true,
    footer: true,
  });

  // doc plugins
  univer.registerPlugin(UniverDocsPlugin, {
    hasScroll: false,
  });
  univer.registerPlugin(UniverDocsUIPlugin);

  // sheet plugins
  univer.registerPlugin(UniverSheetsPlugin);
  univer.registerPlugin(UniverSheetsUIPlugin);
  univer.registerPlugin(UniverSheetsFormulaPlugin);

  // create workbook instance
  workbook.value = univer.createUniverSheet(data);
};

/**
 * Destroy univer instance and workbook instance
 */
const destroyUniver = () => {
  univer.value?.dispose();
  univer.value = null;
  workbook.value = null;
};

/**
 * Get workbook data
 */
 const setData = (data) => {
  destroyUniver()
  init(data)
};

const getData = () => {
  if (!workbook.value) {
    throw new Error('Workbook is not initialized');
  }
  return workbook.value.save();
};

defineExpose({
  getData,
  setData,
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.univer-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* Also hide the menubar */
:global(.univer-menubar) {
  display: none;
}
</style>
