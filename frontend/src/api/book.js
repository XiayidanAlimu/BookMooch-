import { request } from '../service/http'

export const getBooks = async (categoryId) => {
  const params = categoryId ? { category_id: categoryId } : {}
  return request({
    method: 'get',
    url: '/api/books',
    params,
  })
}

export const getCategories = async () => {
  return request({
    method: 'get',
    url: '/api/categories',
  })
}

export const addBook = async (bookData) => {
  return request({
    method: 'post',
    url: '/api/books',
    data: bookData,
  })
}

export const getUserBooks = async (userId) => {
  return request({
    method: 'get',
    url: `/api/users/${userId}/books`,
  })
}
