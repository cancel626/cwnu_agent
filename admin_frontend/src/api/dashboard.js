import { get } from './request.js'

export function getDashboardStats() {
  return get('/api/v1/dashboard/stats')
}
