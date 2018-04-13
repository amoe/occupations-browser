<template>
  <svg :width="width" :height="height">
    <g :transform="rootTranslation">
      <path v-for="node in allButRoot"
            class="link"
            :d="getPathDescription(node)"/>
      
      <!-- The group for nodes and their associated labels -->
      <!-- The funny thing is that it's totally possible to rewrite these as
           a group of computed properties derived from the state. -->
      <!-- We just do it in this d3-ish way as a first pass. -->
      <g v-for="node in allIncludingRoot"
         :class="getNodeGroupClass(node)"
         :transform="getNodeGroupTransformation(node)">
        <circle r="1em"/>
        <text dy="0.31em"
              :transform="getTextRotation(node)"
              :text-anchor="getTextAnchor(node)"
              :x="getTextXOffset(node)">{{getNodeTextContent(node)}}</text>
      </g>
    </g>
  </svg>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
});
</script>

<style>
</style>
