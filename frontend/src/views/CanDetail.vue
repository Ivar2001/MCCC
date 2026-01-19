<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-6 flex items-center">
        <button 
          @click="goBack"
          class="text-gray-600 hover:text-gray-900 mr-4"
        >
          ← Back
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Can Details</h1>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="md:flex">
          <!-- Image -->
          <div class="md:w-1/2 bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center p-12">
            <span class="text-white text-9xl">🥤</span>
          </div>
          
          <!-- Details -->
          <div class="md:w-1/2 p-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Cherry Coke</h2>
            
            <div class="space-y-3">
              <div>
                <span class="text-sm font-medium text-gray-600">Type:</span>
                <p class="text-lg text-gray-900">Flavored</p>
              </div>
              
              <div>
                <span class="text-sm font-medium text-gray-600">Flavor:</span>
                <p class="text-lg text-gray-900">Cherry</p>
              </div>
              
              <div>
                <span class="text-sm font-medium text-gray-600">Year:</span>
                <p class="text-lg text-gray-900">2022</p>
              </div>
              
              <div>
                <span class="text-sm font-medium text-gray-600">Condition:</span>
                <p class="text-lg text-gray-900">Mint</p>
              </div>
              
              <div>
                <span class="text-sm font-medium text-gray-600">Notes:</span>
                <p class="text-gray-700 mt-1">Limited edition design from summer collection.</p>
              </div>
            </div>
            
            <div class="mt-8 space-x-4">
              <button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
                Edit
              </button>
              <button class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// TODO: Fetch can details based on route.params.id

const goBack = () => {
  router.push('/collection')
}
</script>