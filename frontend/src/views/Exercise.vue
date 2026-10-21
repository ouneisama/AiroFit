<template>
  <div class="page">
    <h1>运动训练</h1>
    <div class="exercise-list">
      <el-card class="card" shadow="hover">
        <h3>俯卧撑</h3>
        <p>动作矫正 + 计数</p>
        <el-button type="primary">开始</el-button>
      </el-card>
      <el-card class="card" shadow="hover">
        <h3>深蹲</h3>
        <p>姿势识别训练</p>
        <el-button type="primary">开始</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
export default { name: 'Exercise' }
</script>

<style scoped>
.page { padding: 30px; }
.exercise-list { display: flex; gap: 20px; margin-top: 20px; }
.card { width: 200px; text-align: center; padding: 20px; }
</style>