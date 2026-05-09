import { request } from '../service/http'

export const searchBooks = async (query) => {
  return request({
    method: 'get',
    url: '/api/book-search',
    params: { q: query },
  })
}
