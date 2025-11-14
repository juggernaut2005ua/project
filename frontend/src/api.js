const API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/+$/, '')

function getToken(){
  return localStorage.getItem('api_token') || null
}

async function request(path, options={}){
  const headers = options.headers || {}
  headers['Content-Type'] = headers['Content-Type'] || 'application/json'
  const token = getToken()
  if(token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}/${path.replace(/^\/+/, '')}/`, {
    ...options,
    headers,
  })
  if(!res.ok){
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  const contentType = res.headers.get('content-type') || ''
  if(contentType.includes('application/json')) return res.json()
  return res.text()
}

export default {
  fetchList: (resource) => request(resource, { method: 'GET' }),
  get: (resource, id) => request(`${resource}${id ? `/${id}` : ''}`, { method: 'GET' }),
  create: (resource, payload) => request(resource, { method: 'POST', body: JSON.stringify(payload) }),
}
