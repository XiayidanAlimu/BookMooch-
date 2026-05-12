<template>
  <a-card class="form-card" title="捐书登记">
    <a-form :model="formState" @submit="handleSubmit" layout="vertical">
      <a-form-item label="搜索书名">
        <a-select
          v-model="selectedBookKey"
          remote
          filterable
          :remote-method="handleBookSearch"
          placeholder="输入书名搜索图书"
          :loading="searchLoading"
          allow-clear
          @change="handleSelectBook"
        >
          <a-option
            v-for="item in searchOptions"
            :key="item.key"
            :value="item.key"
          >
            {{ item.label }}
          </a-option>
        </a-select>
      </a-form-item>

      <a-form-item>
        <div class="search-hint">
          请选择匹配项后会自动填写书名、作者和ISBN；如果没有匹配项，请点击“新增数据详情”补充信息。
        </div>
      </a-form-item>

      <a-form-item field="title" label="书名" required>
        <a-input v-model="formState.title" placeholder="图书名称" />
      </a-form-item>
      <a-form-item field="author" label="作者">
        <a-input v-model="formState.author" placeholder="图书作者" />
      </a-form-item>
      <a-form-item field="isbn" label="ISBN">
        <a-input v-model="formState.isbn" placeholder="图书ISBN" />
      </a-form-item>
      <a-form-item field="coverUrl" label="封面地址" v-if="showDetails || formState.cover_url">
        <a-input v-model="formState.cover_url" placeholder="可选，输入封面图片URL" />
      </a-form-item>
      <a-form-item>
        <a-button type="secondary" @click="showDetails = true">
          新增数据详情
        </a-button>
      </a-form-item>
      <a-form-item field="categoryId" label="分类" v-if="showDetails">
        <a-select v-model="formState.categoryId" placeholder="请选择分类">
          <a-option :value="0">请选择分类</a-option>
          <a-option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </a-option>
        </a-select>
      </a-form-item>
      <a-form-item field="description" label="简介" v-if="showDetails">
        <a-textarea
          v-model="formState.description"
          placeholder="可选，简单介绍书籍"
          :rows="4"
        />
      </a-form-item>
      <a-form-item>
        <a-space>
          <a-button type="primary" html-type="submit" :loading="loading">
            提交捐书
          </a-button>
          <a-button @click="$emit('cancel')" type="outline">
            取消
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
    <a-alert
      v-if="!isLoggedIn"
      message="请先登录后再提交捐书。"
      type="warning"
      show-icon
      style="margin-top: 16px;"
    />
  </a-card>
</template>

<script setup>
import { reactive, ref, computed, inject } from 'vue'
import { searchBooks } from '../api/search'
import { Message } from '@arco-design/web-vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['submitted'])
const userStore = inject('userStore') // 从 App.vue 注入 userStore
const booksStore = inject('booksStore') // 从 App.vue 注入 booksStore  

const formState = reactive({
  title: '',
  author: '',
  isbn: '',
  cover_url: '',
  categoryId: 0,
  description: '',
})

const searchOptions = ref([])
const searchResults = ref({})
const selectedBookKey = ref(null)
const searchLoading = ref(false)
const showDetails = ref(false)
const loading = ref(false)
const isLoggedIn = computed(() => userStore.isLoggedIn)

const handleBookSearch = async (query) => {
  if (!query || query.length < 2) {
    searchOptions.value = []
    return
  }

  searchLoading.value = true
  try {
    const response = await searchBooks(query)
    searchResults.value = {}
    searchOptions.value = response.map((item) => {
      searchResults.value[item.id] = item
      return {
        key: item.id,
        label: `${item.title}${item.author ? ` / ${item.author}` : ''}`,
      }
    })
  } catch (error) {
    console.error('搜索图书失败：', error)
    searchOptions.value = []
  } finally {
    searchLoading.value = false
  }
}

const handleSelectBook = (value) => {
  const result = searchResults.value[value]
  if (result) {
    formState.title = result.title
    formState.author = result.author
    formState.isbn = result.isbn
    formState.cover_url = result.cover_url || ''
  }
}

const handleSubmit = async () => {
  if (!isLoggedIn.value) {
    Message.error('请先登录后再提交捐书。')
    return
  }

  if (!formState.title.trim()) {
    Message.error('请填写书名。')
    return
  }

  loading.value = true
  try {
    const bookData = {
      title: formState.title,
      author: formState.author.trim() || '未知作者',
      isbn: formState.isbn,
      cover_url: formState.cover_url,
      description: formState.description,
      category_id: formState.categoryId === 0 ? null : formState.categoryId,
    }

    const result = await booksStore.addBook(bookData)
    if (result.success) {
      Message.success('捐书信息提交成功！')
      Object.assign(formState, {
        title: '',
        author: '',
        isbn: '',
        cover_url: '',
        categoryId: 0,
        description: '',
      })
      selectedBookKey.value = null
      showDetails.value = false
      emit('submitted')
    } else {
      Message.error(result.error)
    }
  } catch (error) {
    Message.error('提交失败，请稍后重试。')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-card {
  max-width: 640px;
  margin: 0 auto;
}

.search-hint {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 8px;
}
</style>
