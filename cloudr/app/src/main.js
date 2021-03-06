// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import $ from 'jquery'
import App from './App'
import 'bootstrap'
import { store } from './store'
import '@mdi/font/css/materialdesignicons.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'animate.css/animate.css'

Vue.config.productionTip = false

function resizeListContainer(event) {
    var listContainer = document.querySelector(".list-container")
    var rec = listContainer.getBoundingClientRect()
    var pageHeight = window.innerHeight
    listContainer.style.height = (pageHeight - rec.top) + "px"
};

window.onresize = resizeListContainer
window.$ = $

$(document).ready(function() {
    resizeListContainer()
})

/* eslint-disable no-new */
new Vue({
    store,
    el: '#app',
    components: { App },
    render: h => h(App)
})
