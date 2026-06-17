<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../service/api';
import { useAuthStore } from '../stores/auth';
import UpgradeModal from '../components/UpgradeModal.vue';

const authStore = useAuthStore();
const isPremium = computed(() => authStore.user?.plan === 'premium');

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const templates = ref([]);
const loading = ref(true);
const wizardData = ref({
  groomName: '',
  brideName: '',
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

const showUpgradeModal = ref(false);

const selectTemplate = async (template) => {
  if (template.required_plan === 'premium' && !isPremium.value) {
    showUpgradeModal.value = true;
    return;
  }

  console.log("Template sélectionné:", template.id);
  try {
    loading.value = true;
    
    // 1. Vérifier si l'utilisateur a déjà un événement
    let eventId = null;
    let cardId = null;
    
    try {
      const myEvents = await api.get('/events/');
      if (myEvents.data && myEvents.data.length > 0) {
        const existingEvent = myEvents.data[myEvents.data.length - 1];
        eventId = existingEvent.id;

        // N'écraser les noms que si le wizard en a de vrais — sinon garder ceux de l'event existant
        const finalGroom = wizardData.value.groomName || existingEvent.groom_name || '';
        const finalBride = wizardData.value.brideName || existingEvent.bride_name || '';
        await api.put(`/events/${eventId}`, {
          title: `Mariage de ${finalGroom} & ${finalBride}`,
          date: wizardData.value.date || existingEvent.date,
          location: wizardData.value.location || existingEvent.location,
          groom_name: finalGroom,
          bride_name: finalBride
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

    let config = manifest.default_config || manifest;

    // Le layout doit toujours correspondre à l'ID du template sélectionné
    config.layout = template.id;

    // Noms finaux : wizard > event > vide
    const finalGroom = wizardData.value.groomName || eventDetail.data.groom_name || '';
    const finalBride = wizardData.value.brideName || eventDetail.data.bride_name || '';
    const namesDisplay = finalGroom && finalBride ? `${finalGroom} & ${finalBride}` : (finalGroom || finalBride);

    // Date formatée en français (pour le champ date_display lu par les templates)
    const rawDate = wizardData.value.date || eventDetail.data.date;
    let dateDisplay = '';
    if (rawDate) {
      try {
        dateDisplay = new Date(rawDate).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
      } catch {}
    }

    const finalLocation = wizardData.value.location || eventDetail.data.location || '';

    if (!config.content) config.content = {};
    config.content.names = namesDisplay;
    config.content.splash_title = namesDisplay;
    // Clés correctes lues par tous les templates
    if (dateDisplay) config.content.date_display = dateDisplay;
    if (finalLocation) config.content.address = finalLocation;
    // Monogramme auto si absent ou toujours celui du démo
    if (finalGroom && finalBride) {
      config.content.monogram = `${finalGroom[0].toUpperCase()} & ${finalBride[0].toUpperCase()}`;
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

onMounted(async () => {
  if (!authStore.user) await authStore.fetchMe();

  const savedData = localStorage.getItem('wizard_data');
  if (savedData) {
    const parsed = JSON.parse(savedData);
    wizardData.value = { ...wizardData.value, ...parsed };
    selectedStyle.value = wizardData.value.style || 'all';
  }

  // Si pas de noms dans le wizard, charger depuis l'événement existant
  if (!wizardData.value.groomName || !wizardData.value.brideName) {
    try {
      const res = await api.get('/events/');
      if (res.data && res.data.length > 0) {
        const ev = res.data[res.data.length - 1];
        if (!wizardData.value.groomName) wizardData.value.groomName = ev.groom_name || '';
        if (!wizardData.value.brideName) wizardData.value.brideName = ev.bride_name || '';
        if (!wizardData.value.date) wizardData.value.date = ev.date ? ev.date.split('T')[0] : '';
        if (!wizardData.value.location) wizardData.value.location = ev.location || '';
      }
    } catch {}
  }

  fetchTemplates();
});
</script>

<template>
  <div class="min-h-screen bg-[#F9F7F2] font-serif selection:bg-[#C5A059] selection:text-white">
    
    <nav class="px-4 sm:px-8 py-4 sm:py-6 border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div class="flex justify-between items-center gap-3">
        <div class="flex items-center gap-3 min-w-0">
          <span class="text-lg sm:text-2xl font-bold tracking-tighter uppercase whitespace-nowrap">Saas Wedding</span>
          <div class="hidden sm:block h-4 w-[1px] bg-gray-200"></div>
          <span class="hidden sm:block text-xs uppercase tracking-widest text-[#C5A059] truncate">
            Pour {{ wizardData.groomName }} & {{ wizardData.brideName }}
          </span>
        </div>

        <button @click="router.push('/dashboard')" class="text-[10px] sm:text-xs uppercase tracking-widest text-gray-400 hover:text-black transition-colors whitespace-nowrap shrink-0">
          Quitter
        </button>
      </div>

      <!-- Filtres de style : scroll horizontal sur mobile pour éviter l'écrasement -->
      <div class="mt-3 sm:mt-4 flex items-center gap-5 sm:gap-8 overflow-x-auto no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
        <button v-for="s in styles" :key="s.id"
             @click="selectedStyle = s.id"
             :class="selectedStyle === s.id ? 'text-[#1A1A1A] border-b border-[#C5A059]' : 'text-gray-400 hover:text-gray-600'"
             class="cursor-pointer text-[10px] sm:text-xs uppercase tracking-[0.15em] sm:tracking-[0.2em] pb-1 transition-all whitespace-nowrap shrink-0">
          {{ s.label }}
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-8 py-10 sm:py-20">

      <header class="mb-12 sm:mb-24 text-center space-y-6 sm:space-y-12">
        <h1 class="text-4xl sm:text-6xl lg:text-7xl text-[#1A1A1A] leading-none">Votre design idéal.</h1>
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

      <div v-else class="grid grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-8 sm:gap-12 lg:gap-16">
        <div
          v-for="tpl in filteredTemplates"
          :key="tpl.id"
          class="group cursor-pointer space-y-5"
          @click="selectTemplate(tpl)"
        >
          <div class="relative aspect-[3/4.5] overflow-hidden bg-white shadow-2xl transition-all duration-700 group-hover:-translate-y-4 border border-gray-100">
            <img
               :src="tpl.thumbnail_url"
               class="absolute inset-0 w-full h-full object-cover transition-all duration-1000 group-hover:scale-105"
               alt="Template"
            />

            <!-- Badge plan (coin supérieur droit) -->
            <div class="absolute top-4 right-4 z-10">
              <span v-if="tpl.required_plan === 'premium'"
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[9px] font-black uppercase tracking-widest bg-[#1A1A1A]/80 backdrop-blur-sm text-[#C5A059] border border-[#C5A059]/40">
                <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 1l3.09 6.26L22 8.27l-5 4.87 1.18 6.88L12 16.77l-6.18 3.25L7 13.14 2 8.27l6.91-1.01L12 1z"/></svg>
                Premium
              </span>
              <span v-else
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[9px] font-black uppercase tracking-widest bg-white/80 backdrop-blur-sm text-gray-600 border border-gray-200">
                Classic
              </span>
            </div>

            <!-- Overlay hover : différent selon plan requis -->
            <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col items-center justify-center p-4 sm:p-12 text-center space-y-4 sm:space-y-6"
                 :class="tpl.required_plan === 'premium' && !isPremium ? 'bg-[#0C0906]/92' : 'bg-[#1A1A1A]/90'">

              <!-- CTA premium verrouillé -->
              <template v-if="tpl.required_plan === 'premium' && !isPremium">
                <svg class="w-10 h-10 text-[#C5A059]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
                <div>
                  <p class="text-[#C5A059] text-[10px] font-black uppercase tracking-widest mb-1">Template Premium</p>
                  <p class="text-white/70 text-[11px] font-sans leading-relaxed">{{ tpl.description }}</p>
                </div>
                <button @click.stop="showUpgradeModal = true"
                        class="flex items-center gap-2 px-8 py-3 bg-[#C5A059] text-white text-[10px] uppercase tracking-widest font-bold hover:bg-[#b08c47] transition-all rounded-sm">
                  Passer au Premium →
                </button>
              </template>

              <!-- CTA normal -->
              <template v-else>
                <div class="w-12 h-[1px] bg-[#C5A059]"></div>
                <p class="text-white text-sm font-sans leading-relaxed opacity-80">{{ tpl.description }}</p>
                <span class="px-8 py-3 border border-white text-white text-[10px] uppercase tracking-widest hover:bg-white hover:text-black transition-all">
                  Choisir ce design
                </span>
              </template>
            </div>

            <!-- Preview nom couple -->
            <div class="absolute bottom-5 sm:bottom-12 inset-x-0 text-center pointer-events-none group-hover:opacity-0 transition-opacity duration-300 px-3">
                <div class="bg-white/95 backdrop-blur-sm py-2.5 px-3 sm:py-4 sm:px-6 inline-block rounded-sm shadow-xl border border-gray-100 max-w-full">
                    <p class="text-[8px] sm:text-[10px] uppercase tracking-[0.2em] sm:tracking-[0.3em] text-[#C5A059] mb-1">Célébration</p>
                    <h4 class="text-sm sm:text-xl text-[#1A1A1A] truncate">{{ wizardData.groomName }} & {{ wizardData.brideName }}</h4>
                </div>
            </div>
          </div>

          <!-- Nom + badge plan -->
          <div class="text-center space-y-2">
            <h4 class="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-[#1A1A1A]">{{ tpl.name }}</h4>
            <span class="inline-block text-[9px] font-black uppercase tracking-widest px-2.5 py-0.5 rounded-full"
                  :class="tpl.required_plan === 'premium'
                    ? 'text-[#C5A059] bg-[#C5A059]/10 border border-[#C5A059]/30'
                    : 'text-gray-400 bg-gray-100 border border-gray-200'">
              {{ tpl.required_plan === 'premium' ? '★ Premium' : 'Classic' }}
            </span>
          </div>
        </div>
      </div>
    </main>
  </div>

  <UpgradeModal v-model="showUpgradeModal" />
</template>

<style scoped>
@keyframes loading-bar {
  0% { left: -100%; width: 100%; }
  100% { left: 100%; width: 100%; }
}
.animate-loading-bar {
  animation: loading-bar 1.5s infinite linear;
}
/* Masque la barre de scroll des filtres horizontaux (mobile) */
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
.no-scrollbar::-webkit-scrollbar { display: none; }
</style>
