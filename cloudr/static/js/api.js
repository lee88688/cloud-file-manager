
let GET_PATH_CONTENT = "/api/get-path-content";
let DELETE_RESOURCE = "/api/delete-resource";
let NEW_DIRECTORY = "/api/new-directory";
let RENAME_RESOURCE = "/api/rename-resource";


function makePromiseRequest(method, url, data) {
    return new Promise(function(resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.responseType = "json";
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onload = function() {
            if(this.status >= 200 && this.status < 300) {
                resolve(this.response);
            }
            else {
                reject({
                    status: this.status,
                    statusText: this.statusText,
                    result: "failure"
                });
            }
        };
        xhr.onerror = function() {
            reject({
                status: this.status,
                statusText: this.statusText,
                result: "failure"
            });
        };
        xhr.send(data);
    });
}


async function apiGetPathContent(path) {
    let data = {};
    data["path"] = path;
    let response = await makePromiseRequest("POST", GET_PATH_CONTENT, JSON.stringify(data));
    return response;
}

async function apiDeleteResource(path, fileList) {
    let data =  {path, fileList};
    let response = await makePromiseRequest("POST", DELETE_RESOURCE, JSON.stringify(data));
    return response;
}

async function apiNewDirectory(path, dirName) {
    let data = {path, dirName};
    let response = await makePromiseRequest("POST", NEW_DIRECTORY, JSON.stringify(data));
    return response;
}

async function apiRenameResource(path, oldname, newname) {
    let data = {path, oldname, newname};
    let response = await makePromiseRequest("POST", RENAME_RESOURCE, JSON.stringify(data));
    return response;
}