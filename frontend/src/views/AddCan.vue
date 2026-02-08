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
      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
        Can added successfully!
      </div>

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
              v-model.number="formData.year"
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
              Origin *
            </label>
            <input 
              v-model="formData.origin"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="e.g., USA, Japan, Limited Edition 2023"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Condition *
            </label>
            <select 
              v-model="formData.condition"
              required
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
            
            <!-- Image Preview -->
            <div v-if="imagePreview" class="mb-3">
              <img 
                :src="imagePreview"
                alt="Preview"
                class="w-full h-48 object-contain bg-gray-100 rounded-lg"
              />
              <button 
                type="button"
                @click="clearImage"
                class="mt-2 text-sm text-red-600 hover:underline"
              >
                Remove image
              </button>
            </div>

            <!-- File Input -->
            <input 
              type="file"
              accept="image/*"
              @change="handleImageSelect"
              ref="fileInput"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            />
            <p class="text-xs text-gray-500 mt-1">
              Supported formats: JPG, PNG, GIF (max 5MB)
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea 
              v-model="formData.description"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              placeholder="Any additional information about this can..."
            ></textarea>
          </div>

          <div class="flex space-x-4">
            <button 
              type="submit"
              :disabled="loading"
              class="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Adding...' : 'Add to Collection' }}
            </button>
            <button 
              type="button"
              @click="goBack"
              :disabled="loading"
              class="px-6 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition disabled:opacity-50"
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
import { cansAPI } from '@/services/api'

const router = useRouter()

const formData = ref({
  flavor: '',
  type: '',
  year: new Date().getFullYear(),
  origin: '',
  condition: 'Mint',
  description: ''
})

const selectedImage = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleImageSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      error.value = 'Please select an image file'
      return
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      error.value = 'Image must be smaller than 5MB'
      return
    }

    selectedImage.value = file
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
    
    error.value = ''
  }
}

const clearImage = () => {
  selectedImage.value = null
  imagePreview.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = false
  
  try {
    // Create the can first
    const newCan = await cansAPI.create({
      flavor: formData.value.flavor,
      type: formData.value.type,
      year: formData.value.year,
      origin: formData.value.origin,
      condition: formData.value.condition,
      description: formData.value.description || null
    })
    
    // If image was selected, upload it
    if (selectedImage.value) {
      await cansAPI.uploadImage(newCan.id, selectedImage.value)
    }
    
    success.value = true
    
    // Redirect to collection after short delay
    setTimeout(() => {
      router.push('/collection')
    }, 1500)
    
  } catch (err) {
    error.value = err.message || 'Failed to add can to collection'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/collection')
}
</script>