import { request } from '../service/http'

export const getWishlist = async () => {
  return request({
    method: 'get',
    url: '/api/wishlist',
  })
}

export const addToWishlist = async (bookId) => {
  return request({
    method: 'post',
    url: `/api/books/${bookId}/wishlist`,
  })
}

export const removeFromWishlist = async (bookId) => {
  return request({
    method: 'delete',
    url: `/api/books/${bookId}/wishlist`,
  })
}
