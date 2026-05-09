import axios from 'axios'
import { Message } from '@arco-design/web-vue'

const DEFAULT_TIMEOUT = 10000
const DEFAULT_DELAY = 150

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: DEFAULT_TIMEOUT,
})

let unauthorizedHandler = null

const getToken = () => localStorage.getItem('donate_token')

export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('donate_token', token)
    http.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

export const clearAuthToken = () => {
  localStorage.removeItem('donate_token')
  delete http.defaults.headers.common['Authorization']
}

export const onUnauthorized = (handler) => {
  unauthorizedHandler = handler
}

export const initRequestService = () => {
  const token = getToken()
  if (token) {
    http.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

const getErrorMessage = (error) => {
  if (error.response && error.response.data && error.response.data.error) {
    return error.response.data.error
  }
  if (error.message) {
    return error.message
  }
  return '网络请求失败，请稍后重试。'
}

http.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

http.interceptors.response.use(
  async (response) => {
    return response
  },
  (error) => {
    const status = error.response?.status
    const message = getErrorMessage(error)
    if (status === 401) {
      Message.error('身份已过期，请重新登录。')
      if (unauthorizedHandler) {
        unauthorizedHandler()
      }
    } else if (status === 403) {
      Message.error('当前无权限访问该资源。')
    } else {
      Message.error(message)
    }
    return Promise.reject(error)
  }
)

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const request = async (config) => {
  try {
    const response = await http.request(config)
    const wait = config.delay === 0 ? 0 : config.delay || DEFAULT_DELAY
    if (wait > 0) {
      await delay(wait)
    }
    return response.data
  } catch (error) {
    throw error
  }
}
