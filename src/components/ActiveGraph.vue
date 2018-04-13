<template>
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
        <node-circle/>
        <text dy="0.31em"
              :transform="getTextRotation(node)"
              :text-anchor="getTextAnchor(node)"
              :x="getTextXOffset(node)">{{getNodeTextContent(node)}}</text>
      </g>
    </g>
  </svg>
</template>

<script lang="ts">
import Vue from 'vue';
import NodeCircle from './NodeCircle.vue';
import * as d3 from 'd3';
import layoutFunctions from '../layout-functions';
import graph from '../graph';

export default Vue.extend({
    props: ['width', 'height', 'yMargin', 'depthOffset', 'textOffset', 'breadth'],
    components: {NodeCircle},
    data() {
        return {
            data: null,
            data2: {
                "name": "Eve",
                "children": [
                    {
                        "name": "Cain"
                    },
                    {
                        "name": "Seth",
                        "children": [
                            {
                                "name": "Enos"
                            },
                            {
                                "name": "Noam"
                            }
                        ]
                    },
                    {
                        "name": "Abel"
                    },
                    {
                        "name": "Awan",
                        "children": [
                            {
                                "name": "Enoch"
                            }
                        ]
                    },
                    {
                        "name": "Azura"
                    }
                ],
            },              
            data3: graph.stratifySentence(["the", "big", "red", "dog"])
        };
    },
    created() {
        //const stratify = d3.stratify().parentId(getParentId);
        d3.csv("flare.csv").then(data => {
            this.data = data;
        });
    },
    mounted() {
    },
    methods: {
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
            console.log("text content requested, %o", d.data.name);

            // data goes here, whereas it's on id when using the stratified set from csv
            return d.data.name;
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
            let root = d3.hierarchy(this.data2, d => d.children);

            return cluster(root);
        }
    }
});
</script>

<style>
.node circle {
    fill: #999;
    cursor: move;
}

.node text {
    font-size: 0.8em;
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
