import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi, getCurrentUser as getCurrentUserApi, logout as logoutApi } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: JSON.parse(localStorage.getItem('donate_user')) || null,
    token: localStorage.getItem('donate_token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.currentUser && !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        const response = await loginApi(username, password)
        this.token = response.token
        this.currentUser = response.user
        localStorage.setItem('donate_token', this.token)
        localStorage.setItem('donate_user', JSON.stringify(this.currentUser))
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '登录失败' }
      }
    },
    async register(userData) {
      try {
        const response = await registerApi(userData)
        return { success: true, user: response }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '注册失败' }
      }
    },
    async loadCurrentUser() {
      if (!this.token) return
      try {
        const response = await getCurrentUserApi()
        this.currentUser = response
        localStorage.setItem('donate_user', JSON.stringify(this.currentUser))
      } catch (error) {
        this.logout()
      }
    },
    async logout() {
      try {
        await logoutApi()
      } catch {
        // ignore logout errors
      }
      this.currentUser = null
      this.token = null
      localStorage.removeItem('donate_token')
      localStorage.removeItem('donate_user')
    },
  },
})
