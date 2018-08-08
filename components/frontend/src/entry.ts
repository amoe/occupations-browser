// entry.ts

import * as log from 'loglevel';
import mymodule from './mymodule';
import ApplicationRoot from './vue/ApplicationRoot.vue';
import Vue from 'vue';
import Vuex from 'vuex';
import * as _ from 'lodash';


import Element from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'
import storeConfiguration from './vuex/store';


Vue.use(Element, { locale })
Vue.use(Vuex);

const store = new Vuex.Store(storeConfiguration);

log.setLevel('debug');

function getRenderingMode() {
    let result: string;

    if (document.compatMode === 'CSS1Compat') {
        result = "STANDARDS_COMPLIANCE";
    } else {
        result = "QUIRKS";
    }

    return result;
}

document.addEventListener("DOMContentLoaded", e => {
    console.log("Rendering mode: %o", getRenderingMode());
    console.log("The answer is: %o", mymodule.meaningOfLife());

});

document.addEventListener("DOMContentLoaded", e => {
    const vueInstance = new Vue({
        render: h => h(ApplicationRoot),
        store: store
    });
    vueInstance.$mount('#vue-outlet');
});
