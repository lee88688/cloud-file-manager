
function resizeListContainer(event) {
    var listContainer = document.querySelector(".list-container");
    var rec = listContainer.getBoundingClientRect();
    var pageHeight = window.innerHeight;
    listContainer.style.height = (pageHeight - rec.top) + "px";
};

window.onresize = resizeListContainer;

$(document).ready(function () {
    resizeListContainer();

    let newDirButton = document.getElementById("new-directory-button");
    newDirButton.onclick = function(event) {
        let inputDirName = document.getElementById("new-dir-name");
        let dirName = inputDirName.value;
        let path = store.state.path;
        store.dispatch("newDirectory", { dirName, path });
        $("#new-directory").modal("hide");
    };
});