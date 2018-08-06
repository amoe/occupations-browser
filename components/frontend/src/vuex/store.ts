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
        dragSource: null,
        dropInteractionCandidate: null,
        isDragInProgress: false,
        lastDrop: null,
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
        taxonomyWidgetElements: []
    },
    mutations: {
        increment(state) {
            state.count++;
        },
        [mc.INCREMENT_RENDER_COUNT_BY_NAME]: (state, name: string) => {
            const s: WidgetDisplaySpecifier = state.widgetOrder.find(x => x === name);

            s.renderCount++;
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
            state.widgetOrder.push(
                {
                    name: id,
                    renderCount: 0
                }
            );
        },
        [mc.REMOVE_WIDGET]: (state, { name }) => {
            state.widgetOrder = _.filter(state.widgetOrder, w => w !== name);
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
