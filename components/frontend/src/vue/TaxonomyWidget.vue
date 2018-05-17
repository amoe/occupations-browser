<template>
  <span>
    <!-- Dragover must be preventDefaulted, because the default handler will
         disallow a drop. -->
    <input draggable="true"
           v-on:dragstart="dragStart"
           v-on:dragover.prevent="dragOver"
           v-on:drop="drop"></input>
  </span>
</template>

<script lang="ts">
import Vue from 'vue';
import {mapGetters} from 'vuex';

export default Vue.extend({
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
        },
        drop(e) {
            console.log("drop occurred, event was %o", e);
        }
    },
    computed: {
        count: function (this: any) {
            return this.$store.state.count;
        }, ...mapGetters([])
    }
})
</script>
        
