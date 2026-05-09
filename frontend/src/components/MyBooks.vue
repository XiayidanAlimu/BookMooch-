<template>
  <a-card class="my-books-card" title="我的捐书记录">
    <a-spin :loading="loading">
      <div v-if="books.length === 0" class="empty-state">
        <a-empty description="您还没有捐书记录" />
      </div>
      <a-list v-else :data="books" bordered>
        <template #item="{ item }">
          <a-list-item>
            <a-list-item-meta>
              <template #title>
                <strong>{{ item.title }}</strong>
                <a-tag v-if="item.category_name" color="blue" style="margin-left: 8px;">
                  {{ item.category_name }}
                </a-tag>
              </template>
              <template #description>
                <div>作者：{{ item.author }}</div>
                <div v-if="item.isbn">ISBN：{{ item.isbn }}</div>
                <div v-if="item.description">{{ item.description }}</div>
                <div style="color: #6b7280; font-size: 12px;">捐赠时间：{{ item.donated_at }}</div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>
  </a-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useBooksStore } from '../stores/books'

const userStore = useUserStore()
const booksStore = useBooksStore()
const books = ref([])
const loading = ref(false)

const fetchMyBooks = async () => {
  if (!userStore.currentUser) return

  loading.value = true
  try {
    books.value = await booksStore.fetchUserBooks(userStore.currentUser.id)
  } catch (error) {
    console.error('获取我的捐书记录失败：', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMyBooks()
})
</script>

<style scoped>
.my-books-card {
  max-width: 800px;
  margin: 0 auto;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}
</style>