<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-full mx-auto px-4 py-6 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">My Collection</h1>
        <div class="space-x-4">
          <button 
            @click="goToAddCan"
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
          >
            + Add Can
          </button>
          <button 
            @click="handleLogout"
            class="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition"
          >
            Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content with Sidebar -->
    <div class="max-w-full mx-auto px-4 py-6 flex gap-6">
      
      <!-- Sidebar Filters -->
      <aside class="w-64 flex-shrink-0">
        <div class="bg-white rounded-lg shadow p-6 sticky top-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4">Filters</h2>
          
          <!-- Year Filter -->
          <div class="mb-6">
            <button 
              @click="toggleSection('year')"
              class="w-full flex items-center justify-between text-left font-semibold text-gray-700 mb-2"
            >
              <span>Year</span>
              <span class="text-xl">{{ openSections.year ? '−' : '+' }}</span>
            </button>
            
            <div v-show="openSections.year" class="space-y-2 pl-2">
              <label 
                v-for="year in availableYears" 
                :key="year"
                class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
              >
                <input 
                  type="checkbox"
                  :value="year"
                  v-model="filters.years"
                  class="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                />
                <span class="text-sm text-gray-700">{{ year }}</span>
              </label>
            </div>
          </div>

          <!-- Type Filter -->
          <div class="mb-6">
            <button 
              @click="toggleSection('type')"
              class="w-full flex items-center justify-between text-left font-semibold text-gray-700 mb-2"
            >
              <span>Type</span>
              <span class="text-xl">{{ openSections.type ? '−' : '+' }}</span>
            </button>
            
            <div v-show="openSections.type" class="space-y-2 pl-2">
              <label 
                v-for="type in availableTypes" 
                :key="type"
                class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
              >
                <input 
                  type="checkbox"
                  :value="type"
                  v-model="filters.types"
                  class="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                />
                <span class="text-sm text-gray-700">{{ type }}</span>
              </label>
            </div>
          </div>

          <!-- Condition Filter -->
          <div class="mb-6">
            <button 
              @click="toggleSection('condition')"
              class="w-full flex items-center justify-between text-left font-semibold text-gray-700 mb-2"
            >
              <span>Condition</span>
              <span class="text-xl">{{ openSections.condition ? '−' : '+' }}</span>
            </button>
            
            <div v-show="openSections.condition" class="space-y-2 pl-2">
              <label 
                v-for="condition in availableConditions" 
                :key="condition"
                class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
              >
                <input 
                  type="checkbox"
                  :value="condition"
                  v-model="filters.conditions"
                  class="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                />
                <span class="text-sm text-gray-700">{{ condition }}</span>
              </label>
            </div>
          </div>

          <!-- Clear Filters Button -->
          <button 
            @click="clearFilters"
            class="w-full bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition text-sm font-medium"
          >
            Clear All Filters
          </button>
        </div>
      </aside>

      <!-- Main Content Area -->
      <div class="flex-1">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <p class="text-gray-500 text-lg">Loading collection...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <!-- Content -->
        <template v-else>
          <!-- Search Bar -->
          <div class="bg-white p-4 rounded-lg shadow mb-6">
            <div class="flex gap-3">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="Search by flavor or description..."
                @keyup.enter="handleSearch"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              />
              <button 
                @click="handleSearch"
                class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition font-medium"
              >
                Search
              </button>
              <button 
                @click="handleAISearch"
                class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-medium flex items-center gap-2"
              >
                <span>🤖</span>
                AI Search
              </button>
            </div>
          </div>

          <!-- Results Info -->
          <div class="mb-4 text-sm text-gray-600">
            Showing {{ filteredCans.length }} of {{ allCans.length }} cans
            <span v-if="activeSearchQuery" class="ml-2">
              • Search: "<span class="font-medium">{{ activeSearchQuery }}</span>"
              <button @click="clearSearch" class="ml-2 text-red-600 hover:underline">
                Clear
              </button>
            </span>
          </div>

          <!-- Collection Grid -->
          <div v-if="filteredCans.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div 
                v-for="can in filteredCans" 
                :key="can.id"
                @click="goToCanDetail(can.id)"
                class="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer overflow-hidden"
              >
                <div class="h-48 bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center relative overflow-hidden">
                  <img 
                    v-if="can.image_path"
                    :src="getImageUrl(can.image_path)"
                    :alt="can.flavor"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                  <span v-else class="text-white text-6xl">🥤</span>
                </div>
              <div class="p-4">
                <h3 class="font-semibold text-lg text-gray-800">{{ can.flavor }}</h3>
                <p class="text-sm text-gray-600">{{ can.type }}</p>
                <div class="flex justify-between items-center mt-2">
                  <p class="text-xs text-gray-500">{{ can.year }}</p>
                  <span class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                    {{ can.condition }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- No Results -->
          <div v-else class="bg-white rounded-lg shadow p-12 text-center">
            <p class="text-gray-500 text-lg">No cans found matching your criteria</p>
            <button 
              @click="clearFilters"
              class="mt-4 text-red-600 hover:underline"
            >
              Clear filters
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { cansAPI, getImageUrl } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

// State
const allCans = ref([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const activeSearchQuery = ref('')

// Filter state
const filters = ref({
  years: [],
  types: [],
  conditions: []
})

// Collapsible sections state
const openSections = ref({
  year: true,
  type: true,
  condition: true
})

// Fetch cans on mount
onMounted(async () => {
  await fetchCans()
})

const fetchCans = async () => {
  loading.value = true
  error.value = ''
  
  try {
    allCans.value = await cansAPI.getAll()
  } catch (err) {
    error.value = 'Failed to load collection'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Extract unique values for filters
const availableYears = computed(() => {
  return [...new Set(allCans.value.map(can => can.year))].sort((a, b) => b - a)
})

const availableTypes = computed(() => {
  return [...new Set(allCans.value.map(can => can.type))].sort()
})

const availableConditions = computed(() => {
  return ['Mint', 'Excellent', 'Good', 'Fair', 'Poor']
})

// Filtered cans based on selected filters and search
const filteredCans = computed(() => {
  let result = allCans.value

  // Apply filter checkboxes
  if (filters.value.years.length > 0) {
    result = result.filter(can => filters.value.years.includes(can.year))
  }
  
  if (filters.value.types.length > 0) {
    result = result.filter(can => filters.value.types.includes(can.type))
  }
  
  if (filters.value.conditions.length > 0) {
    result = result.filter(can => filters.value.conditions.includes(can.condition))
  }

  // Apply search query
  if (activeSearchQuery.value) {
    const query = activeSearchQuery.value.toLowerCase()
    result = result.filter(can => 
      can.flavor.toLowerCase().includes(query) || 
      (can.description && can.description.toLowerCase().includes(query))
    )
  }

  return result
})

// Methods
const toggleSection = (section) => {
  openSections.value[section] = !openSections.value[section]
}

const handleSearch = () => {
  activeSearchQuery.value = searchQuery.value
}

const clearSearch = () => {
  searchQuery.value = ''
  activeSearchQuery.value = ''
}

const handleAISearch = () => {
  alert('AI Search will be implemented later!')
}

const clearFilters = () => {
  filters.value.years = []
  filters.value.types = []
  filters.value.conditions = []
  clearSearch()
}

const goToAddCan = () => {
  router.push('/add-can')
}

const goToCanDetail = (id) => {
  router.push(`/can/${id}`)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const handleImageError = (event) => {
  // If image fails to load, hide it and show emoji fallback
  event.target.style.display = 'none'
}
</script>