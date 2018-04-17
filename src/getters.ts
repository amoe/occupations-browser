export default {
    isDragInProgress(state, getters) {
        return state.isDragInProgress;
    },
    isDropCandidate(state, getters) {
        return state.dropInteractionCandidate !== null;
    },
    lastDrop(state, getters) {
        return state.lastDrop;
    }
};
