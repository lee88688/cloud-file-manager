<template>
    <div class="list-container" style="height: 1px;" id="file-list-container" v-on:click="clickProxy($event)">
        <ul class="list-group-flush ml-0 mr-0 pl-0 mb-0">
            <file-list-item v-for="(item, index) in items"
                            v-bind:item="item"
                            v-bind:key="item.fileType + item.fileName"
                            v-bind:id="index"
            ></file-list-item>
        </ul>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import FileListItem from './FileListItem'
import $ from 'jquery'

const CLICKTYPE = {
    CHECKBOX: "checkbox",
    SHARE: "share",
    DOWNLOAD: "download",
    MOVE: "move",
    COPY: "copy",
    RENAME: "rename",
    DELETE: "delete",
    SETSHARE: "setshare",
    NAME: "name"
}

function deleteItems(store, path, fileList, indexList) {
    let button = document.getElementById("confirm-delete-button")

    button.onclick = function(event) {
        store.dispatch("deleteFiles", { path, fileList, indexList })
        $("#confirm-delete").modal("hide")
    }
    $("#confirm-delete").modal("show")
}

function renameItem(store, path, oldName, index) {
    let button = document.getElementById("rename-button")

    button.onclick = function(event) {
        let newName = document.getElementById("rename-input").value
        store.dispatch("rename", {path, oldName, newName, index})
        $("#rename").modal("hide")
    }
    $("#rename").modal("show")
}

function clickCheckbox(store, index, value) {
    if (value === false) {
        let allCheckbox = document.getElementById("select-all-checkbox")
        if (allCheckbox.checked === true) {
            allCheckbox.checked = false
        }
    }
    store.dispatch("selectOne", {index, value})
}

function clickName(store, dirName) {
    store.dispatch("enterDir", {dirName})
}

function clickProxy(event) {
    let id = event.target.id
    if (!id.startsWith("list-item")) {
        return
    }

    let clickTypeArray = id.split("-")
    let clickType = clickTypeArray[2]
    let index = parseInt(clickTypeArray[clickTypeArray.length - 1])
    let fileName = this.items[index].fileName
    let fileType = this.items[index].fileType
    let store = this.$store

    switch (clickType) {
        case CLICKTYPE.CHECKBOX: {
            clickCheckbox(store, index, event.target.checked)
            break
        }
        case CLICKTYPE.COPY:
            break
        case CLICKTYPE.DELETE: {
            let path = this.path
            let indexList = [index]
            let fileList = [fileName]
            deleteItems(store, path, fileList, indexList)
            break
        }
        case CLICKTYPE.DOWNLOAD:
            break
        case CLICKTYPE.MOVE:
            break
        case CLICKTYPE.NAME: {
            if (fileType === "directory") {
                clickName(store, fileName)
            }
            break
        }
        case CLICKTYPE.RENAME: {
            let path = this.path
            let oldName = fileName
            renameItem(store, path, oldName, index)
            break
        }
        case CLICKTYPE.SETSHARE:
            break
        case CLICKTYPE.SHARE:
            break
        default:
            break
    }
}

export default {
    components: {
        FileListItem
    },
    computed: {
        ...mapState({
            items: 'files',
            path: 'path'
        })
    },
    methods: {
        clickProxy
    },
    mounted() {
        this.$store.dispatch("getCurrentPathContent")
    }
}
</script>
