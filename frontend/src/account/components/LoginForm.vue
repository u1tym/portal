<template>
  <div class="login-form">
    <h2>ログイン</h2>
    <form v-if="!isLoggedIn" @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">ユーザ名:</label>
        <input
          id="username"
          v-model="username"
          type="text"
          required
          :disabled="isLoading"
        />
      </div>

      <div class="form-group">
        <label for="password">パスワード:</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          :disabled="isLoading"
        />
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '処理中...' : 'ログイン' }}
      </button>
    </form>

    <!-- ログイン成功後のメニュー表示 -->
    <div v-if="isLoggedIn" class="menu-section">
      <h3>メニュー</h3>
      <div class="menu-buttons">
        <button
          v-for="(menuItem, index) in menuItems"
          :key="index"
          @click="navigateToMenu(menuItem.url)"
          class="menu-button"
        >
          {{ menuItem.title }}
        </button>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { AuthService } from '../services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const isLoggedIn = ref(false);
const menuItems = ref<Array<{title: string, url: string}>>([]);

const generateHash = async (password: string, key: string): Promise<string> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(password + key);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
};

const showError = (message: string) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = '';
  }, 5000);
};

const handleLogin = async () => {
  if (!username.value || !password.value) {
    showError('ユーザ名とパスワードを入力してください');
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 1. キー値取得
    const keyResponse = await AuthService.getKey({ username: username.value });
    const key = keyResponse.key;

    // 2. ハッシュ値生成
    const hash = await generateHash(password.value, key);

    // 3. ログイン認証
    const loginResponse = await AuthService.login({
      username: username.value,
      key: key,
      hash: hash
    });

    // 4. セッション保存とメニュー表示
    sessionStorage.setItem('session_string', loginResponse.session_string);
    menuItems.value = loginResponse.menu || [];
    isLoggedIn.value = true;

  } catch (error) {
    const message = error instanceof Error ? error.message : 'ログインに失敗しました';
    showError(message);
  } finally {
    isLoading.value = false;
  }
};

const navigateToMenu = (url: string) => {
  window.location.href = url;
};
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  text-align: center;
}

.menu-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.menu-section h3 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-button {
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.menu-button:hover {
  background-color: #218838;
}

.menu-button:active {
  background-color: #1e7e34;
}
</style>
