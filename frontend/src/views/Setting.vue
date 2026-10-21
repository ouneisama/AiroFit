<template>
  <div class="page">
    <h1>系统设置</h1>
    <el-form label-width="100px">
      <el-form-item label="昵称">
        <el-input placeholder="请输入昵称"></el-input>
      </el-form-item>
      <el-form-item label="主题">
        <el-select placeholder="选择主题">
          <el-option label="浅色" value="light"></el-option>
          <el-option label="深色" value="dark"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">保存设置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default { name: 'Setting' }
</script>

<style scoped>
.page { padding: 30px; }
</style>