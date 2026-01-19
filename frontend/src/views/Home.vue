<template>
  <div class="min-h-screen bg-gradient-to-br from-red-600 to-red-800 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-white mb-4">
        🥤 Coca-Cola Collection
      </h1>
      <p class="text-xl text-white/90 mb-8">
        Track and manage your Coca-Cola can collection
      </p>
      <button 
        @click="goToLogin"
        class="bg-white text-red-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition"
      >
        Login to View Collection
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}
</script>