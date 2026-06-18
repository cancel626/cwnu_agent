const API_BASE = '/api/v1'

async function request(url, options = {}) {
  const token = localStorage.getItem('user_token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers
  }

  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers
  })

  if (res.status === 401) {
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_info')
    window.location.href = '/user-login/'
    return { code: 401, message: '登录已过期' }
  }

  return res.json()
}

export const get = (url) => request(url, { method: 'GET' })
export const post = (url, body) => request(url, { method: 'POST', body: JSON.stringify(body) })
export const put = (url, body) => request(url, { method: 'PUT', body: JSON.stringify(body) })
export const del = (url) => request(url, { method: 'DELETE' })

export const upload = async (url, file) => {
  const token = localStorage.getItem('user_token')
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${API_BASE}${url}`, {
    method: 'POST',
    headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    body: formData
  })

  if (res.status === 401) {
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_info')
    window.location.href = '/user-login/'
    return { code: 401, message: '登录已过期' }
  }

  return res.json()
}
