<template>
  <div class="profile-view">
    <div class="profile-page">
        <a-card class="profile-card" title="用户详情">
        <a-descriptions :column="1" bordered>
            <a-descriptions-item label="用户名">
            {{ userStore.currentUser.username }}
            </a-descriptions-item>
            <a-descriptions-item label="真实姓名">
            {{ userStore.currentUser.fullname }}
            </a-descriptions-item>
            <a-descriptions-item label="邮箱">
            {{ userStore.currentUser.email || '未设置' }}
            </a-descriptions-item>
            <a-descriptions-item label="已捐书">
            {{ userStore.currentUser.donated_books_count || 0 }} 本
            </a-descriptions-item>
        </a-descriptions>
        </a-card>

        <a-tabs v-model:activeKey="activeTab" type="line" class="profile-tabs">
        <a-tab-pane key="my-books" title="我的捐书">
            <MyBooks />
        </a-tab-pane>
        <a-tab-pane key="wishlist" title="我的心愿单">
            <WishlistPage />
        </a-tab-pane>
        <a-tab-pane key="orders" title="我的领取订单">
            <OrdersPage />
        </a-tab-pane>
        </a-tabs>
    </div>
  </div>
</template>

<script setup>

import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'
import MyBooks from '../components/MyBooks.vue'
import WishlistPage from '../components/WishlistPage.vue'
import OrdersPage from '../components/OrdersPage.vue'

const activeTab = ref('my-books')

const router = useRouter()
const userStore = inject('userStore') // 从 App.vue 注入 userStore

if (!userStore.isLoggedIn) {
  router.replace({ name: 'Login' })
}

</script>

<style scoped>

.profile-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
}

.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card {
  width: 100%;
}

.profile-tabs {
  width: 100%;
}

</style>
