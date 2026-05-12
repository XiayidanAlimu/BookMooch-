<template>
  <div>
    <a-alert
      v-if="userStore.isLoggedIn"
      :message="`当前用户：${userStore.currentUser.fullname}（${userStore.currentUser.username}），已捐赠 ${userStore.currentUser.donated_books_count || 0} 本书。`"
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

    <a-modal
      v-model:visible="showDonateModal"
      title="捐书登记"
      :width="600"
      :footer="null"
    >
      <BookForm @submitted="handleBookSubmitted" @cancel="showDonateModal = false" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useBooksStore } from '../stores/books'
import { useSettingsStore } from '../stores/settings'
import CategoryFilter from '../components/CategoryFilter.vue'
import BookForm from '../components/BookForm.vue'
import BookList from '../components/BookList.vue'

const booksStore = useBooksStore()
const settingsStore = useSettingsStore()
const showDonateModal = ref(false)
const viewMode = ref('card')

const handleBookSubmitted = () => {
  showDonateModal.value = false
  booksStore.fetchBooks()
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
