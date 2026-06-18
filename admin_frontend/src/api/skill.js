import { request } from './request'

export function getSkillList(params = {}) {
  const qs = new URLSearchParams(params).toString()
  return request(`/api/v1/skill/list?${qs}`)
}

export function getSkill(id) {
  return request(`/api/v1/skill/${id}`)
}

export function createSkill(data) {
  return request('/api/v1/skill/create', { method: 'POST', body: data })
}

export function updateSkill(id, data) {
  return request(`/api/v1/skill/${id}`, { method: 'PUT', body: data })
}

export function deleteSkill(id) {
  return request(`/api/v1/skill/${id}`, { method: 'DELETE' })
}

export function aiGenerateSkill(data) {
  return request('/api/v1/skill/ai-generate', { method: 'POST', body: data })
}

export function generateSystemPrompt(data) {
  return request('/api/v1/skill/generate-system-prompt', { method: 'POST', body: data })
}
