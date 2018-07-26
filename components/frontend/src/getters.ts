export default {
    isDragInProgress(state, getters) {
        return state.isDragInProgress;
    },
    isDropCandidate(state, getters) {
        return state.dropInteractionCandidate !== null;
    },
    lastDrop(state, getters) {
        return state.lastDrop;
    },
    widgetOrder(state, getters) {
        return state.widgetOrder;
    },
    graphData(state, getters) {
        return state.graphData;
    },
    possibleRoots(state, getters) {
        return state.possibleRoots;
    }
};
