<template>
  <div class="page">
    <h1>个人资料</h1>
    <el-form label-width="100px">
      <el-form-item label="头像">
        <el-upload action="#" :show-file-list="false">
          <el-button>上传头像</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group>
          <el-radio label="男"></el-radio>
          <el-radio label="女"></el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="年龄">
        <el-input type="number" placeholder="年龄"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default { name: 'Profile' }
</script>

<style scoped>
.page { padding: 30px; }
</style>