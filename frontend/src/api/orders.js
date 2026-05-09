import { request } from '../service/http'

export const getOrders = async () => {
  return request({
    method: 'get',
    url: '/api/orders',
  })
}

export const placeOrder = async (bookId, orderData) => {
  return request({
    method: 'post',
    url: `/api/books/${bookId}/order`,
    data: orderData,
  })
}
