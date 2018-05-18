<template>
  <div class="page">
    <p>Hello world</p>

    <svg :width="width" :height="height">
      <circle v-for="n in 10"
              cx="50"
              :cy="n * 10" r="2"/>
    </svg>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    components: {},
    data() {
        return {
            width: 1024,
            height: 576
        };
    }
});
</script>

<style>

svg {
    border: 1px solid black;
}

</style>
