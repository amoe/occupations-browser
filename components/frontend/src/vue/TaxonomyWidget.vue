<template>
  <div class="taxonomy-widget"
        draggable="true"
        v-on:dragstart="dragStart"
        v-on:dragover.prevent="dragOver"
        v-on:drop="drop">
    <!-- Dragover must be preventDefaulted, because the default handler will
         disallow a drop. -->
    <input name="taxonomyType" :value="content"></input>
    <input name="taxonomySubtype" :value="content"></input>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {mapGetters} from 'vuex';
import mc from '../mutation-constants';

const DND_DATA_CONTENT_TYPE = 'text/plain';

export default Vue.extend({
    props: ['content', 'name'],
    components: {},
    data: function() {
        return {
        };
    },
    methods: {
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
    background-color: #ff5f00;
    display: inline;
    padding: 1em;
    margin: 1em;
}
</style>
        
