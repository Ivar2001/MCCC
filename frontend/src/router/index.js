import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Collection from '../views/Collection.vue'
import CanDetail from '../views/CanDetail.vue'
import AddCan from '../views/AddCan.vue'
import Register from '../views/Register.vue'

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
      meta: { requiresAuth: true } // We'll use this later for route guards
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
      component: Register,
    }
  ]
})

// TODO: Add navigation guard for authentication later
// router.beforeEach((to, from, next) => {
//   // Check if route requires auth and user is not authenticated
// })

export default router
