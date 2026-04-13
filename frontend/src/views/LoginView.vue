<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref('');
const auth = useAuthStore();
const router = useRouter();
const loading = ref(false);

const handleLogin = async () => {
  try {
    error.value = '';
    loading.value = true;
    await auth.login(email.value, password.value);
    router.push('/dashboard');
  } catch (err) {
    console.error("Login Error:", err);
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) {
        error.value = detail.map(d => d.msg).join(", ");
    } else if (typeof detail === 'string') {
        error.value = detail;
    } else {
        error.value = "Une erreur est survenue lors de la connexion.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-primary-50 relative overflow-hidden px-4">
    <!-- Décoration de fond (subtile) -->
    <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-secondary-200/30 blur-3xl"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-primary-200/30 blur-3xl"></div>

    <div class="w-full max-w-md bg-white p-10 rounded-2xl shadow-xl shadow-primary-900/5 relative z-10 border border-primary-100">
      
      <div class="text-center mb-10">
        <h1 class="text-4xl text-primary-800 mb-2">Saas Wedding</h1>
        <p class="text-sm text-gray-500 font-sans tracking-wide uppercase">L'art de l'invitation digitale</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 font-sans">Adresse Email</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="mariage@expert.com" 
            required 
            class="w-full px-4 py-3 rounded-lg border border-primary-200 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 bg-primary-50/50 text-gray-800 placeholder-gray-400 font-sans"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 font-sans">Mot de passe</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            required 
            class="w-full px-4 py-3 rounded-lg border border-primary-200 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 bg-primary-50/50 text-gray-800 placeholder-gray-400 font-sans"
          />
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors duration-300 flex justify-center items-center shadow-md shadow-primary-600/20 disabled:opacity-70 disabled:cursor-not-allowed font-sans mt-8"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>

        <!-- Message d'erreur -->
        <div v-if="error" class="p-4 bg-red-50 border-l-4 border-red-400 rounded-r-lg mt-6">
          <p class="text-sm text-red-700 font-sans">{{ error }}</p>
        </div>
      </form>
      
      <div class="mt-8 text-center">
         <p class="text-sm text-gray-500 font-sans">Vous n'avez pas de compte ? <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium transition-colors">Créer mon événement</router-link></p>
      </div>

    </div>
  </div>
</template>
