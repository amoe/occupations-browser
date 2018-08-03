<template>
  <div id="graph-controls">
    <el-button v-on:click="updateFromBackend">Update from backend</el-button>

    <div>
      <label>Root</label>

      <el-select filterable
                 remote
                 :remote-method="searchRoots"
                 v-on:change="changed"
                 loading-text="Loading"
                 placeholder="Root"
                 :value="selectedRoot">
        <el-option v-for="item in possibleRoots"
                   :key="item.value"
                   :label="item.label"
                   :value="item.value"/>
      </el-select>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import mc from '../mutation-constants';
import Vue from 'vue';
import {mapGetters} from 'vuex';

export default Vue.extend({
    props: ['zoomDepth'],
    created() {
        this.updateFromBackend();
    },
    methods: {
        searchRoots(query) {
            console.log("remote method called with argument %o", query);
            axios.get("/api/tezra/roots?q=" + query).then(response => {
                this.$store.commit(mc.SET_POSSIBLE_ROOTS, response.data.map(x => ({value: x, label: x})));
            }).catch(error => {
                // Need to fix this
                this.$message.error('Failed to query data from API');
            });
        },
        changed(val) {
            console.log("changed was called with value %o", val);
            this.$store.commit(mc.SELECT_ROOT, val);
            this.updateFromBackend();
        },
        updateFromBackend(this: any) {
            axios.get(
                "/api/tezra/tree?root=" + this.selectedRoot + "&zoom_depth=" + this.zoomDepth
            ).then(response => {
                this.$store.commit(mc.SET_GRAPH_DATA, response.data);
            }).catch(error => {
                this.$message.error('Failed to query data from API');
            });
        }
    },
    computed: { ...mapGetters(['selectedRoot', 'possibleRoots']) }
});
</script>
