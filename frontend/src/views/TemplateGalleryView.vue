<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const templates = ref([]);
const loading = ref(true);
const wizardData = ref({
  groomName: 'Lui',
  brideName: 'Elle',
  date: '',
  location: '',
  style: 'all'
});

// Filters
const selectedStyle = ref('all');
const searchQuery = ref('');

const styles = [
  { id: 'all', label: 'Toutes les inspirations', icon: '✨' },
  { id: 'minimal', label: 'Luxe Minimaliste', icon: '🕊️' },
  { id: 'classic', label: 'Classique Royal', icon: '👑' },
  { id: 'art', label: 'Art & Culture', icon: '🎨' },
  { id: 'boho', label: 'Bohème Chic', icon: '🌿' }
];


const fetchTemplates = async () => {
  try {
    const response = await api.get('/templates/');
    templates.value = response.data;
  } catch (err) {
    console.error("Erreur templates", err);
    templates.value = [];
  } finally {
    loading.value = false;
  }
};

const filteredTemplates = computed(() => {
  let result = templates.value;

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(t =>
      t.name.toLowerCase().includes(q) ||
      (t.description || '').toLowerCase().includes(q)
    );
  }

  if (selectedStyle.value !== 'all') {
    result = result.filter(t => t.category === selectedStyle.value);
  }

  return result;
});

const selectTemplate = async (template) =>
{
  console.log("Template sélectionné:", template.id);
  try {
    loading.value = true;
    
    // 1. Vérifier si l'utilisateur a déjà un événement
    let eventId = null;
    let cardId = null;
    
    try {
      const myEvents = await api.get('/events/');
      if (myEvents.data && myEvents.data.length > 0) {
        // Utiliser le dernier événement créé
        const existingEvent = myEvents.data[myEvents.data.length - 1];
        eventId = existingEvent.id;
        console.log("Réutilisation de l'événement existant:", eventId);
        
        // Mettre à jour l'événement avec les nouvelles infos du Wizard (si présentes)
        await api.put(`/events/${eventId}`, {
          title: `Mariage de ${wizardData.value.groomName} & ${wizardData.value.brideName}`,
          date: wizardData.value.date || existingEvent.date,
          location: wizardData.value.location || existingEvent.location,
          groom_name: wizardData.value.groomName,
          bride_name: wizardData.value.brideName
        });
      }
    } catch (e) {
      console.log("Aucun événement existant trouvé ou erreur lors de la recherche.");
    }

    // 2. Si pas d'événement, en créer un
    if (!eventId) {
      const eventPayload = {
        title: `Mariage de ${wizardData.value.groomName} & ${wizardData.value.brideName}`,
        date: wizardData.value.date || new Date().toISOString().split('T')[0],
        location: wizardData.value.location || 'Lieu à définir',
        groom_name: wizardData.value.groomName,
        bride_name: wizardData.value.brideName,
        template_id: template.id
      };
      console.log("Création d'un nouvel événement avec payload:", eventPayload);
      const eventRes = await api.post('/events/', eventPayload);
      eventId = eventRes.data.id;
    }
    
    // 3. Récupérer la carte associée
    const eventDetail = await api.get(`/events/${eventId}`);
    cardId = eventDetail.data.card?.id;

    if (!cardId) {
       throw new Error("Impossible de trouver la carte associée à l'événement.");
    }

    // 4. Appliquer la config du template
    let manifest = {};
    try {
      manifest = typeof template.manifest_json === 'string' 
        ? JSON.parse(template.manifest_json) 
        : template.manifest_json;
    } catch (e) {
      manifest = template.manifest_json || {};
    }

    // Le manifest peut contenir un champ default_config ou être la config elle-même
    let config = manifest.default_config || manifest;

    if (config.content) {
      config.content.names = `${wizardData.value.groomName} & ${wizardData.value.brideName}`;
      config.content.date = wizardData.value.date || eventDetail.data.date;
      config.content.location = wizardData.value.location || eventDetail.data.location;
    }

    await api.put(`/cards/${cardId}/save`, {
      template_id: template.id,
      config_json: JSON.stringify(config)
    });
    
    localStorage.removeItem('wizard_data');
    router.push(`/cards/edit/${cardId}`);
  } catch (err) {
    console.error("Erreur complète :", err);
    const msg = err.response?.data?.detail || err.message || "Une erreur est survenue lors de la création de votre univers.";
    alert(msg);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const savedData = localStorage.getItem('wizard_data');
  console.log("Données Wizard récupérées dans Gallery:", savedData);
  if (savedData) {
    const parsed = JSON.parse(savedData);
    wizardData.value = { ...wizardData.value, ...parsed };
    selectedStyle.value = wizardData.value.style || 'all';
  }
  fetchTemplates();
});
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] font-serif selection:bg-[#C5A059] selection:text-white">
    
    <nav class="p-8 flex justify-between items-center border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div class="flex items-center space-x-4">
        <span class="text-2xl font-bold tracking-tighter uppercase">Saas Wedding</span>
        <div class="h-4 w-[1px] bg-gray-200"></div>
        <span class="text-xs uppercase tracking-widest text-[#C5A059]">
          Pour {{ wizardData.groomName }} & {{ wizardData.brideName }}
        </span>
      </div>
      
      <div class="flex items-center space-x-8">
        <div v-for="s in styles" :key="s.id" 
             @click="selectedStyle = s.id"
             :class="selectedStyle === s.id ? 'text-[#1A1A1A] border-b border-[#C5A059]' : 'text-gray-400 hover:text-gray-600'"
             class="cursor-pointer text-xs uppercase tracking-[0.2em] pb-1 transition-all">
          {{ s.label }}
        </div>
      </div>

      <button @click="router.push('/dashboard')" class="text-xs uppercase tracking-widest text-gray-400 hover:text-black transition-colors">
        Quitter
      </button>
    </nav>

    <main class="max-w-7xl mx-auto px-8 py-20">
      
      <header class="mb-24 text-center space-y-12">
        <h1 class="text-7xl text-[#1A1A1A] leading-none">Votre design idéal.</h1>
        <div class="max-w-md mx-auto relative group">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher une inspiration..." 
              class="w-full px-8 py-4 bg-white border border-gray-100 rounded-2xl text-xs uppercase tracking-widest outline-none shadow-sm focus:shadow-xl focus:ring-2 focus:ring-[#C5A059]/20 transition-all text-center"
            />
            <div class="absolute inset-x-0 -bottom-1 h-[2px] bg-gradient-to-r from-transparent via-[#C5A059] to-transparent scale-x-0 group-focus-within:scale-x-100 transition-transform duration-700"></div>
        </div>
      </header>

      <div v-if="loading" class="flex flex-col items-center justify-center py-40 space-y-4">
        <div class="w-12 h-1 bg-gray-100 overflow-hidden rounded-full relative">
          <div class="absolute inset-0 bg-[#C5A059] animate-loading-bar"></div>
        </div>
        <span class="text-[10px] uppercase tracking-widest text-[#C5A059]">Préparation de votre univers...</span>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-16">
        <div 
          v-for="tpl in filteredTemplates" 
          :key="tpl.id"
          class="group cursor-pointer space-y-8"
          @click="selectTemplate(tpl)"
        >
          <div class="relative aspect-[3/4.5] overflow-hidden bg-white shadow-2xl transition-all duration-700 group-hover:-translate-y-4 border border-gray-100">
            <img 
               :src="tpl.thumbnail_url" 
               class="absolute inset-0 w-full h-full object-cover transition-all duration-1000 group-hover:scale-105"
               alt="Template"
            />
            
            <div class="absolute inset-0 bg-[#1A1A1A]/90 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col items-center justify-center p-12 text-center space-y-8">
                <div class="w-12 h-[1px] bg-[#C5A059]"></div>
                <p class="text-white text-sm font-sans leading-relaxed opacity-80">{{ tpl.description }}</p>
                <span class="px-8 py-3 border border-white text-white text-[10px] uppercase tracking-widest hover:bg-white hover:text-black transition-all">
                  Choisir ce design
                </span>
            </div>

            <div class="absolute bottom-12 inset-x-0 text-center pointer-events-none group-hover:opacity-0 transition-opacity duration-300 px-4">
                <div class="bg-white/95 backdrop-blur-sm py-4 px-6 inline-block rounded-sm shadow-xl border border-gray-100">
                    <p class="text-[10px] uppercase tracking-[0.3em] text-[#C5A059] mb-1">Célébration</p>
                    <h4 class="text-xl text-[#1A1A1A]">{{ wizardData.groomName }} & {{ wizardData.brideName }}</h4>
                </div>
            </div>
          </div>
          
          <div class="text-center">
            <h4 class="text-sm uppercase tracking-[0.3em] text-[#1A1A1A]">{{ tpl.name }}</h4>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@keyframes loading-bar {
  0% { left: -100%; width: 100%; }
  100% { left: 100%; width: 100%; }
}
.animate-loading-bar {
  animation: loading-bar 1.5s infinite linear;
}
</style>
