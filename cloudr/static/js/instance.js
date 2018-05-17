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

var vm_breadcrumb = new Vue({
    el: "#path-nav",
    data: {
        paths: ["Home", "Library", "Data"]
    }
});
