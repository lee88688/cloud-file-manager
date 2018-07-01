<template>
    <li v-bind:id="'list-item-' + id"
        v-on:mouseenter="fileListMouseEnter($event.target)"
        v-on:mouseleave="fileListMouseLeave($event.target)"
        class="list-group-item list-group-item-action bottom-border d-flex file-list-item">
        <div class="col-7">
            <input type="checkbox" class="mr-1 checkbox" v-bind:id="'list-item-checkbox-' + id">
            <span>
                <i v-bind:class="['mdi', 'li-icon', icon]"></i>
                <a href="javascript:void(0);" v-bind:id="'list-item-name-' + id">{{ item.fileName }}</a>
            </span>
            <div class="float-right" style="display: none;">
                <span>
                    <a href="javascript:void(0);" v-bind:id="'list-item-share-' + id">
                        <i class="mdi mdi-share-variant li-btn-icon"></i>
                    </a>
                </span>
                <span>
                    <a href="javascript:void(0);" v-bind:id="'list-item-download-' + id">
                        <i class="mdi mdi-download li-btn-icon"></i>
                    </a>
                </span>
                <span>
                    <a href="javascript:void(0);" v-bind:id="'list-item-more-' + id" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="mdi mdi-dots-horizontal li-btn-icon"></i>
                    </a>
                    <div class="dropdown-menu" v-bind:aria-labelledby="'list-item-more-' + id" style="font-size: 0.9rem;">
                        <button class="dropdown-item" type="button" v-bind:id="'list-item-move-' + id">移动</button>
                        <button class="dropdown-item" type="button" v-bind:id="'list-item-copy-' + id">复制</button>
                        <button class="dropdown-item" type="button" v-bind:id="'list-item-rename-' + id">重命名</button>
                        <button class="dropdown-item" type="button" v-bind:id="'list-item-delete-' + id">删除</button>
                        <button class="dropdown-item" type="button" v-bind:id="'list-item-setshare-' + id">设置共享</button>
                    </div>
                </span>
            </div>
        </div>
        <div class="col-2">{{ formatFileSize(item.fileSize, item.fileType) }}</div>
        <div class="col-3">{{ item.modifiedTime }}</div>
    </li>
</template>

<script>
import { getIcon } from '../lib/icons'

const KB = 1024
const MB = KB * 1024
const GB = MB * 1024

function formatUnit(size, divisor, unit) {
    if (size < 0) {
        throw RangeError("Size may not be a negative number.")
    }
    return (size / divisor).toFixed(1) + unit
}

function formatFileSize(size, fileType) {
    if (fileType === "directory") {
        return "-"
    }

    if (size < KB) {
        return size + "B"
    }
    else if (size >= KB && size < MB) {
        return formatUnit(size, KB, "K")
    }
    else if (size >= MB && size < GB) {
        return formatUnit(size, MB, "M")
    }
    else {
        return formatUnit(size, GB, "G")
    }
}

function fileListMouseEnter(element) {
    var operateButton = element.querySelector(".float-right")
    operateButton.style.display = "inline"
}

function fileListMouseLeave(element) {
    var operateButton = element.querySelector(".float-right")
    operateButton.style.display = "none"
}

export default {
    props: ["id", "item"],
    methods: {
        fileListMouseEnter,
        fileListMouseLeave,
        formatFileSize
    },
    computed: {
        icon() {
            return getIcon(this.item.fileName, this.item.fileType)
        }
    }
}
</script>
