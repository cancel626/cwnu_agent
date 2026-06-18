import { get, post } from './request.js'

// 爬取数据审核
export function scanCrawlData(limit = 50) {
  return post('/api/v1/audit/crawl/scan', { limit })
}

export function getCrawlViolations(page = 1, pageSize = 20) {
  return get(`/api/v1/audit/crawl/violations?page=${page}&page_size=${pageSize}`)
}

// 聊天消息审核
export function scanMessages(limit = 100) {
  return post('/api/v1/audit/message/scan', { limit })
}

export function getMessageViolations(page = 1, pageSize = 20) {
  return get(`/api/v1/audit/message/violations?page=${page}&page_size=${pageSize}`)
}

// 违规用户
export function getViolatorUsers() {
  return get('/api/v1/audit/message/violators')
}
