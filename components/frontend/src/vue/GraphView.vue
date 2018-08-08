<template>
    <g :transform="rootTranslation">
      <!-- The group for nodes and their associated labels -->
      <!-- The funny thing is that it's totally possible to rewrite these as
           a group of computed properties derived from the state. -->
      <!-- We just do it in this d3-ish way as a first pass. -->

      <graph-node v-for="(node, index) in allIncludingRoot"
                  ref="nodes"
                  :key="index"
                  :group-class="getNodeGroupClass(node)"
                  :group-transform="getNodeGroupTransformation(node)"
                  :text-transform="getTextRotation(node)"
                  :text-anchor="getTextAnchor(node)"
                  :text-x-offset="getTextXOffset(node)"
                  :text-content="getNodeTextContent(node)">
      </graph-node>

      <path v-for="node in allButRoot"
            class="link"
            :d="getPathDescription(node)"/>
    </g>
</template>

<script lang="ts">
import Vue from 'vue';
import GraphNode from './GraphNode.vue';
import * as d3 from 'd3';
import layoutFunctions from '../layout-functions';
import graph from '../graph';
import bus from '../event-bus';
import events from '../events';
import axios from 'axios';
import { PolarPoint, CartesianPoint } from '../interfaces';
import {sprintf} from 'sprintf-js';
import mc from '../mutation-constants';
import {mapGetters} from 'vuex';
import Draggable from 'gsap/Draggable';

export default Vue.extend({
    props: ['width', 'height', 'yMargin', 'depthOffset', 'textOffset', 'breadth'],
    components: {GraphNode},
    data() {
        return {
        };
    },
    watch: {
        graphData(newData, oldData) {
            console.log("GraphView: inside graph data watcher");
            this.$nextTick(() => this.saveNodes());
        }
    },
    methods: {
        saveNodes() {
            console.log("saving nodes");
            console.log("node set was found as %o", this.$refs.nodes);
            this.$store.commit(mc.SET_NODE_DND_TARGETS, this.$refs.nodes);
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

            const sourcePoint: PolarPoint = {
                angle: d.parent.x,
                radius: d.parent.y
            };

            const targetPoint: PolarPoint = {
                angle: d.x,
                radius: d.y
            };

            // console.log("source point is %o", sourcePoint);
            // console.log("target point is %o", targetPoint);
            // console.log("text associated with target point is %o", d.data.id);

            const sourceRadius = 16;

            return layoutFunctions.getPathDescriptionForEdge(sourcePoint, sourceRadius, targetPoint)
        },
        getNodeGroupTransformation(d) {
            const p1: PolarPoint = {
                angle: d.x,
                radius: d.y
            };

            const p2 = layoutFunctions.polarToCartesian(p1);

            return `translate(${p2.x}, ${p2.y})`;
        },
        getNodeGroupClass(d) {
            if (d.children) {
                return "node node--internal";
            } else {
                return "node node--leaf";
            }
        },
        getNodeTextContent(d) {
            return `${d.data.id}`;
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
            if (this.graphData === null)  return null;

            const depth = (this.width / 2) - this.depthOffset;    // This is a radius

            const cluster = d3.cluster().size([this.breadth, depth]);


            // This is one option; not sure if sort is needed
           // const stratify = d3.stratify().parentId(getParentId);
           // const root = stratify(this.data).sort(ourCompare);

            // This is another option
            let root = d3.hierarchy(this.graphData, d => d.children);

            return cluster(root);
        },
        widgetDropTargets: function(this: any) {
            return this.$store.getters.widgetDropTargets;
        }, ...mapGetters(['graphData', 'possibleRoots', 'selectedRoot'])
    }
});
</script>

<style>
.node circle {
    cursor: move;
}

.node text {
    font-size: 0.8em;
}

.link {
      fill: none;
      stroke: cyan;
      stroke-opacity: 1.0;
      stroke-width: 1.5px;
}
</style>
