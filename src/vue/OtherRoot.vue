<template>
  <div>
    <p>The value is: <code>{{count}}</code></p>
    <button v-on:click="greet">Greet</button>
    <button v-on:click="doIncrement">Inc</button>

    <label for="height">Height</label>
    <input id="height" v-model.number="height" type="number">

    <label for="aspect">Aspect</label>
    <input id="aspect" v-model.number="aspect" type="number" step="0.01">

    <label for="yMargin">Y Margin FIXME</label>
    <input id="yMargin" v-model.number="yMargin" type="number">

    <div>
      <!-- original vis is 960x900, aspect 1.06 -->
      <svg :width="width" :height="height">
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Vuex from 'vuex';
import utility from '../utility';
import * as d3 from 'd3';

function project(x, y) {
  var angle = (x - 90) / 180 * Math.PI, radius = y;
  return [radius * Math.cos(angle), radius * Math.sin(angle)];
}

function getParentId(d) {
    return d.id.substring(0, d.id.lastIndexOf("."));
}

function stratifyKey(a, b) {
    return a.height - b.height || a.id.localeCompare(b.id);
 }

// This constructs the 'd' attribute of the path elements.
function getPathDescription(d) {
    return "M" + project(d.x, d.y)
        + "C" + project(d.x, (d.y + d.parent.y) / 2)
        + " " + project(d.parent.x, (d.y + d.parent.y) / 2)
        + " " + project(d.parent.x, d.parent.y);
}

export default Vue.extend({
    components: {
    },
    data: function() {
        return {
            height: 900,
            aspect: 16/15,
            yMargin: 20
        };
    },
    mounted() {
        this.$nextTick(() => {
            this.drawClustered();
        })
    },
    methods: {
        drawClustered() {
            const svg = d3.select("svg");
            const width = this.width;
            const height = this.height;
            
            const xOffset = width / 2;
            const yOffset = (height / 2 + this.yMargin);

            // This only happens once, so it won't react.  FIXME
            const g = svg.append("g").attr("transform", "translate(" + xOffset + "," + yOffset + ")");

            const breadth = 360;              // This is an angle
            const depth = (width / 2) - 120;    // This is a radius

            // This particular formula (w/2)-120 will cause it to fill the whole area.
            // 120 is a pretty arbitrary offset for the depth margin.
            
            console.log("depth is %o", depth);

            var cluster = d3.cluster()
                .size([breadth, depth]);

            d3.csv("flare.csv").then(data => {
                const stratify = d3.stratify().parentId(getParentId);
                const root = stratify(data).sort(stratifyKey);
                const result = cluster(root);

                console.log("result is %o", result);

                var link = g.selectAll(".link")
                    .data(root.descendants().slice(1))
                    .enter().append("path")
                    .attr("class", "link")
                    .attr("d", getPathDescription);

                var node = g.selectAll(".node")
                    .data(root.descendants())
                    .enter().append("g")
                    .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
                    .attr("transform", function(d) { return "translate(" + project(d.x, d.y) + ")"; });

                // Now the question is, what can this do?  It's going to add a circl to this specific group.
                node.append("circle")
                    .attr("r", 2.5);

                node.append("text")
                    .attr("dy", "0.31em")
                    .attr("x", function(d) { return d.x < 180 === !d.children ? 6 : -6; })
                    .style("text-anchor", function(d) { return d.x < 180 === !d.children ? "start" : "end"; })
                    .attr("transform", function(d) { return "rotate(" + (d.x < 180 ? d.x - 90 : d.x + 90) + ")"; })
                    .text(function(d) { return d.id.substring(d.id.lastIndexOf(".") + 1); });
            });
        },
        greet() {
            console.log("hello");
            console.log("state val is %o", this.$store.state.count);
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
        width: function (this: any) {
            return this.height * this.aspect;
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
