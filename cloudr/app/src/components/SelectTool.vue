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
    props: [],
    computed: {
        ...mapState(['select', 'operateFiles', 'files']),
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
        ...mapActions(['modifyOperateFiles']),
        pushOperateFiles() {
            let files = []
            for (let i = 0; i < this.select.length; i++) {
                if (this.select[i]) {
                    files.push(this.files[i])
                }
            }
            this.modifyOperateFiles({ files })
        },
        handleClick(event) {
            let id = event.target.id
            let operate = id.split('-')[1]
            switch (operate) {
                case "move": {
                    console.log("move")
                    this.pushOperateFiles()
                    break
                }
                case "copy": {
                    this.pushOperateFiles()
                    break
                }
                case "delete": {
                    this.pushOperateFiles()
                    break
                }
                case "paste": {
                    break
                }
                case "cancel": {
                    let files = []
                    this.modifyOperateFiles({ files }) // todo: items can not be removed
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
