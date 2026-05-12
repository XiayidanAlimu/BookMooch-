<template>
  <div class="auth-page">
    <LoginForm @login-success="handleLoginSuccess" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import { inject } from 'vue'

const router = useRouter()
const userStore = inject('userStore') // 从 App.vue 注入 userStore

const handleLoginSuccess = async () => {
  await userStore.loadCurrentUser()
  router.push({ name: 'Home' })
}
</script>

<style scoped>
.auth-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px 0;
}
</style>
