// entry.ts

import * as log from 'loglevel';
import mymodule from './mymodule';
import ApplicationRoot from './vue/ApplicationRoot.vue';
import Vue from 'vue';
import Vuex from 'vuex';
import actions from './actions';
import mc from './mutation-constants';
import getters from './getters';
import { DragAndDropOperation, NodeIdentifier } from './interfaces';
import * as _ from 'lodash';


import Element from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(Element)
Vue.use(Vuex);

const store = new Vuex.Store({
    getters,
    state: {
        count: 0,
        dragSource: null,
        dropInteractionCandidate: null,
        isDragInProgress: false,
        lastDrop: null,
        widgetOrder: [
            'alpha', 'beta', 'gamma'
        ]
    },
    mutations: {
        increment(state) {
            state.count++;
        },
        [mc.SET_DROP_INTERACTION_CANDIDATE]: (state, chosen: NodeIdentifier) => {
            state.dropInteractionCandidate = chosen;
        },
        [mc.CLEAR_DROP_INTERACTION_CANDIDATE]: (state) => {
            state.dropInteractionCandidate = null;
        },
        [mc.SWITCH_DRAG_IN_PROGRESS_OFF]: (state, chosen) => {
            state.isDragInProgress = false;
        },
        [mc.SWITCH_DRAG_IN_PROGRESS_ON]: (state, chosen) => {
            state.isDragInProgress = true;
        },
        [mc.SET_DRAG_SOURCE]: (state, source: NodeIdentifier) => {
            state.dragSource = source;
        },
        [mc.CONFIRM_DROP]: (state) => {
            const theDrop: DragAndDropOperation = {
                source: state.dragSource,
                target: state.dropInteractionCandidate
            };

            state.lastDrop = theDrop;
            state.dropInteractionCandidate = null;
            state.dragSource = null;
        },
        [mc.SHUFFLE]: (state) => {
            state.widgetOrder = _.shuffle(state.widgetOrder);
        },
        [mc.SWAP_TAXONOMY_WIDGETS]: (state, { source, target }) => {
            const copy = _.clone(state.widgetOrder);

            const sourceIndex = _.findIndex(state.widgetOrder, w => w === source);
            const targetIndex = _.findIndex(state.widgetOrder, w => w === target);

            // Not sure if this will work because of vue/vuex array
            copy[targetIndex] = source;
            copy[sourceIndex] = target;

            state.widgetOrder = copy;

            console.log("widget order is now %o", state.widgetOrder);
        },
        [mc.ADD_WIDGET]: (state, { id }) => {
            state.widgetOrder.push(id);
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
