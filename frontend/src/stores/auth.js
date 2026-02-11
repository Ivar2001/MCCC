import { defineStore } from 'pinia'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async register(username, email, password, registrationCode) {
      try {
        const user = await authAPI.register(username, email, password, registrationCode)
        return user
      } catch (error) {
        throw error
      }
    },

    async login(username, password) {
      try {
        const data = await authAPI.login(username, password)
        this.token = data.access_token
        localStorage.setItem('access_token', data.access_token)
        
        // Fetch user info
        await this.fetchUser()
      } catch (error) {
        throw error
      }
    },

    async fetchUser() {
      try {
        this.user = await authAPI.getCurrentUser()
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
    },

    // Check if user is still authenticated on app load
    async checkAuth() {
      if (!this.token) {
        this.logout()
      }
      else {
        try {
          await this.fetchUser()
        } catch (error) {
          this.logout()
        }
      }
    }
  }
}
)