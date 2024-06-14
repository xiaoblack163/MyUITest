<template>
    <div class="card">
        <h3>管理执行顺序</h3>
        <div class="parent-list">
            <div v-show="pItem.funcID" class="parent-box" v-for="(pItem, pIndex) in sortData" :key="pItem.funcID">
                <Button  text raised style="width: 100%; height: 3em" class="parent-name" @click="toggleParent(pIndex)"><i class="pi pi-bars" style="font-size: 1.5rem; margin-right: 10px"></i>{{ pItem.funcName }}</Button>
                <transition name="fade">
                    <div class="child-list" v-show="expandedParents[pIndex]">
                        <div class="child-box" v-for="(cItem, cIndex) in pItem.children" :key="cItem.caseID">
                            <Button outlined style="width: 100%; height: 2.5em" class="child-name" @click="toggleChild(pIndex, cIndex)"><i class="pi pi-bars" style="font-size: 1.5rem; margin-right: 10px"></i>{{ cItem.caseName }}</Button>
                            <!-- <transition name="fade"> -->
                                <div class="grandchild-list" v-show="expandedChildren[pIndex] && expandedChildren[pIndex][cIndex]">
                                    <div class="grandchild-box" v-for="cItem2 in cItem.grandchild" :key="cItem2.stepID">
                                        <Button text style="width: 100%; height: 2.5em" class="grandchild-name">{{ cItem2.stepName }}</Button>
                                    </div>
                                </div>
                            <!-- </transition> -->
                        </div>
                    </div>
                </transition>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// npm i sortablejs -S
import Sortable from 'sortablejs';
import { ref, nextTick, onBeforeMount } from 'vue';
import { inject } from 'vue';
const storee = inject('storee');

// 有几个元素就有几个功能可以展开
const sortData = ref([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]);

// 展开子项
const expandedParents = ref(sortData.value.map(() => false));

const expandedChildren = ref(sortData.value.map(() => ({})));

function toggleParent(index: number) {
    expandedParents.value = expandedParents.value.map((_, i) => (i === index ? !expandedParents.value[i] : false));
}

function toggleChild(pIndex: number, cIndex: number) {
    if (!expandedChildren.value[pIndex]) {
        expandedChildren.value[pIndex] = {};
    }
    expandedChildren.value[pIndex][cIndex] = !expandedChildren.value[pIndex][cIndex];
}

// 拖拽排序

interface DropEndType {
    newIndex: number;
    oldIndex: number;
}

interface ParentDropEndType extends DropEndType {
    item: {
        closest: (arg0: string) => Element;
    };
}

interface ChildDropEndType extends ParentDropEndType {
    item: {
        closest: (arg0: string) => Element;
    };
}


const putSortData = (sortData) => {
    fetch(storee.host+'/test_order', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"testOrderData":sortData})
    })
        .then((response) => response.json())
        .catch((error) => {
            console.log('error', '请求错误！', error);
        });
}
// 设置排序
const setSort = () => {
    const parentContainers = document.querySelectorAll('.parent-box');
    const childContainers = document.querySelectorAll('.child-box');

    // 当孙节点排序时触发
    childContainers.forEach((container, index) => {
        new Sortable(container.querySelector('.grandchild-list'), {
            group: `child-${index}`,
            sort: true,
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: (e: ChildDropEndType) => {
                nextTick(() => {
                    const allParentDom = document.querySelectorAll('.parent-box'); // 查找所有的parent-box Dom
                    const parentIndex = Array.from(allParentDom).indexOf(e.item.closest('.parent-box')); // 当前parent-box index
                    const allChildDom = document.querySelectorAll('.parent-box')[parentIndex].querySelectorAll('.child-box'); // // 查找所有的parent-box Dom下的child-box Dom
                    const childIndex = Array.from(allChildDom).indexOf(e.item.closest('.child-box')); // 当前child-box index
                    const grandchildIndex = e.newIndex; // 当前grandchild最新的index
                    // console.log("parentIndex",parentIndex)
                    // console.log("childIndex",childIndex)
                    // console.log("grandchildIndex",grandchildIndex)
                    const targetRow = sortData.value[parentIndex].children[childIndex].grandchild.splice(e.oldIndex, 1)[0];
                    sortData.value[parentIndex].children[childIndex].grandchild.splice(grandchildIndex, 0, targetRow); // 更新sortData
                    // console.log(JSON.stringify(sortData.value));
                    putSortData(sortData.value)
                });
            }
        });
    });

    // 当子节点排序时触发
    parentContainers.forEach((container, index) => {
        new Sortable(container.querySelector('.child-list'), {
            group: `parent-${index}`,
            sort: true,
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: (e: ParentDropEndType) => {
                nextTick(() => {
                    const allParentDom = document.querySelectorAll('.parent-box');
                    const parentIndex = Array.from(allParentDom).indexOf(e.item.closest('.parent-box'));
                    const childIndex = e.newIndex;
                    const targetRow = sortData.value[parentIndex].children.splice(e.oldIndex, 1)[0];
                    sortData.value[parentIndex].children.splice(childIndex, 0, targetRow);
                    putSortData(sortData.value)
                });
            }
        });
    });

    // 当父节点排序时触发
    new Sortable(document.querySelector('.parent-list'), {
        group: 'parent',
        sort: true,
        animation: 300,
        ghostClass: 'sortable-ghost',
        onEnd: (e: DropEndType) => {
            nextTick(() => {
                const targetRow = sortData.value.splice(e.oldIndex, 1)[0];
                sortData.value.splice(e.newIndex, 0, targetRow);
                putSortData(sortData.value)
            });
        }
    });
};


onBeforeMount(async () => {
    setTimeout(() => {
        setSort();// 设置排序
    }, 1000);
    fetch(storee.host+'/test_order', {
        method: 'GET'
    })
        .then((response) => response.json())
        .then((data) => {
            sortData.value = data;
        })
        .catch((error) => {
            console.log('error', '请求错误！', error);
        });
});
</script>

<style lang="scss" scoped>
.parent-list {
    margin-top: 20px;
    .parent-name {
        padding: 10px;
        font: 1.5em sans-serif;
        margin-top: 20px;
        cursor: move;
    }
}
.child-list {
    padding-left: 20px;
    .child-name {
        font: 1.5em sans-serif;
        margin-top: 10px;
        cursor: move;
    }
}
.grandchild-list {
    padding-left: 30px;
    .grandchild-name {
        font: 1.5em sans-serif;
        margin-top: 10px;
        cursor: move;
    }
}
// .fade-enter-active, .fade-leave-active {
//   transition: opacity 0.5s;
// }
// .fade-enter, .fade-leave-to {
//   opacity: 0;
// }
</style>
