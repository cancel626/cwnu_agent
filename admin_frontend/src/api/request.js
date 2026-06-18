const API_BASE = ''

function getToken() {
  return localStorage.getItem('admin_token') || ''
}

export async function request(url, options = {}) {
  const fullUrl = url.startsWith('http') ? url : `${API_BASE}${url}`
  const token = getToken()

  let body = options.body
  if (body && typeof body === 'object' && !(body instanceof FormData) && !(body instanceof Blob) && !(body instanceof URLSearchParams)) {
    body = JSON.stringify(body)
  }

  const res = await fetch(fullUrl, {
    ...options,
    body,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  const data = await res.json().catch(() => ({}))
  if (!res.ok || data.code !== 200) {
    const err = new Error(data.message || data.detail || '请求失败')
    err.code = data.code || res.status
    err.response = data
    throw err
  }
  return data
}

export const get = (url) => request(url, { method: 'GET' })
export const post = (url, body) => request(url, { method: 'POST', body: JSON.stringify(body) })
export const put = (url, body) => request(url, { method: 'PUT', body: JSON.stringify(body) })
export const del = (url) => request(url, { method: 'DELETE' })
