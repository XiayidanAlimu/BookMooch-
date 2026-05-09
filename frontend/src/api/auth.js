import { request, setAuthToken, clearAuthToken, onUnauthorized } from '../service/http'

export const login = async (username, password) => {
  const data = await request({
    method: 'post',
    url: '/api/login',
    data: { username, password },
  })
  setAuthToken(data.token)
  return data
}

export const register = async (userData) => {
  return request({
    method: 'post',
    url: '/api/register',
    data: userData,
  })
}

export const logout = async () => {
  const data = await request({
    method: 'post',
    url: '/api/logout',
  })
  clearAuthToken()
  return data
}

export const getCurrentUser = async () => {
  return request({
    method: 'get',
    url: '/api/me',
  })
}

export const bindUnauthorizedHandler = (handler) => {
  onUnauthorized(handler)
}
