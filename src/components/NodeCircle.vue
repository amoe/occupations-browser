<template>
  <circle r="1em"
          :cx="cx"
          :cy="cy"
          ref="svgElement"
          :pointer-events="pointerEvents"
          v-on:mouseover="handleMouseover"
          v-on:mouseout="handleMouseout"/>
</template>

<script lang="ts">
import Vue from 'vue';
import * as d3 from 'd3';
import events from '../events';

// We use d3's drag behaviour here because programmatically dealing with drag
// of SVG elements is a huge pain.  It's easier to just delegate than to deal
// with the various corner cases.

export default Vue.extend({
    data() {
        return {
            cx: 0,
            cy: 0,
            isPointerEventsEnabled: true
        };
    },
    created() {
    },
    mounted() {
        this.$nextTick(() => {
            const svg  = this.$refs.svgElement;
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
            console.log("start");
            this.isPointerEventsEnabled = false;
        },
        dragEnded(d) {
            console.log("end");
            this.isPointerEventsEnabled = true;
        },
        dragged(d) {
            this.cx = d3.event.x;
            this.cy = d3.event.y;
        },
        handleMouseover() {
            console.log("mouseover");
        },
        handleMouseout() {
            console.log("mouseout");
        }
    },
    computed: {
        // When you are dragging an element it's always put to the front,
        // but that means that it will automatically receive any 
        // mouseover/mouseout events, so we need to temporarily disable them
        // during the drag period.
        pointerEvents(this: any) {
            return this.isPointerEventsEnabled ? "auto" : "none";
        }
    }
});
</script>

<style>
</style>

