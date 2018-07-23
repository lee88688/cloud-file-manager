<template>
    <div class="modal fade" id="img-modal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modal-title">{{ fileName }}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>

                <div class="modal-body" style="text-align: center;">
                    <img v-bind:src="imgUrl" class="img-fluid rounded">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'
import { mapState, mapMutations } from 'vuex'
import { getFileUrl } from '../lib/api'

export default {
    computed: {
        ...mapState({
            fileName: (state) => state.imgModalAttr.fileName,
            show: (state) => state.imgModalAttr.show,
            path: (state) => state.path
        }),
        imgUrl() {
            if (!this.fileName) {
                return ''
            }
            else {
                return getFileUrl(this.path, this.fileName)
            }
        }
    },
    methods: {
        ...mapMutations(['imgModal'])
    },
    watch: {
        show: function() {
            if (this.show) {
                $('#img-modal').modal('show')
            }
            else {
                $('#img-modal').modal('hide')
            }
        }
    },
    mounted: function() {
        $('#img-modal').on('hide.bs.modal', (e) => {
            this.imgModal({ show: false })
        })
    }
}
</script>
