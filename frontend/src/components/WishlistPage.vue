<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="bg-white rounded-xl shadow-sm p-6">
      <h2 class="text-2xl font-bold mb-4">我的心愿单</h2>
      <div v-if="!userStore.isLoggedIn" class="rounded-lg border border-dashed border-gray-300 p-8 text-center text-gray-600">
        <p class="mb-3">请先登录后查看心愿单。</p>
      </div>
      <div v-else>
        <div class="mb-4 flex items-center justify-between gap-4">
          <div>
            <p class="text-sm text-gray-500">已加入心愿单的图书会在此展示。</p>
            <p class="text-sm text-gray-500">支持移除单本图书。</p>
          </div>
          <a-button type="primary" @click="refreshList">刷新列表</a-button>
        </div>

        <vxe-list
          class="rounded-xl border border-gray-100"
          :data="ordersStore.wishlist"
          :height="listHeight"
          :scroll-y="{ enabled: true, gt: 20 }"
          :loading="loading"
        >
          <template #default="{ items }">
            <div v-if="!loading && items.length === 0" class="py-12 text-center text-gray-500">
              暂无心愿单图书，去首页添加一本喜欢的书吧。
            </div>
            <div v-for="item in items" :key="item.id" class="flex flex-col md:flex-row items-start md:items-center gap-4 p-4 border-b border-gray-100 last:border-b-0">
              <div class="flex items-center gap-4 w-full md:w-auto">
                <img :src="item.cover_url || defaultCover(item.isbn)" alt="封面" class="w-20 h-28 object-cover rounded-lg bg-gray-100" @error="onImageError" />
                <div class="min-w-0">
                  <h3 class="text-base font-semibold text-gray-900 truncate">{{ item.title }}</h3>
                  <p class="text-sm text-gray-600 truncate">作者：{{ item.author }}</p>
                  <p class="text-sm text-gray-500 truncate">分类：{{ item.category_name || '未分类' }}</p>
                </div>
              </div>
              <div class="flex-1 text-sm text-gray-600">
                <p class="truncate">捐赠者：{{ item.donor || '匿名' }}</p>
                <p class="truncate">添加时间：{{ formatDate(item.created_at || item.donated_at) }}</p>
                <p v-if="item.description" class="mt-2 text-gray-500 line-clamp-2">{{ item.description }}</p>
              </div>
              <div class="flex flex-col items-start gap-2 md:items-end">
                <a-button size="mini" type="secondary" @click="removeFromWishlist(item)">移除</a-button>
              </div>
            </div>
          </template>
        </vxe-list>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, inject } from 'vue'
import { useOrdersStore } from '../stores/orders'

const ordersStore = useOrdersStore()

const userStore = inject('userStore') // 从 App.vue 注入 userStore
const settingsStore = inject('settingsStore') // 从 App.vue 注入 settingsStore

const loading = ref(false)

const listHeight = computed(() => {
  const offset = 250
  const minHeight = 420
  const height = settingsStore.windowHeight - offset
  return `${height > minHeight ? height : minHeight}px`
})

const refreshList = async () => {
  if (!userStore.isLoggedIn) return
  loading.value = true
  await ordersStore.fetchWishlist()
  loading.value = false
}

const removeFromWishlist = async (item) => {
  const response = await ordersStore.removeFromWishlist(item.book_id || item.id)
  if (response.success) {
    await ordersStore.fetchWishlist()
  }
}

const defaultCover = (isbn) => {
  return isbn ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg` : 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20width=%22200%22%20height=%22300%22%3E%3Crect%20width=%22200%22%20height=%22300%22%20fill=%22%23e5e7eb%22/%3E%3Ctext%20x=%22100%22%20y=%22150%22%20text-anchor=%22middle%22%20fill=%22%236b7280%22%20font-size=%2214%22%3ENo%20Cover%3C/text%3E%3C/svg%3E'
}

const onImageError = (event) => {
  event.target.onerror = null
  event.target.src = defaultCover('')
}

const formatDate = (value) => {
  return value ? new Date(value).toLocaleString('zh-CN') : ''
}

onMounted(async () => {
  if (userStore.isLoggedIn) {
    loading.value = true
    await ordersStore.fetchWishlist()
    loading.value = false
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>