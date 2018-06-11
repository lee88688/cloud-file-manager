let breadcrumb_template = `
<ol class="breadcrumb small-font-size-radius">
    <template v-for="(path, index) in paths">
        <li class="breadcrumb-item" v-if="index != (paths.length - 1)" v-bind:id="'breadcrumb-path-' + index">
            <a href="javascript:void(0);">{{ path }}</a>
        </li>
        <li class="breadcrumb-item active" aria-current="page" v-bind:id="'breadcrumb-path-' + index" v-else>{{ path }}</li>
    </template>
</ol>
`;

Vue.component('breadcrumb', {
    template: breadcrumb_template,
    props: ["paths"],
    methods: {
    }
});