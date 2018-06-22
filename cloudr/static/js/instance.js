
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

function renameItem(path, oldName, index) {
    let button = document.getElementById("rename-button");

    button.onclick = function(event) {
        let newName = document.getElementById("rename-input").value;
        store.dispatch("rename", {path, oldName, newName, index});
        $("#rename").modal("hide");
    }
    $("#rename").modal("show");
}

function clickCheckbox(index, value) {
    if(value === false) {
        let allCheckbox = document.getElementById("select-all-checkbox");
        if(allCheckbox.checked === true) {
            allCheckbox.checked = false;
        }
    }
    store.dispatch("selectOne", {index, value});
}

function clickName(dirName) {
    store.dispatch("enterDir", {dirName});
}

function clickProxy(event) {
    let id = event.target.id;
    if(!id.startsWith("list-item")) {
        return;
    }
    
    let clickTypeArray = id.split("-");
    let clickType = clickTypeArray[2];
    let index = parseInt(clickTypeArray[clickTypeArray.length - 1]);
    let fileName = this.items[index].fileName;
    let fileType = this.items[index].fileType;

    switch(clickType) {
        case CLICKTYPE.CHECKBOX: {
            clickCheckbox(index, event.target.checked);
            break;
        }
        case CLICKTYPE.COPY:
            break;
        case CLICKTYPE.DELETE: {
            let path = this.path;
            let indexList = [index];
            let fileList = [fileName];
            deleteItems(path, fileList, indexList);
            break;
        }
        case CLICKTYPE.DOWNLOAD:
            break;
        case CLICKTYPE.MOVE:
            break;
        case CLICKTYPE.NAME: {
            if(fileType === "directory"){
                clickName(fileName);
            }
            break;
        }
        case CLICKTYPE.RENAME: {
            let path = this.path;
            let oldName = fileName;
            renameItem(path, oldName, index);
            break;
        }
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
        store.dispatch("getCurrentPathContent");
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
    fd.append("path", store.state.path);
    
    let reader = new FileReader();
    reader.onload = function(event) {
        let md5Result = md5(event.target.result);
        fd.append("md5", md5Result);
        console.log(event);
        console.log(fd);
        makeFormDataPromiseRequest("POST", "/file/uploads", fd).then((value) => {
            if(value.result === "success") {
                store.dispatch("getCurrentPathContent");
                $("#upload-modal").modal("hide");
            }
        });
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
