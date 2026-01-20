<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
            Register
        </h2>
        <form @submit.prevent="handleRegistration" class="space-y-4">
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
                class="w-full bg-red-600 text-white py-2 rounded-lg font-semibold hover:bg-red-700 transition"
                >
                Register
            </button>
        </form>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const email = ref('')

    const handleRegistration = () => {
        if (password.value !== confirmPassword.value) {
            alert("Passwords do not match!");
            return;
        }
        router.push('/login')
    }

</script>