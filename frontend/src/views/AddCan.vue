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
        <h1 class="text-3xl font-bold text-gray-900">Add New Can</h1>
      </div>
    </header>

    <div class="max-w-2xl mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Flavor *
            </label>
            <input 
              v-model="formData.flavor"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="e.g., Cherry Coke"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Type *
            </label>
            <select 
              v-model="formData.type"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option value="">Select type...</option>
              <option value="Regular">Regular</option>
              <option value="Flavored">Flavored</option>
              <option value="Zero Sugar">Zero Sugar</option>
              <option value="Diet">Diet</option>
              <option value="Limited Edition">Limited Edition</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Year *
            </label>
            <input 
              v-model="formData.year"
              type="number"
              required
              min="1900"
              max="2030"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="e.g., 2023"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Condition
            </label>
            <select 
              v-model="formData.condition"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option value="Mint">Mint</option>
              <option value="Excellent">Excellent</option>
              <option value="Good">Good</option>
              <option value="Fair">Fair</option>
              <option value="Poor">Poor</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Image
            </label>
            <input 
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            <textarea 
              v-model="formData.notes"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="Any additional information about this can..."
            ></textarea>
          </div>

          <div class="flex space-x-4">
            <button 
              type="submit"
              class="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition"
            >
              Add to Collection
            </button>
            <button 
              type="button"
              @click="goBack"
              class="px-6 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = ref({
  flavor: '',
  type: '',
  year: new Date().getFullYear(),
  condition: 'Mint',
  notes: '',
  image: null
})

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.image = file
    console.log('Image selected:', file.name)
  }
}

const handleSubmit = () => {
  // TODO: Send to backend API later
  console.log('Form submitted:', formData.value)
  alert('Can added successfully! (not really, backend not connected yet)')
  router.push('/collection')
}

const goBack = () => {
  router.push('/collection')
}
</script>