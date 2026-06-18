import { post } from './request.js'

export function aiInquiry(question) {
  return post('/api/v1/ai/inquiry', { question })
}
