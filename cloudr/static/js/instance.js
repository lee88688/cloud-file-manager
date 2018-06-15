
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
};

function deleteItems(path, fileList, indexList) {
    let button = document.getElementById("confirm-delete-button");

    button.onclick = function(event) {
        store.dispatch("deleteFiles", { path, fileList, indexList });
        $("#confirm-delete").modal("hide");
    };
    $("#confirm-delete").modal("show");
}

function clickProxy(event) {
    let id = event.target.id;
    if(!id.startsWith("list-item")) {
        return;
    }
    
    let clickTypeArray = id.split("-");
    let clickType = clickTypeArray[2];
    let index = parseInt(clickTypeArray[clickTypeArray.length - 1]);

    switch(clickType) {
        case CLICKTYPE.CHECKBOX:
            break;
        case CLICKTYPE.COPY:
            break;
        case CLICKTYPE.DELETE: {
            let path = this.path;
            let indexList = [index];
            let fileList = [this.items[index].fileName];
            deleteItems(path, fileList, indexList);
            break;
        }
        case CLICKTYPE.DOWNLOAD:
            break;
        case CLICKTYPE.MOVE:
            break;
        case CLICKTYPE.NAME:
            break;
        case CLICKTYPE.RENAME:
            break;
        case CLICKTYPE.SETSHARE:
            break;
        case CLICKTYPE.SHARE:
            break;
        default:
            break;
    }
}

var vmFileList = new Vue({
    el: "#file-list-container",
    store,
    data: {
    },
    computed: {
        ...Vuex.mapState({
            items: "files",
            path: "path",
        }),
    },
    methods: {
        clickProxy,
    },
    mounted() {
        let path = this.path;
        store.dispatch("getCurrentPathContent", { path });
    }
});

var vmBreadcrumb = new Vue({
    el: "#path-nav",
    store,
    data: {
    },
    computed: {
        ...Vuex.mapGetters({
            paths: 'pathNameArray'
        })
    }
});


function uploadInputClick() {
    let uploadInput = document.getElementById("upload-input");
    uploadInput.click();
}

function getFileName() {
    let uploadInput = document.getElementById("upload-input");
    if(uploadInput.files.length >= 1) {
        this.fileName = uploadInput.files[0].name;
    }
    else{
        this.fileName = "点击选择文件";        
    }
}

function upload_file() {
    let uploadInput = document.getElementById("upload-input");
    let fd = new FormData(document.getElementById("upload-form"));
    if(uploadInput.files.length === 0) {
        alert("未选择文件，请重试！");
        return;
    }

    let file = uploadInput.files[0];
    fd.append("userid", 1);
    fd.append("filesize", file.size);
    fd.append("path", "/");
    
    let reader = new FileReader();
    reader.onload = function(event) {
        let md5Result = md5(event.target.result);
        fd.append("md5", md5Result);
        console.log(event);
        console.log(fd);
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/file/uploads");
        xhr.send(fd);
    };

    reader.readAsArrayBuffer(file);
}

var vmUploadModal = new Vue({
    el: "#upload-modal",
    data: {
        fileName: "点击选择文件"
    },
    methods: {
        uploadInputClick,
        getFileName,
        upload_file
    }
});
