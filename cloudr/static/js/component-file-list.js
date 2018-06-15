let fileListItemTemplate = `
<li v-bind:id="'list-item-' + id" 
    v-on:mouseenter="fileListMouseEnter($event.target)"
    v-on:mouseleave="fileListMouseLeave($event.target)"
    class="list-group-item list-group-item-action bottom-border d-flex file-list-item">
    <div class="col-7">
        <input type="checkbox" class="mr-1 checkbox" v-bind:id="'list-item-checkbox-' + id">
        <span>
            <a href="javascript:void(0);" v-bind:id="'list-item-name-' + id">{{ item.fileName }}</a>
        </span>
        <div class="float-right" style="display: none;">
            <span>
                <a href="javascript:void(0);" v-bind:id="'list-item-share-' + id">分享</a>
            </span>
            <span>
                <a href="javascript:void(0);" v-bind:id="'list-item-download-' + id">下载</a>
            </span>
            <span>
                <a href="javascript:void(0);" v-bind:id="'list-item-more-' + id" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">更多</a>
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
    <div class="col-2">{{ item.fileSize }}</div>
    <div class="col-3">{{ item.modifiedTime }}</div>
</li>
`;

function fileListMouseEnter(element) {
    var operateButton = element.querySelector(".float-right");
    operateButton.style.display = "inline";
}

function fileListMouseLeave(element) {
    var operateButton = element.querySelector(".float-right");
    operateButton.style.display = "none";
}

Vue.component('file-list-item', {
    template: fileListItemTemplate,
    props: ["id", "item"],
    methods: {
        fileListMouseEnter,
        fileListMouseLeave
    }
});

