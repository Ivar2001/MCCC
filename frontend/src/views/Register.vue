<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
            Register
        </h2>
        <form @submit.prevent="handleRegistration" class="space-y-4">
            <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {{ error }}
            </div>
            <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Registration Code
            </label>
            <input 
                v-model="registrationCode"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Enter registration code"
            />
            </div>
            <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Username
            </label>
            <input 
                v-model="username"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Choose a username"
            />
            </div>
            <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Email Address
            </label>
            <input 
                v-model="email"
                type="email"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Enter your email"
            />
            </div>
            <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Password
            </label>
            <input 
                v-model="password"
                type="password"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Create a password"
            />
            </div>
            <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
            </label>
            <input
                v-model="confirmPassword"
                type="password"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Re-enter your password"   
            />
            </div>
            <button 
                type="submit"
                :disabled="loading"
                class="w-full bg-red-600 text-white py-2 rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                {{ loading ? 'Registering...' : 'Register' }}
            </button>
        </form>
        </div>
        <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            Registration successful! Redirecting to login...
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const router = useRouter()
    const authStore = useAuthStore()
    const username = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const email = ref('')
    const error = ref('')
    const loading = ref(false)
    const registrationCode = ref('')
    const success = ref(false)

    const handleRegistration = async () => {
        error.value = ''
        
        if (!username.value || !email.value || !password.value || !registrationCode.value) {
            error.value = "All fields are required!"
            return
        }
        
        if (password.value.length < 6) {
            error.value = "Password must be at least 6 characters!"
            return
        }
        
        if (password.value !== confirmPassword.value) {
            error.value = "Passwords do not match!"
            return
        }

        try {
            loading.value = true
            await authStore.register(username.value, email.value, password.value, registrationCode.value)
            success.value = true
            
            setTimeout(() => {
            router.push('/login')
            }, 1500)
        } catch (err) {
            error.value = err.message || "Registration failed. Please try again."
        } finally {
            loading.value = false
        }
    }

</script>