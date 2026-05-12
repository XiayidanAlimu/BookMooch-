<template>
  <a-card class="register-card" title="用户注册">
    <a-form :model="form" @submit="handleSubmit" layout="vertical">
      <a-form-item field="username" label="用户名" required>
        <a-input v-model="form.username" placeholder="请输入用户名" />
      </a-form-item>
      <a-form-item field="password" label="密码" required>
        <a-input-password v-model="form.password" placeholder="请输入密码" />
      </a-form-item>
      <a-form-item field="fullname" label="真实姓名" required>
        <a-input v-model="form.fullname" placeholder="请输入真实姓名" />
      </a-form-item>
      <a-form-item field="email" label="邮箱">
        <a-input v-model="form.email" placeholder="请输入邮箱（可选）" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="loading" style="width: 100%;">
          注册
        </a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>

import { inject, reactive, ref } from 'vue'
import { Message } from '@arco-design/web-vue'

const userStore = inject('userStore') // 从 App.vue 注入 userStore
const emit = defineEmits(['register-success'])

const form = reactive({
  username: '',
  password: '',
  fullname: '',
  email: '',
})

const loading = ref(false)

const handleSubmit = async () => {
  if (!form.username.trim() || !form.password.trim() || !form.fullname.trim()) {
    Message.error('请填写用户名、密码和真实姓名。')
    return
  }

  loading.value = true
  try {
    const result = await userStore.register(form)
    if (result.success) {
      Message.success('注册成功！请登录。')
      emit('register-success')
    } else {
      Message.error(result.error)
    }
  } catch (error) {
    Message.error('注册失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-card {
  max-width: 400px;
  margin: 0 auto;
}
</style>