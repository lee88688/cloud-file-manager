<template>
    <div class="modal fade" id="offline-download" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="rename-title">离线下载</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <ul class="nav nav-tabs" id="download-tab" role="tablist">
                        <li class="nav-item">
                            <a id="url-download" class="nav-link active" href="#url-download-content" role="tab" data-toggle="tab">新建链接任务</a>
                        </li>
                        <li class="nav-item">
                            <a id="bt-download" class="nav-link" href="#bt-download-content" role="tab" data-toggle="tab">新建BT任务</a>
                        </li>
                    </ul>
                    <div class="tab-content" id="download-tab-content">
                        <div class="tab-pane fade show active" id="url-download-content" role="tabpanel" aria-labelledby="url-download">
                            <form>
                                <div class="form-group">
                                    <label>文件链接：</label>
                                    <input id="offline-download-url" type="text" class="form-control">
                                    <small class="form-text text-muted">
                                        支持HTTP/FTP/SFTP
                                    </small>
                                    <br/>
                                    <label>保存到：{{ formatPath }}</label>
                                </div>
                            </form>
                        </div>
                        <div class="tab-pane fade" id="bt-download-content" role="tabpanel" aria-labelledby="bt-download">
                            <p>BT</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" id="rename-button" v-on:click="postOfflineDownload()">确定</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'
import { mapGetters, mapState } from 'vuex'
import { apiPostOfflineDownload } from '../lib/api'

export default {
    props: ['show'],
    watch: {
        show: function() {
            $('#offline-download').modal('show')
        }
    },
    computed: {
        ...mapGetters([
            'formatPath'
        ]),
        ...mapState([
            'path'
        ])
    },
    methods: {
        async postOfflineDownload() {
            let url = document.getElementById('offline-download-url').value
            let path = this.path
            let response = await apiPostOfflineDownload(path, url)
            if (response.result === 'success') {
                $('#offline-download').modal('hide')
            }
        }
    }
}
</script>
