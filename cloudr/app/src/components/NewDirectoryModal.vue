<template>
    <div class="modal fade" id="new-directory" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5>添加目录</h5>
                </div>
                <div class="modal-body">
                    <form class="input-group" id="new-directory-form">
                        <div class="input-group-append">
                            <span class="input-group-text">目录名称：</span>
                        </div>
                        <input type="text" id="new-dir-name" class="form-control" name="dirName">
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" id="new-directory-button" v-on:click="newDirectory">确定</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'

export default {
    methods: {
        newDirectory(event) {
            let inputDirName = document.getElementById("new-dir-name")
            let dirName = inputDirName.value
            let path = this.$store.state.path
            if (!dirName) {
                return
            }
            this.$store.dispatch("newDirectory", { dirName, path })
            $("#new-directory").modal("hide")
        }
    }
}
</script>
