<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">当前捐书列表</h2>
      
      <a-spin :loading="loading">
        <!-- 空状态 -->
        <div v-if="books.length === 0" class="text-center py-16">
          <a-empty description="目前还没有捐书，欢迎成为第一位捐赠者。" />
        </div>

        <!-- 卡片视图 - GridLayout -->
        <div v-else-if="viewMode === 'card'" class="w-full">
          <grid-layout
            :layout.sync="layout"
            :col-num="12"
            :row-height="30"
            :is-draggable="false"
            :is-resizable="false"
            :is-mirrored="false"
            :margin="[20, 20]"
            :responsive="true"
            :use-css-transforms="true"
          >
            <grid-item
              v-for="(book, index) in books"
              :i="book.id"
              :key="book.id"
              :x="(index % 3) * 4"
              :y="Math.floor(index / 3) * 11"
              :w="4"
              :h="11"
              @resized="onItemMoved"
              @moved="onItemMoved"
            >
              <div class="book-card-container h-full bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden flex flex-col">
                <!-- 书籍封面 -->
                <div class="relative h-48 overflow-hidden bg-gray-100 flex-shrink-0">
                  <img
                    :src="getBookCover(book)"
                    :alt="book.title"
                    class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                    @error="handleImageError"
                  />
                </div>

                <!-- 书籍信息 -->
                <div class="flex-grow overflow-auto p-4 flex flex-col">
                  <!-- 标题 -->
                  <h3 class="text-sm font-bold text-gray-900 mb-3 line-clamp-2 leading-tight">
                    {{ book.title }}
                  </h3>

                  <!-- 基本信息 -->
                  <div class="text-xs text-gray-600 space-y-2 flex-grow">
                    <div class="flex items-start gap-1">
                      <span class="font-semibold flex-shrink-0">作者：</span>
                      <span class="break-words">{{ book.author }}</span>
                    </div>

                    <div v-if="book.isbn" class="flex items-start gap-1">
                      <span class="font-semibold flex-shrink-0">ISBN：</span>
                      <span class="break-words font-mono text-xs">{{ book.isbn }}</span>
                    </div>

                    <div class="flex items-start gap-1">
                      <span class="font-semibold flex-shrink-0">分类：</span>
                      <a-tag v-if="book.category_name" color="blue" class="text-xs">
                        {{ book.category_name }}
                      </a-tag>
                      <span v-else class="text-gray-400">未分类</span>
                    </div>

                    <div v-if="book.donor" class="flex items-start gap-1">
                      <span class="font-semibold flex-shrink-0">捐赠者：</span>
                      <span class="break-words">{{ book.donor }}</span>
                    </div>

                    <div class="flex items-start gap-1">
                      <span class="font-semibold flex-shrink-0">时间：</span>
                      <span class="text-gray-500">{{ formatDate(book.donated_at) }}</span>
                    </div>

                    <div v-if="book.description" class="flex items-start gap-1 pt-1">
                      <span class="font-semibold flex-shrink-0">描述：</span>
                      <p class="text-gray-500 line-clamp-2 text-xs leading-relaxed">
                        {{ book.description }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </grid-item>
          </grid-layout>
        </div>

        <!-- 列表视图 -->
        <a-list v-else :data="books" bordered>
          <template #item="{ item }">
            <a-list-item>
              <a-list-item-meta :avatar="h('img', { src: getBookCover(item), alt: item.title, class: 'list-cover', onError: handleImageError })">
                <template #title>
                  <div class="list-title">
                    <strong>{{ item.title }}</strong>
                    <a-tag v-if="item.category_name" color="blue" style="margin-left: 8px;">
                      {{ item.category_name }}
                    </a-tag>
                  </div>
                </template>
                <template #description>
                  <div class="list-info">
                    <a-space wrap>
                      <span><strong>作者：</strong>{{ item.author }}</span>
                      <span v-if="item.isbn"><strong>ISBN：</strong>{{ item.isbn }}</span>
                      <span v-if="item.donor"><strong>捐赠者：</strong>{{ item.donor }}</span>
                      <span><strong>时间：</strong>{{ formatDate(item.donated_at) }}</span>
                    </a-space>
                    <p v-if="item.description" class="book-desc">{{ item.description }}</p>
                  </div>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </template>
        </a-list>
      </a-spin>
    </div>
  </div>
</template>

<script setup>
import { defineProps, h, ref, computed } from 'vue'

const props = defineProps({
  books: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  viewMode: {
    type: String,
    default: 'list',
  },
})

// GridLayout 布局数据
const layout = computed(() => {
  return props.books.map((book, index) => ({
    x: (index % 3) * 4,
    y: Math.floor(index / 3) * 11,
    w: 4,
    h: 11,
    i: book.id.toString(),
  }))
})

const getBookCover = (book) => {
  if (book.cover_url) return book.cover_url
  if (book.isbn) return `https://covers.openlibrary.org/b/isbn/${book.isbn}-M.jpg`
  return 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22200%22%20height%3D%22300%22%3E%3Crect%20width%3D%22200%22%20height%3D%22300%22%20fill%3D%22%23e5e7eb%22%2F%3E%3Ctext%20x%3D%22100%22%20y%3D%22150%22%20text-anchor%3D%22middle%22%20fill%3D%226b7280%22%20font-size%3D%2214%22%3ENo%20Cover%3C%2Ftext%3E%3C%2Fsvg%3E'
}

const handleImageError = (event) => {
  if (event.target.src === getBookCover({})) return
  event.target.onerror = null
  event.target.src = 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22200%22%20height%3D%22300%22%3E%3Crect%20width%3D%22200%22%20height%3D%22300%22%20fill%3D%22%23e5e7eb%22%2F%3E%3Ctext%20x%3D%22100%22%20y%3D%22150%22%20text-anchor%3D%22middle%22%20fill%3D%226b7280%22%20font-size%3D%2214%22%3ENo%20Cover%3C%2Ftext%3E%3C%2Fsvg%3E'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const onItemMoved = (i, newX, newY) => {
  // GridLayout 项目移动时的回调
}
</script>

<style scoped>
/* GridLayout 容器样式 */
.vue-grid-layout {
  background: transparent;
}

.vue-grid-item {
  padding: 0;
}

/* 列表视图样式 */
.list-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.list-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.list-info {
  padding: 8px 0;
}

.book-desc {
  color: #6b7280;
  font-size: 13px;
  margin-top: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}

/* Tailwind line-clamp 兼容性 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-card-container {
  transition: all 0.3s ease;
}

.book-card-container:hover {
  transform: translateY(-4px);
}

.list-info {
  padding: 8px 0;
}

.list-info span {
  font-size: 14px;
  margin-right: 16px;
}
</style>
