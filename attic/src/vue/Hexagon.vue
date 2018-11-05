<template>
  <polygon :class="className" :points="polygonPoints"/>
</template>

<script lang="ts">
import Vue from 'vue';
import * as _ from 'lodash';

export default Vue.extend({
    props: ['cx', 'cy', 'r', 'className'],
    data() {
        return {
            points: []
        };
    },
    created() {
        console.log("inside created function");
        // calculate the points
        
        let i;
        for (i of _.range(6)) {
            const degree = 60 * i;
            const radian = Math.PI / 180 * degree;

            const x = this.cx + (this.r * Math.cos(radian));
            const y = this.cy + (this.r * Math.sin(radian));
            

            this.points.push({x, y})
        }

        console.log("points are now %o", JSON.stringify(this.points, null, 4));
    },
    computed: {
        polygonPoints: function(this: any) {
            return this.points.map(d => `${d.x},${d.y}`).join(" ");
        }

    }
});
</script>

<style>
  svg {
     border: 1px solid black;
  }
</style>
