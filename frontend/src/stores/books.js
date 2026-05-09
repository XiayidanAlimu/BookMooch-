import { defineStore } from 'pinia'
import axios from 'axios'

export const useBooksStore = defineStore('books', {
  state: () => ({
    books: [],
    categories: [],
    selectedCategoryId: null,
  }),
  actions: {
    async fetchBooks() {
      try {
        const params = this.selectedCategoryId ? { category_id: this.selectedCategoryId } : {}
        const response = await axios.get('/api/books', { params })
        this.books = response.data
      } catch (error) {
        console.error('获取捐书列表失败：', error)
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('/api/categories')
        this.categories = response.data
      } catch (error) {
        console.error('获取分类列表失败：', error)
      }
    },
    async addBook(bookData) {
      try {
        const response = await axios.post('/api/books', bookData)
        this.books.unshift(response.data)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '提交失败' }
      }
    },
    async fetchUserBooks(userId) {
      try {
        const response = await axios.get(`/api/users/${userId}/books`)
        return response.data
      } catch (error) {
        console.error('获取用户捐书记录失败：', error)
        return []
      }
    },
    setSelectedCategory(categoryId) {
      this.selectedCategoryId = categoryId
      this.fetchBooks()
    },
  },
})
