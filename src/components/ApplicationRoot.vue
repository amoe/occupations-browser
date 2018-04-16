<template>
  <div class="page">
    <div class="header">
      <h1>OV {{date}}</h1>
    </div>

    <div class="taxonomy">
    </div>
    
    <div class="control">
      <label for="width">Width</label>
      <input id="width" v-model.number="width">

      <label for="height">Height</label>
      <input id="height" v-model.number="height">

      <label for="yMargin">Y Margin</label>
      <input id="yMargin" v-model.number="yMargin">

      <label for="depthOffset">Depth Offset</label>
      <input id="depthOffset" v-model.number="depthOffset">

      <label for="textOffset">Text Offset</label>
      <input id="textOffset" v-model.number="textOffset">

      <label for="breadth">Breadth</label>
      <input id="breadth" v-model.number="breadth">

    </div>

    <div class="graph">
      <active-graph :width="width"
                    :height="height"
                    :y-margin="yMargin"
                    :depth-offset="depthOffset"
                    :text-offset="textOffset"
                    :breadth="breadth"></active-graph>
    </div>

    <div class="text-view">
    </div>

    <div class="timeline">
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Vuex from 'vuex';
import utility from '../utility';
import * as d3 from 'd3';
import graph from '../graph';
import * as dateFns from 'date-fns';
import ActiveGraph from './ActiveGraph.vue';
import DNDDemo from './DNDDemo.vue';
import Hexagon from './Hexagon.vue';

export default Vue.extend({
    components: {ActiveGraph, DNDDemo, Hexagon},
    data: function() {
        return {
            date: dateFns.format(new Date(), 'YYYY-MM-DD'),
            width: 600,
            height: 600,
            yMargin: 20,
            depthOffset: 120,
            textOffset: 22,   // depends on circle radius
            breadth: 360
        };
    },
    // mapState doesn't work with typescript: "Property 'mapState' does not exist on type"
    // So we manually create the relevant computed properties.
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        }
    }
});
</script>

<style>
@font-face {
    font-family: 'Oxygen';
    src: url("/static/fonts/Oxygen-Regular.ttf");
}

body {
    background-color: #fdfdfd;
    font-family: 'Oxygen', sans-serif;
}

div.taxonomy {
}

div.page {
    display: grid;
    grid-template-columns: repeat(12, [col-start] 1fr);
}

div.header {
    grid-row: 1;
    grid-column: col-start 2 / span 12;
}

h1 {
   font-style: italic;
}


div.taxonomy {
    grid-row: 2;
    height: 8em;
    background-color: #a0a0a0;
    grid-column: col-start / span 12;
    margin: 1em;
}

div.control {
    grid-row: 3;
    grid-column: col-start 2 / span 10;
}

div.graph {
    grid-row: 4;
    grid-column: col-start 4 / span 4;
}

div.text-view {
    grid-row: 5;
    height: 4em;
    background-color: #a0a0a0;
    margin: 1em;
    grid-column: col-start / span 12;
}

div.timeline {
    grid-row: 6;
    height: 4em;
    background-color: #a0a0a0;
    margin: 1em;
    grid-column: col-start / span 12;
}

.glyph {
    fill: red;
}
</style>
