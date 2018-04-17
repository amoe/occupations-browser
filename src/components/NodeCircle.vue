<template>
  <!-- The starting position is given by a containing <g></g> in the scope
       of the containing Vue component. -->
  <g>
    <circle class="real-node"
            r="1em"
            :fill="realNodeFill"
            ref="realNodeSvgCircle"/>

    <!-- The ghost node has to handle all of the events, because it's always
         in front of the real node.  Luckily the fact that the ghost node
         retains its real 'identity' in terms of the drop selection means that
         we're still able to find our way back to the real node. -->
    <circle class="ghost-node"
            :r="ghostRadiusEm"
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
import mc from '../mutation-constants';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';

// We use d3's drag behaviour here because programmatically dealing with drag
// of SVG elements is a huge pain.  It's easier to just delegate than to deal
// with the various corner cases.

export default Vue.extend({
    props: ['identifier'],
    data() {
        return {
            cx: 0,
            cy: 0,
            ghostOpacity: 0.0,
            isPointerEventsEnabled: true,
            ghostRadius: 2,
            realNodeFill: "black"
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
            this.$store.commit(mc.SET_DRAG_SOURCE, this.identifier);
            this.isPointerEventsEnabled = false;

            // Shrink the ghost
            this.ghostRadius = 1;
        },
        dragEnded(d) {
            console.log("end");
            this.$store.commit(mc.SWITCH_DRAG_IN_PROGRESS_OFF);
            this.isPointerEventsEnabled = true;

            // Return the ghost node to its 'home'
            this.cx = 0;
            this.cy = 0;
            this.ghostRadius = 2;
            this.ghostOpacity = 0.0;


            if (this.isDropCandidate) {
                console.log("successful drop");

                this.$store.commit(mc.CONFIRM_DROP);

                // Raise an event to communicate to parents
                bus.$emit(events.DRAG_AND_DROP_OPERATION_CONFIRMED);
            }

            // It should be fine to leave the drag source as it was here
        },
        dragged(d) {
            this.cx = d3.event.x;
            this.cy = d3.event.y;
        },
        // These are handled by nodes when they are acting as 'target nodes'
        handleMouseover() {
            console.log("mouseover");
            

            if (this.isDragInProgress) {
                this.realNodeFill = "green";
                this.$store.commit(mc.SET_DROP_INTERACTION_CANDIDATE, this.identifier);
            } else {
                // Just about to be dragged; 'draggable'
                this.realNodeFill = "blue";
            }
        },
        handleMouseout() {
            console.log("mouseout");
            
            this.realNodeFill = "black";
            
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
        },
        ghostRadiusEm(this: any) {
            return this.ghostRadius + "em";
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

