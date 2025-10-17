<template>
  <div class="schedule-view">
    <h1>スケジュール管理</h1>
    <div v-if="isLoading" class="loading">
      スケジュールを取得中...
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <div v-if="scheduleData" class="schedule-info">
      <p>スケジュール取得完了</p>
      <p>ハッシュ値: {{ scheduleData.hash_value }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ScheduleService } from '../services/api';

const isLoading = ref(false);
const errorMessage = ref('');
const scheduleData = ref<{ hash_value: string } | null>(null);

const getSchedule = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // ローカルストレージからユーザー名とセッション文字列を取得
    const username = 'admin'; // 暫定的に固定値
    const sessionString = localStorage.getItem('session_string');

    if (!sessionString) {
      throw new Error('セッションが見つかりません');
    }

    // スケジュール取得要求
    const response = await ScheduleService.getSchedule({
      username: username,
      hash_value: sessionString
    });

    if (response.success) {
      // 新しいハッシュ値を保持
      scheduleData.value = { hash_value: response.hash_value };
      localStorage.setItem('session_string', response.hash_value);
    } else {
      throw new Error('スケジュール取得に失敗しました');
    }

  } catch (error) {
    const message = error instanceof Error ? error.message : 'スケジュール取得に失敗しました';
    errorMessage.value = message;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  getSchedule();
});
</script>

<style scoped>
.schedule-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f0f2f5;
  padding: 20px;
}

h1 {
  color: #333;
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 30px;
}

.loading {
  padding: 20px;
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
}

.error-message {
  padding: 20px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
}

.schedule-info {
  padding: 20px;
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 8px;
  text-align: center;
}

.schedule-info p {
  margin: 10px 0;
}
</style>
