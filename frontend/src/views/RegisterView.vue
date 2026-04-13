<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const selectedPlan = ref('classic');
const error = ref('');
const auth = useAuthStore();
const router = useRouter();
const loading = ref(false);

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = "Les mots de passe ne correspondent pas.";
    return;
  }

  try {
    error.value = '';
    loading.value = true;
    await auth.register(email.value, password.value, selectedPlan.value);
    router.push('/dashboard');
  } catch (err) {
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) {
        error.value = detail.map(d => d.msg).join(", ");
    } else {
        error.value = detail || "Une erreur est survenue lors de l'inscription.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-primary-50 relative overflow-hidden px-4">
    <!-- Décoration de fond -->
    <div class="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary-200/30 blur-3xl"></div>
    <div class="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-200/30 blur-3xl"></div>

    <div class="w-full max-w-md bg-white p-10 rounded-2xl shadow-xl shadow-primary-900/5 relative z-10 border border-primary-100">
      
      <div class="text-center mb-10">
        <h1 class="text-4xl text-primary-800 mb-2">Rejoignez-nous</h1>
        <p class="text-sm text-gray-500 font-sans tracking-wide uppercase text-pretty">Commencez l'aventure Saas Wedding</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 font-sans">Adresse Email</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="votre@email.com" 
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

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2 font-sans">Confirmer le mot de passe</label>
          <input 
            v-model="confirmPassword" 
            type="password" 
            placeholder="••••••••" 
            required 
            class="w-full px-4 py-3 rounded-lg border border-primary-200 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all duration-300 bg-primary-50/50 text-gray-800 placeholder-gray-400 font-sans"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-4 font-sans">Choisissez votre forfait</label>
          <div class="grid grid-cols-2 gap-4">
            <div 
              @click="selectedPlan = 'classic'"
              :class="selectedPlan === 'classic' ? 'border-primary-600 bg-primary-50 shadow-sm' : 'border-gray-200 bg-white'"
              class="cursor-pointer border-2 rounded-xl p-4 transition-all hover:border-primary-400"
            >
              <div class="font-bold text-gray-900 mb-1">Classic</div>
              <div class="text-[10px] text-gray-500 font-sans uppercase tracking-tight">L'essentiel pour votre mariage</div>
              <div class="mt-2 text-primary-600 font-bold">45 €</div>
            </div>
            <div 
              @click="selectedPlan = 'premium'"
              :class="selectedPlan === 'premium' ? 'border-primary-600 bg-primary-50 shadow-sm' : 'border-gray-200 bg-white'"
              class="cursor-pointer border-2 rounded-xl p-4 transition-all hover:border-primary-400"
            >
              <div class="font-bold text-gray-900 mb-1">Premium</div>
              <div class="text-[10px] text-gray-500 font-sans uppercase tracking-tight">Expérience complète et personnalisée</div>
              <div class="mt-2 text-primary-600 font-bold">99 €</div>
            </div>
          </div>
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
          {{ loading ? 'Création du compte...' : 'Créer mon compte' }}
        </button>

        <div v-if="error" class="p-4 bg-red-50 border-l-4 border-red-400 rounded-r-lg mt-6">
          <p class="text-sm text-red-700 font-sans">{{ error }}</p>
        </div>
      </form>
      
      <div class="mt-8 text-center border-t border-gray-100 pt-8">
         <p class="text-sm text-gray-500 font-sans">Déjà inscrit ? <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium transition-colors">Se connecter</router-link></p>
      </div>

    </div>
  </div>
</template>
