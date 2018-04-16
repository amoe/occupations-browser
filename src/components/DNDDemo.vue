<template>
  <div>
    <svg width="640" height="480">
      <!-- Need the groups to put them in the correct order -->
      <g id="targetElements">
        <circle r="1em" cx="400" cy="400" fill="#ff5f00" id="target" 
                ref="targetElement"
                v-on:mouseover="handleMouseover"
                v-on:mouseout="handleMouseout"/>
        
      </g>
      <g id="draggingElements">
        <circle r="1em" :cx="cx" :cy="cy" fill="#5f3653" id="source" ref="sourceElement"
                :pointer-events="pointerEvents"/>
      </g>
    </svg>

    <p>{{selectedNode}}</p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import * as d3 from 'd3';

export default Vue.extend({
    data() {
        return {
            selectedNode: null,
            cx: 100,
            cy: 100,
            isBlockingPointerEvents: false
        };
    },
    mounted() {
        this.$nextTick(() => {
            const svg  = this.$refs.sourceElement;
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
            this.isBlockingPointerEvents = true;
        },
        dragEnded(d) {
            console.log("end");
            this.isBlockingPointerEvents = false;
        },
        dragged(d) {
            this.cx = d3.event.x;
            this.cy = d3.event.y;
        },
        handleMouseover() {
            console.log("target element received mouseover");
            this.selectedNode = "Something";
        },
        handleMouseout() {
            console.log("target element received mouseout");
            this.selectedNode = null;            
        }
    },
    computed: {
        // When you are dragging an element it's always put to the front,
        // but that means that it will automatically receive any 
        // mouseover/mouseout events, so we need to temporarily disable them
        // during the drag period.
        pointerEvents: function(this: any) {
            return this.isBlockingPointerEvents ? "none" : "auto";
        }
    }
});  
</script>

<style>
</style>
