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
    <!--
    <circle class="ghost-node"
            :r="ghostRadiusPx"
            ref="ghostNodeSvgCircle"
            :cx="cx"
            :cy="cy"
            :opacity="ghostOpacity">
      <title>This is a tooltip</title>
    </circle>
    -->
  </g>
</template>

<script lang="ts">
import Vue from 'vue';
import * as d3 from 'd3';
import mc from '../mutation-constants';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';

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
    methods: {
    },
    computed: {
        ghostRadiusPx(this: any) {
            return this.ghostRadius;
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

