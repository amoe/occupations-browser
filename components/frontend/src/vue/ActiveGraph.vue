<template>
<div>
  <el-button v-on:click="removeNode">foo</el-button>
  <el-button v-on:click="removeNodeFromBackend">Remove node from backing store</el-button>
  <el-button v-on:click="clearEntireGraph">Clear entire graph</el-button>
  <el-button v-on:click="updateFromBackend">Update from backend</el-button>

  <test-component></test-component>

  <div>
    <el-select filterable
               remote
               v-model="currentRoot"
               :remote-method="searchRoots"
               v-on:change="changed">
      <el-option v-for="item in possibleRoots"
                 :key="item.value"
                 :label="item.label"
                 :value="item.value"/>
    </el-select>
  </div>

  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="200" height="200">
      <circle slot="reference" v-popover:inside cx="50" cy="50" r="50"/>
    </el-popover>
  </svg>

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
        <node-circle :identifier="getNodeTextContent(node)"/>
        <text dy="0.31em"
              :transform="getTextRotation(node)"
              :text-anchor="getTextAnchor(node)"
              :x="getTextXOffset(node)">{{getNodeTextContent(node)}}</text>
      </g>
    </g>
  </svg>
</div>
</template>

<script lang="ts">
import Vue from 'vue';
import NodeCircle from './NodeCircle.vue';
import TestComponent from './TestComponent.vue';
import * as d3 from 'd3';
import layoutFunctions from '../layout-functions';
import graph from '../graph';
import bus from '../event-bus';
import events from '../events';
import axios from 'axios';

export default Vue.extend({
    props: ['width', 'height', 'yMargin', 'depthOffset', 'textOffset', 'breadth', 'zoomDepth'],
    components: {NodeCircle, TestComponent},
    data() {
        return {
            data: null,
            data3: graph.stratifySentence(["the", "big", "red", "dog"]),
            possibleRoots: [],
            value9: null,
            currentRoot: 'Oyl'
        };
    },
    created() {
        bus.$on(events.DRAG_AND_DROP_OPERATION_CONFIRMED, () => this.handleDragAndDrop());
        this.updateFromBackend();
    },
    mounted() {
    },
    methods: {
        searchRoots(query) {
            console.log("remote method called with argument %o", query);
            axios.get("/api/tezra/roots?q=" + query).then(response => {
                this.possibleRoots = response.data.map(x => ({value: x, label: x}));
            }).catch(error => {
                this.$message.error('Failed to query data from API');
            });
        },
        changed(val) {
            console.log("changed was called with value %o", val);
            this.updateFromBackend();
        },
        clearEntireGraph() {
            axios.post("/api/clear_all_nodes").then(response => {
                this.$message('Cleared graph');
                this.updateFromBackend();
            }).catch(error => {
                this.$message.error('Something went wrong.');
            });
        },

        removeNodeFromBackend() {
            const rootToken = 'the';

            // silliness
            axios.post("/api/delete_some_node").then(response => {
                this.$message('Removed an arbitrary node.');
                this.updateFromBackend();
            }).catch(error => {
                this.$message.error('Something went wrong.');
            });
        },
        updateFromBackend() {
            axios.get("/api/tezra/tree?root=" + this.currentRoot + "&zoom_depth=" + this.zoomDepth).then(response => {
                this.data = response.data;
            }).catch(error => {
                this.$message.error('Failed to query data from API');
            });
        },
        handleDragAndDrop(this: any) {
            console.log("detected a drag and drop");
            console.log("lastDrop was %o => %o", this.lastDrop.source, this.lastDrop.target);
            const removedChildren = this.data2.children[1].children.splice(0, 1);
            this.data.children[1].name +=  "\u00b7" + removedChildren[0].name;
        },
        removeNode() {
            console.log("remove node %o", true);
            const removedElt = this.data.children.shift();
            console.log("removed element: %o", removedElt);
        },
        handleMousedown() {
            console.log("got mousedown %o", arguments);
        },
        handleMousemove() {
            console.log("got mousemove");
        },
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
            if (layoutFunctions.isOnRightSide(node)) {
                return "start";
            } else {
                return "end";
            }
        },
        getTextXOffset(node) {
            // This is like exclusive or or some shit.
            if (layoutFunctions.isOnRightSide(node)) {
                return this.textOffset;
            } else {
                return -this.textOffset;
            }
        },
        getPathDescription(node) {
            const d = node;
            return "M" + layoutFunctions.project(d.x, d.y)
                + "C" + layoutFunctions.project(d.x, (d.y + d.parent.y) / 2)
                + " " + layoutFunctions.project(d.parent.x, (d.y + d.parent.y) / 2)
                + " " + layoutFunctions.project(d.parent.x, d.parent.y);
        },
        getNodeGroupTransformation(d) {
            return "translate(" + layoutFunctions.project(d.x, d.y) + ")";
        },
        getNodeGroupClass(d) {
            if (d.children) {
                return "node node--internal";
            } else {
                return "node node--leaf";
            }
        },
        getNodeTextContent(d) {
//            console.log("text content requested, %o", d.data);

            // data goes here, whereas it's on id when using the stratified set from csv
            return d.data.id;
        },
    },
    computed: {
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
        },
        root: function(this: any) {
            if (this.data === null)  return null;

            const depth = (this.width / 2) - this.depthOffset;    // This is a radius

            const cluster = d3.cluster().size([this.breadth, depth]);


            // This is one option; not sure if sort is needed
           // const stratify = d3.stratify().parentId(getParentId);
           // const root = stratify(this.data).sort(ourCompare);

            // This is another option
            let root = d3.hierarchy(this.data, d => d.children);

            return cluster(root);
        },
        lastDrop: function(this: any) {
            return this.$store.getters.lastDrop;
        },
        isDragInProgress: function(this: any) {
            return this.$store.getters.isDragInProgress;
        }
    }
});
</script>

<style>
/* All of the fill stuff here has been superseded by the stuff in the nodecircle
   component */

.node circle {
/*    fill: #999;*/
    cursor: move;
}

.node text {
    font-size: 0.8em;
}

.node--internal circle {

/*  fill: #555;*/
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

svg {
    border: 1px solid #a0a0a0;
}
</style>
