<template>
  <div class="page">
    <p>Hello world</p>

    <svg :width="width" :height="height">
      <g v-for="bar in data" :transform="getBarTransformation(bar)">
        <g v-for="(groupTotal, groupIndex)  in bar.groups"
           :transform="getGroupTransformation(bar.groups, groupIndex)">
          <circle v-for="i in groupTotal"
                  cx="50" :cy="i * 10" r="2"/>
        </g>
      </g>
    </svg>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import * as _ from 'lodash';

const GLYPH_Y_OFFSET = 10;

export default Vue.extend({
    components: {},
    data() {
        return {
            width: 1024,
            height: 576,
            data: [
                {
                    x: 1,
                    groups: [25, 25, 25, 25],
                },
                {
                    x: 2,
                    groups: [0, 50, 25, 25],
                },
                {
                    x: 3,
                    groups: [2, 2, 48, 48],
                }            
            ]
        };
    },
    methods: {
        getBarTransformation(bar) {
            const xTranslation = bar.x * 20;

            return `translate(${xTranslation}, 0)`;
        },
        getGroupTransformation(groups, indexWithinGroup) {
            console.log("groups passed were %o", groups);
            console.log("index within group passed was %o", indexWithinGroup);
        }
    },
    computed: {
    }
});
</script>

<style>
svg {
    border: 1px solid black;
}
</style>
