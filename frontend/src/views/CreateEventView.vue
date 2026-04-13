<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../service/api';

const router = useRouter();
const loading = ref(false);
const error = ref('');
const templates = ref([]);

const eventData = ref({
  title: '',
  groom_name: '',
  bride_name: '',
  date: '',
  location: '',
  template_id: 'modern-chic',
  has_cover_page: true,
  has_countdown: true
});

const fetchTemplates = async () => {
  try {
    const res = await api.get('/templates/');
    templates.value = res.data;
  } catch (err) {
    console.error("Erreur templates", err);
  }
};

const handleCreateEvent = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    await api.post('/events/', eventData.value);
    router.push('/dashboard');
  } catch (err) {
    error.value = "Une erreur est survenue lors de la création de l'événement.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTemplates);
</script>

<template>
  <div class="min-h-screen bg-primary-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
    <div class="max-w-4xl mx-auto">
      <div class="mb-10 flex items-center justify-between">
        <div>
          <button @click="router.push('/dashboard')" class="text-primary-600 hover:text-primary-700 flex items-center text-sm font-medium mb-4 transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Retour au tableau de bord
          </button>
          <h1 class="text-4xl text-gray-900 font-serif">Créer votre événement</h1>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Formulaire -->
        <div class="lg:col-span-2 bg-white rounded-3xl p-8 shadow-sm border border-primary-100 h-fit">
          <form @submit.prevent="handleCreateEvent" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2 font-sans">Nom de l'événement</label>
              <input v-model="eventData.title" type="text" placeholder="Ex: Notre Mariage" required class="w-full px-4 py-3 rounded-xl border border-primary-200 focus:ring-2 focus:ring-primary-400 outline-none transition-all bg-primary-50/30"/>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Prénom du Marié</label>
                <input v-model="eventData.groom_name" type="text" placeholder="Prénom" class="w-full px-4 py-3 rounded-xl border border-primary-200 focus:ring-2 focus:ring-primary-400 outline-none transition-all bg-primary-50/30"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Prénom de la Mariée</label>
                <input v-model="eventData.bride_name" type="text" placeholder="Prénom" class="w-full px-4 py-3 rounded-xl border border-primary-200 focus:ring-2 focus:ring-primary-400 outline-none transition-all bg-primary-50/30"/>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Date</label>
                <input v-model="eventData.date" type="date" required class="w-full px-4 py-3 rounded-xl border border-primary-200 focus:ring-2 focus:ring-primary-400 outline-none transition-all bg-primary-50/30"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Lieu</label>
                <input v-model="eventData.location" type="text" placeholder="Ex: Lyon" required class="w-full px-4 py-3 rounded-xl border border-primary-200 focus:ring-2 focus:ring-primary-400 outline-none transition-all bg-primary-50/30"/>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-6 border-t border-gray-100">
              <div class="flex items-center justify-between p-4 bg-primary-50/30 rounded-2xl border border-primary-100">
                <div>
                  <p class="text-sm font-bold text-gray-800">Page de garde</p>
                  <p class="text-[10px] text-gray-500 uppercase tracking-wider">Écran "Save the Date"</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="eventData.has_cover_page" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
              
              <div class="flex items-center justify-between p-4 bg-primary-50/30 rounded-2xl border border-primary-100">
                <div>
                  <p class="text-sm font-bold text-gray-800">Compte à rebours</p>
                  <p class="text-[10px] text-gray-500 uppercase tracking-wider">Afficher le temps restant</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="eventData.has_countdown" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>

            <div v-if="error" class="p-4 bg-red-50 text-red-700 text-xs rounded-xl">{{ error }}</div>

            <div class="pt-6 border-t border-gray-100 flex justify-end">
              <button type="submit" :disabled="loading" class="px-8 py-3 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700 shadow-lg shadow-primary-600/20 transition-all disabled:opacity-50">
                {{ loading ? 'Création...' : 'Créer mon événement' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Sélection de Template -->
        <div class="space-y-4">
          <h2 class="text-xs font-bold text-gray-400 uppercase tracking-widest px-2">Choisir un style</h2>
          <div class="space-y-4">
            <div 
              v-for="tpl in templates" 
              :key="tpl.id"
              @click="eventData.template_id = tpl.id"
              class="group cursor-pointer bg-white rounded-2xl overflow-hidden border-2 transition-all hover:shadow-md"
              :class="eventData.template_id === tpl.id ? 'border-primary-500 ring-4 ring-primary-500/10' : 'border-transparent'"
            >
              <div class="aspect-video bg-gray-100 overflow-hidden">
                <img :src="tpl.thumbnail_url" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
              </div>
              <div class="p-4">
                <h3 class="font-bold text-gray-900">{{ tpl.name }}</h3>
                <p class="text-[10px] text-gray-400 uppercase mt-1 tracking-wider">{{ tpl.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
