import { get, post, put, del } from './request.js'

export function getUserList(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return get(`/api/v1/user/list?${qs}`)
}

export function createUser(data) {
  return post('/api/v1/user/create', data)
}

export function updateUser(id, data) {
  return put(`/api/v1/user/${id}`, data)
}

export function deleteUser(id) {
  return del(`/api/v1/user/${id}`)
}
