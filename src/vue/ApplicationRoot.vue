<template>
  <div class="page">
    <div class="header">
      <h1>OV {{date}}</h1>
    </div>


    <div class="widget-bar">
      <widget-bar>
      </widget-bar>
    </div>


    <div class="graph">
      <graph-controls :zoom-depth="zoomDepth"></graph-controls>

      <textarea>{{taxonomyData}}</textarea>

      <el-popover placement="bottom"
                  title="Title"
                  width="200"
                  trigger="manual"
                  :value="popoverActive">
        <el-button>Link</el-button>
      </el-popover>

      <svg id="svg-frame" :width="width" :height="height">
        <graph-view :width="width"
                    :height="height"
                    :x-margin="xMarginPx"
                    :y-margin="yMarginPx"
                    :depth-offset="depthOffset"
                    :text-offset="textOffset"
                    :breadth="breadth"></graph-view>
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import utility from '../utility';
import * as d3 from 'd3';
import graph from '../graph';
import * as dateFns from 'date-fns';
import GraphView from './GraphView.vue';
import GraphControls from './GraphControls.vue';
import DNDDemo from './DNDDemo.vue';
import Hexagon from './Hexagon.vue';
import WidgetBar from './WidgetBar.vue';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';
import TextView from './TextView.vue';
import TimelineRoot from './TimelineRoot.vue';
import axios from 'axios';
import * as log from 'loglevel';
import * as TreeModel from 'tree-model';

export default Vue.extend({
    components: {GraphControls, GraphView, DNDDemo, Hexagon, WidgetBar, TextView, TimelineRoot},
    data: function() {
        return {
            taxonomyData: [],
            visible: false,
            activeControls: [],
            date: dateFns.format(new Date(), 'YYYY-MM-DD'),
            width: 600,
            height: 600,
            yMarginVh: 0.4,
            xMarginVh: 0.15,
            depthOffset: 120,
            textOffset: 22,   // depends on circle radius
            breadth: 360,
            zoomDepth: 2
        };
    },
    methods: {
        handleChange(val) {
            log.trace("collapse was modified with value %o", val);
        }
    },
    created: function() {
        axios.get('/api/taxonomy').then(r => {
            console.log("taxonomy data result was %o", r.data);
            this.taxonomyData = r.data;

             const treeModelConfig = {
                 childrenPropertyName: 'children',
                 // you can also use modelcomparatorfn here to auto sort the tree
             };


             const apiTree = new TreeModel(treeModelConfig);
             const apiRoot = apiTree.parse(r.data);

             console.log("new api root is %o", apiRoot);
        });
    },
    // mapState doesn't work with typescript: "Property 'mapState' does not exist on type"
    // So we manually create the relevant computed properties.
    computed: {
        yMarginPx: function (this: any) {
            return document.documentElement.clientHeight * this.yMarginVh;
        },
        xMarginPx: function (this: any) {
            return document.documentElement.clientHeight * this.xMarginVh;
        },

        count: function (this: any) {
            return this.$store.state.count;
        }, ...mapGetters(['isDragInProgress', 'lastDrop', 'popoverActive'])
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
    grid-column: col-start 2 / span 10;
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
    grid-column: col-start / span 12;
    margin: 1em;
}

div.control-collapse {
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

/* The svg frame is 'pinned', taken outside of the flow layout, and occupies 
   the entire page. */
#svg-frame {
    position: absolute;
    top: 0px;
    right: 0px;
    left: 0px;
    bottom: 0px;
    width: 100vw;
    height: 100vh;

    /* It's gotta have such a z-index, otherwise it will block HTML items from
       being interacted with. */
    z-index: -1;
}

</style>
