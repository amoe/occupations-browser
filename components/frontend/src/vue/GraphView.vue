<template>
    <g :transform="rootTranslation">
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


      <path v-for="node in allButRoot"
            class="link"
            :d="getPathDescription(node)"/>
    </g>
</template>

<script lang="ts">
import Vue from 'vue';
import NodeCircle from './NodeCircle.vue';
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
    components: {NodeCircle},
    data() {
        return {
        };
    },
    watch: {
        graphData(newData, oldData) {
            console.log("graph data changed");
            this.$nextTick(function() {
                console.log("inside dom graph data callback");

                const vars = {
                    onDragEnd: function(this: any) {
                        console.log("drag ended");

                        if (this.hitTest('#dndtarget')) {
                            console.log("drop received");
                        }
                    }
                };


                const result = Draggable.create('circle.ghost-node');
                console.log("result of creating draggable was %o", result);
            })
        }
    },
    created() {
        bus.$on(events.DRAG_AND_DROP_OPERATION_CONFIRMED, () => this.handleDragAndDrop());
    },
    methods: {
        handleDragAndDrop(this: any) {
            console.log("detected a drag and drop");
            console.log("lastDrop was %o => %o", this.lastDrop.source, this.lastDrop.target);
            const removedChildren = this.data2.children[1].children.splice(0, 1);
            this.data.children[1].name +=  "\u00b7" + removedChildren[0].name;
        },
        removeNode() {
            console.log("disabled");
            /*
            console.log("remove node %o", true);
            const removedElt = this.data.children.shift();
            console.log("removed element: %o", removedElt);
            */
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
        lastDrop: function(this: any) {
            return this.$store.getters.lastDrop;
        },
        isDragInProgress: function(this: any) {
            return this.$store.getters.isDragInProgress;
        }, ...mapGetters(['graphData', 'possibleRoots', 'selectedRoot'])
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
p
.node--internal circle {

/*  fill: #555;*/
}

.node--internal text {
  text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
}

.link {
      fill: none;
      stroke: cyan;
      stroke-opacity: 1.0;
      stroke-width: 1.5px;
}

svg {
    border: 1px solid #a0a0a0;
}
</style>
