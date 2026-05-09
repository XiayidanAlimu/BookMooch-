import { defineStore } from 'pinia'
import { getBooks, getCategories, addBook as addBookApi, getUserBooks as getUserBooksApi } from '../api/book'

export const useBooksStore = defineStore('books', {
  state: () => ({
    books: [],
    categories: [],
    selectedCategoryId: null,
  }),
  actions: {
    async fetchBooks() {
      try {
        this.books = await getBooks(this.selectedCategoryId)
      } catch (error) {
        console.error('获取捐书列表失败：', error)
      }
    },
    async fetchCategories() {
      try {
        this.categories = await getCategories()
      } catch (error) {
        console.error('获取分类列表失败：', error)
      }
    },
    async addBook(bookData) {
      try {
        const response = await addBookApi(bookData)
        this.books.unshift(response)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '提交失败' }
      }
    },
    async fetchUserBooks(userId) {
      try {
        return await getUserBooksApi(userId)
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
