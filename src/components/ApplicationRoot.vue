<template>
  <div>
    <h1>RAD-DEN</h1>
    <p>The value is: <code>{{count}}</code></p>
    <button v-on:click="greet">Greet</button>
    <button v-on:click="doIncrement">Inc</button>

    <div>
      <svg width="960" height="900">
        <g transform="translate(480, 470)">
          <path v-for="node in allButRoot"
                class="link"
                :d="getPathDescription(node)"/>
          
          <!-- The group for nodes and their associated labels -->
          <g v-for="node in allIncludingRoot"
             class=""
             transform="">
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


export default Vue.extend({
    components: {
    },
    data: function() {
        return {
            root: null
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
        getPathDescription(node) {
            const d = node;
            return "M" + project(d.x, d.y)
                + "C" + project(d.x, (d.y + d.parent.y) / 2)
                + " " + project(d.parent.x, (d.y + d.parent.y) / 2)
                + " " + project(d.parent.x, d.parent.y);
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
        }
    }
});
</script>

<style>
body {
    max-width: 64rem;
    margin-left: auto;
    margin-right: auto;
    background-color: #fdfdfd;
}

h1,h2 { font-family: Georgia; }

p, label { font-family: Arial, sans-serif; }


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
