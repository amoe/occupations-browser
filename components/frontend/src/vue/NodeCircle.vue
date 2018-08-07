<template>
  <!-- The starting position is given by a containing <g></g> in the scope
       of the containing Vue component. -->
  <g>
    <circle class="real-node"
            r="16"
            :fill="realNodeFill"
            ref="realNodeSvgCircle"/>

    <!-- The ghost node has to handle all of the events, because it's always
         in front of the real node.  Luckily the fact that the ghost node
         retains its real 'identity' in terms of the drop selection means that
         we're still able to find our way back to the real node. -->

    <circle class="ghost-node"
            :r="ghostRadiusPx"
            ref="ghostNodeSvgCircle"
            :cx="cx"
            :cy="cy"
            :opacity="ghostOpacity">
      <title>This is a tooltip</title>
    </circle>
  </g>
</template>

<script lang="ts">
import Vue from 'vue';
import * as d3 from 'd3';
import mc from '../mutation-constants';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';
import Draggable from 'gsap/Draggable';
import TweenLite from 'gsap/TweenLite';

export default Vue.extend({
    props: ['identifier', 'source'],
    data() {
        return {
            cx: 0,
            cy: 0,
            ghostOpacity: 0.0,
            isPointerEventsEnabled: true,
            ghostRadius: 32,
            realNodeFill: "black"
        };
    },
    created() {
    },
    mounted() {
        const instance = this;

        this.$nextTick(function() {
            const ghostCircle = instance.$refs.ghostNodeSvgCircle;

            console.log("inside circle node callback");

            const vars = {
                onDragStart: function(this: any) {
                    console.log("drag started");
                    instance.ghostOpacity = 0.2;
                    instance.ghostRadius = 16;
                },
                onDragEnd: function(this: any) {
                    console.log("drag ended");

                    // hittest can't accept a class, only an id, and should really be element

                    const targetsHit = instance.widgetDropTargets.filter(
                        e => this.hitTest(e)
                    );

                    console.log("hit targets were %o", targetsHit);

                    TweenLite.to(
                        this.target, 1, { x: 0, y: 0 }
                    );
                }
            };


            const result = Draggable.create(ghostCircle, vars);
            console.log("result of creating draggable was %o", result);
        })
    },
    methods: {
    },
    computed: {
        // Just a utility method to convert between the units.
        ghostRadiusPx(this: any) {
            return this.ghostRadius;
        },
        widgetDropTargets: function(this: any) {
            return this.$store.getters.widgetDropTargets;
        }
    }
});
</script>

<style>
/*
circle:hover {
    fill: red;
}
*/
</style>

