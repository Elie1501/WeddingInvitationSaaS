<script setup>
import { ref, onMounted, watch, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';
import { useAuthStore } from '../stores/auth';
import { getPlanInfo } from '../service/plans';

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const cardId = route.params.id;

const activePageIndex = ref(0); // 0 = Invitation, 1+ = Extra Pages, -1 = Cover
const isEditingCover = ref(false); 
const card = ref(null);
const event = ref(null);
const loading = ref(true);
const saving = ref(false);
const lastSaved = ref(null);
const versions = ref([]);
const showVersionsModal = ref(false);
const fileInput = ref(null);
const fileInputSplash = ref(null);
const fileInputMusic = ref(null);

const defaultMusicTracks = [
  { name: 'Piano Romantique', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' },
  { name: 'Violon Élégant', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3' },
  { name: 'Guitare Douce', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3' },
  { name: 'Ambiance Jazz', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3' }
];

const planInfo = computed(() => getPlanInfo(auth.user?.plan || 'classic'));

// Configuration dynamique
const config = reactive({
  colors: {
    primary: '#FFFFFF',
    accent: '#4f46e5',
    text: '#1f2937'
  },
  typography: {
    headings: 'serif',
    body: 'sans-serif'
  },
  media: {
    banner_url: '',
    splash_url: ''
  },
  content: {
    intro_text: '',
    splash_top_text: 'Save the Date',
    splash_title: '',
    splash_subtitle: '',
    splash_button_text: 'Ouvrir l\'invitation',
    rsvp_title: 'Confirmez votre présence',
    rsvp_subtitle: 'Veuillez nous donner une réponse avant la date limite.'
  },
  splash: {
    overlay_opacity: 40,
    use_image: true,
    background_color: '#ffffff'
  },
  rsvp: {
    ask_email: true,
    ask_plus_ones: true,
    ask_dietary: true,
    ask_message: true
  },
  has_cover_page: false,
  show_countdown_splash: false,
  show_countdown_invitation: false,
  sections: [
    { type: 'banner', id: 'sec-1' },
    { type: 'details', id: 'sec-3' }
  ],
  pages: [], 
  itinerary: [] 
});

const fetchCard = async () => {
  console.log("Fetching card with ID:", cardId);
  try {
    const response = await api.get(`/cards/${cardId}`);
    console.log("Card response received:", response.data);
    card.value = response.data;
    event.value = response.data.event;
    
    if (card.value.config_json) {
      console.log("Parsing config_json...");
      try {
        const savedConfig = JSON.parse(card.value.config_json);
        console.log("Parsed config:", savedConfig);
        // Fusion profonde pour ne pas perdre les nouvelles clés
        Object.keys(savedConfig).forEach(key => {
          if (typeof savedConfig[key] === 'object' && savedConfig[key] !== null && !Array.isArray(savedConfig[key])) {
            config[key] = { ...config[key], ...savedConfig[key] };
          } else {
            config[key] = savedConfig[key];
          }
        });
      } catch (parseErr) {
        console.error("Error parsing config_json:", parseErr);
      }
    } else {
      console.log("No config_json, using defaults from card object");
      config.content.intro_text = card.value.intro_text;
      config.colors.accent = card.value.theme_color;
      config.media.banner_url = card.value.media_url;
      config.has_cover_page = card.value.has_cover_page;
    }

    // Formater la date pour l'input datetime-local (YYYY-MM-DDThh:mm)
    if (event.value && event.value.date) {
      try {
        const d = new Date(event.value.date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        event.value.date = `${year}-${month}-${day}T${hours}:${minutes}`;
        console.log("Formatted date:", event.value.date);
      } catch (e) {
        console.error("Erreur formatage date", e);
      }
    }

    if (card.value.sub_events && card.value.sub_events.length > 0) {
      config.itinerary = card.value.sub_events;
    }
  } catch (err) {
    console.error("Erreur lors de la récupération", err);
  } finally {
    loading.value = false;
    console.log("Loading finished, event is:", event.value);
  }
};

const addPage = () => {
  const currentTotal = (config.has_cover_page ? 1 : 0) + 1 + config.pages.length;
  if (currentTotal >= planInfo.value.max_pages) {
    alert(`Votre forfait ${planInfo.value.name} est limité à ${planInfo.value.max_pages} pages.`);
    return;
  }
  const newId = Date.now();
  config.pages.push({ 
    id: newId, 
    title: `Page ${config.pages.length + 1}`,
    banner_url: '',
    sections: [{ type: 'banner', id: 'banner-' + newId }, { type: 'text', id: 'sec-' + newId, content: 'Écrivez ici le contenu de votre nouvelle page...' }] 
  });
  activePageIndex.value = config.pages.length;
  isEditingCover.value = false;
};

const removePage = (index) => {
  if (confirm("Supprimer cette page ?")) {
    config.pages.splice(index, 1);
    activePageIndex.value = 0;
  }
};

const handleFileUpload = async (e, target = 'banner', pageIdx = null) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', target === 'music' ? 'music' : 'image');

  try {
    saving.value = true;
    const res = await api.post(`/cards/${cardId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    if (pageIdx !== null) {
      config.pages[pageIdx].banner_url = res.data.url;
    } else if (target === 'splash') {
      config.media.splash_url = res.data.url;
    } else if (target === 'music') {
      card.value.music_url = res.data.url;
    } else {
      config.media.banner_url = res.data.url;
    }
  } catch (err) {
    alert("Erreur lors de l'upload.");
  } finally {
    saving.value = false;
  }
};

const addItineraryItem = () => {
  if (!config.itinerary) config.itinerary = [];
  config.itinerary.push({ title: '', time: '', location: '', description: '' });
  
  // S'assurer que la section 'itinerary' est présente dans l'invitation principale (idx 0)
  if (!config.sections.find(s => s.type === 'itinerary')) {
    config.sections.push({ type: 'itinerary', id: 'sec-itinerary-' + Date.now() });
  }
};

const removeItineraryItem = (index) => {
  config.itinerary.splice(index, 1);
};

const fetchVersions = async () => {
  try {
    const response = await api.get(`/cards/${cardId}/versions`);
    versions.value = response.data;
    showVersionsModal.value = true;
  } catch (err) {
    console.error("Erreur versions", err);
  }
};

const rollback = async (versionNumber) => {
  if (!confirm(`Restaurer la version ${versionNumber} ?`)) return;
  try {
    const response = await api.post(`/cards/${cardId}/rollback/${versionNumber}`);
    card.value = response.data;
    if (card.value.config_json) {
      Object.assign(config, JSON.parse(card.value.config_json));
    }
    showVersionsModal.value = false;
  } catch (err) {
    alert("Erreur rollback");
  }
};

function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

const autoSave = debounce(async () => {
  if (!card.value) return;
  saving.value = true;
  try {
    await api.put(`/cards/${cardId}/save`, {
      config_json: JSON.stringify(config),
      intro_text: config.content.intro_text,
      theme_color: config.colors.accent,
      media_url: config.media.banner_url,
      music_url: card.value.music_url,
      has_cover_page: config.has_cover_page,
      sub_events: config.itinerary,
      template_id: card.value.template_id,
      title: event.value.title,
      groom_name: event.value.groom_name,
      bride_name: event.value.bride_name,
      date: event.value.date,
      location: event.value.location
    });
    lastSaved.value = new Date().toLocaleTimeString();
  } catch (err) {
    console.error("Erreur auto-save", err);
  } finally {
    saving.value = false;
  }
}, 2000);

watch([config, () => card.value?.template_id, () => card.value?.music_url, event], () => autoSave(), { deep: true });

const publish = async () => {
  try {
    const response = await api.post(`/cards/${cardId}/publish`);
    card.value.is_published = response.data.is_published;
    card.value.slug = response.data.slug;
  } catch (err) {
    console.error("Erreur publication", err);
  }
};

onMounted(fetchCard);
</script>

<template>
  <div class="flex h-screen bg-gray-100 overflow-hidden font-sans">
    <!-- Sidebar gauche -->
    <aside class="w-96 bg-white border-r border-gray-200 flex flex-col shadow-xl z-20 overflow-hidden">
      <div class="p-6 border-b border-gray-100 flex items-center justify-between bg-white sticky top-0">
        <div>
          <button @click="router.push('/dashboard')" class="text-xs text-gray-400 hover:text-primary-600 mb-1 flex items-center transition-colors">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Dashboard
          </button>
          <h1 class="text-xl font-semibold text-gray-900">Concepteur</h1>
        </div>
        <div class="flex flex-col items-end">
          <span v-if="saving" class="text-[10px] text-primary-500 animate-pulse font-medium uppercase tracking-wider">Sauvegarde...</span>
          <span v-else-if="lastSaved" class="text-[10px] text-gray-400 font-medium uppercase tracking-wider">Enregistré à {{ lastSaved }}</span>
        </div>
      </div>

      <div v-if="event" class="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar pb-32">
        <!-- Navigation Pages -->
        <div class="flex bg-gray-50 p-1 rounded-xl overflow-x-auto no-scrollbar">
          <button 
            @click="isEditingCover = true; activePageIndex = -1"
            :class="isEditingCover ? 'bg-white shadow-sm text-primary-600' : 'text-gray-400'"
            class="flex-none px-4 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded-lg transition-all"
          >
            Couverture
          </button>
          <button 
            @click="isEditingCover = false; activePageIndex = 0"
            :class="!isEditingCover && activePageIndex === 0 ? 'bg-white shadow-sm text-primary-600' : 'text-gray-400'"
            class="flex-none px-4 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded-lg transition-all"
          >
            Invitation
          </button>
          <button 
            v-for="(page, idx) in config.pages" 
            :key="page.id"
            @click="isEditingCover = false; activePageIndex = idx + 1"
            :class="!isEditingCover && activePageIndex === idx + 1 ? 'bg-white shadow-sm text-primary-600' : 'text-gray-400'"
            class="flex-none px-4 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded-lg transition-all"
          >
            Page {{ idx + 1 }}
          </button>
          <button @click="addPage" class="flex-none px-3 text-primary-600 font-bold text-base">+</button>
        </div>

        <!-- Section MUSIQUE (Toujours visible et bien placée) -->
        <section class="space-y-4 pt-2 pb-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center">
              <svg class="w-3.5 h-3.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
              Musique d'ambiance
            </h3>
          </div>
          
          <div class="grid grid-cols-1 gap-2">
            <div 
              v-for="track in defaultMusicTracks" 
              :key="track.url"
              @click="card.music_url = track.url"
              :class="card?.music_url === track.url ? 'border-primary-500 bg-primary-50 ring-1 ring-primary-100' : 'border-gray-100 hover:border-primary-200 bg-white'"
              class="flex items-center justify-between p-3 border rounded-xl cursor-pointer transition-all group shadow-sm"
            >
              <span class="text-xs font-medium text-gray-700">{{ track.name }}</span>
              <div v-if="card?.music_url === track.url" class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full bg-primary-500 animate-pulse"></div>
              </div>
            </div>
          </div>

          <div v-if="card?.music_url" class="space-y-3 mt-4">
             <div class="flex items-center justify-between bg-primary-50 p-3 rounded-xl border border-primary-100">
                <div class="flex items-center overflow-hidden">
                  <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mr-3 flex-shrink-0">
                    <svg class="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"></path></svg>
                  </div>
                  <span class="text-[10px] text-primary-700 font-medium truncate italic">{{ card.music_url.split('/').pop().substring(0, 20) }}...</span>
                </div>
                <button @click="card.music_url = ''" class="text-primary-400 hover:text-red-500 transition-colors p-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
             </div>
             <audio :src="card.music_url" controls class="w-full h-8 scale-90 origin-left"></audio>
          </div>

          <div class="pt-1">
            <button 
              @click="planInfo.can_upload_music ? $refs.fileInputMusic.click() : null"
              :class="planInfo.can_upload_music ? 'hover:border-primary-300 hover:text-primary-500 cursor-pointer' : 'opacity-50 cursor-not-allowed bg-gray-50'"
              class="w-full py-3 border-2 border-dashed border-gray-100 rounded-xl text-[10px] font-bold uppercase tracking-widest text-gray-400 transition-all flex flex-col items-center justify-center gap-1"
            >
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                Upload ton MP3
              </div>
              <span v-if="!planInfo.can_upload_music" class="text-[8px] text-amber-600 lowercase tracking-normal italic">(Réservé aux membres Premium)</span>
            </button>
            <input v-if="planInfo.can_upload_music" type="file" ref="fileInputMusic" class="hidden" accept="audio/*" @change="e => handleFileUpload(e, 'music')">
          </div>
        </section>

        <!-- Édition COUVERTURE -->
        <div v-if="isEditingCover" class="space-y-8 animate-in fade-in slide-in-from-left-2">
           <section class="space-y-4">
             <div class="flex justify-between items-center bg-primary-50 p-4 rounded-2xl border border-primary-100">
               <div>
                 <h3 class="text-[11px] font-bold text-primary-900 uppercase tracking-widest">Activer la page de garde</h3>
                 <p class="text-[9px] text-primary-600 mt-0.5">Une page d'accueil élégante avant l'invitation</p>
               </div>
               <label class="relative inline-flex items-center cursor-pointer">
                 <input type="checkbox" v-model="config.has_cover_page" class="sr-only peer">
                 <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
               </label>
             </div>

             <div v-if="config.has_cover_page" class="space-y-4 pt-2">
               <div class="flex bg-gray-50 p-1 rounded-xl">
                 <button 
                   @click="config.splash.use_image = true"
                   :class="config.splash.use_image ? 'bg-white shadow-sm text-primary-600' : 'text-gray-400'"
                   class="flex-1 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded-lg transition-all"
                 >
                   Image
                 </button>
                 <button 
                   @click="config.splash.use_image = false"
                   :class="!config.splash.use_image ? 'bg-white shadow-sm text-primary-600' : 'text-gray-400'"
                   class="flex-1 py-1.5 text-[10px] font-bold uppercase tracking-wider rounded-lg transition-all"
                 >
                   Couleur
                 </button>
               </div>

               <div v-if="config.splash.use_image">
                 <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1.5 ml-1">Photo de couverture</label>
                 <div class="aspect-[4/3] bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center overflow-hidden relative group" :style="(config.media.splash_url || config.media.banner_url) ? { backgroundImage: `url(${config.media.splash_url || config.media.banner_url})`, backgroundSize: 'cover', backgroundPosition: 'center', border: 'none' } : {}">
                    <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center z-10">
                      <button @click="$refs.fileInputSplash.click()" class="bg-white text-gray-900 px-4 py-2 rounded-full text-xs font-bold shadow-xl">Changer la photo</button>
                    </div>
                    <input type="file" ref="fileInputSplash" class="hidden" accept="image/*" @change="e => handleFileUpload(e, 'splash')">
                    <div v-if="config.media.splash_url || config.media.banner_url" class="absolute inset-0 bg-black/30 flex flex-col items-center justify-center p-2 text-center pointer-events-none">
                       <span class="text-[8px] text-white/80 uppercase tracking-widest mb-1">{{ config.content.splash_top_text }}</span>
                       <span class="text-[10px] text-white font-serif">{{ config.content.splash_title || (event?.groom_name + ' & ' + event?.bride_name) }}</span>
                    </div>
                 </div>
                 <input v-model="config.media.splash_url" type="text" placeholder="URL de l'image..." class="w-full text-[11px] p-2 bg-gray-50 border-gray-100 rounded-lg mt-2 focus:outline-none">
                 <p class="text-[9px] text-gray-400 mt-1 italic">* Si vide, l'image de l'invitation sera utilisée.</p>
               </div>

               <div v-else class="space-y-2">
                 <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1.5 ml-1">Couleur de fond</label>
                 <div class="flex items-center space-x-3 bg-gray-50 p-3 rounded-xl border border-gray-100">
                   <input type="color" v-model="config.splash.background_color" class="h-10 w-10 rounded-lg cursor-pointer border-none bg-transparent">
                   <input type="text" v-model="config.splash.background_color" class="bg-transparent border-none text-xs font-mono w-24 focus:ring-0">
                 </div>
               </div>

               <div class="space-y-4">
                 <input v-model="config.content.splash_top_text" type="text" placeholder="Petit texte du haut" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none">
                 <input v-model="config.content.splash_title" type="text" placeholder="Titre Principal (Optionnel)" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none">
                 <textarea v-model="config.content.splash_subtitle" rows="2" placeholder="Sous-titre..." class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
                 
                 <div class="space-y-1">
                    <label class="text-[10px] font-bold text-gray-400 uppercase tracking-widest ml-1">Opacité voile noir ({{ config.splash.overlay_opacity }}%)</label>
                    <input v-model.number="config.splash.overlay_opacity" type="range" min="0" max="80" step="5" class="w-full accent-primary-600">
                 </div>

                 <div class="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100">
                   <span class="text-[11px] font-medium text-gray-700">Compte à rebours</span>
                   <label class="relative inline-flex items-center cursor-pointer scale-75">
                     <input type="checkbox" v-model="config.show_countdown_splash" class="sr-only peer">
                     <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                   </label>
                 </div>
               </div>
             </div>
           </section>
        </div>

        <!-- Édition INVITATION -->
        <div v-else-if="!isEditingCover && activePageIndex === 0" class="space-y-8 animate-in fade-in slide-in-from-left-2">
           <button @click="fetchVersions" class="w-full py-2 bg-gray-50 border border-gray-200 rounded-xl text-xs font-semibold text-gray-600 hover:bg-gray-100 transition-all flex items-center justify-center">
             <svg class="w-3.5 h-3.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
             Versions
           </button>

           <!-- INFOS GÉNÉRALES -->
           <section class="space-y-4 pt-2">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Infos de l'événement</h3>
             
             <div class="space-y-3">
               <div>
                 <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Titre de l'invitation</label>
                 <input v-model="event.title" type="text" placeholder="Ex: Mariage de Julie & Thomas" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none transition-all">
               </div>

               <div class="grid grid-cols-2 gap-3">
                 <div>
                   <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Marié(e) 1</label>
                   <input v-model="event.groom_name" type="text" placeholder="Prénom" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                 </div>
                 <div>
                   <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Marié(e) 2</label>
                   <input v-model="event.bride_name" type="text" placeholder="Prénom" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none transition-all">
                 </div>
               </div>

               <div>
                 <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Date & Heure</label>
                 <input v-model="event.date" type="datetime-local" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none transition-all">
               </div>

               <div>
                 <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Lieu principal (Adresse)</label>
                 <textarea v-model="event.location" rows="2" placeholder="Ex: Château de la Verrière, 75001 Paris" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none transition-all"></textarea>
               </div>
             </div>
           </section>

           <section class="space-y-4">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Choix du Modèle</h3>
             <div class="grid grid-cols-2 gap-3">
               <button 
                 v-for="tpl in [
                   { id: 'modern-chic', name: 'Moderne Chic', color: '#1f2937' },
                   { id: 'romantic-pink', name: 'Rose Romantique', color: '#fbcfe8' },
                   { id: 'classic-elegance', name: 'Élégance Classique', color: '#fef3c7' },
                   { id: 'luxury-minimal', name: 'Luxe Minimaliste', color: '#000000' }
                 ]" 
                 :key="tpl.id"
                 @click="card.template_id = tpl.id"
                 :class="card?.template_id === tpl.id ? 'border-primary-600 ring-2 ring-primary-100' : 'border-gray-100 hover:border-primary-200'"
                 class="p-3 border rounded-2xl transition-all text-center bg-white shadow-sm group"
               >
                 <div :style="{ backgroundColor: tpl.color }" class="w-full h-12 rounded-xl mb-2 opacity-80 group-hover:opacity-100 transition-opacity"></div>
                 <span class="text-[10px] font-bold uppercase tracking-wider text-gray-700">{{ tpl.name }}</span>
               </button>
             </div>
           </section>

           <section class="space-y-4">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Image de Fond</h3>
             <div class="aspect-video bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center overflow-hidden relative group" :style="config.media.banner_url ? { backgroundImage: `url(${config.media.banner_url})`, backgroundSize: 'cover', backgroundPosition: 'center', border: 'none' } : {}">
               <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <button @click="$refs.fileInput.click()" class="bg-white text-gray-900 px-4 py-2 rounded-full text-xs font-bold shadow-xl">Changer</button>
               </div>
               <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="e => handleFileUpload(e, 'banner')">
             </div>
             <input v-model="config.media.banner_url" type="text" placeholder="URL..." class="w-full text-[11px] p-2 bg-gray-50 border-gray-100 rounded-lg focus:outline-none">
           </section>

           <section class="space-y-4 pt-4 border-t border-gray-100">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center">
               <svg class="w-3.5 h-3.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
               Programme de l'événement
             </h3>
             
             <div class="space-y-4">
               <div v-for="(item, idx) in config.itinerary" :key="idx" class="p-4 bg-gray-50 rounded-2xl border border-gray-100 space-y-3 relative group">
                 <button @click="removeItineraryItem(idx)" class="absolute top-2 right-2 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                   <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                 </button>

                 <div class="grid grid-cols-3 gap-2">
                   <input v-model="item.time" type="text" placeholder="14:30" class="col-span-1 bg-white border-gray-100 rounded-lg text-[11px] p-2 focus:ring-1 focus:ring-primary-500 outline-none">
                   <input v-model="item.title" type="text" placeholder="Titre (ex: Cérémonie)" class="col-span-2 bg-white border-gray-100 rounded-lg text-[11px] p-2 focus:ring-1 focus:ring-primary-500 outline-none">
                 </div>
                 <input v-model="item.location" type="text" placeholder="Adresse complète (pour Google Maps)" class="w-full bg-white border-gray-100 rounded-lg text-[11px] p-2 focus:ring-1 focus:ring-primary-500 outline-none">
                 <textarea v-model="item.description" rows="2" placeholder="Petite description..." class="w-full bg-white border-gray-100 rounded-lg text-[11px] p-2 focus:ring-1 focus:ring-primary-500 outline-none"></textarea>
               </div>

               <button @click="addItineraryItem" class="w-full py-3 bg-white border-2 border-dashed border-gray-200 rounded-xl text-[10px] font-bold uppercase tracking-widest text-gray-400 hover:border-primary-300 hover:text-primary-500 transition-all flex items-center justify-center">
                 <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                 Ajouter une étape au programme
               </button>
             </div>
           </section>

           <section class="space-y-4">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Style & Texte</h3>
             <div class="grid grid-cols-2 gap-4">
               <div class="bg-gray-50 p-2 rounded-xl border border-gray-100 flex items-center space-x-2">
                 <input type="color" v-model="config.colors.accent" class="h-6 w-6 rounded-md cursor-pointer">
                 <span class="text-xs font-mono">{{ config.colors.accent }}</span>
               </div>
               <select v-model="config.typography.headings" class="w-full bg-gray-50 border-gray-100 rounded-xl text-xs p-2 focus:outline-none">
                 <option value="serif">Serif</option>
                 <option value="cursive">Cursive</option>
                 <option value="sans-serif">Sans</option>
               </select>
             </div>
             <textarea v-model="config.content.intro_text" rows="6" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-4 focus:ring-2 focus:ring-primary-500 outline-none" placeholder="Message..."></textarea>
           </section>
        </div>

        <!-- Édition PAGES SUPPLÉMENTAIRES -->
        <div v-else-if="!isEditingCover && activePageIndex > 0" class="space-y-8 animate-in fade-in slide-in-from-right-2">
           <section class="space-y-4">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Image de la Page</h3>
             <div class="aspect-video bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center overflow-hidden relative group" :style="config.pages[activePageIndex - 1].banner_url ? { backgroundImage: `url(${config.pages[activePageIndex - 1].banner_url})`, backgroundSize: 'cover', backgroundPosition: 'center', border: 'none' } : {}">
               <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <button @click="$refs['fileInputPage' + (activePageIndex - 1)][0].click()" class="bg-white text-gray-900 px-4 py-2 rounded-full text-xs font-bold shadow-xl">Changer</button>
               </div>
               <input type="file" :ref="'fileInputPage' + (activePageIndex - 1)" class="hidden" accept="image/*" @change="e => handleFileUpload(e, 'page', activePageIndex - 1)">
             </div>
             <input v-model="config.pages[activePageIndex - 1].banner_url" type="text" placeholder="URL..." class="w-full text-[11px] p-2 bg-gray-50 border-gray-100 rounded-lg focus:outline-none">
           </section>

           <section class="space-y-4">
             <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest">Configuration</h3>
             <input v-model="config.pages[activePageIndex - 1].title" type="text" class="w-full bg-gray-50 border-gray-100 rounded-xl text-sm p-3 focus:ring-2 focus:ring-primary-500 outline-none" placeholder="Titre de la page" />
             <div v-for="section in config.pages[activePageIndex - 1].sections" :key="section.id">
               <textarea v-if="section.type === 'text'" v-model="section.content" rows="10" class="w-full bg-gray-50 border-gray-100 rounded-2xl text-sm p-4 focus:ring-2 focus:ring-primary-500 outline-none" placeholder="Contenu..."></textarea>
             </div>
             <button @click="removePage(activePageIndex - 1)" class="w-full py-2.5 text-red-500 text-xs font-bold border border-red-100 rounded-xl hover:bg-red-50">Supprimer la page</button>
           </section>
        </div>

        <!-- Footer Sidebar -->
        <section class="pt-6 border-t border-gray-100 space-y-3 pb-32">
          <div class="bg-gray-50 rounded-2xl p-4 border border-gray-100 space-y-3">
            <button @click="publish" :class="card?.is_published ? 'bg-white text-gray-700 border-gray-200' : 'bg-primary-600 text-white'" class="w-full py-2.5 rounded-xl text-sm font-semibold border shadow-sm transition-all">
              {{ card?.is_published ? 'Dépublier' : 'Publier' }}
            </button>
            
            <a v-if="card?.is_published && card?.slug" :href="'/cards/' + card.slug" target="_blank" class="block w-full py-2.5 rounded-xl text-sm font-semibold text-center bg-white border border-gray-200 text-primary-600 hover:bg-primary-50 transition-all shadow-sm">
              Voir l'invitation
            </a>
          </div>
        </section>
      </div>
    </aside>

    <!-- Aperçu Central -->
    <main class="flex-1 overflow-y-auto bg-gray-100 p-12 flex justify-center items-start custom-scrollbar relative">
      <!-- Bouton Retour Dashboard (Fixe à droite) -->
      <div class="fixed top-8 right-8 z-30">
        <button 
          @click="router.push('/dashboard')" 
          class="group flex items-center bg-white/90 backdrop-blur-md px-5 py-3 rounded-2xl border border-gray-200 shadow-xl shadow-black/5 text-gray-700 hover:text-primary-600 transition-all transform hover:-translate-x-1"
        >
          <div class="w-8 h-8 bg-primary-50 rounded-xl flex items-center justify-center mr-3 group-hover:bg-primary-100 transition-colors">
            <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          </div>
          <span class="text-xs font-bold uppercase tracking-widest">Tableau de bord</span>
        </button>
      </div>

      <div v-if="loading" class="flex flex-col items-center py-20">
        <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-primary-600 mb-4"></div>
        <span class="text-xs text-gray-400 uppercase font-medium">Chargement...</span>
      </div>
      <div v-else-if="event" class="w-full max-w-[500px] transform origin-top transition-all duration-500">
        <CardRenderer 
          :config="config" 
          :event="event" 
          :templateId="card?.template_id" 
          :activePageIndex="activePageIndex" 
          :forceSplash="isEditingCover"
          :isEditor="true"
          class="rounded-[40px] shadow-2xl overflow-hidden ring-1 ring-black/5" 
        />
      </div>
    </main>

    <!-- Modals (Versions, etc.) -->
    <div v-if="showVersionsModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-2xl font-serif text-gray-900">Versions</h2>
          <button @click="showVersionsModal = false" class="text-gray-400 text-2xl">&times;</button>
        </div>
        <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
           <div v-for="version in versions" :key="version.id" class="p-4 bg-gray-50 rounded-2xl border border-gray-100 flex justify-between items-center">
              <div>
                <p class="text-sm font-bold text-gray-900">V{{ version.version_number }}</p>
                <p class="text-[10px] text-gray-400">{{ new Date(version.created_at).toLocaleString() }}</p>
              </div>
              <button @click="rollback(version.version_number)" class="px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-xs font-bold text-primary-600 hover:bg-primary-50">Restaurer</button>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@reference "tailwindcss";
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 10px; }
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>