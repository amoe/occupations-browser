<template>
  <div class="widget-panel">
    <div class="widget-hbar">
      <taxonomy-widget v-for="item in widgetOrder"
                       ref="widgets"
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
import {VueConstructor} from 'vue';
import Draggable from 'gsap/Draggable';

// This 

type MyRefExtensions = VueConstructor<Vue & { $refs: { widgets: Vue[] } }>

export default (Vue as MyRefExtensions).extend({
    components: {TaxonomyWidget},
    // this.$refs.widgets will store list of dom nodes
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
    watch: {
        widgetOrder(this: any, newValue, oldValue) {
            console.log("widget order changed");
            this.$nextTick(() => this.configureDraggables())
        }
    },
    created: function() {
        // Set up all of our events
        bus.$on(events.WIDGET_REMOVED, (name) => this.handleWidgetRemoved(name));
    },
    mounted: function() {
        console.log("inside mounted callback");
        this.$nextTick(() => this.configureDraggables())
    },
    methods: {
        configureDraggables() {
            const widgetBar = this;

            console.log("about to configure draggables");

            const elements = this.$refs.widgets.map(x => x.$el);

            console.log("refs list is now %o", elements);

            const draggableOptions = {
                onDragStart: function(this: any) {
                    console.log("taxonomywidget: drag started");
                },
                onDragEnd: function(this: any) {
                    console.log("taxonomywidget: drag ended");

                    // hittest can't accept a class, only an id, and should really be element

                    const droppedTargets = elements.filter(validTarget => this.hitTest(validTarget));

                    if (droppedTargets.length === 0) {
                        console.log("taxonomywidget: hit NOT detected");
                    } else {
                        console.log("taxonomywidget: drop received");

                        console.log("droppedTargets is %o", droppedTargets);

                        widgetBar.handleDrop();
                    }
                }
            };


            const result = Draggable.create(elements, draggableOptions);
            console.log("taxonomywidget: result of creating draggable was %o", result);
        },
        handleDrop() {
            console.log("handling drop");

            // const source = e.dataTransfer.getData(DND_DATA_CONTENT_TYPE);
            // const target = this.name;
            // console.log("drop occurred, drop data was %o", source);

            // this.$store.commit(mc.SWAP_TAXONOMY_WIDGETS, {source, target});
        },
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
.widget-hbar {
    display: flex;
    flex-direction: row;
}
</style>
