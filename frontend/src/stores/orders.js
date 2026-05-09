import { defineStore } from 'pinia'
import { getWishlist as getWishlistApi, addToWishlist as addToWishlistApi, removeFromWishlist as removeFromWishlistApi } from '../api/wishlist'
import { getOrders as getOrdersApi, placeOrder as placeOrderApi } from '../api/orders'

export const useOrdersStore = defineStore('orders', {
  state: () => ({
    wishlist: [],
    orders: [],
  }),
  actions: {
    async addToWishlist(bookId) {
      try {
        const response = await addToWishlistApi(bookId)
        return { success: true, message: response.message || '已加入心愿单' }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '添加心愿单失败' }
      }
    },
    async placeOrder(bookId, orderData) {
      try {
        const response = await placeOrderApi(bookId, orderData)
        return { success: true, data: response }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '下单失败' }
      }
    },
    async fetchWishlist() {
      try {
        this.wishlist = await getWishlistApi()
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '加载心愿单失败' }
      }
    },
    async removeFromWishlist(bookId) {
      try {
        await removeFromWishlistApi(bookId)
        this.wishlist = this.wishlist.filter((item) => item.book_id !== bookId && item.id !== bookId)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '删除心愿单失败' }
      }
    },
    async fetchOrders() {
      try {
        this.orders = await getOrdersApi()
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '加载订单失败' }
      }
    },
  },
})
