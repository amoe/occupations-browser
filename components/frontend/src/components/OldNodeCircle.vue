<template>
  <circle r="1em"
          :cx="cx"
          :cy="cy"
          v-on:mousemove="handleMousemove"
          v-on:mousedown="handleMousedown"
          v-on:mouseup="handleMouseup"/>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    data() {
        return {
            isBeingDragged: false,
            originalLocation: null,
            cx: 0,
            cy: 0
        };
    },
    methods: {
        handleMousemove(event) {
            console.log("move");

            if (this.isBeingDragged) {
                console.log("move event is %o", event);
                
                const diffX = event.clientX - this.originalLocation.x;
                const diffY = event.clientY - this.originalLocation.y;

                this.cx = diffX;
                this.cy = diffY;
            }
            
        },
        handleMousedown(event) {
            console.log("down");
            
            this.isBeingDragged = true;
            this.originalLocation = {
                x: event.clientX,
                y: event.clientY
            };
        },
        handleMouseup() {
            console.log("up");

            this.isBeingDragged = false;
        }
    }
});
</script>

<style>
</style>

