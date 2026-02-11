const API_BASE_URL = 'http://localhost:8000'

// Get token from localStorage
function getAuthHeader() {
  const token = localStorage.getItem('access_token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

// Generic API request handler
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  
  // Check if body is FormData
  const isFormData = options.body instanceof FormData
  
  const config = {
    ...options,
    headers: {
      // Only add Content-Type for JSON, not FormData
      ...(!isFormData && { 'Content-Type': 'application/json' }),
      ...getAuthHeader(),
      ...options.headers,
    },
  }

  const response = await fetch(url, config)

  if (response.status === 401) {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'API request failed')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

// Auth API
export const authAPI = {
  async register(username, email, password, registrationCode) {
    return apiRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, registration_code: registrationCode }),
    })
  },

  async login(username, password) {
    return apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  },

  async getCurrentUser() {
    return apiRequest('/api/auth/me')
  },
}

// Cans API
export const cansAPI = {
  async getAll() {
    return apiRequest('/api/cans/')
  },

  async getById(id) {
    return apiRequest(`/api/cans/${id}`)
  },

  async create(canData) {
    return apiRequest('/api/cans/', {
      method: 'POST',
      body: JSON.stringify(canData),
    })
  },

  async update(id, canData) {
    return apiRequest(`/api/cans/${id}`, {
      method: 'PUT',
      body: JSON.stringify(canData),
    })
  },

  async delete(id) {
    return apiRequest(`/api/cans/${id}`, {
      method: 'DELETE',
    })
  },

  async uploadImage(canId, file) {
    const formData = new FormData()
    formData.append('file', file)

    return apiRequest(`/api/cans/${canId}/upload-image`, {
      method: 'POST',
      headers: {
        // Don't set Content-Type - browser will set it with boundary for FormData
        ...getAuthHeader(),
      },
      body: formData,
    })
  },
}

// Helper to get image URL
export function getImageUrl(imagePath) {
  if (!imagePath) return null
  // The backend stores full paths like "/app/uploads/can_1_20260120_123456.jpg"
  // We need to convert to URL like "http://localhost:8000/uploads/can_1_20260120_123456.jpg"
  const filename = imagePath.split('/').pop()
  return `${API_BASE_URL}/uploads/${filename}`
}