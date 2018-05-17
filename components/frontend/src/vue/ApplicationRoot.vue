<template>
  <div class="page">
    <div>
      <taxonomy-widget></taxonomy-widget>
      <taxonomy-widget></taxonomy-widget>
      <taxonomy-widget></taxonomy-widget>
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
import TaxonomyWidget from './TaxonomyWidget.vue';

export default Vue.extend({
    components: {TaxonomyWidget},
    data: function() {
        return {
            widgetColSpan: 8,
            value: null,
            options: [
                {'label': 'Foo', 'value': 'foo'},
                {'label': 'Bar', 'value': 'bar'}
            ]
        };
    },
    methods: {
        dragStart(e) {
            console.log("drag started, event was %o", e);
        },
        drop(e) {
            console.log("drop occurred, event was %o", e);
        }
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
.grid-content {
    border-radius: 4px;
    min-height: 36px;
}
</style>
