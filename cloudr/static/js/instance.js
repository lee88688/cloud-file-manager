var vm_file_list = new Vue({
    el: "#file-list-container",
    data: {
        items: [
            {
                id: 0, 
                fileName: "我的文件", 
                fileSize: "-", 
                modifiedTime: "2014-06-20 15:06"
            }, 
            {
                id: 0, 
                fileName: "我的资源", 
                fileSize: "-", 
                modifiedTime: "2014-06-20 15:06"
            }
        ]
    }
});

var vmBreadcrumb = new Vue({
    el: "#path-nav",
    data: {
        paths: ["Home", "Library", "Data"]
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

var vmUploadModal = new Vue({
    el: "#upload-modal",
    data: {
        fileName: "点击选择文件"
    },
    methods: {
        uploadInputClick,
        getFileName
    }
});
