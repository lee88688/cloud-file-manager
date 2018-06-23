<template>
    <nav aria-label="breadcrumb" id="path-nav">
        <ol class="breadcrumb small-font-size-radius mb-0">
            <template v-for="(path, index) in paths">
                <li class="breadcrumb-item" v-if="index != (paths.length - 1)" v-bind:id="'breadcrumb-path-' + index" v-bind:key="index">
                    <a href="javascript:void(0);" v-on:click="changeDir($event)">{{ path }}</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page" v-bind:id="'breadcrumb-path-' + index" v-else v-bind:key="index">{{ path }}</li>
            </template>
        </ol>
    </nav>
</template>

<script>
import Vuex from 'vuex'

export default {
    name: "breadcrumb",
    computed: {
        ...Vuex.mapGetters({
            paths: 'pathNameArray'
        })
    },
    methods: {
        ...Vuex.mapActions([
            'enterParentDir'
        ]),
        changeDir(event) {
            let id = event.target.parentElement.id
            let parentDirName = event.target.innerText
            if (id && parentDirName) {
                let arr = id.split('-')
                let index = parseInt(arr[arr.length - 1])
                if (Number.isNaN(index)) {
                    throw new TypeError(event.target.outerHTML + "id is not valid")
                }
                this.enterParentDir({parentDirName, index})
            }
        }
    }
}

</script>
