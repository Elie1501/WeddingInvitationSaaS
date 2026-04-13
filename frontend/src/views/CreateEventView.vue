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
  <div class="min-h-screen bg-neutral-50 py-16 px-4 sm:px-6 lg:px-8 font-sans selection:bg-primary-100 selection:text-primary-900">
    <div class="max-w-5xl mx-auto">
      
      <!-- Header -->
      <div class="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <button @click="router.push('/dashboard')" class="group text-neutral-400 hover:text-primary-600 flex items-center text-[10px] font-bold uppercase tracking-[0.2em] mb-6 transition-all">
            <svg class="w-4 h-4 mr-2 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Retour au tableau de bord
          </button>
          <h1 class="text-4xl md:text-5xl text-neutral-900 font-serif italic">Créer votre événement</h1>
          <p class="mt-3 text-neutral-500 font-light tracking-wide">Remplissez les informations de base pour commencer votre invitation.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <!-- Formulaire Principal -->
        <div class="lg:col-span-8 space-y-8">
          <div class="bg-white rounded-[2.5rem] p-10 md:p-14 shadow-[0_20px_50px_rgba(0,0,0,0.04)] border border-neutral-100">
            <form @submit.prevent="handleCreateEvent" class="space-y-10">
              
              <!-- Section Infos de base -->
              <div class="space-y-8">
                <div class="flex items-center space-x-4 mb-2">
                  <span class="w-8 h-[1px] bg-primary-200"></span>
                  <h2 class="text-[10px] font-bold text-primary-500 uppercase tracking-[0.4em]">Informations Générales</h2>
                </div>

                <div class="space-y-2">
                  <label class="block text-[11px] font-bold text-neutral-400 uppercase tracking-widest ml-1">Titre de l'invitation</label>
                  <input v-model="eventData.title" type="text" placeholder="Ex: Mariage de Sarah & Marc" required 
                    class="w-full px-6 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300 font-serif text-lg"/>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div class="space-y-2">
                    <label class="block text-[11px] font-bold text-neutral-400 uppercase tracking-widest ml-1">Marié(e) 1</label>
                    <input v-model="eventData.groom_name" type="text" placeholder="Prénom" required
                      class="w-full px-6 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300"/>
                  </div>
                  <div class="space-y-2">
                    <label class="block text-[11px] font-bold text-neutral-400 uppercase tracking-widest ml-1">Marié(e) 2</label>
                    <input v-model="eventData.bride_name" type="text" placeholder="Prénom" required
                      class="w-full px-6 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300"/>
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div class="space-y-2">
                    <label class="block text-[11px] font-bold text-neutral-400 uppercase tracking-widest ml-1">Date de l'événement</label>
                    <input v-model="eventData.date" type="datetime-local" required 
                      class="w-full px-6 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300 appearance-none"/>
                  </div>
                  <div class="space-y-2">
                    <label class="block text-[11px] font-bold text-neutral-400 uppercase tracking-widest ml-1">Lieu principal</label>
                    <input v-model="eventData.location" type="text" placeholder="Ville, Domaine, Adresse..." required 
                      class="w-full px-6 py-4 rounded-2xl border border-neutral-100 bg-neutral-50 focus:bg-white focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none transition-all duration-300"/>
                  </div>
                </div>
              </div>

              <!-- Options Affichage -->
              <div class="pt-10 border-t border-neutral-50 space-y-6">
                <div class="flex items-center space-x-4 mb-2">
                  <span class="w-8 h-[1px] bg-primary-200"></span>
                  <h2 class="text-[10px] font-bold text-primary-500 uppercase tracking-[0.4em]">Options d'Affichage</h2>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div class="flex items-center justify-between p-6 bg-neutral-50 rounded-[1.5rem] border border-neutral-100 group hover:bg-white hover:shadow-xl hover:shadow-neutral-900/5 transition-all duration-500">
                    <div>
                      <p class="text-sm font-bold text-neutral-800">Page de garde</p>
                      <p class="text-[10px] text-neutral-400 uppercase tracking-widest font-medium mt-1">Écran d'accueil immersif</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" v-model="eventData.has_cover_page" class="sr-only peer">
                      <div class="w-12 h-6 bg-neutral-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary-900"></div>
                    </label>
                  </div>
                  
                  <div class="flex items-center justify-between p-6 bg-neutral-50 rounded-[1.5rem] border border-neutral-100 group hover:bg-white hover:shadow-xl hover:shadow-neutral-900/5 transition-all duration-500">
                    <div>
                      <p class="text-sm font-bold text-neutral-800">Compte à rebours</p>
                      <p class="text-[10px] text-neutral-400 uppercase tracking-widest font-medium mt-1">Temps restant dynamique</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" v-model="eventData.has_countdown" class="sr-only peer">
                      <div class="w-12 h-6 bg-neutral-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary-900"></div>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Feedback Erreur -->
              <div v-if="error" class="p-6 bg-red-50/50 border border-red-100 text-red-600 text-sm rounded-2xl text-center animate-pulse">
                {{ error }}
              </div>

              <!-- Action Button -->
              <div class="pt-6 flex justify-center">
                <button type="submit" :disabled="loading" 
                  class="group relative px-12 py-5 bg-neutral-900 text-white rounded-2xl font-bold uppercase tracking-[0.3em] text-[12px] shadow-2xl shadow-neutral-900/20 hover:shadow-neutral-900/40 transition-all duration-500 transform active:scale-[0.98] overflow-hidden">
                  <div class="absolute inset-0 bg-white/10 w-0 group-hover:w-full transition-all duration-500"></div>
                  <span class="relative z-10">{{ loading ? 'Création en cours...' : 'Créer mon événement' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Sélection de Template (Sidebar) -->
        <div class="lg:col-span-4 space-y-8">
          <div class="sticky top-24 space-y-6">
            <div class="flex items-center space-x-4 mb-2">
              <span class="w-8 h-[1px] bg-primary-200"></span>
              <h2 class="text-[10px] font-bold text-primary-500 uppercase tracking-[0.4em]">Choisir un style</h2>
            </div>
            
            <div class="space-y-6 max-h-[calc(100vh-250px)] overflow-y-auto pr-2 custom-scrollbar">
              <div 
                v-for="tpl in templates" 
                :key="tpl.id"
                @click="eventData.template_id = tpl.id"
                class="group cursor-pointer bg-white rounded-[2rem] overflow-hidden border-2 transition-all duration-500 relative"
                :class="eventData.template_id === tpl.id ? 'border-primary-900 shadow-2xl shadow-primary-900/10 -translate-y-1' : 'border-transparent hover:border-neutral-200 hover:shadow-xl hover:shadow-neutral-900/5'"
              >
                <!-- Badge Selected -->
                <div v-if="eventData.template_id === tpl.id" class="absolute top-4 right-4 z-20 bg-primary-900 text-white p-2 rounded-full shadow-lg">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
                </div>

                <div class="aspect-[4/3] bg-neutral-100 overflow-hidden relative">
                  <img :src="tpl.thumbnail_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=800'" 
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-[1.5s] ease-out">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                </div>
                
                <div class="p-6">
                  <h3 class="font-bold text-neutral-900 font-serif italic text-lg">{{ tpl.name }}</h3>
                  <p class="text-[10px] text-neutral-400 uppercase mt-1 tracking-widest font-medium">{{ tpl.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e5e5;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #d4d4d4;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
</style>
