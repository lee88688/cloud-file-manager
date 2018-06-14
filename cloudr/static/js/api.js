
let GET_PATH_CONTENT = "/api/get-path-content";
let DELETE_RESOURCE = "/api/delete-resource";
let NEW_DIRECTORY = "/api/new-directory";
let RENAME_RESOURCE = "/api/rename-resource";


function makePromiseRequest(method, url, formData) {
    return new Promise(function(resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
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
        xhr.send(formData);
    });
}


async function apiGetPathContent(path) {
    let formData = new FormData();

    // formData.append("username", userName);
    formData.append("path", path);
    let responseJSON = await makePromiseRequest("POST", GET_PATH_CONTENT, formData);
    let response = JSON.parse(responseJSON);
    if(response.result === 'success') {
        return response.files;
    }
}