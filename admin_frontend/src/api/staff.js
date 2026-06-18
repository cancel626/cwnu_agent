import { get, post, put, del } from './request.js'

export function getStaffList(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return get(`/api/v1/staff/list?${qs}`)
}

export function getStaffStats() {
  return get('/api/v1/staff/stats')
}

export function createStaff(data) {
  return post('/api/v1/staff/create', data)
}

export function updateStaff(id, data) {
  return put(`/api/v1/staff/update/${id}`, data)
}

export function deleteStaff(id) {
  return del(`/api/v1/staff/delete/${id}`)
}
