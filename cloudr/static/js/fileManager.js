
function resizeListContainer(event) {
    var listContainer = document.querySelector(".list-container");
    var rec = listContainer.getBoundingClientRect();
    var pageHeight = window.innerHeight;
    listContainer.style.height = (pageHeight - rec.top) + "px";
};

window.onresize = resizeListContainer;

$(document).ready(function () {
    resizeListContainer();
});