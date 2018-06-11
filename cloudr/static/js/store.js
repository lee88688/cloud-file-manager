const store = new Vuex.Store({
    state: {
        path: '/',
    },
    getters: {
        pathNameArray(state) {
            if(state.path === '/') {
                return ["Home"];
            }

            let paths = state.path.split('/');
            paths[0] = 'Home'
            return paths;
        }
    },
    mutations: {
        enterDir(state, { dirName }) {
            if(state.path.endsWith('/')) {
                state.path += dirName;
            }
            else {
                state.path += ('/' + dirName);
            }
        },
        enterParentDir(state, { parentDirName, index }) {
            if(state.path !== '/') {
                let path = state.path.toString();
                let nameArr = path.split('/');
                parentDirName = parentDirName.replace(/\//g, "");  // remove / in upperDirName
                if(nameArr[index] === parentDirName) {
                    path = nameArr.slice(0, index + 1).join('/');
                    path = (path === "") ? "/" : path;
                    state.path = path;
                }
            }
        }
    }
});