<template>
  <div class="page">
    <div>
      <taxonomy-widget v-for="item in widgetOrder"
                       :key="item"
                       :name="item"
                       :category="widgets[item].category"
                       :content="widgets[item].content"
                       :includedInWorkingSet="widgets[item].includedInWorkingSet">
        </taxonomy-widget>
    </div>

    <button v-on:click="shuffle">Shuffle!</button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import utility from '../utility';
import * as d3 from 'd3';
import graph from '../graph';
import * as dateFns from 'date-fns';
import * as _ from 'lodash';
import {mapGetters} from 'vuex';
import bus from '../event-bus';
import events from '../events';
import mc from '../mutation-constants';
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
            ],
            widgets: {
                alpha: {
                    content: "Alpha Widget",
                    category: 'title',
                    includedInWorkingSet: true
                },
                beta: {
                    content: "Beta Widget",
                    category: 'place',
                    includedInWorkingSet: false
                },
                gamma: {
                    content: "Gamma Widget",
                    category: 'object',
                    includedInWorkingSet: true
                }
            },
        };
    },
    methods: {
        shuffle() {
            console.log("about to shuffle");
            this.$store.commit(mc.SHUFFLE);
        },
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
        },
        widgetOrder: function (this: any) {
            return this.$store.getters.widgetOrder;
        },
    }
});
</script>

<style>

body {
    margin-top: 2em;
}

button { margin: 2em; }
</style>
