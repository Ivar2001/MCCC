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
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-500 text-lg">Loading...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {{ error }}
        <button @click="goBack" class="ml-4 underline">Go back</button>
      </div>

      <!-- Can Details -->
      <div v-else-if="can" class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="md:flex">
          <!-- Image Section -->
          <div class="md:w-1/2 bg-gradient-to-br from-red-400 to-red-600 flex flex-col items-center justify-center p-8 relative">
            <!-- Display Image or Placeholder -->
            <div class="w-full h-96 flex items-center justify-center mb-4 relative">
              <img 
                v-if="can.image_path"
                :src="getImageUrl(can.image_path)"
                :alt="can.flavor"
                class="max-w-full max-h-full object-contain rounded-lg"
                @error="imageLoadError = true"
              />
              <span v-else class="text-white text-9xl">🥤</span>
            </div>

            <!-- Upload Image Button -->
            <div class="w-full">
              <label 
                for="image-upload"
                class="block w-full bg-white text-red-600 px-4 py-2 rounded-lg text-center cursor-pointer hover:bg-gray-100 transition font-medium"
              >
                {{ can.image_path ? 'Change Image' : 'Upload Image' }}
              </label>
              <input 
                id="image-upload"
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="hidden"
              />
              <p v-if="uploadingImage" class="text-white text-sm text-center mt-2">
                Uploading...
              </p>
              <p v-if="uploadError" class="text-red-200 text-sm text-center mt-2">
                {{ uploadError }}
              </p>
            </div>
          </div>
          
          <!-- Details Section -->
          <div class="md:w-1/2 p-8">
            <!-- Edit Mode -->
            <div v-if="editMode">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">Edit Can</h2>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Flavor</label>
                  <input 
                    v-model="editData.flavor"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Type</label>
                  <select 
                    v-model="editData.type"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  >
                    <option value="Regular">Regular</option>
                    <option value="Flavored">Flavored</option>
                    <option value="Zero Sugar">Zero Sugar</option>
                    <option value="Diet">Diet</option>
                    <option value="Limited Edition">Limited Edition</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Year</label>
                  <input 
                    v-model.number="editData.year"
                    type="number"
                    min="1900"
                    max="2030"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Origin</label>
                  <input 
                    v-model="editData.origin"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Condition</label>
                  <select 
                    v-model="editData.condition"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  >
                    <option value="Mint">Mint</option>
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Description</label>
                  <textarea 
                    v-model="editData.description"
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  ></textarea>
                </div>

                <div class="flex space-x-3 pt-4">
                  <button 
                    @click="saveEdit"
                    :disabled="saving"
                    class="flex-1 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
                  >
                    {{ saving ? 'Saving...' : 'Save' }}
                  </button>
                  <button 
                    @click="cancelEdit"
                    :disabled="saving"
                    class="flex-1 bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400 transition disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>

            <!-- View Mode -->
            <div v-else>
              <h2 class="text-3xl font-bold text-gray-900 mb-4">{{ can.flavor }}</h2>
              
              <div class="space-y-3">
                <div>
                  <span class="text-sm font-medium text-gray-600">Type:</span>
                  <p class="text-lg text-gray-900">{{ can.type }}</p>
                </div>
                
                <div>
                  <span class="text-sm font-medium text-gray-600">Year:</span>
                  <p class="text-lg text-gray-900">{{ can.year }}</p>
                </div>

                <div>
                  <span class="text-sm font-medium text-gray-600">Origin:</span>
                  <p class="text-lg text-gray-900">{{ can.origin }}</p>
                </div>
                
                <div>
                  <span class="text-sm font-medium text-gray-600">Condition:</span>
                  <p class="text-lg text-gray-900">{{ can.condition }}</p>
                </div>
                
                <div v-if="can.description">
                  <span class="text-sm font-medium text-gray-600">Description:</span>
                  <p class="text-gray-700 mt-1">{{ can.description }}</p>
                </div>
              </div>
              
              <div class="mt-8 space-x-4">
                <button 
                  @click="startEdit"
                  class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Edit
                </button>
                <button 
                  @click="confirmDelete"
                  class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div 
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showDeleteModal = false"
    >
      <div 
        class="bg-white rounded-lg p-6 max-w-md w-full mx-4"
        @click.stop
      >
        <h3 class="text-xl font-bold text-gray-900 mb-4">Confirm Delete</h3>
        <p class="text-gray-700 mb-6">
          Are you sure you want to delete "{{ can?.flavor }}"? This action cannot be undone.
        </p>
        <div class="flex space-x-4">
          <button 
            @click="handleDelete"
            :disabled="deleting"
            class="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
          >
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
          <button 
            @click="showDeleteModal = false"
            :disabled="deleting"
            class="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { cansAPI, getImageUrl } from '@/services/api'

const router = useRouter()
const route = useRoute()

const can = ref(null)
const loading = ref(false)
const error = ref('')
const editMode = ref(false)
const editData = ref({})
const saving = ref(false)
const showDeleteModal = ref(false)
const deleting = ref(false)
const uploadingImage = ref(false)
const uploadError = ref('')
const imageLoadError = ref(false)

onMounted(async () => {
  await fetchCan()
})

const fetchCan = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const canId = route.params.id
    can.value = await cansAPI.getById(canId)
  } catch (err) {
    error.value = 'Failed to load can details'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Please select an image file'
    return
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = 'Image must be smaller than 5MB'
    return
  }

  uploadingImage.value = true
  uploadError.value = ''

  try {
    const updatedCan = await cansAPI.uploadImage(can.value.id, file)
    can.value = updatedCan
    imageLoadError.value = false
  } catch (err) {
    uploadError.value = 'Failed to upload image'
    console.error(err)
  } finally {
    uploadingImage.value = false
    // Reset file input
    event.target.value = ''
  }
}

const startEdit = () => {
  editData.value = { ...can.value }
  editMode.value = true
}

const cancelEdit = () => {
  editMode.value = false
  editData.value = {}
}

const saveEdit = async () => {
  saving.value = true
  
  try {
    const updated = await cansAPI.update(can.value.id, {
      flavor: editData.value.flavor,
      type: editData.value.type,
      year: editData.value.year,
      origin: editData.value.origin,
      condition: editData.value.condition,
      description: editData.value.description
    })
    
    can.value = updated
    editMode.value = false
  } catch (err) {
    error.value = 'Failed to update can'
    console.error(err)
  } finally {
    saving.value = false
  }
}

const confirmDelete = () => {
  showDeleteModal.value = true
}

const handleDelete = async () => {
  deleting.value = true
  
  try {
    await cansAPI.delete(can.value.id)
    router.push('/collection')
  } catch (err) {
    error.value = 'Failed to delete can'
    console.error(err)
    showDeleteModal.value = false
  } finally {
    deleting.value = false
  }
}

const goBack = () => {
  router.push('/collection')
}
</script>