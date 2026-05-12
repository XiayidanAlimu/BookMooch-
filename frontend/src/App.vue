<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="header-content">
        <h1 class="app-title" @click="goHome" tabindex="0">公益图书馆</h1>
        <div class="user-actions">
          <a-button @click="router.push({ name: 'Help' })" type="text">帮助</a-button>

          <template v-if="!userStore.isLoggedIn">
            <a-button @click="router.push({ name: 'Login' })" type="text">登录</a-button>
            <a-button @click="router.push({ name: 'Register' })" type="text">注册</a-button>
          </template>

          <template v-else>
            <a-dropdown trigger="click">
              <template #default>
                <div class="user-dropdown-trigger">
                  <a-avatar :size="40" class="user-avatar">
                    {{ userStore.currentUser.fullname ? userStore.currentUser.fullname[0] : 'U' }}
                  </a-avatar>
                  <span class="user-name">{{ userStore.currentUser.fullname || userStore.currentUser.username }}</span>
                </div>
              </template>
              <template #content>
                <div class="dropdown-menu">
                  <a-button type="text" class="dropdown-item" @click="router.push({ name: 'Profile' })">Profile</a-button>
                  <a-button type="text" class="dropdown-item" @click="handleLogout">Logout</a-button>
                </div>
              </template>
            </a-dropdown>
          </template>
        </div>
      </div>
    </a-layout-header>

    <a-layout-content class="content">
      <div class="container">
        <router-view />
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup>

import { onMounted, onBeforeUnmount, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { useBooksStore } from './stores/books'
import { useSettingsStore } from './stores/settings'

const router = useRouter()
const userStore = useUserStore()
const booksStore = useBooksStore()
const settingsStore = useSettingsStore()

provide('userStore', userStore)
provide('booksStore', booksStore)
provide('settingsStore', settingsStore)

const goHome = () => {
  router.push({ name: 'Home' })
}

const handleLogout = () => {
  userStore.logout()
  router.push({ name: 'Login' })
}

const updateWindowSize = () => {
  settingsStore.updateWindowSize(window.innerWidth, window.innerHeight)
}

onMounted(async () => {
  settingsStore.initWindowSize()
  window.addEventListener('resize', updateWindowSize)

  await booksStore.fetchCategories()
  await userStore.loadCurrentUser()
  await booksStore.fetchBooks()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateWindowSize)
})
</script>

<style>
.layout {
  min-height: 100vh;
}

.header {
    
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
    height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.app-title {
  margin: 0;
  color: #1d4ed8;
  cursor: pointer;
  user-select: none;
  font-size: 20px;
}

.user-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.user-dropdown-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.user-name {
  font-weight: 500;
  color: #1f2937;
}

.dropdown-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
}

.dropdown-item {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
}

.content {
  background: #f5f7fb;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 16px;
}

.toolbar {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>