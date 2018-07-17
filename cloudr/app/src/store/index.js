import Vue from 'vue'
import Vuex from 'vuex'
import { apiDeleteResource, apiGetPathContent, apiNewDirectory, apiRenameResource, apiPasteFiles } from "../lib/api"

Vue.use(Vuex)

export const store = new Vuex.Store({
    state: {
        path: '/',
        files: [],
        select: [],
        notification: [], // notification message like {level: 'info', content: 'this is a info'}
        operateFiles: [] // this array includes the selected operate files
    },
    getters: {
        pathNameArray(state) {
            if (state.path === '/') {
                return ['Home']
            }

            let paths = state.path.split('/')
            paths[0] = 'Home'
            return paths
        },
        isFileItemSelected({ select }) {
            return select.every((v) => !v)
        },
        formatPath(state, { pathNameArray }) {
            return pathNameArray.join('/')
        },
        hasMessage({ notification }) {
            return (notification.length > 0)
        },
        firstMessage({ notification }) {
            return notification[0]
        }
    },
    mutations: {
        enterDir(state, { dirName }) {
            if (state.path.endsWith('/')) {
                state.path += dirName
            }
            else {
                state.path += ('/' + dirName)
            }
        },
        enterParentDir(state, { parentDirName, index }) {
            if (state.path !== '/') {
                let path = state.path.toString()
                let nameArr = path.split('/')
                nameArr[0] = 'Home'
                parentDirName = parentDirName.toString().replace(/\//g, '') // remove / in upperDirName
                if (nameArr[index] === parentDirName) {
                    path = nameArr.slice(0, index + 1).join('/')
                    path = path.startsWith('Home') ? path.replace('Home', '') : path
                    path = (path === '') ? '/' : path
                    state.path = path
                }
            }
        },
        changeFiles({ files, select }, { newFiles }) {
            let length = files.length > newFiles.length ? files.length : newFiles.length
            newFiles.sort(compareFileName)
            files.splice(0, length, ...newFiles)
            select.splice(0, length, ...getFalseIter(newFiles.length))
        },
        deleteFiles({ files }, { indexList }) {
            indexList.sort().reverse()
            for (let index of indexList) {
                files.splice(index, 1)
            }
        },
        addDir({ files }, { file }) {
            files.push(file)
        },
        rename({ files }, { newName, index }) {
            let file = files[index]
            file.fileName = newName
            files.splice(index, 1, file)
        },
        selectOne({ select }, { index, value }) {
            if (typeof (value) !== 'boolean') {
                throw TypeError('Value must be boolean.')
            }
            select.splice(index, 1, value)
        },
        selectAll({ select }, { value }) {
            if (typeof (value) !== 'boolean') {
                throw TypeError('Value must be boolean.')
            }
            if (value === true) {
                select.splice(0, select.length, ...getTrueIter(select.length))
            }
            else {
                select.splice(0, select.length, ...getFalseIter(select.length))
            }
        },
        pushMessage({ notification }, payload) {
            notification.push(payload)
        },
        deleteLatestMessage({ notification }) {
            if (notification.length > 0) {
                notification.shift()
            }
        },
        modifyOperateFiles({ operateFiles }, { files }) {
            let length = operateFiles.length > files.length ? operateFiles.length : files.length
            if (files.length > 0) {
                operateFiles.splice(0, length, ...files)
            }
            else {
                operateFiles.splice(0, length)
            }
        }
    },
    actions: {
        enterDir(context, payload) {
            context.commit('enterDir', payload)
            context.dispatch('getCurrentPathContent')
        },
        enterParentDir(context, payload) {
            context.commit('enterParentDir', payload)
            context.dispatch('getCurrentPathContent')
        },
        async getCurrentPathContent(context) {
            let path = context.state.path
            let response = await apiGetPathContent(path)
            let newFiles = response.files
            context.commit('changeFiles', { newFiles })
        },
        async deleteFiles(context, {path, fileList, indexList}) {
            let response = await apiDeleteResource(path, fileList)
            if (response.result === 'success') {
                context.commit('deleteFiles', { indexList })
            }
        },
        async newDirectory(context, {path, dirName}) {
            let response = await apiNewDirectory(path, dirName)
            if (response.result === 'success') {
                context.commit('addDir', { file: response.file })
            }
        },
        async rename(context, {path, oldName, newName, index}) {
            let response = await apiRenameResource(path, oldName, newName)
            if (response.result === 'success') {
                context.commit('rename', { newName, index })
            }
        },
        selectOne(context, payload) {
            context.commit('selectOne', payload)
        },
        selectAll(context, payload) {
            context.commit('selectAll', payload)
        },
        publishMessage({ commit, dispatch }, payload) {
            commit('pushMessage', payload)
            setTimeout(() => dispatch('deleteLatestMessage'), 5000)
        },
        deleteLatestMessage({ commit }) {
            commit('deleteLatestMessage')
        },
        modifyOperateFiles({ commit, dispatch }, payload) {
            commit('modifyOperateFiles', payload)
        },
        async pasteFiles({ dispatch }, { fileNames, path, newPath }) {
            let response = await apiPasteFiles(fileNames, path, newPath)
            return response
        }
    }
})

const fileType = ['directory', 'image', 'video', 'audio', 'document', 'zip', 'other']

function compareString(str1, str2) {
    if (str1 > str2) {
        return 1
    }
    else if (str1 < str2) {
        return -1
    }
    else {
        return 0
    }
}

function compareFileName(f1, f2) {
    if (f1.fileType === 'directory' && f2.fileType !== 'directory') {
        return 1
    }
    else if (f1.fileType !== 'directory' && f2.fileType === 'directory') {
        return -1
    }
    else {
        return compareString(f1.fileName, f2.fileName)
    }
}

function compareFileNameWithTime(f1, f2) {
    if (f1.fileType === 'directory' && f2.fileType === 'directory') {
        return compareString(f1.modifiedTime, f2.modifiedTime)
    }
    else if (f1.fileType === 'directory' && f2.fileType !== 'directory') {
        return 1
    }
    else if (f1.fileType !== 'directory' && f2.fileType === 'directory') {
        return -1
    }
    else {
        let rv = compareString(f1.modifiedTime, f2.modifiedTime)
        if (rv === 0) {
            return compareString(f1.fileName, f2.fileName)
        }

        return rv
    }
}

function compareFileNameWithSize(f1, f2) {
    if (f1.fileType === 'directory' && f2.fileType !== 'directory') {
        return 1
    }
    else if (f1.fileType !== 'directory' && f2.fileType === 'directory') {
        return -1
    }
    else {
        let rv = compareString(f1.fileSize, f2.fileSize)
        if (rv === 0) {
            return compareString(f1.fileName, f2.fileName)
        }

        return rv
    }
}

function* getFalseIter(length) {
    for (let i = 0; i < length; i++) {
        yield false
    }
}

function* getTrueIter(length) {
    for (let i = 0; i < length; i++) {
        yield true
    }
}
