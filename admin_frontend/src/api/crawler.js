import { request } from './request.js'

const PREFIX = '/api/v1'

export function getSourceList() {
  return request(`${PREFIX}/crawler/source`)
}

export function createSource(data) {
  return request(`${PREFIX}/crawler/source`, { method: 'POST', body: data })
}

export function updateSource(id, data) {
  return request(`${PREFIX}/crawler/source/${id}`, { method: 'PUT', body: data })
}

export function deleteSource(id) {
  return request(`${PREFIX}/crawler/source/${id}`, { method: 'DELETE' })
}

export function getTaskList() {
  return request(`${PREFIX}/crawler/task`)
}

export function createTask(data) {
  return request(`${PREFIX}/crawler/task`, { method: 'POST', body: data })
}

export function getTaskResult(taskId) {
  return request(`${PREFIX}/crawler/task/${taskId}/result`)
}

export function saveData(data) {
  return request(`${PREFIX}/crawler/data/save`, { method: 'POST', body: data })
}

export function getSavedData() {
  return request(`${PREFIX}/crawler/data/saved`)
}

export function getDataOverview() {
  return request(`${PREFIX}/crawler/data/overview`)
}

export function deleteData(id) {
  return request(`${PREFIX}/crawler/data/${id}`, { method: 'DELETE' })
}

export function cleanData(data) {
  return request(`${PREFIX}/crawler/data/clean`, { method: 'POST', body: data })
}
