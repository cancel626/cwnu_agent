import { get, post, put, del } from './request.js'

export function adminLogin(data) {
  return post('/api/v1/admin/login', data)
}

export function adminRegister(data) {
  return post('/api/v1/admin/register', data)
}

export function getAdminMe() {
  return get('/api/v1/admin/me')
}

export function getAdminList(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return get(`/api/v1/admin/list?${qs}`)
}

export function createAdmin(data) {
  return post('/api/v1/admin/register', data)
}

export function updateAdmin(id, data) {
  return put(`/api/v1/admin/${id}`, data)
}

export function deleteAdmin(id) {
  return del(`/api/v1/admin/${id}`)
}
