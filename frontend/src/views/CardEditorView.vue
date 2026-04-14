<script setup>
import { ref, onMounted, watch, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';

const route = useRoute();
const router = useRouter();
const cardId = route.params.id;

// UI States
const activeTab = ref('design'); 
const viewMode = ref('edit'); 
const zoomLevel = ref(0.75);
const card = ref(null);
const event = reactive({
  title: '', groom_name: '', bride_name: '', date: '', location: ''
});
const subEvents = ref([]);
const loading = ref(true);
const saving = ref(false);
const lastSaved = ref(null);

const config = reactive({
  canvas: { width: 1080, height: 1920, background_color: '#ffffff' },
  elements: [],
  music_url: '',
  show_countdown: true,
  theme: { primaryColor: '#000000', secondaryColor: '#ffffff', fontFamily: 'serif' }
});

const fetchCard = async () => {
  if (!cardId || cardId === 'undefined') {
    router.push('/dashboard');
    return;
  }
  try {
    loading.value = true;
    const response = await api.get(`/cards/${cardId}`);
    card.value = response.data;
    if (response.data.event) {
      Object.assign(event, response.data.event);
      if (event.date) event.date = new Date(event.date).toISOString().slice(0, 16);
    }
    if (card.value.config_json) {
      Object.assign(config, JSON.parse(card.value.config_json));
    }
    subEvents.value = card.value.sub_events || [];
  } catch (err) {
    router.push('/dashboard');
  } finally {
    loading.value = false;
  }
};

const saveCard = async (isAuto = true) => {
  if (saving.value) return;
  try {
    saving.value = true;
    const payload = {
      config_json: JSON.stringify(config),
      sub_events: subEvents.value,
      title: event.title,
      groom_name: event.groom_name,
      bride_name: event.bride_name,
      date: event.date ? new Date(event.date).toISOString() : null,
      location: event.location
    };
    await api.put(`/cards/${cardId}/save`, payload);
    lastSaved.value = new Date().toLocaleTimeString();
  } catch (err) {
    console.error(err);
  } finally {
    saving.value = false;
  }
};

let timeout = null;
watch([config, event, subEvents], () => {
  if (timeout) clearTimeout(timeout);
  timeout = setTimeout(() => saveCard(true), 2000);
}, { deep: true });

const publishCard = async () => {
  try {
    saving.value = true;
    const res = await api.post(`/cards/${cardId}/publish`);
    const publicUrl = `${window.location.origin}/cards/${res.data.slug}`;
    alert(`Félicitations ! Votre invitation est en ligne :\n${publicUrl}`);
    saveCard(false);
    fetchCard();
  } catch (err) {
    alert("Erreur lors de la publication.");
  } finally {
    saving.value = false;
  }
};

const handleFileUpload = async (e, type) => {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', type);
  try {
    saving.value = true;
    const res = await api.post(`/cards/${cardId}/upload`, formData);
    if (type === 'image') {
      let hero = config.elements.find(el => el.id === 'hero_image');
      if (hero) hero.content = res.data.url;
      else config.elements.push({ id: 'hero_image', type: 'image', x: 100, y: 100, width: 880, height: 1200, content: res.data.url, style: { objectFit: 'cover', borderRadius: '20px' } });
    } else if (type === 'music') config.music_url = res.data.url;
  } catch (err) {
    alert("Erreur upload.");
  } finally {
    saving.value = false;
  }
};

onMounted(fetchCard);
const fonts = ['Playfair Display', 'Cormorant Garamond', 'Montserrat', 'Inter', 'Great Vibes'];
</script>

<template>
  <div class="h-screen flex flex-col bg-[#F8F9FA] overflow-hidden font-sans text-slate-900">
    
    <!-- MAIN AREA -->
    <div class="flex-1 flex overflow-hidden relative">
      
      <!-- SIDEBAR -->
      <aside 
        class="w-full lg:w-[450px] bg-white border-r border-slate-200 flex flex-col shadow-sm z-20"
        :class="{'hidden lg:flex': viewMode === 'preview', 'flex': viewMode === 'edit'}"
      >
        <div class="p-4 lg:p-6 border-b border-slate-100 flex justify-between items-center">
          <h1 class="text-lg font-bold">Studio Design</h1>
          <button @click="router.push('/dashboard')" class="text-slate-400 hover:text-slate-600">
             <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          </button>
        </div>

        <nav class="flex border-b border-slate-100">
          <button v-for="t in [{id:'design', l:'Style'}, {id:'content', l:'Texte'}, {id:'program', l:'Prgm'}, {id:'media', l:'Média'}]"
            :key="t.id" @click="activeTab = t.id"
            :class="activeTab === t.id ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'"
            class="flex-1 py-4 text-[10px] font-black uppercase border-b-2 flex flex-col items-center"
          >
            <span>{{ t.l }}</span>
          </button>
        </nav>

        <div class="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
          <!-- DESIGN TAB -->
          <div v-if="activeTab === 'design'" class="space-y-6 animate-in">
             <section class="space-y-3">
                <label class="text-[10px] font-black uppercase text-slate-400">Modèle</label>
                <button @click="router.push({ path: '/templates', query: { eventId: event?.id || card?.event_id } })"
                  class="w-full bg-slate-50 p-4 rounded-xl text-xs font-bold border border-slate-100 hover:bg-slate-100 flex justify-between">
                  <span>Changer de modèle</span><span>→</span>
                </button>
             </section>
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase text-slate-400">Couleurs</label>
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Fond</span>
                    <input type="color" v-model="config.canvas.background_color" class="w-full h-10 rounded-lg cursor-pointer bg-slate-50 border-none p-1">
                  </div>
                  <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Texte</span>
                    <input type="color" v-model="config.theme.primaryColor" class="w-full h-10 rounded-lg cursor-pointer bg-slate-50 border-none p-1">
                  </div>
                </div>
             </section>
             <section class="space-y-3">
                <label class="text-[10px] font-black uppercase text-slate-400">Police</label>
                <select v-model="config.theme.fontFamily" class="w-full bg-slate-50 p-4 rounded-xl text-xs font-bold border border-slate-100">
                  <option v-for="f in fonts" :key="f" :value="f">{{ f }}</option>
                </select>
             </section>
             <section class="space-y-3">
                <label class="text-[10px] font-black uppercase text-slate-400">Options</label>
                <div class="flex items-center justify-between bg-slate-50 p-3 rounded-xl border border-slate-100">
                   <span class="text-xs font-bold text-slate-600">Compte à rebours</span>
                   <input type="checkbox" v-model="config.show_countdown" class="w-5 h-5 accent-indigo-600">
                </div>
             </section>
          </div>

          <!-- TEXTE TAB -->
          <div v-if="activeTab === 'content'" class="space-y-6 animate-in">
             <div class="space-y-4">
                <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Titre</span>
                  <input v-model="event.title" class="w-full bg-slate-50 p-3 rounded-xl text-sm font-medium border border-slate-100"></div>
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Lui</span><input v-model="event.groom_name" class="w-full bg-slate-50 p-3 rounded-xl text-sm border border-slate-100"></div>
                  <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Elle</span><input v-model="event.bride_name" class="w-full bg-slate-50 p-3 rounded-xl text-sm border border-slate-100"></div>
                </div>
                <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Date</span>
                  <input v-model="event.date" type="datetime-local" class="w-full bg-slate-50 p-3 rounded-xl text-sm border border-slate-100"></div>
                <div class="space-y-1"><span class="text-[9px] text-slate-400 uppercase font-bold">Lieu</span>
                  <textarea v-model="event.location" rows="3" class="w-full bg-slate-50 p-3 rounded-xl text-sm border border-slate-100"></textarea></div>
             </div>
          </div>

          <!-- PRGM TAB -->
          <div v-if="activeTab === 'program'" class="space-y-4 animate-in">
             <button @click="subEvents.push({title:'Nouvelle étape', time:'12:00', location: ''})" class="w-full py-3 border-2 border-dashed border-slate-200 rounded-xl text-[10px] font-bold uppercase text-slate-400 hover:border-indigo-300 hover:text-indigo-600 transition-all">+ Ajouter une étape</button>
             <div v-for="(se, idx) in subEvents" :key="idx" class="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-2 relative group">
                <button @click="subEvents.splice(idx,1)" class="absolute top-2 right-2 text-slate-300 hover:text-red-500">×</button>
                <input v-model="se.title" class="bg-transparent font-bold text-xs w-full outline-none" placeholder="Titre">
                <div class="flex space-x-2">
                  <input v-model="se.time" type="time" class="bg-white border border-slate-100 rounded p-1 text-[10px] w-20">
                  <input v-model="se.location" class="bg-white border border-slate-100 rounded p-1 text-[10px] flex-1" placeholder="Lieu">
                </div>
             </div>
          </div>

          <!-- MEDIA TAB -->
          <div v-if="activeTab === 'media'" class="space-y-6 animate-in">
             <div class="space-y-2">
                <label class="text-[10px] font-black uppercase text-slate-400">Photo de Couverture</label>
                <div class="border-2 border-dashed border-slate-200 rounded-xl p-6 text-center relative group">
                  <input type="file" @change="handleFileUpload($event, 'image')" class="absolute inset-0 opacity-0 cursor-pointer">
                  <span class="text-xs font-bold text-slate-400">Uploader une image</span>
                </div>
             </div>
             <div class="bg-indigo-50 p-4 rounded-xl">
                <p class="text-[10px] font-black uppercase text-indigo-900 mb-2">Musique de fond</p>
                <input type="file" @change="handleFileUpload($event, 'music')" class="text-[10px] text-indigo-600">
             </div>
          </div>
        </div>

        <div class="hidden lg:flex p-6 border-t border-slate-100 flex-col space-y-4 bg-white">
          <div v-if="card?.is_published" class="bg-green-50 p-3 rounded-lg border border-green-100">
             <p class="text-[9px] font-black uppercase text-green-600 mb-1">Invitation en ligne</p>
             <div class="flex items-center space-x-2">
                <input readonly :value="`${$viewport && window.location.origin}/cards/${card.slug}`" class="flex-1 bg-white border border-green-200 rounded px-2 py-1 text-[9px] font-mono text-green-700">
                <a :href="`/cards/${card.slug}`" target="_blank" class="text-[9px] font-black text-green-600 uppercase underline">Voir</a>
             </div>
          </div>
          <div class="flex items-center justify-between">
            <div class="text-[9px] font-bold uppercase text-slate-400 flex items-center">
              <div :class="saving ? 'bg-amber-400' : 'bg-green-500'" class="w-1.5 h-1.5 rounded-full mr-2"></div>
              {{ saving ? 'Sync...' : (lastSaved ? `Sauvé à ${lastSaved}` : 'Prêt') }}
            </div>
            <button @click="publishCard" class="px-5 py-2.5 bg-indigo-600 text-white text-[10px] font-black uppercase rounded-lg hover:bg-indigo-700 shadow-md">Publier l'invitation</button>
          </div>
        </div>
      </aside>

      <!-- PREVIEW AREA -->
      <main 
        class="flex-1 bg-slate-100 relative overflow-hidden flex flex-col"
        :class="{'hidden lg:flex': viewMode === 'edit', 'flex': viewMode === 'preview'}"
      >
        <!-- Preview Toolbar (Zoom & Status) -->
        <div class="bg-white/80 backdrop-blur border-b border-slate-200 px-6 py-3 flex items-center justify-between relative z-10">
          <div class="flex items-center space-x-4">
            <span class="text-[10px] font-black uppercase tracking-widest text-slate-400">Aperçu Mobile</span>
            <div class="flex items-center space-x-2 bg-slate-100 rounded-full px-3 py-1">
              <span class="text-[10px] text-slate-500">Zoom</span>
              <input type="range" v-model="zoomLevel" min="0.4" max="1.2" step="0.05" class="w-24 h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
              <span class="text-[10px] font-mono text-slate-500 w-8">{{ Math.round(zoomLevel * 100) }}%</span>
            </div>
          </div>
        </div>

        <!-- Preview Container -->
        <div class="flex-1 overflow-auto p-4 lg:p-12 flex items-start justify-center custom-scrollbar">
          <div 
            class="bg-white shadow-[0_30px_100px_-10px_rgba(0,0,0,0.2)] transition-transform duration-300 origin-top mb-20"
            :style="{ 
              width: '375px', 
              minHeight: '812px',
              transform: `scale(${zoomLevel})`,
              borderRadius: '32px',
              overflow: 'hidden',
              border: '8px solid #1e293b'
            }"
          >
            <!-- Notch -->
            <div class="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-slate-800 rounded-b-2xl z-50"></div>
            
            <div class="h-full overflow-y-auto hide-scrollbar">
              <CardRenderer 
                :config="config" 
                :event="event" 
                :sub-events="subEvents" 
              />
            </div>
          </div>
        </div>
      </main>

    </div>

    <!-- MOBILE NAV -->
    <div class="lg:hidden flex flex-col bg-white border-t border-slate-200 relative z-30">
      <div v-if="card?.is_published && viewMode === 'edit'" class="px-4 py-2 bg-green-50 border-b border-green-100 flex items-center justify-between">
         <span class="text-[9px] font-black text-green-600 uppercase truncate">En ligne : {{ card.slug }}</span>
         <a :href="`/cards/${card.slug}`" target="_blank" class="text-[9px] font-black text-green-600 uppercase underline">Voir</a>
      </div>
      <div class="flex h-20 items-center px-4">
        <button @click="viewMode = 'edit'" :class="viewMode === 'edit' ? 'text-indigo-600' : 'text-slate-400'" class="flex-1 flex flex-col items-center">
          <span class="text-[10px] font-bold uppercase mt-1">Modifier</span>
        </button>
        <div class="w-[1px] h-8 bg-slate-100"></div>
        <button @click="viewMode = 'preview'" :class="viewMode === 'preview' ? 'text-indigo-600' : 'text-slate-400'" class="flex-1 flex flex-col items-center">
          <span class="text-[10px] font-bold uppercase mt-1">Aperçu</span>
        </button>
        <div class="w-[1px] h-8 bg-slate-100"></div>
        <button @click="publishCard" class="flex-1 flex flex-col items-center text-green-600">
          <span class="text-[10px] font-bold uppercase mt-1">Publier</span>
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 10px; }
.hide-scrollbar::-webkit-scrollbar { display: none; }
.animate-in { animation: animate-in 0.4s cubic-bezier(0.19, 1, 0.22, 1); }
@keyframes animate-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 12px;
  width: 12px;
  border-radius: 50%;
  background: #4f46e5;
  cursor: pointer;
}
</style>
