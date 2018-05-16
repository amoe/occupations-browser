<template>
  <div>
    <p>Test component</p>

    <el-popover placement="top-start"
                title="Title"
                width="200"
                trigger="hover"
                ref="daveref"
                content="this is content, this is content, this is content">
    </el-popover>

    <el-button v-popover:daveref>Hover to activate</el-button>
  </div>
</template>

<script>
import Vue from 'vue';

export default Vue.extend({
});
</script>
