<template>
  <div class="login-view">
    <LoginForm />
  </div>
</template>

<script setup lang="ts">
import LoginForm from '../components/LoginForm.vue';
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f2f5;
}
</style>
