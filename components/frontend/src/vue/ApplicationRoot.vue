<template>
  <div class="page">
    <div class="header">
      <h1>OV {{date}}</h1>
    </div>

    <div class="widget-bar">
      <widget-bar>
      </widget-bar>
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

      <label for="zoomDepth">Zoom Depth</label>
      <input id="zoomDepth" v-model.number="zoomDepth">
    </div>

    <div>
      <p>Drag in progress: {{isDragInProgress}}, last drop {{lastDrop}}</p>
    </div>

    <div class="graph">
      <active-graph :width="width"
                    :height="height"
                    :y-margin="yMargin"
                    :depth-offset="depthOffset"
                    :text-offset="textOffset"
                    :breadth="breadth"
                    :zoom-depth="zoomDepth"></active-graph>
    </div>

    <div class="text-view">
      <text-view/>
    </div>

    <div class="timeline">
      <timeline-root/>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import utility from '../utility';
import * as d3 from 'd3';
import graph from '../graph';
import * as dateFns from 'date-fns';
import ActiveGraph from './ActiveGraph.vue';
import DNDDemo from './DNDDemo.vue';
import Hexagon from './Hexagon.vue';
import WidgetBar from './WidgetBar.vue';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';
import TextView from './TextView.vue';
import TimelineRoot from './TimelineRoot.vue';

export default Vue.extend({
    components: {ActiveGraph, DNDDemo, Hexagon, WidgetBar, TextView, TimelineRoot},
    data: function() {
        return {
            date: dateFns.format(new Date(), 'YYYY-MM-DD'),
            width: 600,
            height: 600,
            yMargin: 20,
            depthOffset: 120,
            textOffset: 22,   // depends on circle radius
            breadth: 360,
            zoomDepth: 2
        };
    },
    methods: {
    },
    created: function() {
    },
    // mapState doesn't work with typescript: "Property 'mapState' does not exist on type"
    // So we manually create the relevant computed properties.
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        }, ...mapGetters(['isDragInProgress', 'lastDrop'])
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

.widget-bar {
    grid-row: 2;
    grid-column: col-start 1 / span 12;
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
    margin: 1em;
    grid-column: col-start 2 / span 10;
}

div.timeline {
    grid-row: 6;
    height: 4em;
    grid-column: col-start 2 / span 10;     
}

.glyph {
    fill: red;
}
</style>
