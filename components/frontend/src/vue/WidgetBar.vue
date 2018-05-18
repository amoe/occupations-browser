<template>
  <div class="widget-bar">
    <div>
      <taxonomy-widget v-for="item in widgetOrder"
                       :key="item"
                       :name="item"
                       :category="widgets[item].category"
                       :content="widgets[item].content"
                       :includedInWorkingSet="widgets[item].includedInWorkingSet">
      </taxonomy-widget>
    </div>

    <el-button v-on:click="addWidget"
               type="primary"
               icon="el-icon-plus"
               circle></el-button>

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
import { v4 as uuidv4 } from 'uuid';

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
    created: function() {
        // Set up all of our events
        bus.$on(events.WIDGET_REMOVED, (name) => this.handleWidgetRemoved(name));
    },
    methods: {
        handleWidgetRemoved(name) {
            console.log("received widget removed event, name was %o", name);
            this.$store.commit(mc.REMOVE_WIDGET, {name});
        },
        addWidget() {
            console.log("adding widget");

            // This should really happen in one mutation
            const id = uuidv4();
            this.widgets[id] = {
                content: "New widget",
                category: 'title',
                includedInWorkingSet: false
            };

            this.$store.commit(mc.ADD_WIDGET, {id});
        },
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
