<template>
  <a-card class="login-card" title="用户登录">
    <a-form :model="form" @submit="handleSubmit" layout="vertical">
      <a-form-item field="username" label="用户名" required>
        <a-input v-model="form.username" placeholder="请输入用户名" />
      </a-form-item>
      <a-form-item field="password" label="密码" required>
        <a-input-password v-model="form.password" placeholder="请输入密码" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading" style="width: 100%;">
          登录
        </a-button>
      </a-form-item>
    </a-form>
    <a-alert
      message="默认测试账号：alice / password，bob / password"
      type="info"
      show-icon
      style="margin-top: 16px;"
    />
  </a-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { Message } from '@arco-design/web-vue'

const userStore = useUserStore()
const emit = defineEmits(['login-success'])

const form = reactive({
  username: '',
  password: '',
})

const loading = ref(false)

const handleSubmit = async () => {
  if (!form.username.trim() || !form.password.trim()) {
    Message.error('请填写用户名和密码。')
    return
  }

  loading.value = true
  try {
    const result = await userStore.login(form.username, form.password)
    if (result.success) {
      Message.success('登录成功！')
      emit('login-success')
    } else {
      Message.error(result.error)
    }
  } catch (error) {
    Message.error('登录失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-card {
  max-width: 400px;
  margin: 0 auto;
}
</style>
