<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="header-content">
        <h1>公益图书馆</h1>
        <div class="user-actions">
          <a-button @click="currentPage = 'home'" type="text">首页</a-button>
          <a-button @click="currentPage = 'wishlist'" type="text">我的心愿单</a-button>
          <a-button @click="currentPage = 'orders'" type="text">领取订单</a-button>
          <a-button @click="currentPage = 'help'" type="text">帮助</a-button>
          <a-button v-if="!userStore.isLoggedIn" @click="currentPage = 'login'" type="text">登录</a-button>
          <a-button v-if="!userStore.isLoggedIn" @click="currentPage = 'register'" type="text">注册</a-button>
          <a-button v-if="userStore.isLoggedIn" @click="currentPage = 'profile'" type="text">我的详情</a-button>
          <a-button v-if="userStore.isLoggedIn" @click="currentPage = 'my-books'" type="text">我的捐书</a-button>
          <a-button v-if="userStore.isLoggedIn" @click="userStore.logout()" type="text">登出</a-button>
        </div>
      </div>
    </a-layout-header>

    <a-layout-content class="content">
      <div class="container">
        <template v-if="currentPage === 'login'">
          <LoginForm @login-success="handleLoginSuccess" />
        </template>

        <template v-else-if="currentPage === 'register'">
          <RegisterForm @register-success="handleRegisterSuccess" />
        </template>

        <template v-else-if="currentPage === 'profile'">
          <UserProfile :user="userStore.currentUser" />
        </template>

        <template v-else-if="currentPage === 'my-books'">
          <MyBooks />
        </template>

        <template v-else-if="currentPage === 'wishlist'">
          <WishlistPage />
        </template>

        <template v-else-if="currentPage === 'orders'">
          <OrdersPage />
        </template>

        <template v-else-if="currentPage === 'help'">
          <HelpPage />
        </template>

        <template v-else>
          <a-alert
            v-if="userStore.isLoggedIn"
            :message="`当前用户：${userStore.currentUser.fullname}（${userStore.currentUser.username}），已捐赠 ${userStore.currentUser.donated_books_count} 本书。`"
            type="info"
            show-icon
            style="margin-bottom: 16px;"
          />

          <div class="toolbar">
            <a-space>
              <a-button @click="showDonateModal = true" type="primary">
                我要捐书
              </a-button>
              <a-radio-group v-model="viewMode" type="button">
                <a-radio value="card">卡片视图</a-radio>
                <a-radio value="list">列表视图</a-radio>
              </a-radio-group>
            </a-space>
          </div>

          <CategoryFilter
            :categories="booksStore.categories"
            :selected-category-id="booksStore.selectedCategoryId"
            @category-change="booksStore.setSelectedCategory"
          />

          <BookList :books="booksStore.books" :view-mode="viewMode" />
        </template>

        <a-modal
          v-model:visible="showDonateModal"
          title="捐书登记"
          :width="600"
          :footer="null"
        >
          <BookForm @submitted="handleBookSubmitted" @cancel="showDonateModal = false" />
        </a-modal>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useUserStore } from './stores/user'
import { useBooksStore } from './stores/books'
import { useSettingsStore } from './stores/settings'
import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import UserProfile from './components/UserProfile.vue'
import MyBooks from './components/MyBooks.vue'
import WishlistPage from './components/WishlistPage.vue'
import OrdersPage from './components/OrdersPage.vue'
import HelpPage from './components/HelpPage.vue'
import CategoryFilter from './components/CategoryFilter.vue'
import BookForm from './components/BookForm.vue'
import BookList from './components/BookList.vue'

const userStore = useUserStore()
const booksStore = useBooksStore()
const settingsStore = useSettingsStore()
const currentPage = ref('home')
const showDonateModal = ref(false)
const viewMode = ref('card')

const handleLoginSuccess = () => {
  currentPage.value = 'home'
}

const handleRegisterSuccess = () => {
  currentPage.value = 'login'
}

const handleBookSubmitted = () => {
  showDonateModal.value = false
  booksStore.fetchBooks()
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

.header-content h1 {
  margin: 0;
  color: #1d4ed8;
}

.user-actions {
  display: flex;
  gap: 8px;
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