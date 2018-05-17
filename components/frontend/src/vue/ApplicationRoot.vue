<template>
  <div class="page">
    <el-row>
      <el-col :span="24">
        <div class="grid-content bg-purple-dark">
          <p>Content content content content</p>
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <div class="grid-content bg-purple-dark">
          <p>Content content content content</p>
        </div>
      </el-col>
    </el-row>
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
.grid-content {
    border-radius: 4px;
    min-height: 36px;
}
</style>
