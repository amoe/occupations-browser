import * as _ from 'lodash';
import actions from './actions';
import mc from '../mutation-constants';
import getters from './getters';
import Vuex from 'vuex';
import { DragAndDropOperation, NodeIdentifier, WidgetDisplaySpecifier } from '../interfaces';

const storeConfiguration = {
    getters,
    state: {
        count: 0,
        widgetOrder: [
            { name: 'alpha', renderCount: 0 },
            { name: 'beta', renderCount: 0 },
            { name: 'gamma', renderCount: 0 }
        ],
        // needs to be initialized to null, not an empty array, otherwise you
        // see a strange intermediate state
        graphData: null,
        possibleRoots: [],
        selectedRoot: 'Oyl',
        // Stores a reference to the DOM elements that get populated by the
        // taxonomy widgets; this is needed to allow registering them as
        // potential hit areas for draggable.
        widgetDropTargets: []
    },
    mutations: {
        increment(state) {
            state.count++;
        },
        [mc.SET_WIDGET_DROP_TARGETS]: (state, elements: HTMLElement[]) => {
            state.widgetDropTargets = elements;
        },
        [mc.INCREMENT_RENDER_COUNT_BY_NAME]: (state, name: string) => {
            console.log("checking for render count for %o", name);

            // We just try to re-render all of them, cargo cultishly
            // This is not as smooth as before, but it gets around some layout bugs

            state.widgetOrder.forEach(w => w.renderCount++)
        },
        [mc.SHUFFLE]: (state) => {
            state.widgetOrder = _.shuffle(state.widgetOrder);
        },
        [mc.SWAP_TAXONOMY_WIDGETS]: (state, { source, target }) => {
            console.log("will try to swap source %o and target %o", source, target);
            const copy = _.clone(state.widgetOrder);

            const sourceIndex = _.findIndex(state.widgetOrder, w => w.name === source);
            const targetIndex = _.findIndex(state.widgetOrder, w => w.name === target);

            console.log("sourceindex is %o", sourceIndex);
            console.log("targetindex is %o", targetIndex);

            if (targetIndex === -1) throw new Error("target not found, can't happen");

            // Not sure if this will work because of vue/vuex array
            copy[targetIndex] = state.widgetOrder[sourceIndex];
            copy[sourceIndex] = state.widgetOrder[targetIndex];

            state.widgetOrder = copy;

            console.log("widget order is now %o", state.widgetOrder);
        },
        [mc.ADD_WIDGET]: (state, { id }) => {
            state.widgetOrder.push(
                {
                    name: id,
                    renderCount: 0
                }
            );
        },
        [mc.REMOVE_WIDGET]: (state, { name }) => {
            state.widgetOrder = _.filter(state.widgetOrder, w => w.name !== name);
        },
        [mc.SET_GRAPH_DATA]: (state, data) => {
            state.graphData = data;
        },
        [mc.SET_POSSIBLE_ROOTS]: (state, possibleRoots) => {
            state.possibleRoots = possibleRoots;
        },
        [mc.SELECT_ROOT]: (state, newRoot) => {
            state.selectedRoot = newRoot;
        }
    },
    actions
};

export default storeConfiguration;
