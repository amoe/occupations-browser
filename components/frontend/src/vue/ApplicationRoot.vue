<template>
  <div class="page">
    <div class="taxonomy">
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import utility from '../utility';
import * as d3 from 'd3';
import graph from '../graph';
import * as dateFns from 'date-fns';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';

export default Vue.extend({
    components: {},
    data: function() {
        return {
        };
    },
    methods: {
    },
    created: function() {
    },
    // mapState doesn't work with typescript: "Property 'mapState' does not exist on type"
    // So we manually create the relevant computed properties.
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        }, ...mapGetters([])
    }
});
</script>

<style>
</style>
