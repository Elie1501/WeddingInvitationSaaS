<script setup>
import { ref, reactive, watch, onMounted, onUnmounted, computed, provide, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';

const route = useRoute();
const router = useRouter();
const cardId = route.params.id;

// ==========================================
// 2. UI STATE
// ==========================================
const loading = ref(true);
const saving = ref(false);
const showSaveToast = ref(false);
const hasUnsavedChanges = ref(false);

const activeTab = ref('context');
const selectedBlock = ref(null);
const editingField = ref(null);
const quickUploadField = ref(null);
const quickUploadInput = ref(null);
const previewDevice = ref('mobile'); // 'mobile' | 'desktop'
const zoomLevel = ref(100);

const tabs = [
  { id: 'context', label: '✦ Sélection' },
  { id: 'design', label: 'Style' },
  { id: 'cover', label: 'Garde' },
  { id: 'structure', label: 'Blocs' },
  { id: 'content', label: 'Textes' },
  { id: 'media', label: 'Médias' }
];

provide('isEditorMode', true);
provide('editingField', editingField);
provide('triggerQuickUpload', (fieldPath) => {
  quickUploadField.value = fieldPath;
  quickUploadInput.value?.click();
});

const handleQuickUpload = async (event) => {
  if (!quickUploadField.value) return;
  await handleFileUpload(event, quickUploadField.value);
  quickUploadField.value = null;
};

// ==========================================
// 3. DATA STATE
// ==========================================
const config = reactive({
  layout: 'riviera-blanche',
  sections: [],
  theme: {
    background: '#FAFAF8', accent: '#2E6E8E', text: '#1C2B3A',
    titleColor: '#1C2B3A', namesColor: '#2E6E8E',
    fontFamily: 'Jost', fontSize: '1rem', titleSize: '4rem'
  },
  content: {
    names: 'Emma & Lucas', monogram: 'E & L', date_display: '15 Juin 2026', address: 'Villa Ephrussi, Cap Ferrat',
    intro_text: 'Nous serions honorés de votre présence pour célébrer notre union.', rsvp_title: 'Serez-vous des nôtres ?', rsvp_deadline_text: 'Réponse souhaitée avant le 1er Mai.',
    divider_symbol: '✦', footer_text: 'Fait avec amour • 2026',
    splash_title: 'Emma & Lucas', splash_top_text: 'Save the Date', splash_button_text: 'Entrer dans l\'invitation'
  },
  media: { image_url: '', music_url: '', splash_url: '' },
  show_countdown: true,
  show_splash: false,
  show_countdown_splash: true
});

const eventData = reactive({ date: '2026-06-15', location: 'Villa Ephrussi, Cap Ferrat' });
const subEvents = ref([]);

// ==========================================
// 4. HISTORIQUE UNDO / REDO
// ==========================================
const history = ref([]);
const historyIndex = ref(-1);
const isUndoRedo = ref(false);

const snapshot = () => JSON.parse(JSON.stringify(config));

let historyTimeout = null;
watch(config, () => {
  hasUnsavedChanges.value = true;
  if (isUndoRedo.value) return;
  
  if (historyTimeout) clearTimeout(historyTimeout);
  historyTimeout = setTimeout(() => {
    history.value = history.value.slice(0, historyIndex.value + 1);
    history.value.push(snapshot());
    if (history.value.length > 30) history.value.shift();
    historyIndex.value = history.value.length - 1;
  }, 500);
}, { deep: true });

const undo = () => {
  if (historyIndex.value <= 0) return;
  isUndoRedo.value = true;
  historyIndex.value--;
  Object.assign(config, history.value[historyIndex.value]);
  nextTick(() => { isUndoRedo.value = false; });
};

const redo = () => {
  if (historyIndex.value >= history.value.length - 1) return;
  isUndoRedo.value = true;
  historyIndex.value++;
  Object.assign(config, history.value[historyIndex.value]);
  nextTick(() => { isUndoRedo.value = false; });
};

// ==========================================
// 5. DRAG & DROP (Structure)
// ==========================================
const dragIndex = ref(null);
const dragOverIndex = ref(null);

const dragStart = (index) => { dragIndex.value = index; };
const dragOver = (index) => { dragOverIndex.value = index; };
const dragEnd = () => {
  if (dragIndex.value !== null && dragOverIndex.value !== null && dragIndex.value !== dragOverIndex.value) {
    const sections = [...config.sections];
    const [moved] = sections.splice(dragIndex.value, 1);
    sections.splice(dragOverIndex.value, 0, moved);
    config.sections = sections;
  }
  dragIndex.value = null;
  dragOverIndex.value = null;
};

// ==========================================
// 6. METHODES CRUD BLOCS
// ==========================================
const availableBlocks = [
  { id: 'countdown', label: 'Compte à rebours', icon: '⏱️', desc: 'Anime l\'attente jusqu\'au jour J' },
  { id: 'program', label: 'Programme', icon: '📅', desc: 'Détail des étapes de la journée' },
  { id: 'rsvp', label: 'Formulaire RSVP', icon: '📩', desc: 'Collectez les présences' },
  { id: 'footer', label: 'Pied de page', icon: '✨', desc: 'Message de fin et crédits' },
  { id: 'custom-text', label: 'Texte libre', icon: '📝', desc: 'Un bloc de texte personnalisé' }
];

const addBlock = (blockId) => {
  let finalId = blockId;
  
  // Éviter les doublons pour les blocs uniques
  if (['countdown', 'rsvp', 'footer', 'program'].includes(blockId)) {
    if (config.sections.includes(blockId)) {
      alert("Ce bloc est déjà présent sur votre invitation.");
      return;
    }
  }

  // Gérer les blocs de texte multiples
  if (blockId === 'custom-text') {
    const count = config.sections.filter(s => s.startsWith('custom-text-')).length;
    finalId = `custom-text-${Date.now()}`;
    config.content[finalId] = { title: 'Nouveau titre', content: 'Votre texte ici...' };
  }

  config.sections.push(finalId);
  activeTab.value = 'structure';
  selectedBlock.value = finalId;
  
  // Animation de scroll vers le nouveau bloc
  nextTick(() => {
    const el = document.querySelector(`[data-section-id="${finalId}"]`);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  });
};

const deleteBlock = (index) => {
  const sec = config.sections[index];
  if (sec.includes('hero') || sec.includes('full')) {
    alert("Le bloc principal ne peut pas être supprimé.");
    return;
  }
  config.sections.splice(index, 1);
  selectedBlock.value = null;
};

const getBlockLabel = (id) => {
  if (id.includes('hero') || id.includes('full')) return 'Bannière';
  const labels = {
    'countdown': 'Compte à rebours',
    'program': 'Programme',
    'rsvp': 'Formulaire RSVP',
    'footer': 'Pied de page',
    'gallery': 'Galerie Photo'
  };
  return labels[id] || 'Bloc personnalisé';
};

// ==========================================
// 7. EDITION INLINE
// ==========================================
const startInlineEdit = (fieldPath) => {
  editingField.value = fieldPath;
  const tabMap = {
    'names': 'content', 'intro_text': 'content', 'address': 'content',
    'date_display': 'content', 'rsvp_title': 'content', 'footer_text': 'content',
    'theme.accent': 'design', 'theme.background': 'design', 'theme.fontFamily': 'design'
  };
  if (tabMap[fieldPath]) activeTab.value = tabMap[fieldPath];
  
  nextTick(() => {
    const field = document.querySelector(`[data-field="${fieldPath}"]`);
    if (field) field.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
};

const commitInlineEdit = (fieldPath, event) => {
  const newValue = event.target.innerText.trim();
  if (fieldPath.includes('.')) {
    const [obj, key] = fieldPath.split('.');
    config[obj][key] = newValue;
  } else {
    config.content[fieldPath] = newValue;
  }
  editingField.value = null;
};

// Pour utilisation dans le template : <h1 @dblclick="startInlineEdit('names')" @blur="commitInlineEdit('names', $event)" ...>
provide('startInlineEdit', startInlineEdit);
provide('commitInlineEdit', commitInlineEdit);

// Résolution de chemin pour les champs du context
const resolveModel = (path) => {
  const parts = path.split('.');
  if (parts[0] === 'eventData') {
    return { get: () => eventData[parts[1]], set: (v) => eventData[parts[1]] = v };
  }
  return {
    get: () => parts.reduce((o, k) => o?.[k], config),
    set: (v) => {
      let target = config;
      for (let i = 0; i < parts.length - 1; i++) target = target[parts[i]];
      target[parts[parts.length - 1]] = v;
    }
  };
};

// ==========================================
// 8. SIDEBAR CONTEXTUELLE
// ==========================================
const contextFields = computed(() => {
  if (!selectedBlock.value) return null;
  const maps = {
    'hero': {
      label: 'Bannière principale',
      fields: [
        { type: 'text', label: 'Noms des mariés', model: 'content.names' },
        { type: 'text', label: 'Date affichée', model: 'content.date_display' },
        { type: 'text', label: 'Monogramme', model: 'content.monogram' },
        { type: 'text', label: 'Lieu', model: 'content.address' },
        { type: 'textarea', label: 'Texte d\'intro', model: 'content.intro_text' },
        { type: 'color', label: 'Couleur Noms', model: 'theme.namesColor' },
        { type: 'image', label: 'Image de fond', model: 'media.image_url' }
      ]
    },
    'splash': {
      label: 'Page de garde',
      fields: [
        { type: 'text', label: 'Titre principal', model: 'content.splash_title' },
        { type: 'text', label: 'Petit texte haut', model: 'content.splash_top_text' },
        { type: 'text', label: 'Sous-titre', model: 'content.splash_subtitle' },
        { type: 'text', label: 'Texte bouton', model: 'content.splash_button_text' },
        { type: 'toggle', label: 'Afficher le décompte', model: 'show_countdown_splash' },
        { type: 'image', label: 'Image de fond', model: 'media.splash_url' }
      ]
    },
    'rsvp': {
      label: 'Formulaire de confirmation',
      fields: [
        { type: 'text', label: 'Titre RSVP', model: 'content.rsvp_title' },
        { type: 'text', label: 'Date limite', model: 'content.rsvp_deadline_text' }
      ]
    },
    'countdown': {
      label: 'Compte à rebours',
      fields: [
        { type: 'toggle', label: 'Afficher le compte à rebours', model: 'show_countdown' }
      ]
    },
    'program': {
      label: 'Programme du mariage',
      isProgram: true
    },
    'footer': {
      label: 'Pied de page',
      fields: [
        { type: 'text', label: 'Texte de fin', model: 'content.footer_text' }
      ]
    }
  };

  if (selectedBlock.value.startsWith('custom-text-')) {
    return {
      label: 'Bloc texte personnalisé',
      fields: [
        { type: 'text', label: 'Titre du bloc', model: `content.${selectedBlock.value}.title` },
        { type: 'textarea', label: 'Contenu du texte', model: `content.${selectedBlock.value}.content` }
      ]
    };
  }

  if (selectedBlock.value.includes('-full') || selectedBlock.value.includes('-hero')) return maps['hero'];
  return maps[selectedBlock.value] || null;
});

const addProgramStep = () => {
  subEvents.value.push({ time: '00:00', title: 'Nouvel événement', location: '', description: '' });
};

const removeProgramStep = (index) => {
  subEvents.value.splice(index, 1);
};

// Auto-switch vers 'context' quand on sélectionne un bloc
watch(selectedBlock, (newVal) => {
  if (newVal && contextFields.value) activeTab.value = 'context';
});

// ==========================================
// 9. API & PERSISTENCE
// ==========================================
let saveTimeout = null;
watch([config, subEvents], () => {
  if (saveTimeout) clearTimeout(saveTimeout);
  saveTimeout = setTimeout(saveCard, 2000);
}, { deep: true });

const fetchCard = async () => {
  try {
    loading.value = true;
    const response = await api.get(`/cards/${cardId}`);
    if (response.data.config_json) {
      const parsed = typeof response.data.config_json === 'string' ? JSON.parse(response.data.config_json) : response.data.config_json;
      Object.assign(config, parsed);
      
      // Initialiser l'historique
      history.value = [snapshot()];
      historyIndex.value = 0;
    }
    if (response.data.event) {
      eventData.date = response.data.event.date?.split('T')[0] || '';
      eventData.location = response.data.event.location || '';
      
      // Charger les sous-événements réels depuis l'API
      if (response.data.sub_events) {
        subEvents.value = response.data.sub_events.map(se => ({
          time: se.time,
          title: se.title,
          location: se.location,
          description: se.description
        }));
      }
    }
  } catch (err) {
    console.error("Fetch Error:", err);
  } finally {
    loading.value = false;
  }
};

const saveCard = async () => {
  try {
    saving.value = true;
    const payload = { 
      config_json: JSON.stringify(config), 
      sub_events: subEvents.value,
      ...eventData 
    };
    await api.put(`/cards/${cardId}/save`, payload);
    
    saving.value = false;
    hasUnsavedChanges.value = false;
    showSaveToast.value = true;
    setTimeout(() => showSaveToast.value = false, 2000);
  } catch (err) {
    console.error("Save Error:", err);
    saving.value = false;
  }
};

const handleFileUpload = async (event, fieldPath) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', 'image');

    const response = await api.post(`/cards/${cardId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    const url = response.data.url;
    // Mise à jour du modèle
    const model = resolveModel(fieldPath);
    model.set(url);
    
    // Forcer la sauvegarde
    saveCard();
  } catch (err) {
    console.error("Upload Error:", err);
    alert("Erreur lors de l'envoi de l'image.");
  }
};

// ==========================================
// 10. WATCHERS & FONTS
// ==========================================
const loadedFonts = new Set();
const loadGoogleFont = (fontName) => {
  if (!fontName || loadedFonts.has(fontName)) return;
  const formatted = fontName.replace(/ /g, '+');
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `https://fonts.googleapis.com/css2?family=${formatted}:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&display=swap`;
  document.head.appendChild(link);
  loadedFonts.add(fontName);
};

watch(() => config.theme.fontFamily, (newFont) => { loadGoogleFont(newFont); }, { immediate: true });

// ==========================================
// 11. LIFECYCLE
// ==========================================
const handleKeyboard = (e) => {
  const isMac = navigator.platform.includes('Mac');
  const ctrlOrCmd = isMac ? e.metaKey : e.ctrlKey;
  if (ctrlOrCmd && e.key === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
  if (ctrlOrCmd && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) { e.preventDefault(); redo(); }
};

onMounted(() => {
  fetchCard();
  document.addEventListener('keydown', handleKeyboard);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboard);
  if (saveTimeout) clearTimeout(saveTimeout);
});
</script>

<template>
  <div v-if="!loading" class="flex h-screen bg-[#F3F4F6] font-sans overflow-hidden">
    
    <!-- BARRE DE PROGRESSION AUTO-SAVE -->
    <div class="fixed top-0 left-0 right-0 h-[2px] z-50 bg-transparent">
      <div class="h-full bg-[#C5A059] transition-all duration-100"
           :style="{ width: saving ? '100%' : hasUnsavedChanges ? '60%' : '0%',
                     opacity: saving || hasUnsavedChanges ? 1 : 0,
                     transition: saving ? 'width 2s linear' : 'width 0.3s ease, opacity 0.3s ease' }">
      </div>
    </div>

    <!-- TOAST DE SAUVEGARDE -->
    <Transition name="toast">
      <div v-if="showSaveToast"
           class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 bg-[#1A1A1A] text-white px-6 py-3 rounded-full flex items-center space-x-3 shadow-2xl shadow-black/30">
        <div class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
        <span class="text-[10px] font-black uppercase tracking-widest">Invitation sauvegardée</span>
      </div>
    </Transition>

    <!-- SIDEBAR GAUCHE -->
    <aside class="w-[400px] flex flex-col bg-white border-r border-gray-200 shadow-xl z-30">
      
      <!-- HEADER TOOLBAR -->
      <div class="flex items-center justify-between p-4 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          <button @click="router.push('/templates')" class="p-2 -ml-2 rounded-lg hover:bg-gray-100 transition-all text-gray-400 hover:text-[#C5A059]" title="Retour aux modèles">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
          </button>
          <h1 class="text-xs font-black uppercase tracking-widest text-gray-800">Studio</h1>
        </div>
        
        <!-- Undo / Redo -->
        <div class="flex items-center space-x-1">
          <button @click="undo" :disabled="historyIndex <= 0" class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-20 transition-all" title="Annuler (Ctrl+Z)">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 10h10a5 5 0 010 10H9" stroke-linecap="round"/><path d="M3 10l4-4M3 10l4 4" stroke-linecap="round"/></svg>
          </button>
          <button @click="redo" :disabled="historyIndex >= history.length - 1" class="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-20 transition-all" title="Rétablir (Ctrl+Y)">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10H11a5 5 0 000 10h4" stroke-linecap="round"/><path d="M21 10l-4-4M21 10l-4 4" stroke-linecap="round"/></svg>
          </button>
          <span class="text-[8px] text-gray-400 font-mono pl-2">{{ historyIndex + 1 }}/{{ history.length }}</span>
        </div>
      </div>

      <!-- ONGLETS -->
      <div class="flex overflow-x-auto custom-scrollbar border-b border-gray-100 bg-gray-50/50">
        <button v-for="tab in tabs" :key="tab.id"
                @click="activeTab = tab.id"
                class="px-4 py-3 text-[10px] font-bold uppercase tracking-wider whitespace-nowrap transition-colors border-b-2"
                :class="activeTab === tab.id ? 'border-[#C5A059] text-[#1A1A1A] bg-white' : 'border-transparent text-gray-400 hover:text-gray-600'">
          {{ tab.label }}
        </button>
      </div>

      <!-- CONTENU DES ONGLETS -->
      <div class="flex-1 overflow-y-auto p-6 custom-scrollbar bg-[#FAFAFA]">
        
        <!-- ONGLET : CONTEXTE -->
        <div v-if="activeTab === 'context'" class="animate-in space-y-6">
          <div v-if="!selectedBlock || !contextFields" class="py-20 text-center space-y-4">
            <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto">
              <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
            </div>
            <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest">
              Cliquez sur un bloc<br>dans l'aperçu à droite
            </p>
          </div>

          <template v-else>
            <div class="flex items-center space-x-3 pb-4 border-b border-gray-200">
              <div class="w-2 h-8 rounded-full" :style="{ backgroundColor: config.theme.accent }"></div>
              <div>
                <p class="text-[9px] font-black uppercase text-gray-400 tracking-widest">Bloc sélectionné</p>
                <p class="text-sm font-bold text-gray-900">{{ contextFields.label }}</p>
              </div>
            </div>

            <!-- Cas particulier : Programme -->
            <div v-if="contextFields.isProgram" class="space-y-6">
               <div v-for="(step, idx) in subEvents" :key="idx" class="p-4 bg-white border border-gray-100 rounded-2xl space-y-3 relative group">
                  <button @click="removeProgramStep(idx)" class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center shadow-lg">×</button>
                  <div class="flex gap-2">
                    <input v-model="step.time" type="time" class="w-24 p-2 bg-gray-50 rounded-lg text-xs outline-none focus:ring-1 focus:ring-[#C5A059]">
                    <input v-model="step.title" type="text" placeholder="Titre de l'étape" class="flex-1 p-2 bg-gray-50 rounded-lg text-xs outline-none focus:ring-1 focus:ring-[#C5A059]">
                  </div>
                  <input v-model="step.location" type="text" placeholder="Lieu" class="w-full p-2 bg-gray-50 rounded-lg text-[10px] outline-none focus:ring-1 focus:ring-[#C5A059]">
                  <textarea v-model="step.description" placeholder="Description courte" class="w-full p-2 bg-gray-50 rounded-lg text-[10px] outline-none focus:ring-1 focus:ring-[#C5A059] h-16 resize-none"></textarea>
               </div>
               <button @click="addProgramStep" class="w-full py-3 border-2 border-dashed border-gray-200 rounded-2xl text-[10px] font-bold uppercase text-gray-400 hover:border-[#C5A059] hover:text-[#C5A059] transition-all">
                 + Ajouter une étape
               </button>
            </div>

            <!-- Rendu générique des champs -->
            <div v-else class="space-y-4">
              <div v-for="field in contextFields.fields" :key="field.model" class="space-y-1">
                <label class="text-[10px] font-bold uppercase text-gray-500 tracking-wider" :data-field="field.model">{{ field.label }}</label>
                
                <input v-if="field.type === 'text'" :value="resolveModel(field.model).get()" @input="resolveModel(field.model).set($event.target.value)"
                       class="w-full p-3 bg-white border border-gray-200 rounded-xl text-xs focus:border-[#C5A059] focus:ring-2 focus:ring-[#C5A059]/20 outline-none transition-all">
                
                <textarea v-else-if="field.type === 'textarea'" :value="resolveModel(field.model).get()" @input="resolveModel(field.model).set($event.target.value)"
                          class="w-full p-3 bg-white border border-gray-200 rounded-xl text-xs h-32 resize-none focus:border-[#C5A059] outline-none transition-all"></textarea>
                
                <div v-else-if="field.type === 'color'" class="flex items-center bg-white border border-gray-200 rounded-xl p-1 pr-3">
                  <input type="color" :value="resolveModel(field.model).get()" @input="resolveModel(field.model).set($event.target.value)"
                         class="w-10 h-10 border-0 p-0 bg-transparent cursor-pointer rounded-lg">
                  <span class="ml-3 text-xs font-mono text-gray-500 uppercase">{{ resolveModel(field.model).get() }}</span>
                </div>

                <label v-else-if="field.type === 'toggle'" class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-xl cursor-pointer">
                  <span class="text-xs font-bold text-gray-700">{{ resolveModel(field.model).get() ? 'Affiché' : 'Masqué' }}</span>
                  <input type="checkbox" :checked="resolveModel(field.model).get()" @change="resolveModel(field.model).set($event.target.checked)"
                         class="w-5 h-5 accent-[#C5A059] rounded">
                </label>

                <div v-else-if="field.type === 'image'" class="space-y-2">
                  <div class="flex gap-2">
                    <input type="text" :value="resolveModel(field.model).get()" @input="resolveModel(field.model).set($event.target.value)"
                           placeholder="URL de l'image..."
                           class="flex-1 p-3 bg-white border border-gray-200 rounded-xl text-xs focus:border-[#C5A059] outline-none transition-all">
                    <label class="p-3 bg-gray-100 hover:bg-gray-200 rounded-xl cursor-pointer transition-colors flex items-center justify-center aspect-square">
                      <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                      <input type="file" class="hidden" accept="image/*" @change="handleFileUpload($event, field.model)">
                    </label>
                  </div>
                  <div v-if="resolveModel(field.model).get()" class="aspect-video rounded-xl overflow-hidden border border-gray-100 bg-gray-50">
                    <img :src="resolveModel(field.model).get()" class="w-full h-full object-cover">
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-6 mt-6 border-t border-gray-200">
              <button v-if="!selectedBlock.includes('full') && !selectedBlock.includes('hero')" 
                      @click="deleteBlock(config.sections.indexOf(selectedBlock))"
                      class="w-full py-3 text-[10px] font-black uppercase text-red-500 bg-red-50 hover:bg-red-100 rounded-xl transition-colors tracking-widest">
                Supprimer ce bloc
              </button>
            </div>
          </template>
        </div>

        <!-- ONGLET : GARDE -->
        <div v-if="activeTab === 'cover'" class="animate-in space-y-6">
          <div class="bg-white border border-gray-200 rounded-2xl p-6 space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-xs font-black text-gray-800 uppercase tracking-widest">Page de garde</h3>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="config.show_splash" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C5A059]"></div>
              </label>
            </div>
            
            <p class="text-[10px] text-gray-400 italic leading-relaxed">
              La page de garde est la première chose que vos invités verront. Elle permet d'introduire l'invitation avec élégance.
            </p>

            <div v-if="config.show_splash" class="space-y-4 animate-in">
              <button @click="selectedBlock = 'splash'" 
                      class="w-full py-3 bg-gray-50 border border-gray-100 rounded-xl text-[10px] font-black uppercase tracking-widest hover:border-[#C5A059] transition-all">
                Configurer les textes
              </button>
              
              <div class="space-y-2">
                <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Image de fond (Splash)</label>
                <div class="flex gap-2">
                  <input type="text" v-model="config.media.splash_url" placeholder="URL de l'image..." class="flex-1 p-3 bg-gray-50 border border-transparent rounded-xl text-xs focus:border-[#C5A059] outline-none">
                  <label class="p-3 bg-gray-100 hover:bg-gray-200 rounded-xl cursor-pointer transition-colors flex items-center justify-center aspect-square">
                    <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                    <input type="file" class="hidden" accept="image/*" @change="handleFileUpload($event, 'media.splash_url')">
                  </label>
                </div>
              </div>

              <label class="flex items-center justify-between p-3 bg-gray-50 rounded-xl cursor-pointer">
                <span class="text-xs font-bold text-gray-700">Décompte sur la garde</span>
                <input type="checkbox" v-model="config.show_countdown_splash" class="w-5 h-5 accent-[#C5A059] rounded">
              </label>
            </div>
          </div>
        </div>

        <!-- ONGLET : DESIGN -->
        <div v-if="activeTab === 'design'" class="animate-in space-y-8">
          
          <div class="space-y-4">
            <h3 class="flex items-center text-xs font-black text-gray-800 uppercase tracking-widest">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.172-1.172a4 4 0 115.656 5.656L15 13"></path></svg>
              Palette de couleurs
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="(label, key) in { background: 'Fond', text: 'Texte', titleColor: 'Titres', namesColor: 'Prénoms', accent: 'Accentuation' }" :key="key"
                   class="bg-white border border-gray-200 p-2 rounded-xl flex items-center">
                <input type="color" v-model="config.theme[key]" class="w-8 h-8 rounded-lg cursor-pointer border-0 p-0 bg-transparent">
                <span class="ml-2 text-[10px] font-bold uppercase text-gray-500">{{ label }}</span>
              </div>
            </div>
          </div>

          <div class="space-y-4 pt-6 border-t border-gray-200">
            <h3 class="flex items-center text-xs font-black text-gray-800 uppercase tracking-widest">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 5v12m0 0H7m2 0h2M3 20h12M21 12h-6"></path></svg>
              Typographie
            </h3>
            <div class="bg-white border border-gray-200 p-4 rounded-xl space-y-4">
              <select v-model="config.theme.fontFamily" class="w-full bg-gray-50 border border-gray-100 rounded-lg p-2 text-xs font-bold text-gray-800 outline-none">
                <option value="Playfair Display">Playfair Display</option>
                <option value="Cormorant Garamond">Cormorant Garamond</option>
                <option value="Jost">Jost</option>
                <option value="Lato">Lato</option>
                <option value="Cinzel">Cinzel</option>
                <option value="Spectral">Spectral</option>
                <option value="Anton">Anton</option>
              </select>
              
              <div class="space-y-1">
                <div class="flex justify-between"><span class="text-[10px] font-bold uppercase text-gray-500">Taille Titres</span><span class="text-xs font-mono">{{ config.theme.titleSize }}</span></div>
                <input type="range" v-model="config.theme.titleSize" min="2" max="10" step="0.5" class="w-full accent-[#1A1A1A]">
              </div>
            </div>
          </div>
        </div>

        <!-- ONGLET : STRUCTURE (Drag & Drop + Ajout) -->
        <div v-if="activeTab === 'structure'" class="animate-in space-y-8">
          
          <section class="space-y-4">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest text-center">Structure actuelle</p>
            <div class="space-y-2">
              <div v-for="(section, index) in config.sections" :key="section"
                   draggable="true" @dragstart="dragStart(index)" @dragover.prevent="dragOver(index)" @dragend="dragEnd"
                   class="flex items-center justify-between p-4 bg-white border rounded-xl shadow-sm transition-all cursor-grab active:cursor-grabbing"
                   :class="[dragOverIndex === index ? 'border-[#C5A059] bg-amber-50 scale-[1.02]' : 'border-gray-200', selectedBlock === section ? 'ring-2 ring-[#C5A059] border-transparent' : '']"
                   @click="selectedBlock = section">
                <div class="flex items-center">
                  <div class="mr-3 text-gray-300 hover:text-gray-500">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><circle cx="9" cy="6" r="1.5"/><circle cx="15" cy="6" r="1.5"/><circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/><circle cx="9" cy="18" r="1.5"/><circle cx="15" cy="18" r="1.5"/></svg>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-gray-800 uppercase tracking-wide">{{ getBlockLabel(section) }}</p>
                    <p class="text-[9px] font-mono text-gray-400 mt-0.5">id: {{ section }}</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="pt-8 border-t border-gray-200">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest text-center mb-6">Ajouter une section</p>
            <div class="grid grid-cols-2 gap-3">
               <button v-for="block in availableBlocks" :key="block.id"
                       @click="addBlock(block.id)"
                       class="p-4 bg-white border border-gray-100 rounded-2xl hover:border-[#C5A059] hover:shadow-md transition-all text-center group">
                  <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">{{ block.icon }}</div>
                  <p class="text-[10px] font-bold text-gray-800 uppercase leading-tight">{{ block.label }}</p>
               </button>
            </div>
          </section>
        </div>

        <!-- ONGLET : CONTENU (Legacy, on redirige vers Context si possible, mais utile pour vue globale) -->
        <div v-if="activeTab === 'content'" class="animate-in space-y-6">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-6">Paramètres globaux</p>
            <div class="space-y-4">
                <div class="space-y-1">
                    <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider" data-field="names">Noms des mariés</label>
                    <input type="text" v-model="config.content.names" class="w-full p-3 bg-white border border-gray-200 rounded-xl text-xs focus:border-[#C5A059] outline-none">
                </div>
                <div class="space-y-1">
                    <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider" data-field="date_display">Date affichée</label>
                    <input type="text" v-model="config.content.date_display" class="w-full p-3 bg-white border border-gray-200 rounded-xl text-xs focus:border-[#C5A059] outline-none">
                </div>
                 <div class="space-y-1">
                    <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider" data-field="address">Lieu / Adresse</label>
                    <input type="text" v-model="config.content.address" class="w-full p-3 bg-white border border-gray-200 rounded-xl text-xs focus:border-[#C5A059] outline-none">
                </div>
            </div>
        </div>

        <!-- ONGLET : MEDIA -->
        <div v-if="activeTab === 'media'" class="animate-in space-y-6">
           <div class="bg-white border border-gray-200 rounded-xl p-4 space-y-4">
              <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Image de couverture (URL)</label>
              <input type="text" v-model="config.media.image_url" placeholder="https://..." class="w-full p-3 bg-gray-50 border border-transparent rounded-xl text-xs focus:border-[#C5A059] outline-none">
              <div v-if="config.media.image_url" class="aspect-[4/3] rounded-lg overflow-hidden border border-gray-200 bg-gray-100">
                  <img :src="config.media.image_url" class="w-full h-full object-cover">
              </div>
           </div>
        </div>

      </div>

      <!-- FOOTER SIDEBAR -->
      <div class="p-6 bg-white border-t border-gray-200 flex space-x-3">
        <button @click="router.push('/dashboard')" class="px-6 py-3 bg-gray-100 text-gray-600 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-gray-200 transition-colors">
          Quitter
        </button>
        <button @click="saveCard" class="flex-1 py-3 bg-[#1A1A1A] text-white rounded-xl text-[10px] font-black uppercase tracking-[0.2em] shadow-lg hover:bg-black transition-transform active:scale-[0.98]">
          Publier
        </button>
      </div>
    </aside>

    <!-- ZONE PREVIEW -->
    <main class="flex-1 relative flex flex-col items-center justify-center p-8 bg-[#F3F4F6]">
      
      <!-- Toolbar flottante Preview -->
      <div class="absolute top-6 flex items-center space-x-2 bg-white/90 backdrop-blur-md px-4 py-2 rounded-full border border-gray-200 shadow-sm z-20">
        <button @click="previewDevice = 'mobile'" :class="previewDevice === 'mobile' ? 'text-black' : 'text-gray-400'" class="p-1 hover:text-black transition-colors" title="Vue Mobile">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2" ry="2" stroke-width="2"/><path d="M12 18h.01" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
        <button @click="previewDevice = 'desktop'" :class="previewDevice === 'desktop' ? 'text-black' : 'text-gray-400'" class="p-1 hover:text-black transition-colors" title="Vue Ordinateur">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke-width="2"/><path d="M8 21h8M12 17v4" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
        <div class="w-[1px] h-4 bg-gray-300 mx-2"></div>
        <button @click="zoomLevel = Math.max(50, zoomLevel - 10)" class="p-1 text-gray-400 hover:text-black">-</button>
        <span class="text-[10px] font-mono font-bold w-10 text-center">{{ zoomLevel }}%</span>
        <button @click="zoomLevel = Math.min(150, zoomLevel + 10)" class="p-1 text-gray-400 hover:text-black">+</button>
      </div>

      <!-- Container Rendu -->
      <div class="transition-all duration-500 ease-out origin-top flex items-center justify-center h-full w-full"
           :style="{ transform: `scale(${zoomLevel / 100})` }">
        
        <div :class="previewDevice === 'mobile' ? 'w-[400px] h-[850px] rounded-[3rem] ring-[12px] ring-gray-900 shadow-2xl' : 'w-full max-w-5xl h-[800px] rounded-xl shadow-2xl'"
             class="bg-white overflow-hidden relative flex flex-col transition-all duration-500 border border-gray-200">
          
          <div v-if="previewDevice === 'mobile'" class="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-gray-900 rounded-b-2xl z-50"></div>
          
          <div class="flex-1 overflow-y-auto overflow-x-hidden custom-scrollbar bg-white" @click.self="selectedBlock = null">
            <!-- INJECTION DU MOTEUR DE RENDU -->
            <CardRenderer :config="config" :event="eventData" :subEvents="subEvents" :selectedBlock="selectedBlock" @select-block="selectedBlock = $event" />
          </div>
        </div>
      </div>
      
    </main>
  </div>
  
  <div v-else class="h-screen flex items-center justify-center bg-[#F9F7F2]">
     <div class="text-center space-y-6">
        <div class="w-12 h-1 bg-gray-200 mx-auto overflow-hidden"><div class="w-full h-full bg-[#C5A059] animate-pulse"></div></div>
        <p class="text-[10px] font-black uppercase tracking-[0.3em] text-[#C5A059]">Ouverture du Studio</p>
     </div>
  </div>

  <!-- INPUT CACHÉ POUR LES TÉLÉCHARGEMENTS RAPIDES (CLIC SUR IMAGE) -->
  <input ref="quickUploadInput" type="file" class="hidden" accept="image/*" @change="handleQuickUpload">
</template>

<style>
/* Utilities animations */
.animate-in { animation: fadeSlide 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes fadeSlide { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

/* Scrollbars */
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #E5E7EB; border-radius: 4px; }

/* Transitions Toast */
.toast-enter-active, .toast-leave-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translate(-50%, 20px) scale(0.95); }

/* --- CSS INJECTÉ POUR L'ÉDITION INLINE DANS LE PREVIEW --- */
.editable-element {
  cursor: default;
  border-radius: 4px;
  transition: outline 0.15s ease, background 0.15s ease;
  position: relative;
}
.editable-element:hover {
  outline: 1.5px dashed rgba(197, 160, 89, 0.5);
  outline-offset: 4px;
  cursor: text;
}
[contenteditable="true"].inline-editing {
  outline: 2px solid #C5A059;
  outline-offset: 4px;
  background: rgba(197, 160, 89, 0.05);
  border-radius: 4px;
  min-width: 20px;
  min-height: 1em;
  caret-color: #C5A059;
}
.editable-element:hover::after {
  content: 'Double-clic pour modifier';
  position: absolute;
  top: -28px;
  left: 50%;
  transform: translateX(-50%);
  background: #1A1A1A;
  color: white;
  font-size: 9px;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 8px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  animation: tooltipFade 0.2s 0.5s ease forwards;
  z-index: 100;
}
@keyframes tooltipFade { to { opacity: 1; } }

/* Selection d'un bloc dans CardRenderer */
.card-engine > div:hover {
  outline: 1px dashed rgba(197, 160, 89, 0.4);
  outline-offset: -1px;
}
.card-engine > div.ring-4 {
  outline: 2px solid #C5A059;
  outline-offset: -2px;
  box-shadow: 0 0 0 4px rgba(197, 160, 89, 0.15);
}
</style>
