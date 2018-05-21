<template>
  <div class="page">
    <p>Hello world</p>

    <svg :width="width" :height="height">
      <g v-for="bar in data" :transform="getBarTransformation(bar)">
        <g v-for="(groupTotal, groupIndex)  in bar.groups"
           class="bar-group"
           :transform="getGroupTransformation(bar.groups, groupIndex)">
          <circle v-for="i in groupTotal"
                  :fill="groupColors[groupIndex]"
                  cx="50" :cy="i * constants.GLYPH_Y_OFFSET" r="2"/>
        </g>
      </g>
    </svg>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import * as _ from 'lodash';

const BAR_X_OFFSET = 5;
const GLYPH_Y_OFFSET = 7;
const GROUP_MAX = 4;
const TIMELINE_POINTS = 200;

function createGroup(n) {
    return _.map(_.range(n), i => _.random(GROUP_MAX));
}

export default Vue.extend({
    components: {},
    data() {
        return {
            width: 1366,
            height: "8em",
            data: [
                {
                    x: 1,
                    groups: [25, 25, 25, 25]
                },
                {
                    x: 2,
                    groups: [0, 50, 25, 25]
                },
                {
                    x: 3,
                    groups: [2, 2, 48, 48]
                }            
            ],
            constants: {
                GLYPH_Y_OFFSET, BAR_X_OFFSET
            },
            groupColors: [
                'red', 'green', 'blue', 'purple'
            ]
        };
    },
    created() {
        console.log("data is %o", JSON.stringify(this.data));
        this.generateData();
    },
    methods: {
        generateData() {
            this.data = _.map(_.range(TIMELINE_POINTS), x => ({x: x, groups: createGroup(4)}));
        },
        getBarTransformation(bar) {
            const xTranslation = bar.x * BAR_X_OFFSET;
            return `translate(${xTranslation}, 0)`;
        },
        getGroupTransformation(groups, indexWithinGroup) {
            const previousGlyphs = _.take(groups, indexWithinGroup);
            const previousSpace = _.sum(previousGlyphs) * GLYPH_Y_OFFSET;
            const yTranslation = previousSpace;
            return `translate(0, ${yTranslation})`;
        },
        getGroupColor(indexWithinGroup) {
            return this.groupColors[indexWithinGroup];
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
