<template>
  <a-card class="profile-card" title="用户详情">
    <a-descriptions :column="1" bordered>
      <a-descriptions-item label="用户名">
        {{ user.username }}
      </a-descriptions-item>
      <a-descriptions-item label="真实姓名">
        {{ user.fullname }}
      </a-descriptions-item>
      <a-descriptions-item label="邮箱">
        {{ user.email || '未设置' }}
      </a-descriptions-item>
      <a-descriptions-item label="已捐书">
        {{ user.donated_books_count || 0 }} 本
      </a-descriptions-item>
    </a-descriptions>
  </a-card>
</template>

<script setup>
const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})
</script>

<style scoped>
.profile-card {
  max-width: 600px;
  margin: 0 auto;
}
</style>
