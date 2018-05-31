<template>
  <div class="taxonomy-widget"
        draggable="true"
        v-on:dragstart="dragStart"
        v-on:dragover.prevent="dragOver"
        v-on:drop="drop"
        v-bind:style="calculateStyle()"
        :class="category">
    <!-- Dragover must be preventDefaulted, because the default handler will
         disallow a drop. -->
    <el-button v-on:click="removeWidget"
               type="info"
               icon="el-icon-close"></el-button>


    <el-select v-model="taxonomyType" placeholder="Taxonomy type">
      <el-option
        v-for="item in availableTaxonomyTypes"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select> 

    <!-- These funky names are just to disambiguate and avoid the use of the
         word 'type'. -->
    <el-input name="phylum" :value="content"></el-input>
    <el-input name="subPhylum" :value="content"></el-input>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {mapGetters} from 'vuex';
import mc from '../mutation-constants';
import events from '../events';
import bus from '../event-bus';

const DND_DATA_CONTENT_TYPE = 'text/plain';

export default Vue.extend({
    props: ['content', 'name', 'category', 'includedInWorkingSet'],
    components: {},
    data: function() {
        return {
            availableTaxonomyTypes: [
                {label: 'Title', value: 'title'},
                {label: 'Place', value: 'place'},
                {label: 'Object', value: 'object'}
            ],
            taxonomyType: null
        };
    },
    methods: {
        removeWidget() {
            console.log("about to broadcast event");
            // This should be broacasting an event on the bus.
            bus.$emit(events.WIDGET_REMOVED, this.name);
        },
        dragOver(e) {
            console.log("drag over event happened, event was %o");
        },
        dragStart(e) {
            console.log("drag started, event was %o", e);
            e.dataTransfer.setData(DND_DATA_CONTENT_TYPE, this.name);
            e.dataTransfer.dropEffect = 'move';
        },
        drop(e) {
            const source = e.dataTransfer.getData(DND_DATA_CONTENT_TYPE);
            const target = this.name;
            console.log("drop occurred, drop data was %o", source);

            this.$store.commit(mc.SWAP_TAXONOMY_WIDGETS, {source, target});
        },
        getClass() {
            return {
                'title': true
            };
        },
        calculateStyle() {
            console.log("computed style called");

            // const hue = 22.4;
            // const lightness = 50;

            const hue = 222;
            const lightness = 88.2;

            const saturation = this.includedInWorkingSet ? 100 : 50;

            const colorExpression = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

            const foo =  `background-color: ${colorExpression}`;
            console.log("foo is %o", foo);
            return foo;
        }
    },
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        }, ...mapGetters([])
    }
})
</script>

<style>
.taxonomy-widget {
    border: 1px solid black;
    padding: 1em;
    margin: 1em;
    display: flex;
    flex-direction: column;
    width: 8em;
}

/*
.title {
    background-color: hsl(22.4, 100%, 50%);
}

.place {
    background-color: hsl(317.6, 100%, 29.2%);
}

.object {
    background-color: hsl(198.1, 100%, 44.3%);
}
*/
</style>
        
