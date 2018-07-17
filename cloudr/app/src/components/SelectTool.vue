<template>
    <div class="btn-group" @click="handleClick($event)">
        <template v-if="mode === 'normal'">
            <button id="tool-move" class="btn btn-outline-info small-font-size-radius">移动</button>
            <button id="tool-copy" class="btn btn-outline-info small-font-size-radius">复制</button>
            <button id="tool-delete" class="btn btn-outline-info small-font-size-radius">删除</button>
        </template>
        <template v-else-if="mode === 'operate'">
            <button id="tool-paste" class="btn btn-outline-info small-font-size-radius">粘贴</button>
            <button id="tool-cancel" class="btn btn-outline-info small-font-size-radius">取消</button>
        </template>
        <template v-else></template>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    data() {
        return {
            originalPath: '/'
        }
    },
    props: [],
    computed: {
        ...mapState(['select', 'operateFiles', 'files', 'path']),
        mode() {
            if (this.operateFiles.length > 0) {
                return 'operate'
            }
            else if (this.select.some((e) => e)) {
                return 'normal'
            }
            else {
                return 'other'
            }
        }
    },
    methods: {
        ...mapActions(['modifyOperateFiles', 'pasteFiles', 'getCurrentPathContent']),
        pushOperateFiles() {
            let files = []
            for (let i = 0; i < this.select.length; i++) {
                if (this.select[i]) {
                    files.push(this.files[i])
                }
            }
            this.modifyOperateFiles({ files })
        },
        async handleClick(event) {
            let id = event.target.id
            let operate = id.split('-')[1]
            switch (operate) {
                case "move": {
                    console.log("move")
                    this.pushOperateFiles()
                    this.originalPath = this.path
                    break
                }
                case "copy": {
                    this.pushOperateFiles()
                    this.originalPath = this.path
                    break
                }
                case "delete": {
                    this.pushOperateFiles()
                    this.originalPath = this.path
                    break
                }
                case "paste": {
                    let fileNames = []
                    for (let item of this.operateFiles) {
                        fileNames.push(item.fileName)
                    }
                    let payload = {
                        fileNames: fileNames,
                        path: this.originalPath,
                        newPath: this.path
                    }
                    let response = await this.pasteFiles(payload)
                    if (response.result === 'success') {
                        await this.getCurrentPathContent()
                        document.getElementById('tool-cancel').click()
                    }
                    break
                }
                case "cancel": {
                    let files = []
                    this.modifyOperateFiles({ files })
                    let checkallbox = document.getElementById('select-all-checkbox')
                    if (checkallbox.checked === true) {
                        checkallbox.click()
                    }
                    else {
                        checkallbox.click()
                        checkallbox.click()
                    }
                    break
                }
                default:
                    break
            }
        }
    }
}
</script>

<style scoped>

</style>
