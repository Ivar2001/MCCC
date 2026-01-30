import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Collection from '../views/Collection.vue'
import CanDetail from '../views/CanDetail.vue'
import AddCan from '../views/AddCan.vue'
import Registration from '../views/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/collection',
      name: 'collection',
      component: Collection,
      meta: { requiresAuth: true }
    },
    {
      path: '/can/:id',
      name: 'can-detail',
      component: CanDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/add-can',
      name: 'add-can',
      component: AddCan,
      meta: { requiresAuth: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Registration,
      meta: { requiresAuth: false }
    }
  ]
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check authentication status on first load
  if (authStore.token && !authStore.user) {
    await authStore.checkAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login if trying to access protected route
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    // Redirect to collection if already logged in and trying to access login
    next({ name: 'collection' })
  } else {
    next()
  }
})

export default router