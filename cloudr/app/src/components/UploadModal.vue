<template>
    <div class="modal fade" id="upload-modal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modal-title">上传文件</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>

                <div class="modal-body">
                    <form id="upload-form" action="/api/uploads" method="POST" enctype="multipart/form-data">
                        <div class="form-group row" style="margin-left: 0px; margin-right: 0px;">
                            <input id="upload-input" v-on:change="getFileName()" type="file" class="form-control-file" name="file" style="display: none;">
                            <label class="col col-form-label upload-box" v-on:click="uploadInputClick()">{{ fileName }}</label>
                        </div>
                    </form>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" v-on:click="uploadFile()">上传</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'
import md5 from 'js-md5'
import { makeFormDataPromiseRequest } from '../lib/api'

function uploadInputClick() {
    let uploadInput = document.getElementById("upload-input")
    uploadInput.click()
}

function getFileName() {
    let uploadInput = document.getElementById("upload-input")
    if (uploadInput.files.length >= 1) {
        this.fileName = uploadInput.files[0].name
    }
    else {
        this.fileName = "点击选择文件"
    }
}

function uploadFile() {
    let uploadInput = document.getElementById("upload-input")
    let fd = new FormData(document.getElementById("upload-form"))
    if (uploadInput.files.length === 0) {
        alert("未选择文件，请重试！")
        return
    }

    let file = uploadInput.files[0]
    let self = this
    fd.append("userid", 1)
    fd.append("filesize", file.size)
    fd.append("path", this.$store.state.path)

    let reader = new FileReader()
    reader.onload = function(event) {
        let md5Result = md5(event.target.result)
        fd.append("md5", md5Result)
        makeFormDataPromiseRequest("POST", "/file/uploads", fd).then((value) => {
            if (value.result === "success") {
                self.$store.dispatch("getCurrentPathContent")
                $("#upload-modal").modal("hide")
            }
        })
    }

    reader.readAsArrayBuffer(file)
}

export default {
    data() {
        return {
            fileName: "点击选择文件"
        }
    },
    methods: {
        uploadInputClick,
        getFileName,
        uploadFile
    }
}
</script>
