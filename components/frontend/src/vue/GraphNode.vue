<template>
  <g :class="groupClass" :transform="groupTransform">
  <!-- The starting position is given by a containing <g></g> in the scope
       of the containing Vue component. -->
    <circle class="real-node"
            r="16"
            :fill="realNodeFill"
            ref="realNodeSvgCircle"/>

    <!-- The ghost node has to handle all of the events, because it's always
         in front of the real node.  -->
    <circle class="ghost-node"
            :r="ghostRadiusPx"
            ref="ghostNodeSvgCircle"
            :cx="cx"
            :cy="cy"
            :opacity="ghostOpacity">
      <title>This is a tooltip</title>
    </circle>

    <text dy="0.31em"
          :transform="textTransform"
          :text-anchor="textAnchor"
          :x="textXOffset">{{textContent}}</text>
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
import constants from '../constants';

export default Vue.extend({
    props: [
        'source', 'text-transform', 'text-anchor', 'text-x-offset', 'text-content',
        'group-transform', 'group-class'
    ],
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
        bus.$on(events.DRAG_OPERATION_STARTED, () => this.globalDragStartHandler());
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
                    bus.$emit(events.DRAG_OPERATION_STARTED);
                },
                onDrag: function(this: any) {
                    // The problem here is that the nodeDropTargets becomes of type g.
                    // Whereas node.target is registered on the circle itself.
                    console.log("drop target length is %o", instance.nodeDropTargets.length);
                    console.log("typeof this.target = %o", this.target);
                    console.log("typeof first item = %o", instance.nodeDropTargets[0]);

                    const withoutMe = instance.nodeDropTargets.filter(x => x !== this.target);
          
                    console.log("withoutMe length is %o", withoutMe.length);

                    const targetsHit = withoutMe.filter(e => this.hitTest(e));
 
                    console.log("targets hit = %o", targetsHit)
                },
                onDragEnd: function(this: any) {
                    console.log("drag ended");

                    // hittest can't accept a class, only an id, and should really be element

                    const targetsHit = instance.widgetDropTargets.filter(
                        e => this.hitTest(e)
                    );

                    console.log("hit targets were %o", targetsHit);

                    TweenLite.to(
                        this.target, constants.TWEEN_GHOST_RETURN_TIME_SECONDS, { x: 0, y: 0 }
                    );
                }
            };


            const result = Draggable.create(ghostCircle, vars);
            console.log("result of creating draggable was %o", result);
        })
    },
    methods: {
        globalDragStartHandler() {
            console.log("registered start of drag");
        }
    },
    computed: {
        // Just a utility method to convert between the units.
        ghostRadiusPx(this: any) {
            return this.ghostRadius;
        },
        widgetDropTargets: function(this: any) {
            return this.$store.getters.widgetDropTargets;
        },
        nodeDropTargets: function(this: any) {
            return this.$store.getters.nodeDropTargets;
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

