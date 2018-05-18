<template>
  <div class="page">
    <p>Hello world</p>

    <svg :width="width" :height="height">
      <g v-for="bar in data">
        <g v-for="groupTotal in bar.groups">
          <circle v-for="i in groupTotal"
                  cx="50" :cy="i * 10" r="2"/>
        </g>
      </g>
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
            height: 576,
            data: [
                {
                    x: 1,
                    groups: [25, 25, 25, 25],
                },
                {
                    x: 2,
                    groups: [0, 50, 25, 25],
                },
                {
                    x: 3,
                    groups: [2, 2, 48, 48],
                }            
            ]
        };
    }
});
</script>

<style>

svg {
    border: 1px solid black;
}

</style>
