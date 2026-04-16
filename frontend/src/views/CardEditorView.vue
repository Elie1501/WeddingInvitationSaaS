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
const selectedBlock = ref(null); // Pour la mise en surbrillance
const tabs = [
  { id: 'design', label: 'Style' },
  { id: 'structure', label: 'Structure' },
  { id: 'content', label: 'Textes' },
  { id: 'program', label: 'Planning' },
  { id: 'media', label: 'Médias' }
];
const zoomLevel = ref(0.75);
const loading = ref(true);
const saving = ref(false);
const lastSaved = ref(null);

// Data
const card = ref(null);
const subEvents = ref([]);
const isPublished = ref(false);
const slug = ref('');
const eventData = reactive({ groom_name: '', bride_name: '', date: '', location: '' });

const config = reactive({
  layout: 'arch',
  sections: [],
  theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
  content: { 
    names: '', 
    show_petals: true,
    s1_label: 'Union Civile', s1_title: 'La Mairie', 
    s1_location: 'Hôtel de Ville, 75004 Paris',
    s2_label: 'Cérémonie Religieuse', s2_title: 'Houppa & Soirée',
    family_left: 'Famille du Marié', family_right: 'Famille de la Mariée',
    hebrew_names: '',
    announcement_text: 'Ont la joie de vous faire part du mariage de leurs enfants',
    intro_text_s2: 'Seront honorés de votre présence à la cérémonie religieuse...',
    tribute_title: 'Une pensée très émue pour nos disparus',
    tribute_text: '',
    gallery_label: 'Nos Souvenirs',
    footer_text: 'Fait avec amour • 2026'
  },
  show_countdown: true,
  music_url: ''
});

const moveSection = (index, direction) => {
  const newIndex = index + direction;
  if (newIndex < 0 || newIndex >= config.sections.length) return;
  const sections = [...config.sections];
  const [removed] = sections.splice(index, 1);
  sections.splice(newIndex, 0, removed);
  config.sections = sections;
};

const sectionLabels = {
  hero: 'Bannière Classique',
  'ora-hero': 'Bannière Ora (Pétales)',
  'ora-section1': 'Bloc Mairie (Ora)',
  'ora-parallax': 'Image Parallaxe',
  'ora-section2': 'Bloc Religieux (Ora)',
  'ora-tribute': 'Carte Hommage',
  'ora-gallery': 'Galerie Photos',
  'es-hero': 'Bannière ES (Luxe)',
  'es-intro': 'Introduction ES',
  'es-details': 'Détails ES',
  'es-footer': 'Pied de page ES',
  countdown: 'Compte à rebours',
  program: 'Programme',
  footer: 'Pied de page'
};

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
    isPublished.value = card.value.is_published;
    slug.value = card.value.slug;
    if (card.value.event) Object.assign(eventData, card.value.event);
    
    if (card.value.config_json) {
      const parsed = JSON.parse(card.value.config_json);
      // Initialisation de la structure si vide, dépendante du template
      if (!parsed.sections || parsed.sections.length === 0) {
          if (card.value.template_id === 'ora-parallax') {
            parsed.sections = ['ora-hero', 'ora-section1', 'ora-parallax', 'ora-section2', 'ora-tribute', 'ora-gallery', 'footer'];
            parsed.layout = 'ora';
          } else if (card.value.template_id === 'es-template') {
            parsed.sections = ['es-hero', 'es-intro', 'es-details', 'es-footer'];
            parsed.layout = 'es';
          } else {
            parsed.sections = ['hero', 'countdown', 'program', 'footer'];
          }
      }
      Object.assign(config, parsed);
    }
    subEvents.value = card.value.sub_events || [];
  } catch (err) { router.push('/dashboard'); } finally { loading.value = false; }
};

const saveCard = async (redirect = false) => {
  if (saving.value && !redirect) return;
  try {
    saving.value = true;
    const payload = {
      config_json: JSON.stringify(config),
      sub_events: subEvents.value,
      ...eventData
    };
    await api.put(`/cards/${cardId}/save`, payload);
    lastSaved.value = new Date().toLocaleTimeString();
    if (redirect) router.push('/dashboard');
  } finally { saving.value = false; }
};

const publishCard = async () => {
  try {
    saving.value = true;
    const response = await api.post(`/cards/${cardId}/publish`);
    isPublished.value = response.data.is_published;
    slug.value = response.data.slug;
  } finally { saving.value = false; }
};

let timeout = null;
watch([config, eventData, subEvents], () => {
  if (timeout) clearTimeout(timeout);
  timeout = setTimeout(() => saveCard(), 2000);
}, { deep: true });

const handleFileUpload = async (e, type, field = null) => {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', 'image');
  try {
    saving.value = true;
    const res = await api.post(`/cards/${cardId}/upload`, formData);
    if (field) config.content[field] = res.data.url;
    else if (type === 'image') config.content.image_url = res.data.url;
    else if (type === 'music') config.music_url = res.data.url;
    setTimeout(() => saveCard(), 500);
  } finally { saving.value = false; }
};

const handleBlockSelection = (sectionId) => {
  selectedBlock.value = sectionId;
  // Si le bloc a des réglages de texte, on va dans l'onglet contenu
  const contentBlocks = ['ora-section1', 'ora-section2', 'ora-tribute', 'hero', 'ora-hero'];
  if (contentBlocks.includes(sectionId)) {
    activeTab.value = 'content';
  } else if (sectionId === 'program') {
    activeTab.value = 'program';
  } else if (sectionId === 'countdown') {
    // Peut-être rester sur structure ou aller ailleurs
  }
};

onMounted(fetchCard);
</script>

<template>
  <div class="h-screen flex flex-col bg-[#FDFCFB] overflow-hidden font-serif">
    <div class="flex-1 flex overflow-hidden">
      <aside class="w-[400px] bg-white border-r border-gray-100 flex flex-col shadow-2xl z-20">
        <!-- TABS SANS EMOJI -->
        <nav class="flex px-2 pt-4 border-b border-gray-50 bg-gray-50/50">
          <button v-for="t in tabs" :key="t.id" @click="activeTab = t.id"
            :class="activeTab === t.id ? 'text-[#C5A059] border-b-2 border-[#C5A059] bg-white' : 'text-gray-400 hover:text-gray-600'"
            class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest transition-all"
          >
            {{ t.label }}
          </button>
        </nav>

        <div class="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar pb-32">
          
          <!-- DESIGN TAB -->
          <div v-if="activeTab === 'design'" class="space-y-8 animate-in">
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase text-gray-400">Style de l'en-tête</label>
                <div class="grid grid-cols-2 gap-2">
                  <button v-for="l in ['arch', 'typography-focus', 'split', 'ora', 'es']" :key="l"
                    @click="config.layout = l"
                    :class="config.layout === l ? 'bg-black text-white' : 'bg-gray-50 text-gray-400'"
                    class="py-2 text-[9px] uppercase rounded-lg transition-all"
                  >{{ l.toUpperCase() }}</button>
                </div>
             </section>
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase text-gray-400">Typographie</label>
                <select v-model="config.theme.fontFamily" class="w-full p-4 bg-gray-50 rounded-xl text-sm border-none outline-none">
                  <option v-for="f in fonts" :key="f.name" :value="f.name">{{ f.label }}</option>
                </select>
             </section>
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase text-gray-400">Couleur du texte</label>
                <input type="color" v-model="config.theme.accent" class="w-full h-12 rounded-xl cursor-pointer">
             </section>
          </div>

          <!-- STRUCTURE TAB -->
          <div v-if="activeTab === 'structure'" class="space-y-6 animate-in">
            <p class="text-[10px] text-gray-400 uppercase font-black mb-4">Ordre des blocs</p>
            <div class="space-y-3">
              <div v-for="(section, index) in config.sections" :key="index" 
                   @click="selectedBlock = section"
                   :class="selectedBlock === section ? 'border-[#C5A059] ring-1 ring-[#C5A059]' : 'border-gray-100'"
                   class="flex items-center justify-between p-4 bg-white border rounded-2xl shadow-sm transition-all cursor-pointer">
                <div class="flex items-center space-x-3">
                  <div class="w-6 h-6 rounded-full bg-gray-50 flex items-center justify-center text-[10px] font-bold text-gray-400">{{ index + 1 }}</div>
                  <span class="text-xs font-bold text-gray-700">{{ sectionLabels[section] || section }}</span>
                </div>
                <div class="flex space-x-1">
                  <button @click.stop="moveSection(index, -1)" :disabled="index === 0" class="p-1 text-[#C5A059] disabled:opacity-20">Haut</button>
                  <button @click.stop="moveSection(index, 1)" :disabled="index === config.sections.length - 1" class="p-1 text-[#C5A059] disabled:opacity-20">Bas</button>
                  <button @click.stop="config.sections.splice(index, 1)" class="p-1 text-red-300 hover:text-red-500">Suppr</button>
                </div>
              </div>
            </div>
            <div class="pt-6 border-t space-y-2">
               <p class="text-[9px] font-black uppercase text-gray-400 mb-3">Ajouter un bloc</p>
               <div class="grid grid-cols-1 gap-2">
                  <button v-for="(label, id) in sectionLabels" :key="id" 
                          v-show="!config.sections.includes(id) && 
                                 (id.startsWith('ora-') ? config.layout === 'ora' : 
                                  id.startsWith('es-') ? config.layout === 'es' : 
                                  !id.startsWith('ora-') && !id.startsWith('es-'))"
                          @click="config.sections.push(id)" 
                          class="text-left px-4 py-3 bg-gray-50 hover:bg-[#C5A059] hover:text-white rounded-xl text-[10px] font-bold uppercase transition-all">
                    + {{ label }}
                  </button>
               </div>
            </div>
          </div>

          <!-- CONTENT TAB (Dynamique selon la structure) -->
          <div v-if="activeTab === 'content'" class="space-y-8 animate-in pb-20">
             <section class="space-y-4">
                <label class="text-[10px] font-black uppercase text-gray-400">Identité</label>
                <div class="grid grid-cols-2 gap-3">
                  <input v-model="eventData.groom_name" placeholder="Lui" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
                  <input v-model="eventData.bride_name" placeholder="Elle" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
                </div>
                <input v-model="config.content.names" placeholder="Affichage (ex: O & S)" class="w-full p-3 bg-white border border-gray-200 rounded-lg text-xs italic">
             </section>

             <section v-if="config.sections.includes('es-intro')" class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-[#C5A059]">Introduction ES</label>
                <textarea v-model="config.content.intro_text" placeholder="Texte d'introduction" class="w-full p-3 bg-gray-50 rounded-lg text-xs h-24"></textarea>
             </section>

             <section v-if="config.sections.includes('es-footer')" class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-[#C5A059]">Pied de page ES</label>
                <input v-model="config.content.footer_text" placeholder="Texte de fin" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
             </section>

             <!-- CHAMPS CONDITIONNELS À LA STRUCTURE -->
             <section v-if="config.sections.includes('ora-section1')" class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-[#C5A059]">Union Civile</label>
                <input v-model="config.content.s1_title" placeholder="Titre (ex: La Mairie)" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
                <textarea v-model="config.content.s1_location" placeholder="Adresse" class="w-full p-3 bg-gray-50 rounded-lg text-xs h-20"></textarea>
             </section>

             <section v-if="config.sections.includes('ora-section2')" class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-[#C5A059]">Familles & Hébreu</label>
                <div class="grid grid-cols-2 gap-2">
                  <textarea v-model="config.content.family_left" placeholder="Famille NABET..." class="w-full p-2 bg-gray-50 rounded text-[9px] h-20"></textarea>
                  <textarea v-model="config.content.family_right" placeholder="Famille ATTARD..." class="w-full p-2 bg-gray-50 rounded text-[9px] h-20"></textarea>
                </div>
                <input v-model="config.content.hebrew_names" placeholder="Prénoms en Hébreu" class="w-full p-3 bg-gray-50 text-right text-sm">
             </section>

             <section v-if="config.sections.includes('ora-tribute')" class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-gray-400">Hommage</label>
                <input v-model="config.content.tribute_title" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
                <textarea v-model="config.content.tribute_text" placeholder="Noms des disparus..." class="w-full p-3 bg-gray-50 rounded-lg text-xs h-24"></textarea>
             </section>

             <section class="space-y-4 border-t pt-8">
                <label class="text-[10px] font-black uppercase text-gray-400">Date & Lieu Global</label>
                <input type="date" v-model="eventData.date" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
                <input v-model="eventData.location" placeholder="Lieu général" class="w-full p-3 bg-gray-50 rounded-lg text-xs">
             </section>
          </div>

          <!-- PLANNING -->
          <div v-if="activeTab === 'program' && config.sections.includes('program')" class="space-y-6 animate-in">
             <button @click="addSubEvent" class="w-full py-4 border-2 border-dashed border-gray-100 rounded-2xl text-[10px] font-black uppercase text-gray-400 hover:bg-gray-50">+ Ajouter une étape</button>
             <div v-for="(se, idx) in subEvents" :key="idx" class="p-6 bg-gray-50 rounded-3xl space-y-4 relative group">
                <button @click="removeSubEvent(idx)" class="absolute top-4 right-4 text-[9px] uppercase font-black text-gray-300 hover:text-red-500">Supprimer</button>
                <div class="flex space-x-2">
                  <input v-model="se.time" type="time" class="bg-white p-3 rounded-xl text-[10px] border-none outline-none shadow-sm">
                  <input v-model="se.title" class="flex-1 bg-white p-3 rounded-xl text-[10px] font-bold border-none outline-none shadow-sm" placeholder="Titre">
                </div>
                <input v-model="se.location" class="w-full bg-white p-3 rounded-xl text-[10px] border-none outline-none shadow-sm" placeholder="Lieu">
             </div>
          </div>

          <!-- MEDIAS -->
          <div v-if="activeTab === 'media'" class="space-y-8 animate-in">
             <section v-if="config.sections.includes('hero') || config.sections.includes('ora-hero')" class="space-y-4">
                <label class="text-[10px] font-black uppercase text-gray-400">Image Principale</label>
                <input type="file" @change="e => handleFileUpload(e, 'image')" class="text-[10px] w-full">
             </section>
             <section v-if="config.sections.includes('ora-parallax')" class="space-y-4 border-t pt-6">
                <label class="text-[10px] font-black uppercase text-gray-400">Image Parallaxe</label>
                <input type="file" @change="e => handleFileUpload(e, 'parallax', 'parallax_image_url')" class="text-[10px] w-full">
             </section>
             <section v-if="config.sections.includes('ora-gallery')" class="space-y-4 border-t pt-6">
                <label class="text-[10px] font-black uppercase text-gray-400">Galerie</label>
                <div class="grid grid-cols-1 gap-2">
                    <input v-for="i in [1,2,3]" :key="i" type="file" @change="e => handleFileUpload(e, 'gallery', `gal_img${i}`)" class="text-[8px]">
                </div>
             </section>
          </div>
        </div>

        <!-- FOOTER ACTIONS -->
        <div class="p-8 border-t border-gray-50 bg-white space-y-4 shadow-[0_-10px_20px_-5px_rgba(0,0,0,0.05)]">
          <div class="flex items-center justify-between">
            <span class="text-[9px] font-black uppercase" :class="saving ? 'text-amber-500' : 'text-green-500'">{{ saving ? 'Sync...' : 'Sauvegardé' }}</span>
            <span class="text-[9px] font-black uppercase text-gray-400">{{ isPublished ? 'En ligne' : 'Brouillon' }}</span>
          </div>
          <button @click="publishCard" :class="isPublished ? 'bg-white border-2 border-black text-black' : 'bg-black text-white'" class="w-full py-4 text-[10px] font-black uppercase rounded-2xl transition-all shadow-xl">
            {{ isPublished ? 'Dépublier' : 'Publier' }}
          </button>
        </div>
      </aside>

      <!-- APERÇU -->
      <main class="flex-1 bg-[#F9F7F2] relative flex flex-col items-center justify-center p-12">
        <div class="absolute top-8 right-8 bg-white/50 backdrop-blur-md rounded-full px-6 py-3 border border-white shadow-sm flex items-center space-x-3">
          <span class="text-[9px] font-black uppercase text-gray-400">Aperçu</span>
          <input type="range" v-model="zoomLevel" min="0.4" max="1" step="0.05" class="w-32 accent-black cursor-pointer">
        </div>
        <div class="bg-white shadow-[0_50px_100px_-20px_rgba(0,0,0,0.2)] transition-all duration-500 origin-center" :style="{ width: '450px', height: '800px', transform: `scale(${zoomLevel})`, borderRadius: '48px', border: '14px solid #1A1A1A', overflow: 'hidden' }">
          <div class="h-full overflow-y-auto custom-scrollbar bg-white">
            <CardRenderer :config="config" :event="eventData" :sub-events="subEvents" :selected-block="selectedBlock" @select-block="handleBlockSelection" />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style>
.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #E5E7EB; border-radius: 10px; }
.animate-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
</style>
