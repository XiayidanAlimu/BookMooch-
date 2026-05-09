<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">当前捐书列表</h2>

      <a-spin :loading="loading">
        <div v-if="books.length === 0" class="text-center py-16">
          <a-empty description="目前还没有捐书，欢迎成为第一位捐赠者。" />
        </div>

        <div v-else-if="viewMode === 'card'" class="w-full" :style="{ minHeight: bookListHeight }">
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <div
              v-for="book in books"
              :key="book.id"
              class="book-card-container h-full bg-white rounded-2xl shadow-sm hover:shadow-lg transition-shadow duration-300 overflow-hidden flex flex-col"
            >
              <div class="relative h-52 overflow-hidden bg-gray-100 flex-shrink-0">
                <img
                  :src="getBookCover(book)"
                  :alt="book.title"
                  class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  @error="handleImageError"
                />
              </div>

              <div class="flex-grow p-5 flex flex-col">
                <h3 class="text-base font-semibold text-gray-900 mb-3 line-clamp-2 leading-tight">
                  {{ book.title }}
                </h3>

                <div class="text-sm text-gray-600 space-y-2 flex-grow">
                  <div class="flex items-start gap-2">
                    <span class="font-semibold text-gray-800">作者：</span>
                    <span class="break-words">{{ book.author }}</span>
                  </div>
                  <div v-if="book.isbn" class="flex items-start gap-2">
                    <span class="font-semibold text-gray-800">ISBN：</span>
                    <span class="break-words font-mono text-xs">{{ book.isbn }}</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <span class="font-semibold text-gray-800">分类：</span>
                    <a-tag v-if="book.category_name" color="blue" class="text-xs">
                      {{ book.category_name }}
                    </a-tag>
                    <span v-else class="text-gray-400">未分类</span>
                  </div>
                  <div v-if="book.donor" class="flex items-start gap-2">
                    <span class="font-semibold text-gray-800">捐赠者：</span>
                    <span class="break-words">{{ book.donor }}</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <span class="font-semibold text-gray-800">时间：</span>
                    <span class="text-gray-500">{{ formatDate(book.donated_at) }}</span>
                  </div>
                  <div v-if="book.description" class="pt-2">
                    <p class="text-gray-500 line-clamp-2 text-sm leading-relaxed">
                      {{ book.description }}
                    </p>
                  </div>
                </div>

                <div class="mt-4 pt-4 border-t border-gray-100 flex flex-wrap gap-3 justify-end">
                  <a-button size="mini" type="primary" @click="addToWishlist(book)">加入心愿单</a-button>
                  <a-button size="mini" type="secondary" @click="openOrderModal(book)">直接领取</a-button>
                </div>
              </div>
            </div>
          </div>
        </div>

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
                    <div class="mt-3 flex flex-wrap gap-3 justify-end">
                      <a-button size="mini" type="primary" @click="addToWishlist(item)">加入心愿单</a-button>
                      <a-button size="mini" type="secondary" @click="openOrderModal(item)">直接领取</a-button>
                    </div>
                  </div>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </template>
        </a-list>
      </a-spin>

      <a-modal
        v-model:visible="orderModalVisible"
        title="填写邮寄信息"
        :width="520"
        :footer="null"
      >
        <div class="space-y-4">
          <a-form-item label="收件人姓名" :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }">
            <a-input v-model:value="orderForm.recipient_name" placeholder="请输入收件人姓名" />
          </a-form-item>
          <a-form-item label="邮寄地址" :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }">
            <a-input v-model:value="orderForm.address" placeholder="请输入邮寄地址" />
          </a-form-item>
          <a-form-item label="联系电话" :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }">
            <a-input v-model:value="orderForm.phone" placeholder="请输入联系电话" />
          </a-form-item>
          <a-form-item label="备注" :label-col="{ span: 5 }" :wrapper-col="{ span: 19 }">
            <a-textarea v-model:value="orderForm.note" placeholder="可填写收货说明" rows="4" />
          </a-form-item>
          <div class="flex justify-end gap-3 pt-2">
            <a-button type="text" @click="orderModalVisible = false">取消</a-button>
            <a-button type="primary" :loading="orderLoading" @click="submitOrder">提交领取</a-button>
          </div>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup>
import { defineProps, h, ref, computed } from 'vue'
import { Message } from '@arco-design/web-vue';
import { useSettingsStore } from '../stores/settings'
import { useOrdersStore } from '../stores/orders'

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

const settingsStore = useSettingsStore()
const ordersStore = useOrdersStore()
const orderModalVisible = ref(false)
const orderBook = ref(null)
const orderForm = ref({
  recipient_name: '',
  address: '',
  phone: '',
  note: '',
})
const orderLoading = ref(false)

const bookListHeight = computed(() => {
  const offset = 280
  const minHeight = 420
  const height = settingsStore.windowHeight - offset
  return `${height > minHeight ? height : minHeight}px`
})

const openOrderModal = (book) => {
  orderBook.value = book
  orderForm.value = {
    recipient_name: '',
    address: '',
    phone: '',
    note: '',
  }
  orderModalVisible.value = true
}

const addToWishlist = async (book) => {
  const response = await ordersStore.addToWishlist(book.id)
  if (response.success) {
    Message.success(response.message)
  } else {
    Message.error(response.error)
  }
}

const submitOrder = async () => {
  if (!orderBook.value) return
  orderLoading.value = true
  const response = await ordersStore.placeOrder(orderBook.value.id, orderForm.value)
  orderLoading.value = false
  if (response.success) {
    Message.success('已成功提交领取订单，请等待处理。')
    orderModalVisible.value = false
  } else {
    Message.error(response.error)
  }
}

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
</script>

<style scoped>
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
</style>
