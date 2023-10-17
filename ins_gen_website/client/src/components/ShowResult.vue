<template>
    <div class="result">
      <el-table
          :data = "content"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          style="width: 100%;height: 300px;">
          <el-table-column
              prop="ci"
              label="词"
              width="300">
          </el-table-column>
          <el-table-column
              prop="ju"
              label="句"
              width="900">
          </el-table-column>
      </el-table>
    </div>
    
</template>

<script>
export default {
  name: 'ShowResult',
  props: ['content'],
}
</script>

<style scoped>
</style>
