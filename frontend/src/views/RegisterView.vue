<template>
  <div class="auth-page">
    <RegisterForm @register-success="handleRegisterSuccess" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import RegisterForm from '../components/RegisterForm.vue'

const router = useRouter()

const handleRegisterSuccess = () => {
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.auth-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px 0;
}
</style>
