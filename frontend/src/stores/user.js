import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: JSON.parse(localStorage.getItem('donate_user')) || null,
    token: localStorage.getItem('donate_token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.currentUser && !!state.token,
  },
  actions: {
    initializeAxios() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    },
    async login(username, password) {
      try {
        const response = await axios.post('/api/login', { username, password })
        this.token = response.data.token
        this.currentUser = response.data.user
        localStorage.setItem('donate_token', this.token)
        localStorage.setItem('donate_user', JSON.stringify(this.currentUser))
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '登录失败' }
      }
    },
    async register(userData) {
      try {
        const response = await axios.post('/api/register', userData)
        return { success: true, user: response.data }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '注册失败' }
      }
    },
    async loadCurrentUser() {
      if (!this.token) return
      try {
        const response = await axios.get('/api/me')
        this.currentUser = response.data
        localStorage.setItem('donate_user', JSON.stringify(this.currentUser))
      } catch (error) {
        this.logout()
      }
    },
    logout() {
      this.currentUser = null
      this.token = null
      localStorage.removeItem('donate_token')
      localStorage.removeItem('donate_user')
      delete axios.defaults.headers.common['Authorization']
    },
  },
})
