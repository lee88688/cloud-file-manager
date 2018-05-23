let breadcrumb_template = `
<ol class="breadcrumb small-font-size-radius">
    <template v-for="(path, index) in paths" v-bind:key="index">
        <li class="breadcrumb-item" v-if="index != (paths.length - 1)">
            <a href="javascript:void(0);">{{ path }}</a>
        </li>
        <li class="breadcrumb-item active" aria-current="page" v-else>{{ path }}</li>
    </template>
</ol>
`;

Vue.component('breadcrumb', {
    template: breadcrumb_template,
    props: ["paths"],
    methods: {
    }
});