<template>
  <!-- The starting position is given by a containing <g></g> in the scope
       of the containing Vue component. -->
  <g>
    <circle class="real-node"
            r="1em"
            ref="realNodeSvgCircle"/>

    <!-- The ghost node has to handle all of the events, because it's always
         in front of the real node.  Luckily the fact that the ghost node
         retains its real 'identity' in terms of the drop selection means that
         we're still able to find our way back to the real node. -->
    <circle class="ghost-node"
            r="1em"
            ref="ghostNodeSvgCircle"
            :cx="cx"
            :cy="cy"
            :opacity="ghostOpacity"
            v-on:mouseover="handleMouseover"
            v-on:mouseout="handleMouseout"
            :pointer-events="pointerEvents"/>

  </g>
</template>

<script lang="ts">
import Vue from 'vue';
import * as d3 from 'd3';
import events from '../events';
import mc from '../mutation-constants';
import {mapGetters} from 'vuex';

// We use d3's drag behaviour here because programmatically dealing with drag
// of SVG elements is a huge pain.  It's easier to just delegate than to deal
// with the various corner cases.

export default Vue.extend({
    data() {
        return {
            cx: 0,
            cy: 0,
            ghostOpacity: 0.0,
            isPointerEventsEnabled: true
        };
    },
    created() {
    },
    mounted() {
        this.$nextTick(() => {
            const svg  = this.$refs.ghostNodeSvgCircle;
            const selection = d3.select(svg);
            console.log("selection is %o", selection);
            
            const dragBehaviourAdder = d3.drag()
                .on('start', this.dragStarted)
                .on('drag', this.dragged)
                .on('end', this.dragEnded);
                                   
            selection.call(dragBehaviourAdder);
        })
    },
    methods: {
        dragStarted(d) {
            this.ghostOpacity = 0.2;
            console.log("start");
            this.$store.commit(mc.SWITCH_DRAG_IN_PROGRESS_ON);
            this.isPointerEventsEnabled = false;
        },
        dragEnded(d) {
            console.log("end");
            this.$store.commit(mc.SWITCH_DRAG_IN_PROGRESS_OFF);
            this.isPointerEventsEnabled = true;

            // Return the ghost node to its 'home'
            this.cx = 0;
            this.cy = 0;

            if (this.isDropCandidate) {
                console.log("successful drop");
            }
        },
        dragged(d) {
            this.cx = d3.event.x;
            this.cy = d3.event.y;
        },
        handleMouseover() {
            console.log("mouseover");

            if (this.isDragInProgress) {
                this.$store.commit(mc.SET_DROP_INTERACTION_CANDIDATE, 'something');
            }
        },
        handleMouseout() {
            console.log("mouseout");
            this.$store.commit(mc.CLEAR_DROP_INTERACTION_CANDIDATE);
        }
    },
    computed: {
        // When you are dragging an element it's always put to the front,
        // but that means that it will automatically receive any 
        // mouseover/mouseout events, so we need to temporarily disable them
        // during the drag period.
        pointerEvents(this: any) {
            return this.isPointerEventsEnabled ? "auto" : "none";
        },
        isDragInProgress(this: any) {
            return this.$store.getters['isDragInProgress'];
        },
        isDropCandidate(this: any) {
            return this.$store.getters['isDropCandidate'];
        }

    }
});
</script>

<style>
/*
circle:hover {
    fill: red;
}
*/
</style>

