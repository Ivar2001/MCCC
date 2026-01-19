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

          <!-- Flavor Filter -->
          <div class="mb-6">
            <button 
              @click="toggleSection('flavor')"
              class="w-full flex items-center justify-between text-left font-semibold text-gray-700 mb-2"
            >
              <span>Flavor</span>
              <span class="text-xl">{{ openSections.flavor ? '−' : '+' }}</span>
            </button>
            
            <div v-show="openSections.flavor" class="space-y-2 pl-2">
              <label 
                v-for="flavor in availableFlavors" 
                :key="flavor"
                class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
              >
                <input 
                  type="checkbox"
                  :value="flavor"
                  v-model="filters.flavors"
                  class="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500"
                />
                <span class="text-sm text-gray-700">{{ flavor }}</span>
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
        <!-- Search Bar -->
        <div class="bg-white p-4 rounded-lg shadow mb-6">
          <div class="flex gap-3">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Search by title or description..."
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
              AI Search
            </button>
          </div>
        </div>

        <!-- Results Info -->
        <div class="mb-4 text-sm text-gray-600">
          Showing {{ filteredCans.length }} of {{ mockCans.length }} cans
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
            <div class="h-48 bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
              <span class="text-white text-6xl">🥤</span>
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Search state
const searchQuery = ref('')
const activeSearchQuery = ref('') // Only updates when Search button is clicked

// Filter state
const filters = ref({
  years: [],
  types: [],
  flavors: [],
  conditions: []
})

// Collapsible sections state
const openSections = ref({
  year: true,
  type: true,
  flavor: true,
  condition: true
})

// Mock data - will come from backend later
const mockCans = ref([
  { id: 1, flavor: 'Classic Coke', type: 'Regular', year: 2023, condition: 'Mint', description: 'Standard red can' },
  { id: 2, flavor: 'Cherry Coke', type: 'Flavored', year: 2022, condition: 'Excellent', description: 'Cherry flavored variant' },
  { id: 3, flavor: 'Vanilla Coke', type: 'Flavored', year: 2023, condition: 'Mint', description: 'Vanilla flavored edition' },
  { id: 4, flavor: 'Coke Zero', type: 'Zero Sugar', year: 2021, condition: 'Good', description: 'Zero sugar black can' },
  { id: 5, flavor: 'Diet Coke', type: 'Diet', year: 2023, condition: 'Mint', description: 'Diet version silver can' },
  { id: 6, flavor: 'Classic Coke', type: 'Limited Edition', year: 2020, condition: 'Fair', description: 'Olympic games special edition' },
  { id: 7, flavor: 'Orange Vanilla', type: 'Flavored', year: 2022, condition: 'Excellent', description: 'Orange and vanilla mix' },
  { id: 8, flavor: 'Coke Zero Cherry', type: 'Zero Sugar', year: 2023, condition: 'Mint', description: 'Cherry zero sugar variant' },
])

// Extract unique values for filters - will come from backend later
const availableYears = computed(() => {
  return [...new Set(mockCans.value.map(can => can.year))].sort((a, b) => b - a)
})

const availableTypes = computed(() => {
  return [...new Set(mockCans.value.map(can => can.type))].sort()
})

const availableFlavors = computed(() => {
  return [...new Set(mockCans.value.map(can => can.flavor))].sort()
})

const availableConditions = computed(() => {
  return ['Mint', 'Excellent', 'Good', 'Fair', 'Poor']
})

// Filtered cans based on selected filters and search
const filteredCans = computed(() => {
  let result = mockCans.value

  // Apply filter checkboxes
  if (filters.value.years.length > 0) {
    result = result.filter(can => filters.value.years.includes(can.year))
  }
  
  if (filters.value.types.length > 0) {
    result = result.filter(can => filters.value.types.includes(can.type))
  }
  
  if (filters.value.flavors.length > 0) {
    result = result.filter(can => filters.value.flavors.includes(can.flavor))
  }
  
  if (filters.value.conditions.length > 0) {
    result = result.filter(can => filters.value.conditions.includes(can.condition))
  }

  // Apply search query (only when search button clicked)
  if (activeSearchQuery.value) {
    const query = activeSearchQuery.value.toLowerCase()
    result = result.filter(can => 
      can.flavor.toLowerCase().includes(query) || 
      can.description.toLowerCase().includes(query)
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
  // TODO: Implement AI search later
  alert('AI Search will be implemented later!')
}

const clearFilters = () => {
  filters.value.years = []
  filters.value.types = []
  filters.value.flavors = []
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
  router.push('/')
}
</script>