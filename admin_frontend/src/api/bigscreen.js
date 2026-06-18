import { get } from './request.js'

export function getBigscreenData() {
  return get('/api/v1/bigscreen/warehouse')
}
