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
const zoomLevel = ref(0.75);
const loading = ref(true);
const saving = ref(false);
const lastSaved = ref(null);

// Data
const card = ref(null);
const subEvents = ref([]);
const eventData = reactive({
  groom_name: '',
  bride_name: '',
  date: '',
  location: ''
});

const config = reactive({
  layout: 'arch',
  theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
  content: { names: '', date: '', location: '', message: 'Nous nous marions !', image_url: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200' },
  show_countdown: true,
  music_url: ''
});

const fonts = [
  { name: 'Playfair Display', label: 'Luxe (Serif)' },
  { name: 'Montserrat', label: 'Moderne (Sans)' },
  { name: 'Cormorant Garamond', label: 'Élégant (Serif)' },
  { name: 'Inter', label: 'Minimal (Sans)' }
];

const fetchCard = async () => {
  try {
    loading.value = true;
    const response = await api.get(`/cards/${cardId}`);
    card.value = response.data;
    
    if (card.value.event) {
      Object.assign(eventData, card.value.event);
      if (eventData.date) {
        eventData.date = new Date(eventData.date).toISOString().split('T')[0];
      }
    }
    
    if (card.value.config_json) {
      const parsedConfig = JSON.parse(card.value.config_json);
      Object.assign(config, parsedConfig);
    }
    subEvents.value = card.value.sub_events || [];
  } catch (err) {
    console.error("Erreur fetch card:", err);
    router.push('/dashboard');
  } finally {
    loading.value = false;
  }
};

const saveCard = async (redirect = false) => {
  if (saving.value && !redirect) return;
  try {
    saving.value = true;
    const payload = {
      config_json: JSON.stringify(config),
      sub_events: subEvents.value,
      groom_name: eventData.groom_name,
      bride_name: eventData.bride_name,
      date: eventData.date,
      location: eventData.location
    };
    await api.put(`/cards/${cardId}/save`, payload);
    lastSaved.value = new Date().toLocaleTimeString();
    if (redirect) {
      router.push('/dashboard');
    }
  } catch (err) {
    console.error("Erreur save:", err);
    alert("Erreur lors de la sauvegarde.");
  } finally {
    saving.value = false;
  }
};

// Auto-save debounced
let timeout = null;
watch([config, eventData, subEvents], () => {
  if (timeout) clearTimeout(timeout);
  timeout = setTimeout(() => saveCard(), 2000);
}, { deep: true });

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
      config.content.image_url = res.data.url;
    } else if (type === 'music') {
      config.music_url = res.data.url;
    }
    setTimeout(() => saveCard(), 500); // Sauvegarde forcée après upload
  } catch (err) {
    const errorMsg = err.response?.data?.detail || "Erreur lors de l'upload.";
    alert(errorMsg);
  } finally {
    saving.value = false;
  }
};

const addSubEvent = () => {
  subEvents.value.push({ title: 'Nouvelle étape', time: '12:00', location: 'Lieu de l\'étape' });
};

const removeSubEvent = (idx) => {
  subEvents.value.splice(idx, 1);
};

onMounted(fetchCard);
</script>

<template>
  <div class="h-screen flex flex-col bg-[#FDFCFB] overflow-hidden font-serif">
    
    <div class="flex-1 flex overflow-hidden">
      
      <!-- STUDIO SIDEBAR -->
      <aside class="w-[400px] bg-white border-r border-gray-100 flex flex-col shadow-2xl z-20">
        
        <div class="p-8 border-b border-gray-50 flex justify-between items-center">
          <div class="space-y-1">
            <h1 class="text-xl font-bold tracking-tight uppercase">Atelier Design</h1>
            <p class="text-[9px] uppercase tracking-widest text-[#C5A059]">Personnalisation Premium</p>
          </div>
          <button @click="router.push('/dashboard')" class="p-2 hover:bg-gray-50 rounded-full transition-colors">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          </button>
        </div>

        <nav class="flex px-4 pt-4 border-b border-gray-50">
          <button v-for="t in [{id:'design', l:'Visuel'}, {id:'content', l:'Textes'}, {id:'program', l:'Programme'}, {id:'media', l:'Médias'}]"
            :key="t.id" @click="activeTab = t.id"
            :class="activeTab === t.id ? 'text-[#C5A059] border-b-2 border-[#C5A059]' : 'text-gray-300'"
            class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest transition-all"
          >
            {{ t.l }}
          </button>
        </nav>

        <div class="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar">
          
          <div v-if="activeTab === 'design'" class="space-y-8 animate-in">
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Layout</label>
                <div class="grid grid-cols-3 gap-2">
                  <button v-for="l in ['arch', 'typography-focus', 'split']" :key="l"
                    @click="config.layout = l"
                    :class="config.layout === l ? 'bg-[#1A1A1A] text-white' : 'bg-gray-50 text-gray-400'"
                    class="py-2 text-[9px] uppercase tracking-widest rounded-lg transition-all"
                  >{{ l.split('-')[0] }}</button>
                </div>
             </section>

             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Typographie</label>
                <select v-model="config.theme.fontFamily" class="w-full p-4 bg-gray-50 border-none rounded-xl text-sm outline-none">
                  <option v-for="f in fonts" :key="f.name" :value="f.name">{{ f.label }}</option>
                </select>
             </section>

             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Options</label>
                <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100">
                   <span class="text-xs font-bold uppercase tracking-widest">Compte à rebours</span>
                   <div @click="config.show_countdown = !config.show_countdown" 
                        :class="config.show_countdown ? 'bg-[#C5A059]' : 'bg-gray-200'"
                        class="w-12 h-6 rounded-full relative cursor-pointer transition-colors"
                   >
                     <div :class="config.show_countdown ? 'translate-x-6' : 'translate-x-1'" 
                          class="absolute top-1 w-4 h-4 bg-white rounded-full transition-transform shadow-sm"
                     ></div>
                   </div>
                </div>
             </section>
          </div>

          <div v-if="activeTab === 'content'" class="space-y-8 animate-in">
             <div class="space-y-6">
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Lui</label>
                    <input v-model="eventData.groom_name" class="w-full p-4 bg-gray-50 border-none rounded-xl text-sm">
                  </div>
                  <div class="space-y-2">
                    <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Elle</label>
                    <input v-model="eventData.bride_name" class="w-full p-4 bg-gray-50 border-none rounded-xl text-sm">
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Le Jour J</label>
                  <input v-model="eventData.date" type="date" class="w-full p-4 bg-gray-50 border-none rounded-xl text-sm">
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Le Lieu</label>
                  <textarea v-model="eventData.location" rows="2" class="w-full p-4 bg-gray-50 border-none rounded-xl text-sm"></textarea>
                </div>
             </div>
          </div>

          <div v-if="activeTab === 'program'" class="space-y-6 animate-in">
             <button @click="addSubEvent" class="w-full py-4 border-2 border-dashed border-gray-100 rounded-xl text-[10px] font-black uppercase tracking-widest text-gray-400 hover:bg-gray-50 transition-all">+ Ajouter une étape</button>
             
             <div v-for="(se, idx) in subEvents" :key="idx" class="p-6 bg-gray-50 rounded-2xl space-y-4 relative group">
                <button @click="removeSubEvent(idx)" class="absolute top-4 right-4 text-gray-300 hover:text-red-500 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
                <div class="flex space-x-2">
                  <input v-model="se.time" type="time" class="bg-white p-2 rounded-lg text-[10px] border-none outline-none">
                  <input v-model="se.title" class="flex-1 bg-white p-2 rounded-lg text-[10px] font-bold border-none outline-none" placeholder="Titre">
                </div>
                <input v-model="se.location" class="w-full bg-white p-2 rounded-lg text-[10px] border-none outline-none" placeholder="Lieu">
             </div>
          </div>

          <div v-if="activeTab === 'media'" class="space-y-8 animate-in">
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Photo Principale</label>
                <div class="border-2 border-dashed border-gray-100 rounded-2xl p-10 text-center relative hover:bg-gray-50 transition-colors">
                  <input type="file" @change="e => handleFileUpload(e, 'image')" class="absolute inset-0 opacity-0 cursor-pointer">
                  <div class="space-y-2 pointer-events-none">
                    <span class="text-3xl block">🖼️</span>
                    <span class="text-[9px] font-black uppercase tracking-widest text-gray-400">Uploader votre photo</span>
                  </div>
                </div>
             </section>

             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Musique de fond (MP3)</label>
                <div class="p-6 bg-indigo-50/50 rounded-2xl border border-indigo-100 flex flex-col items-center space-y-4">
                  <div class="relative w-full">
                    <input type="file" @change="e => handleFileUpload(e, 'music')" class="w-full text-[9px] text-indigo-600">
                  </div>
                  <div v-if="config.music_url" class="flex items-center space-x-2">
                    <span class="text-[8px] text-green-600 uppercase font-black tracking-widest">✓ Musique chargée</span>
                    <button @click="config.music_url = ''" class="text-red-400 hover:text-red-600">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                  </div>
                </div>
             </section>
          </div>

        </div>

        <div class="p-8 border-t border-gray-50 bg-white shadow-inner">
          <div class="flex items-center justify-between mb-4">
            <span class="text-[9px] font-black uppercase tracking-widest" :class="saving ? 'text-amber-500' : 'text-green-500'">
              {{ saving ? 'Synchronisation...' : (lastSaved ? `Sauvegardé à ${lastSaved}` : 'Modifications prêtes') }}
            </span>
          </div>
          <button @click="saveCard(true)" class="w-full py-4 bg-[#1A1A1A] text-white text-[10px] font-black uppercase tracking-[0.3em] rounded-xl hover:bg-black transition-all shadow-xl">
            Terminer le Design
          </button>
        </div>
      </aside>

      <!-- PREVIEW CANVAS -->
      <main class="flex-1 bg-[#F9F7F2] relative overflow-hidden flex flex-col items-center justify-center p-12">
        <div class="absolute top-8 right-8 flex items-center space-x-2 bg-white/50 backdrop-blur-md rounded-full px-4 py-2 border border-white">
          <span class="text-[9px] font-black uppercase tracking-widest text-gray-400">Zoom</span>
          <input type="range" v-model="zoomLevel" min="0.4" max="1" step="0.05" class="w-24 accent-[#C5A059]">
        </div>

        <div class="bg-white shadow-[0_50px_100px_-20px_rgba(0,0,0,0.15)] transition-all duration-500 origin-center relative"
             :style="{ 
               width: '450px', 
               height: '800px',
               transform: `scale(${zoomLevel})`,
               borderRadius: '40px',
               border: '12px solid #1A1A1A',
               overflow: 'hidden'
             }"
        >
          <div class="h-full w-full overflow-y-auto overflow-x-hidden custom-scrollbar bg-white">
            <CardRenderer 
              :config="config" 
              :event="eventData"
              :sub-events="subEvents"
            />
          </div>
        </div>
      </main>

    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #F3F4F6; border-radius: 10px; }
.animate-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
