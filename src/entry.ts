// entry.ts

import * as log from 'loglevel';
import mymodule from './mymodule';
import ApplicationRoot from './components/ApplicationRoot.vue';
import Vue from 'vue';
import Vuex from 'vuex';
import actions from './actions';
import mc from './mutation-constants';
import getters from './getters';

Vue.use(Vuex);

const store = new Vuex.Store({
    getters,
    state: {
        count: 0,
        dropInteractionCandidate: null,
        isDragInProgress: false
    },
    mutations: {
        increment(state) {
            state.count++;
        },
        [mc.SET_DROP_INTERACTION_CANDIDATE]: (state, chosen) => {
            state.dropInteractionCandidate = chosen;
        },
        [mc.CLEAR_DROP_INTERACTION_CANDIDATE]: (state, chosen) => {
            state.dropInteractionCandidate = null;
        },
        [mc.SWITCH_DRAG_IN_PROGRESS_OFF]: (state, chosen) => {
            state.isDragInProgress = false;
        },
        [mc.SWITCH_DRAG_IN_PROGRESS_ON]: (state, chosen) => {
            state.isDragInProgress = true;
        }
    },
    actions
});

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
