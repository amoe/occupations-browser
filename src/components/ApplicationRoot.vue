<template>
  <div>
    <h1>Cluster demo</h1> 
    
    <div class="control">
      <label for="width">Width</label>
      <input id="width" v-model.number="width">

      <label for="height">Height</label>
      <input id="height" v-model.number="height">

      <label for="yMargin">Y Margin</label>
      <input id="yMargin" v-model.number="yMargin">
    </div>

    <div>
      <svg :width="width" :height="height">
        <g :transform="rootTranslation">
          <path v-for="node in allButRoot"
                class="link"
                :d="getPathDescription(node)"/>
          
          <!-- The group for nodes and their associated labels -->
          <!-- The funny thing is that it's totally possible to rewrite these as
               a group of computed properties derived from the state. -->
          <!-- We just do it in this d3-ish way as a first pass. -->
          <g v-for="node in allIncludingRoot"
             :class="getNodeGroupClass(node)"
             :transform="getNodeGroupTransformation(node)">
            <circle r="2.5"/>
            <text dy="0.31em"
                  :transform="getTextRotation(node)"
                  :text-anchor="getTextAnchor(node)"
                  :x="getTextXOffset(node)">{{getNodeTextContent(node)}}</text>
          </g>
        </g>
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Vuex from 'vuex';
import utility from '../utility';
import * as d3 from 'd3';

function getParentId(d) {
    return d.id.substring(0, d.id.lastIndexOf("."));
}

// Not sure what's happening here
function ourCompare(a, b) {
    return a.height - b.height || a.id.localeCompare(b.id);
}

// Projection function
function project(x, y) {
    var angle = (x - 90) / 180 * Math.PI, radius = y;
    return [radius * Math.cos(angle), radius * Math.sin(angle)];
}

function isOnRightSide(node) {
    const isInFirstHalf = node.x < 180;
    const isLeafNode = !node.children;

    return isInFirstHalf == isLeafNode;
}

export default Vue.extend({
    components: {
    },
    data: function() {
        return {
            root: null,
            width: 960,
            height: 900,
            yMargin: 20
        };
    },
    created() {
        //const stratify = d3.stratify().parentId(getParentId);
        d3.csv("flare.csv").then(data => {
            const width = 960;
            const height = 900;
            
            const breadth = 360;                // This is an angle
            const depth = (width / 2) - 120;    // This is a radius

            const cluster = d3.cluster().size([breadth, depth]);

            const stratify = d3.stratify().parentId(getParentId);
            const root = stratify(data).sort(ourCompare);

            this.root = cluster(root);
        });
    },
    mounted() {
    },
    methods: {
        getTextRotation(node) {
            let rotation;

            if (node.x < 180) {
                rotation = node.x - 90;
            } else {
                rotation = node.x + 90;
            }

            return "rotate(" + rotation + ")";
        },
        getTextAnchor(node) {
            if (isOnRightSide(node)) {
                return "start";
            } else {
                return "end";
            }
        },
        getTextXOffset(node) {
            // This is like exclusive or or some shit.
            if (isOnRightSide(node)) {
                return 6;
            } else {
                return -6;
            }
        },
        getPathDescription(node) {
            const d = node;
            return "M" + project(d.x, d.y)
                + "C" + project(d.x, (d.y + d.parent.y) / 2)
                + " " + project(d.parent.x, (d.y + d.parent.y) / 2)
                + " " + project(d.parent.x, d.parent.y);
        },
        getNodeGroupTransformation(d) {
            return "translate(" + project(d.x, d.y) + ")";
        },
        getNodeGroupClass(d) {
            if (d.children) {
                return "node node--internal";
            } else {
                return "node node--leaf";
            }
        },
        getNodeTextContent(d) {
            return d.id.substring(d.id.lastIndexOf(".") + 1);
        },
        greet() {
            console.log("hello");
        },
        doIncrement() {
            this.$store.dispatch('increment');
        },
    },
    // mapState doesn't work with typescript: "Property 'mapState' does not exist on type"
    // So we manually create the relevant computed properties.
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        },
        allButRoot: function(this: any) {
            if (this.root === null) {
                return [];
            } else {
                return this.root.descendants().slice(1);
            }
        },
        allIncludingRoot: function(this: any) {
            if (this.root === null) {
                return [];
            } else {
                return this.root.descendants();
            }
        },
        rootTranslation: function(this: any) {
            const xOffset = this.width / 2;
            const yOffset = (this.height / 2) + this.yMargin;
            
            return "translate(" + xOffset + "," + yOffset + ")";
        }
    }
});
</script>

<style>

.node circle {
  fill: #999;
}

.node text {
  font: 10px sans-serif;
}

.node--internal circle {
  fill: #555;
}

.node--internal text {
  text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
}

.link {
  fill: none;
  stroke: #555;
  stroke-opacity: 0.4;
  stroke-width: 1.5px;
}

</style>
