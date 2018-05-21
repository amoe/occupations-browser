<template>
  <div>
    <ul class="text-lines">
    </ul>


    <el-table :data="tableData" :cell-class-name="cellClassName">
      <el-table-column prop="text" label="Text"></el-table-column>

      <el-table-column
        label="Operations" width="180">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleEdit(scope.$index, scope.row)">Confirm</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">Deny</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    components: {},
    data() {
        return {
            tableData: [
                {
                    text: "On this afternoon I saw prisoners loitering about the yard"
                },
                {
                    text: "On gaining access to the roof we saw Hall standing by a quantity of lead which had been ripped off and was ready for removal"
                },
                {
                    text: "On being takes to the station and charged they made no reply"
                }
            ]
        };
    },
    methods: {
        cellClassName(arg) {
            if (arg.columnIndex === 0) {
                return 'text-cell';
            }
        }
    }

});
</script>

<style>
ul.text-lines {
    list-style-type: none;
    font-family: monospace;
}

.text-cell {
    font-family: monospace;
}
</style>
