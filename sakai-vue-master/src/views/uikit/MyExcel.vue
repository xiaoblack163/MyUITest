
<template>
    <!-- https://github.com/awesome-univer/sheets-vue3-demo/blob/main/README-zh.md -->
    <div>
        <Dialog v-model:visible="visible" modal header="选择文档" :style="{ width: '25rem', height: '20rem' }">
            <div v-for="cItem2 in excelList" :key="cItem2.excelID">
                <Button
                    @click="
                        GetExcelData(cItem2.excelID);
                        visible = false;
                    "
                    text
                    style="width: 100%; height: 2.5em"
                    >{{ cItem2.excelName }}</Button
                >
            </div>
        </Dialog>
    </div>
    <div>
        <Dialog v-model:visible="visible2" modal header="添加文档" :style="{ width: '25rem' }">
          <div class="flex align-items-center gap-3 mb-5">
            <InputText v-model="PostExcelName" class="flex-auto" autocomplete="off" placeholder="请输入文档名称" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visible2 = false"></Button>
            <Button
                type="button"
                label="Save"
                @click="
                    visible2 = false;
                    PostExcelData()
                "
            ></Button>
        </div>
        </Dialog>
    </div>
    <div class="card" style="height: 82vh">
        <UniverSheet id="sheet" ref="univerRef" />
        <SpeedDial class="box-b" :model="items" direction="up" />
    </div>
</template>
  
  <script setup>
//重命名，新建excel,选择excel,删除excel,保存excel
import UniverSheet from './UniverSheet.vue';
import { ref, onBeforeMount } from 'vue';
import { useToast } from 'primevue/usetoast'; // 弹出提示
const toast = useToast(); // 弹出提示
import { inject } from 'vue';

const utilss = inject('utilss');
const univerRef = ref(null);
const visible = ref(false);
const visible2 = ref(false);
const PostExcelName = ref('');
const excelList = ref([]);
const items = ref([
    {
        label: 'save',
        icon: 'pi pi-save',
        command: () => {
            PutExcelData();
        }
    },
    {
        label: 'Delete',
        icon: 'pi pi-trash',
        command: () => {
          DeleteExcelData();
        }
    },
    {
        label: 'Add',
        icon: 'pi pi-plus',
        command: () => {
            visible2.value = true
        }
    },
    {
        label: 'Select',
        icon: 'pi pi-external-link',
        command: async () => {
            excelList.value = await utilss.GetExcelDatas()
            visible.value = true;
        }
    }
]);
const GetExcelData =async (excelID) => {
    var data = await utilss.GetExcelData(excelID);
    univerRef.value.setData(JSON.parse(data.excelData));
    localStorage.setItem('excelID', data.excelID);
    localStorage.setItem('excelName', data.excelName); 
};

const PostExcelData = () => {
  if (PostExcelName.value===''){
    toast.add({ severity: 'info', summary: '信息', detail: '请输入文档名!', life: 3000 });
    return false;
  }
  utilss.PostExcelData(toast,{
            excelID: crypto.randomUUID(),
            excelName: PostExcelName.value,
            excelData:
                `{
		"id": "` +
                crypto.randomUUID() +
                `",
		"sheetOrder": [
		  "sheet-01"
		],
		"name": "universheet",
		"appVersion": "3.0.0-alpha",
		"locale": "zhCN",
		"styles": {},
		"sheets": {
		  "sheet-01": {
			"type": 0,
			"id": "sheet-01",
			"cellData": {
			  "0": {
				"0": {
				  "v": "",
				  "t": 1
				}
			  }
			},
			"name": "sheet1",
			"hidden": 0,
			"rowCount": 1000,
			"columnCount": 20,
			"zoomRatio": 1,
			"scrollTop": 200,
			"scrollLeft": 100,
			"defaultColumnWidth": 93,
			"defaultRowHeight": 27,
			"status": 1,
			"showGridlines": 1,
			"hideRow": [],
			"hideColumn": [],
			"rowHeader": {
			  "width": 46,
			  "hidden": 0
			},
			"columnHeader": {
			  "height": 20,
			  "hidden": 0
			},
			"selections": [
			  "A2"
			],
			"rightToLeft": 0,
			"pluginMeta": {},
			"freeze": {
			  "xSplit": 0,
			  "ySplit": 0,
			  "startRow": -1,
			  "startColumn": -1
			},
			"mergeData": [],
			"rowData": {
			  "0": {
				"hd": 0,
				"h": 27,
				"ah": 27
			  }
			},
			"columnData": {}
		  }
		},
		"resources": []
	  }`
        })
};

const PutExcelData = () => {
    const result = univerRef.value.getData();
    utilss.PutExcelData(toast,{ excelID: localStorage.getItem('excelID'), excelName: localStorage.getItem('excelName'), excelData: JSON.stringify(result)})
};

const DeleteExcelData = () => {
    utilss.DeleteExcelData(toast, localStorage.getItem('excelID'))
};

onBeforeMount(async () => {
    GetExcelData(localStorage.getItem('excelID'));
});
</script>


<style>
.box-b {
    position: absolute;
    bottom: 20%;
    right: 10%;
    z-index: 999;
}
</style>