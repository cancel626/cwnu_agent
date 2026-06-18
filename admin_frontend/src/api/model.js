import { get, post, put, del } from './request.js'

export function getModelList(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return get(`/api/v1/model/list?${qs}`)
}

export function getDefaultModel() {
  return get('/api/v1/model/default')
}

export function createModel(data) {
  return post('/api/v1/model/create', data)
}

export function updateModel(id, data) {
  return put(`/api/v1/model/${id}`, data)
}

export function deleteModel(id) {
  return del(`/api/v1/model/${id}`)
}

export function setDefaultModel(id) {
  return post(`/api/v1/model/${id}/set-default`)
}

export function testModel(id, data) {
  return post(`/api/v1/model/${id}/test`, data)
}
