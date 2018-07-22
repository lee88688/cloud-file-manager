<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="#">Cloudr</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto" style="width: 100%;">
                    <li class="nav-item active mr-auto">
                        <a class="nav-link" href="javascript:void(0);">Home
                            <span class="sr-only">(current)</span>
                        </a>
                    </li>
                    <li>
                        <div class="input-group">
                            <input id="search-content" v-model="searchContent" class="form-control" type="search" aria-label="Search">
                            <div class="input-group-append">
                                <button class="btn btn-secondary" v-on:click="searchClick">搜索</button>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="contianer-fluid">
            <div class="row ml-0 mr-0">
                <div class="col-md-2 d-none d-md-block bg-light">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="javascript:void(0);"><i class="li-icon mdi mdi-folder-multiple mr-2"></i>全部文件</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="javascript:void(0);"><i class="li-icon mdi mdi-image-multiple mr-2"></i>图片</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="javascript:void(0);"><i class="li-icon mdi mdi-note-multiple mr-2"></i>文档</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="javascript:void(0);"><i class="li-icon mdi mdi-video-4k-box mr-2"></i>视频</a>
                        </li>
                    </ul>
                </div>
                <div class="col-md-10" style="font-size: 0.9rem;">
                    <div class="clearfix pt-2 pb-2">
                        <button type="button" class="btn btn-primary mr-1 small-font-size-radius" data-toggle="modal" data-target="#upload-modal">
                            <i class="mdi mdi-upload btn-icon"></i>上传
                        </button>
                        <button type="button" class="btn btn-secondary mr-1 small-font-size-radius" v-on:click="showNewDirectoryModal = !showNewDirectoryModal">
                            <i class="mdi mdi-folder-plus btn-icon"></i>新建文件夹
                        </button>
                        <button type="button" class="btn btn-secondary mr-1 small-font-size-radius" v-on:click="showOfflineDownloadModal = !showOfflineDownloadModal">离线下载</button>
                        <Select-Tool mode="normal"/>
                    </div>

                    <breadcrumb/>

                    <div>
                        <ul class="list-group-flush row ml-0 mr-0 pl-0 mb-0">
                            <li class="list-group-item list-group-item-action col-7 bottom-border">
                                <input type="checkbox" class="mr-1 checkbox" id="select-all-checkbox" v-on:change="selectAllCheckbox">
                                <span>文件名</span>
                            </li>
                            <li class="list-group-item list-group-item-action col-2 bottom-border">
                                大小
                            </li>
                            <li class="list-group-item list-group-item-action col-3 bottom-border">
                                修改日期
                            </li>
                        </ul>

                        <File-List-Container/>
                    </div>
                </div>
            </div>
        </div>

        <!-- Upload Modal -->
        <Upload-Modal v-bind:show.sync="showUploadModal"/>

        <!-- Comfirm delete Modal -->
        <Comfirm-Delete-Modal/>

        <!-- New Directory Modal -->
        <New-Directory-Modal v-bind:show.sync="showNewDirectoryModal"/>

        <!-- Rename Modal -->
        <Rename-Modal/>

        <!-- Offline Download Modal -->
        <Offline-Download-Modal v-bind:show.sync="showOfflineDownloadModal"/>

        <Message-Notification/>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import breadcrumb from './components/breadcrumb'
import UploadModal from './components/UploadModal'
import RenameModal from './components/RenameModal'
import NewDirectoryModal from './components/NewDirectoryModal'
import ComfirmDeleteModal from './components/ComfirmDeleteModal'
import FileListContainer from './components/FileListContainer'
import OfflineDownloadModal from './components/OfflineDownloadModal'
import MessageNotification from './components/MessageNotification'
import SelectTool from './components/SelectTool'

function selectAllCheckbox(event) {
    let value = event.target.checked
    this.$store.dispatch('selectAll', { value })
    let list = document.querySelectorAll(
        '.list-container input[type="checkbox"]'
    )
    for (let item of list.values()) {
        item.checked = value
    }
}

async function searchClick(event) {
    let path = this.path
    let query = this.searchContent
    this.search({ query, path })
}

export default {
    name: 'App',
    components: {
        breadcrumb,
        UploadModal,
        RenameModal,
        NewDirectoryModal,
        ComfirmDeleteModal,
        FileListContainer,
        OfflineDownloadModal,
        MessageNotification,
        SelectTool
    },
    methods: {
        ...mapActions(['search']),
        selectAllCheckbox,
        searchClick
    },
    computed: {
        ...mapState(['path'])
    },
    data() {
        return {
            searchContent: '',
            showNewDirectoryModal: false,
            showOfflineDownloadModal: false,
            showUploadModal: false
        }
    }
}
</script>

<style>

html,
body {
    height: 100%;
    width: 100%;
    overflow: hidden;
}

div.contianer-fluid {
    width: 100%;
}

div.contianer-fluid > div {
    width: 100%;
}

.small-font-size-radius {
    font-size: 0.9rem;
    border-radius: 0.1rem;
}

.list-container {
    overflow: auto;
}

.bottom-border {
    border-top: 0px;
    border-left: 0px;
    border-right: 0px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125) !important;
    margin-bottom: -1px !important;
}

.checkbox {
    min-width: 32px;
}

.file-list-item {
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 1px;
    padding-left: 0px;
    padding-right: 0px;
}

.file-list-item > div {
    padding-left: 20px;
    padding-right: 20px;
}

.upload-box {
    text-align: center;
    border: 2px dashed #bbb;
    border-radius: 5px;
    margin-left: 10px;
    margin-right: 10px;
    color: #bbb;
}

.btn-icon {
    height: 1rem;
    width: 1rem;
    font-size: 1rem;
    line-height: 1rem;
    vertical-align: text-bottom;
}

.li-icon {
    font-size: 1.5rem;
    height: 1.5rem;
    line-height: 1.5rem;
    vertical-align: text-bottom;
    margin-right: 0.3rem;
}

.li-btn-icon {
    font-size: 1.2rem;
    height: 1.2rem;
    width: 1.2rem;
    line-height: 1.2rem;
    vertical-align: text-bottom;
}
</style>
