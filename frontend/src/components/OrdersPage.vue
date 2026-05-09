<template>
  <div class="max-w-6xl mx-auto p-6">
    <div class="bg-white rounded-xl shadow-sm p-6">
      <h2 class="text-2xl font-bold mb-4">领取订单</h2>
      <div v-if="!userStore.isLoggedIn" class="rounded-lg border border-dashed border-gray-300 p-8 text-center text-gray-600">
        <p class="mb-3">请先登录后查看领取订单。</p>
      </div>
      <div v-else>
        <div class="mb-4 flex items-center justify-between gap-4">
          <div>
            <p class="text-sm text-gray-500">展示您的领取订单记录。</p>
            <p class="text-sm text-gray-500">仅显示当前用户下单记录。</p>
          </div>
          <a-button type="primary" @click="refreshOrders">刷新列表</a-button>
        </div>

        <vxe-list
          class="rounded-xl border border-gray-100"
          :data="ordersStore.orders"
          :height="listHeight"
          :scroll-y="{ enabled: true, gt: 20 }"
          :loading="loading"
        >
          <template #default="{ items }">
            <div v-if="!loading && items.length === 0" class="py-12 text-center text-gray-500">
              暂无领取订单，先去发起领取吧。
            </div>
            <div v-for="item in items" :key="item.id" class="p-4 border-b border-gray-100 last:border-b-0 rounded-xl bg-white mb-4 shadow-sm">
              <div class="flex flex-col md:flex-row md:justify-between gap-4">
                <div class="min-w-0">
                  <h3 class="text-base font-semibold text-gray-900 truncate">{{ item.title }}</h3>
                  <p class="text-sm text-gray-600 truncate">作者：{{ item.author }}</p>
                  <p class="text-sm text-gray-600 truncate">捐赠者：{{ item.donor || '匿名' }}</p>
                </div>
                <div class="text-sm text-gray-600">
                  <p>状态：<span class="font-semibold text-gray-900">{{ item.status }}</span></p>
                  <p>订单时间：{{ formatDate(item.created_at) }}</p>
                </div>
              </div>
              <div class="mt-4 grid gap-3 sm:grid-cols-2">
                <div>
                  <p class="text-sm text-gray-500">收件人</p>
                  <p class="text-gray-800">{{ item.recipient_name }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">邮寄地址</p>
                  <p class="text-gray-800 break-words">{{ item.address }}</p>
                </div>
                <div class="sm:col-span-2">
                  <p class="text-sm text-gray-500">联系电话</p>
                  <p class="text-gray-800">{{ item.phone || '未填写' }}</p>
                </div>
                <div class="sm:col-span-2">
                  <p class="text-sm text-gray-500">备注</p>
                  <p class="text-gray-800">{{ item.note || '无' }}</p>
                </div>
              </div>
            </div>
          </template>
        </vxe-list>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useSettingsStore } from '../stores/settings'
import { useOrdersStore } from '../stores/orders'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const ordersStore = useOrdersStore()
const settingsStore = useSettingsStore()
const loading = ref(false)

const listHeight = computed(() => {
  const offset = 250
  const minHeight = 420
  const height = settingsStore.windowHeight - offset
  return `${height > minHeight ? height : minHeight}px`
})

const refreshOrders = async () => {
  if (!userStore.isLoggedIn) return
  loading.value = true
  await ordersStore.fetchOrders()
  loading.value = false
}

const formatDate = (value) => {
  return value ? new Date(value).toLocaleString('zh-CN') : ''
}

onMounted(async () => {
  if (userStore.isLoggedIn) {
    loading.value = true
    await ordersStore.fetchOrders()
    loading.value = false
  }
})
</script>

<style scoped>
</style>