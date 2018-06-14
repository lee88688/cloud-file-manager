
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
