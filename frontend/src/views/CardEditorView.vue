<script setup>
import { ref, reactive, watch, onMounted, onUnmounted, computed, provide, nextTick } from 'vue';

// ── Champs texte par layout (source unique) ────────────────────────────

const TEMPLATE_FIELDS = {
  'aquarelle':        [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text', placeholder: 'ex: 15 Juin 2026' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
  ],
  'monolithe':        [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'section_title',label: 'Titre section',        type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'quote',        label: 'Citation',             type: 'textarea' },
    { key: 'dress_code',   label: 'Tenue vestimentaire',  type: 'text' },
    { key: 'image_url',    label: 'Image de couverture',  type: 'image' },
  ],
  'tel-aviv':         [
    { key: 'names',         label: 'Prénoms',              type: 'text' },
    { key: 'date_display',  label: 'Date affichée',         type: 'text', placeholder: '15 JUIN 2026' },
    { key: 'address',       label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',    label: 'Texte d\'introduction', type: 'textarea' },
  ],
  'riviera-blanche':  [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'monogram',     label: 'Monogramme',          type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'divider_symbol',label: 'Symbole décoratif',   type: 'text' },
  ],
  'jardin-celeste':   [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'monogram',     label: 'Monogramme',          type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'divider_symbol',label: 'Symbole décoratif',   type: 'text' },
  ],
  'empire-abstrait':  [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'monogram',     label: 'Monogramme',          type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'divider_symbol',label: 'Symbole décoratif',   type: 'text' },
  ],
  'arch':             [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'section_title',label: 'Titre de cérémonie',   type: 'text', placeholder: 'Union Sacrée' },
    { key: 'intro_text',   label: 'Citation / intro',     type: 'textarea' },
  ],
  'split':            [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'section_title',label: 'Titre section',        type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'image_url',    label: 'Photo principale',     type: 'image' },
    { key: 'image_url_2',  label: 'Photo secondaire',     type: 'image' },
  ],
  'es':               [
    { key: 'names',        label: 'Prénoms (séparés par & ou /)', type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Texte d\'introduction',type: 'textarea' },
    { key: 'image_url',    label: 'Image',                type: 'image' },
  ],
  'typography-focus': [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'section_title',label: 'Titre section',        type: 'text', placeholder: 'Première Mondiale' },
    { key: 'intro_text',   label: 'Citation / intro',     type: 'textarea' },
    { key: 'image_url',    label: 'Photo héro',           type: 'image' },
    { key: 'image_url_2',  label: 'Photos pellicule',     type: 'image' },
  ],
  'couture':          [
    { key: 'names',        label: 'Prénoms',             type: 'text' },
    { key: 'date_display', label: 'Date affichée',        type: 'text' },
    { key: 'address',      label: 'Lieu',                 type: 'text' },
    { key: 'intro_text',   label: 'Citation lookbook',    type: 'textarea' },
    { key: 'image_url',    label: 'Photo lookbook 1',     type: 'image' },
    { key: 'image_url_2',  label: 'Photo lookbook 2',     type: 'image' },
  ],
  'ora':              [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'image_url',    label: 'Photo de couverture',  type: 'image' },
    { key: 'intro_text',   label: "Texte d'invitation",   type: 'textarea' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
  ],
  'japonais':         null, // alias → arch
  'riviera':          null, // alias → split
  'film':             null, // alias → typography-focus
  'cinema': [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',   label: 'Synopsis',              type: 'textarea' },
    { key: 'image_url',    label: 'Photo héro',            type: 'image' },
  ],
  'celestial': [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',   label: 'Citation céleste',      type: 'textarea' },
  ],
  'wabi-sabi': [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',   label: 'Citation wabi-sabi',    type: 'textarea' },
    { key: 'image_url',    label: 'Photo de couverture',   type: 'image' },
  ],
  'gatsby': [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',   label: "Texte d'invitation",    type: 'textarea' },
    { key: 'dress_code',   label: 'Tenue vestimentaire',   type: 'text' },
    { key: 'image_url',    label: 'Photo de couverture',   type: 'image' },
  ],
  'velvet-noir': [
    { key: 'names',        label: 'Prénoms',              type: 'text' },
    { key: 'date_display', label: 'Date affichée',         type: 'text' },
    { key: 'address',      label: 'Lieu',                  type: 'text' },
    { key: 'intro_text',   label: 'Texte velours',         type: 'textarea' },
    { key: 'dress_code',   label: 'Tenue vestimentaire',   type: 'text' },
    { key: 'image_url',    label: 'Photo de couverture',   type: 'image' },
  ],
};
// Résoudre les alias
TEMPLATE_FIELDS['japonais']   = TEMPLATE_FIELDS['arch'];
TEMPLATE_FIELDS['riviera']    = TEMPLATE_FIELDS['split'];
TEMPLATE_FIELDS['film']       = TEMPLATE_FIELDS['typography-focus'];
import { useRoute, useRouter } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';
import UpgradeModal from '../components/UpgradeModal.vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';

const { notifyError, notifyInfo } = useToast();
const authStore = useAuthStore();
const isPremium = computed(() => authStore.user?.plan === 'premium');

// Blocs réservés au Premium (doit rester synchronisé avec PREMIUM_SECTION_IDS du backend)
const PREMIUM_SECTIONS = ['countdown', 'program', 'custom-text', 'image'];
// Sections par défaut : un compte Classic ne doit jamais recevoir de bloc Premium,
// sinon l'auto-save est rejeté par le backend (« blocs réservés au forfait Premium »).
const defaultSections = () => isPremium.value
  ? ['hero', 'countdown', 'program', 'rsvp', 'footer']
  : ['hero', 'rsvp', 'footer'];
const eventTitle = computed(() =>
  eventData.groom_name && eventData.bride_name
    ? `${eventData.groom_name} & ${eventData.bride_name}`
    : 'Mon Mariage'
);

const route = useRoute();
const router = useRouter();
const cardId = route.params.id;

// ==========================================
// 2. UI STATE
// ==========================================
const loading = ref(true);
const saving = ref(false);
const publishing = ref(false);
const showSaveToast = ref(false);
const hasUnsavedChanges = ref(false);
const isPublished = ref(false);
const cardSlug = ref(null);
const showCopiedToast = ref(false);
const publicUrl = computed(() => cardSlug.value ? `${window.location.origin}/i/${cardSlug.value}` : null);

const showUpgradeModal = ref(false);
const activeTab = ref('cover');
const selectedBlock = ref(null);
const editingField = ref(null);
const quickUploadField = ref(null);
const quickUploadInput = ref(null);
const previewDevice = ref('mobile'); // 'mobile' | 'desktop'
const zoomLevel = ref(100);

const tabs = [
  { id: 'cover',     label: 'Garde'  },
  { id: 'design',    label: 'Style'  },
  { id: 'structure', label: 'Blocs'  },
  { id: 'media',     label: 'Médias' },
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
  sections: defaultSections(),
  theme: {
    background: '#FAFAF8', accent: '#2E6E8E', text: '#1C2B3A',
    sectionTitleColor: '#1C2B3A', namesColor: '#2E6E8E', countdownColor: '',
    fontFamily: 'Playfair Display', textScale: 'medium'
  },
  content: {
    names: '', monogram: '', date_display: '', address: '',
    intro_text: '', rsvp_title: 'Serez-vous des nôtres ?', rsvp_deadline_text: 'Réponse souhaitée avant le 1er Mai.',
    divider_symbol: '✦', footer_text: 'Fait avec amour • 2026',
    splash_title: '', splash_top_text: 'Save the Date', splash_button_text: 'Entrer dans l\'invitation'
  },
  media: { image_url: '', music_url: '', splash_url: '' },
  show_countdown: true,
  show_splash: false,
  show_countdown_splash: true
});

const eventData = reactive({ date: '', location: '', groom_name: '', bride_name: '' });
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
  { id: 'countdown',   label: 'Compte à rebours', icon: '⏱️', desc: 'Anime l\'attente jusqu\'au jour J', premium: true  },
  { id: 'program',     label: 'Programme',         icon: '📅', desc: 'Détail des étapes de la journée',  premium: true  },
  { id: 'custom-text', label: 'Texte libre',        icon: '📝', desc: 'Un bloc de texte personnalisé',    premium: true  },
  { id: 'image',       label: 'Image',              icon: '🖼️', desc: 'Ajoutez une photo pleine largeur',  premium: true  },
  { id: 'rsvp',        label: 'Formulaire RSVP',   icon: '📩', desc: 'Collectez les présences',           premium: false },
  { id: 'footer',      label: 'Pied de page',       icon: '✨', desc: 'Message de fin et crédits',         premium: false },
];

const addBlock = (blockId) => {
  let finalId = blockId;
  
  // Éviter les doublons pour les blocs uniques
  if (['countdown', 'rsvp', 'footer', 'program'].includes(blockId)) {
    if (config.sections.includes(blockId)) {
      notifyInfo("Ce bloc est déjà présent sur votre invitation.");
      return;
    }
  }

  // Gérer les blocs de texte multiples
  if (blockId === 'custom-text') {
    finalId = `custom-text-${Date.now()}`;
    config.content[finalId] = { title: 'Nouveau titre', content: 'Votre texte ici...' };
  }

  // Bloc image avec placeholder immédiat
  if (blockId === 'image') {
    finalId = `image-${Date.now()}`;
    config.content[finalId] = { image_url: '/placeholder-mariage.svg', caption: '' };
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
    notifyInfo("Le bloc principal ne peut pas être supprimé.");
    return;
  }
  config.sections.splice(index, 1);
  selectedBlock.value = null;
  // Rester sur la liste des blocs plutôt que d'être renvoyé sur l'onglet Garde.
  activeTab.value = 'structure';
};

const getBlockLabel = (id) => {
  if (id.includes('hero') || id.includes('full')) return 'Bannière';
  if (id.startsWith('custom-text-')) return 'Texte libre';
  if (id.startsWith('image-')) return 'Image';
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
        { type: 'textarea', label: 'Descriptif', model: 'content.rsvp_deadline_text', placeholder: 'Ex : Réponse souhaitée avant le 1er mai.' }
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

  if (selectedBlock.value.startsWith('image-')) {
    return {
      label: 'Bloc Image',
      fields: [
        { type: 'image', label: 'Image', model: `content.${selectedBlock.value}.image_url` },
        { type: 'text', label: 'Légende (optionnel)', model: `content.${selectedBlock.value}.caption` },
      ]
    };
  }

  const isHeroBlock = selectedBlock.value === 'hero'
    || selectedBlock.value.includes('-full')
    || selectedBlock.value.includes('-hero');

  if (isHeroBlock) {
    const aliasMap = { japonais: 'arch', riviera: 'split', brutaliste: 'es', film: 'typography-focus' };
    const resolvedLayout = aliasMap[config.layout] || config.layout;
    const tplFields = TEMPLATE_FIELDS[resolvedLayout];
    if (!tplFields) return maps['hero'];
    return {
      label: 'Bannière principale',
      fields: [
        ...tplFields.map(f => ({
          type: f.type,
          label: f.label,
          model: 'content.' + f.key,
          placeholder: f.placeholder || ''
        })),
        { type: 'color', label: 'Couleur Noms', model: 'theme.namesColor' }
      ]
    };
  }

  return maps[selectedBlock.value] || null;
});

const addProgramStep = () => {
  subEvents.value.push({ time: '00:00', title: 'Nouvel événement', location: '', description: '' });
};

const removeProgramStep = (index) => {
  subEvents.value.splice(index, 1);
};

// Auto-switch vers 'context' quand on sélectionne un bloc
// (sauf si on est dans 'cover' — la garde gère sa propre preview)
watch(selectedBlock, (newVal) => {
  if (newVal && contextFields.value && activeTab.value !== 'cover') {
    activeTab.value = 'context';
  }
  if (!newVal && activeTab.value === 'context') {
    activeTab.value = 'cover';
  }
});

// Onglet Garde : sync preview ↔ onglet
watch(activeTab, (newTab, oldTab) => {
  if (newTab === 'cover') {
    // Entrer → montrer la garde dans la preview si activée
    selectedBlock.value = config.show_splash ? 'splash' : null;
  }
  if (oldTab === 'cover') {
    // Quitter → retour carte normale
    selectedBlock.value = null;
  }
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

      // Garantir que les sections de base sont toujours présentes
      if (!config.sections || config.sections.length === 0) {
        config.sections = defaultSections();
      } else if (!config.sections.some(s => s.includes('hero') || s.includes('full'))) {
        config.sections.unshift('hero');
      }

      // Migration : anciennes cartes "full" (hero seul, sections incrustées dans le
      // composant). Désormais countdown/programme/RSVP/footer sont des blocs gérés
      // par CardRenderer → on les rétablit comme blocs déplaçables s'ils manquent.
      if (config.sections.length === 1 && config.sections[0] === 'hero') {
        config.sections = defaultSections();
      }

      // Un compte Classic ne peut pas enregistrer de blocs Premium : on les retire
      // d'une carte existante pour éviter le rejet 403 à l'auto-save.
      if (!isPremium.value) {
        config.sections = config.sections.filter(s => !PREMIUM_SECTIONS.includes(s));
      }

      // Initialiser l'historique
      history.value = [snapshot()];
      historyIndex.value = 0;
    }
    isPublished.value = response.data.is_published || false;
    cardSlug.value = response.data.slug || null;

    if (response.data.event) {
      const ev = response.data.event;
      eventData.date = ev.date?.split('T')[0] || '';
      eventData.location = ev.location || '';
      eventData.groom_name = ev.groom_name || '';
      eventData.bride_name = ev.bride_name || '';

      // Auto-remplir depuis l'event si les champs sont absents dans le config
      if (ev.groom_name && ev.bride_name) {
        const namesFromEvent = `${ev.groom_name} & ${ev.bride_name}`;
        if (!config.content.names) config.content.names = namesFromEvent;
        if (!config.content.splash_title) config.content.splash_title = namesFromEvent;
        if (!config.content.monogram) {
          config.content.monogram = `${ev.groom_name[0].toUpperCase()} & ${ev.bride_name[0].toUpperCase()}`;
        }
      }
      if (ev.date && !config.content.date_display) {
        config.content.date_display = new Date(ev.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
      }
      if (ev.location && !config.content.address) {
        config.content.address = ev.location;
      }
      
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
    notifyError(err, { fallback: "Impossible d'enregistrer l'invitation. Veuillez réessayer." });
  }
};

const publishCard = async () => {
  try {
    publishing.value = true;
    await saveCard();
    const response = await api.post(`/cards/${cardId}/publish`);
    isPublished.value = response.data.is_published;
    cardSlug.value = response.data.slug;
  } catch (err) {
    console.error('Publish Error:', err);
    notifyError(err, { fallback: "Impossible de publier l'invitation. Veuillez réessayer." });
  } finally {
    publishing.value = false;
  }
};

const copyPublicUrl = async () => {
  if (!publicUrl.value) return;
  await navigator.clipboard.writeText(publicUrl.value);
  showCopiedToast.value = true;
  setTimeout(() => showCopiedToast.value = false, 2000);
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
    notifyError(err, { fallback: "Erreur lors de l'envoi de l'image." });
  }
};

const uploadingMusic = ref(false);

const handleMusicUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  uploadingMusic.value = true;
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', 'music');
    const response = await api.post(`/cards/${cardId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    config.media.music_url = response.data.url;
    saveCard();
  } catch (err) {
    notifyError(err, { fallback: "Erreur lors de l'envoi de la musique." });
  } finally {
    uploadingMusic.value = false;
  }
};

const removeMusic = () => {
  config.media.music_url = '';
  saveCard();
};

// ==========================================
// 10. COMPUTED TEMPLATE FIELDS & TAILLES
// ==========================================
const currentTemplateFields = computed(() =>
  TEMPLATE_FIELDS[config.layout] || [
    { key: 'names',        label: 'Prénoms',      type: 'text' },
    { key: 'date_display', label: 'Date affichée', type: 'text' },
    { key: 'address',      label: 'Lieu',          type: 'text' },
  ]
);

const TEXT_SIZES = [
  { id: 'small',  label: 'Petit' },
  { id: 'medium', label: 'Moyen' },
  { id: 'large',  label: 'Grand' },
];

const FONT_OPTIONS = [
  { value: 'Playfair Display', label: 'Élégant' },
  { value: 'Cormorant Garamond', label: 'Romantique' },
  { value: 'Jost', label: 'Moderne' },
  { value: 'Dancing Script', label: 'Manuscrit' },
];
const textScale = computed({
  get: () => config.theme.textScale || 'medium',
  set: v => { config.theme.textScale = v; },
});

// ==========================================
// 11. WATCHERS & FONTS
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

onMounted(async () => {
  // S'assurer que le plan de l'utilisateur est à jour (évite d'afficher les upsells aux comptes Premium)
  if (!authStore.user) await authStore.fetchMe();

  // Migration silencieuse une fois par session — corrige les cartes existantes avec demo data
  if (!sessionStorage.getItem('cards_synced')) {
    try { await api.post('/events/admin/sync-cards-data'); } catch {}
    sessionStorage.setItem('cards_synced', '1');
  }

  fetchCard();
  document.addEventListener('keydown', handleKeyboard);

  // Retour depuis Stripe Checkout → confirmer le paiement et rafraîchir le plan
  const sessionId = route.query.session_id;
  const paymentSuccess = route.query.payment_success;
  if (paymentSuccess === 'true' && sessionId) {
    try {
      await api.post('/payments/confirm-payment', { session_id: sessionId });
      await authStore.fetchMe();
    } catch { /* le webhook a peut-être déjà mis à jour le plan */ }
    router.replace({ query: {} });
  }
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboard);
  if (saveTimeout) clearTimeout(saveTimeout);
});
</script>

<template>
  <div v-if="!loading" class="flex flex-col h-screen bg-[#F3F4F6] font-sans overflow-hidden">

    <!-- BARRE DE PROGRESSION AUTO-SAVE (fine ligne au-dessus de tout) -->
    <div class="fixed top-0 left-0 right-0 h-[2px] z-50 bg-transparent pointer-events-none">
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

    <!-- ═══ HEADER PLEINE LARGEUR ═══ -->
    <header class="h-14 flex-shrink-0 bg-white border-b border-gray-200 flex items-center justify-between px-4 z-40 shadow-sm">

      <!-- LEFT : ← Galerie -->
      <div class="flex items-center min-w-0 lg:min-w-[140px]">
        <button @click="router.push('/templates')"
                class="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.12em] text-gray-500 hover:text-[#C5A059] transition-colors">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/>
          </svg>
          <span class="hidden sm:inline">Galerie</span>
        </button>
      </div>

      <!-- CENTER : nom événement + undo/redo -->
      <div class="flex items-center gap-3 flex-1 justify-center px-2 sm:px-4 min-w-0">
        <span class="text-xs sm:text-sm font-semibold text-gray-800 truncate max-w-[90px] sm:max-w-[200px]">{{ eventTitle }}</span>
        <div class="hidden sm:flex items-center gap-1 border-l border-gray-200 pl-3">
          <button @click="undo" :disabled="historyIndex <= 0"
                  class="p-1.5 rounded-lg hover:bg-gray-100 disabled:opacity-20 transition-all" title="Annuler (Ctrl+Z)">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M3 10h10a5 5 0 010 10H9" stroke-linecap="round"/>
              <path d="M3 10l4-4M3 10l4 4" stroke-linecap="round"/>
            </svg>
          </button>
          <button @click="redo" :disabled="historyIndex >= history.length - 1"
                  class="p-1.5 rounded-lg hover:bg-gray-100 disabled:opacity-20 transition-all" title="Rétablir (Ctrl+Y)">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M21 10H11a5 5 0 000 10h4" stroke-linecap="round"/>
              <path d="M21 10l-4-4M21 10l-4 4" stroke-linecap="round"/>
            </svg>
          </button>
          <span class="text-[8px] text-gray-400 font-mono pl-1 tabular-nums">{{ historyIndex + 1 }}/{{ history.length }}</span>
        </div>
      </div>

      <!-- RIGHT : statut + actions publication + Mon espace -->
      <div class="flex items-center gap-2 sm:gap-3 min-w-0 lg:min-w-[320px] justify-end">

        <!-- Statut de publication -->
        <div class="flex items-center gap-1.5">
          <span v-if="isPublished" class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse flex-shrink-0"></span>
          <span v-else class="w-2 h-2 rounded-full bg-gray-300 flex-shrink-0"></span>
          <span class="hidden sm:inline text-[10px] font-bold uppercase tracking-widest"
                :class="isPublished ? 'text-emerald-600' : 'text-gray-400'">
            {{ isPublished ? 'En ligne' : 'Hors ligne' }}
          </span>
        </div>

        <!-- Voir en ligne (si publié) -->
        <a v-if="isPublished && publicUrl" :href="publicUrl" target="_blank"
           class="text-[10px] font-bold text-blue-600 hover:text-blue-800 transition-colors flex items-center gap-1 whitespace-nowrap">
          Voir en ligne
          <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/>
          </svg>
        </a>

        <!-- Copier le lien (si publié) -->
        <button v-if="isPublished && publicUrl" @click="copyPublicUrl"
                class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors" title="Copier le lien d'invitation">
          <svg v-if="!showCopiedToast" class="w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke-width="2"/>
            <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke-width="2"/>
          </svg>
          <svg v-else class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
          </svg>
        </button>

        <!-- Bouton Publier / Dépublier -->
        <button @click="publishCard" :disabled="publishing"
                class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-wider transition-all flex items-center gap-2 shadow-sm flex-shrink-0"
                :class="isPublished
                  ? 'bg-red-50 text-red-500 hover:bg-red-100 border border-red-100'
                  : 'bg-[#1A1A1A] text-white hover:bg-black'">
          <span v-if="publishing" class="w-3 h-3 border-2 border-current/40 border-t-current rounded-full animate-spin flex-shrink-0"/>
          <span v-else>{{ isPublished ? 'Dépublier' : 'Publier' }}</span>
        </button>

        <!-- Séparateur -->
        <div class="hidden sm:block w-px h-6 bg-gray-200 flex-shrink-0"></div>

        <!-- Mon espace -->
        <button @click="router.push('/dashboard')"
                class="text-[10px] font-black uppercase tracking-[0.12em] text-gray-500 hover:text-[#C5A059] transition-colors flex items-center gap-1.5 whitespace-nowrap">
          <span class="hidden sm:inline">Mon espace</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- ═══ CORPS : SIDEBAR + PREVIEW ═══ -->
    <div class="flex flex-col lg:flex-row flex-1 overflow-hidden">

    <!-- SIDEBAR GAUCHE (en bas sur mobile, à gauche sur desktop) -->
    <aside class="order-2 lg:order-1 w-full lg:w-[360px] basis-3/5 lg:basis-auto min-h-0 flex flex-col bg-white border-t lg:border-t-0 lg:border-r border-gray-200 shadow-sm z-30 flex-shrink-0">

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
      <div class="flex-1 overflow-y-auto p-4 sm:p-6 custom-scrollbar bg-[#FAFAFA]">
        
        <!-- ONGLET : CONTEXTE (auto-activé au clic sur un bloc, hors nav) -->
        <div v-if="activeTab === 'context'" class="animate-in space-y-6">
          <!-- Bouton retour -->
          <button @click="selectedBlock = null"
                  class="flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-[#C5A059] transition-colors">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
            Retour
          </button>
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
                       :placeholder="field.placeholder || ''"
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
        <div v-if="activeTab === 'cover'" class="animate-in space-y-4 pb-4">

          <!-- ── Activation ── -->
          <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden">
            <label class="flex items-center gap-4 p-5 cursor-pointer group">
              <!-- Icône -->
              <div class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 transition-colors"
                   :class="config.show_splash ? 'bg-[#1A1A1A]' : 'bg-gray-100'">
                <svg class="w-5 h-5 transition-colors" :class="config.show_splash ? 'text-[#C5A059]' : 'text-gray-400'"
                     fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"
                        d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-[11px] font-black uppercase tracking-widest text-gray-900">Page de garde</p>
                <p class="text-[10px] text-gray-400 mt-0.5">Écran d'accueil avant l'invitation</p>
              </div>
              <!-- Toggle -->
              <div class="relative shrink-0">
                <input type="checkbox" v-model="config.show_splash" class="sr-only peer"
                       @change="config.show_splash ? (selectedBlock = 'splash') : (selectedBlock = null)">
                <div class="w-11 h-6 rounded-full transition-colors peer-checked:bg-[#1A1A1A] bg-gray-200
                            after:content-[''] after:absolute after:top-0.5 after:left-0.5
                            after:bg-white after:rounded-full after:h-5 after:w-5
                            after:transition-all peer-checked:after:translate-x-5 after:shadow-sm"></div>
              </div>
            </label>
          </div>

          <!-- ── Contenu (visible si activé) ── -->
          <template v-if="config.show_splash">

            <!-- Photo de fond -->
            <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden">
              <div class="px-5 pt-5 pb-3">
                <p class="text-[9px] font-black uppercase tracking-[0.2em] text-gray-400 mb-3">Photo de fond</p>
                <!-- Miniature cliquable -->
                <label class="block relative group cursor-pointer">
                  <div class="w-full h-28 rounded-xl overflow-hidden bg-gray-100 border border-gray-200">
                    <img v-if="config.media.splash_url" :src="config.media.splash_url"
                         class="w-full h-full object-cover" />
                    <div v-else class="w-full h-full flex flex-col items-center justify-center gap-2 text-gray-300">
                      <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                      </svg>
                      <span class="text-[9px] uppercase tracking-widest">Choisir une photo</span>
                    </div>
                  </div>
                  <!-- Overlay hover -->
                  <div class="absolute inset-0 rounded-xl bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <span class="text-white text-[9px] font-bold uppercase tracking-widest">Changer</span>
                  </div>
                  <input type="file" class="hidden" accept="image/*" @change="handleFileUpload($event, 'media.splash_url')">
                </label>
              </div>
              <!-- URL manuelle -->
              <div class="px-5 pb-5">
                <input type="text" v-model="config.media.splash_url"
                       placeholder="ou coller une URL…"
                       class="w-full p-2.5 bg-gray-50 border border-gray-100 rounded-xl text-[10px] text-gray-600 placeholder-gray-300 focus:border-[#C5A059] focus:bg-white outline-none transition-colors" />
              </div>
            </div>

            <!-- Textes -->
            <div class="bg-white rounded-2xl border border-gray-100 divide-y divide-gray-50">
              <p class="px-5 pt-4 pb-2 text-[9px] font-black uppercase tracking-[0.2em] text-gray-400">Textes</p>

              <div v-for="field in [
                { key: 'splash_top_text',    label: 'Texte haut',     placeholder: 'Save the Date' },
                { key: 'splash_title',       label: 'Titre principal', placeholder: 'Prénom1 & Prénom2' },
                { key: 'splash_subtitle',    label: 'Sous-titre',      placeholder: 'Une journée inoubliable…' },
                { key: 'splash_button_text', label: 'Bouton entrer',   placeholder: 'Entrer dans l\'invitation' },
              ]" :key="field.key" class="px-5 py-3.5 flex items-center gap-3">
                <span class="text-[9px] text-gray-400 w-24 shrink-0 font-medium">{{ field.label }}</span>
                <input type="text"
                       v-model="config.content[field.key]"
                       :placeholder="field.placeholder"
                       class="flex-1 bg-gray-50 border border-transparent rounded-lg px-3 py-2 text-[11px] text-gray-800 placeholder-gray-300 focus:border-[#C5A059] focus:bg-white outline-none transition-colors" />
              </div>
            </div>

            <!-- Options -->
            <div class="bg-white rounded-2xl border border-gray-100 divide-y divide-gray-50">
              <p class="px-5 pt-4 pb-2 text-[9px] font-black uppercase tracking-[0.2em] text-gray-400">Options</p>

              <label class="flex items-center justify-between px-5 py-4 cursor-pointer group">
                <div>
                  <p class="text-[11px] font-bold text-gray-800">Compte à rebours</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Afficher le décompte sur la garde</p>
                </div>
                <div class="relative">
                  <input type="checkbox" v-model="config.show_countdown_splash" class="sr-only peer">
                  <div class="w-9 h-5 rounded-full transition-colors peer-checked:bg-[#1A1A1A] bg-gray-200
                              after:content-[''] after:absolute after:top-0.5 after:left-0.5
                              after:bg-white after:rounded-full after:h-4 after:w-4
                              after:transition-all peer-checked:after:translate-x-4 after:shadow-sm"></div>
                </div>
              </label>
            </div>

            <!-- Couleurs de la garde -->
            <div class="bg-white rounded-2xl border border-gray-100 divide-y divide-gray-50">
              <p class="px-5 pt-4 pb-2 text-[9px] font-black uppercase tracking-[0.2em] text-gray-400">Couleurs</p>

              <!-- Fond -->
              <div class="px-5 py-3.5 flex items-center justify-between">
                <div>
                  <p class="text-[11px] font-bold text-gray-800">Couleur de fond</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Si pas de photo, cette couleur est utilisée</p>
                </div>
                <label class="relative cursor-pointer">
                  <div class="w-9 h-9 rounded-xl border-2 border-white shadow-md ring-1 ring-black/10 overflow-hidden"
                       :style="{ backgroundColor: config.theme.background || '#0a0a0a' }">
                    <input type="color" v-model="config.theme.background"
                           class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                  </div>
                </label>
              </div>

              <!-- Accentuation -->
              <div class="px-5 py-3.5 flex items-center justify-between">
                <div>
                  <p class="text-[11px] font-bold text-gray-800">Couleur d'accentuation</p>
                  <p class="text-[9px] text-gray-400 mt-0.5">Titres, ornements, séparateurs</p>
                </div>
                <label class="relative cursor-pointer">
                  <div class="w-9 h-9 rounded-xl border-2 border-white shadow-md ring-1 ring-black/10 overflow-hidden"
                       :style="{ backgroundColor: config.theme.accent || '#C5A059' }">
                    <input type="color" v-model="config.theme.accent"
                           class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                  </div>
                </label>
              </div>
            </div>

            <!-- Info device actif -->
            <div class="flex items-center gap-2 px-1">
              <svg class="w-3.5 h-3.5 text-gray-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke-width="1.5"/>
                <path d="M12 8v4m0 4h.01" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p class="text-[9px] text-gray-400 leading-relaxed">
                La garde s'affiche dans le cadre
                <span class="font-bold text-gray-600">{{ previewDevice === 'mobile' ? 'téléphone' : 'ordinateur' }}</span>.
                Changez le cadre via la barre en haut de la preview.
              </p>
            </div>

          </template>

        </div>

        <!-- ONGLET : DESIGN -->
        <div v-if="activeTab === 'design'" class="animate-in space-y-8">
          
          <div class="space-y-4">
            <h3 class="flex items-center text-xs font-black text-gray-800 uppercase tracking-widest">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.172-1.172a4 4 0 115.656 5.656L15 13"></path></svg>
              Palette de couleurs
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="(label, key) in { namesColor: 'Noms', countdownColor: 'Compte à rebours', sectionTitleColor: 'Titre', text: 'Textes', background: 'Fond' }" :key="key"
                   class="bg-white border border-gray-200 p-2 rounded-xl flex items-center">
                <input type="color" :value="config.theme[key] || '#2E6E8E'" @input="config.theme[key] = $event.target.value" class="w-8 h-8 rounded-lg cursor-pointer border-0 p-0 bg-transparent">
                <span class="ml-2 text-[10px] font-bold uppercase text-gray-500">{{ label }}</span>
              </div>
            </div>
          </div>

          <div class="space-y-4 pt-6 border-t border-gray-200">
            <h3 class="flex items-center text-xs font-black text-gray-800 uppercase tracking-widest">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 5v12m0 0H7m2 0h2M3 20h12M21 12h-6"/></svg>
              Typographie
              <span v-if="!isPremium" class="ml-2 inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-100 text-[#C5A059] text-[9px] font-bold uppercase">
                <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24"><path d="M18 8h-1V6A5 5 0 007 6v2H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10a2 2 0 00-2-2zM12 17a2 2 0 110-4 2 2 0 010 4zm3.1-9H8.9V6a3.1 3.1 0 016.2 0v2z"/></svg>
                Premium
              </span>
            </h3>
            <div class="relative">
              <div class="bg-white border border-gray-200 p-4 rounded-xl space-y-5"
                   :class="!isPremium ? 'opacity-50 pointer-events-none select-none' : ''">

              <!-- Police -->
              <div class="space-y-2">
                <span class="text-[10px] font-bold uppercase text-gray-500">Police de caractères</span>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="font in FONT_OPTIONS" :key="font.value"
                    @click="config.theme.fontFamily = font.value"
                    class="flex flex-col items-start gap-0.5 px-3 py-2.5 rounded-xl border-2 transition-all text-left"
                    :class="config.theme.fontFamily === font.value
                      ? 'border-amber-400 bg-amber-50'
                      : 'border-gray-100 bg-gray-50 hover:border-gray-200'"
                  >
                    <span class="text-lg leading-tight" :style="{ fontFamily: font.value }">Aa</span>
                    <span class="text-[9px] font-bold uppercase tracking-widest text-gray-500 truncate w-full">{{ font.label }}</span>
                  </button>
                </div>
              </div>

              <!-- Taille du texte -->
              <div class="space-y-2">
                <span class="text-[10px] font-bold uppercase text-gray-500">Taille du texte</span>
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="size in TEXT_SIZES" :key="size.id"
                    @click="textScale = size.id"
                    class="flex flex-col items-center gap-1.5 py-3 rounded-xl border-2 transition-all"
                    :class="textScale === size.id
                      ? 'border-[#C5A059] bg-amber-50 text-[#C5A059]'
                      : 'border-gray-200 bg-white text-gray-400 hover:border-gray-300 hover:text-gray-600'"
                  >
                    <span class="font-serif leading-none transition-all"
                          :class="size.id === 'small' ? 'text-base' : size.id === 'medium' ? 'text-xl' : 'text-3xl'">A</span>
                    <span class="text-[9px] font-black uppercase tracking-wider">{{ size.label }}</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-if="!isPremium"
                 class="absolute inset-0 rounded-xl flex items-center justify-center cursor-pointer"
                 @click="showUpgradeModal = true">
              <span class="px-3 py-2 bg-amber-100 text-[#C5A059] rounded-xl text-[10px] font-black uppercase tracking-widest flex items-center gap-1.5 shadow-sm">
                <svg class="w-3 h-3 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M18 8h-1V6A5 5 0 007 6v2H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10a2 2 0 00-2-2zM12 17a2 2 0 110-4 2 2 0 010 4zm3.1-9H8.9V6a3.1 3.1 0 016.2 0v2z"/></svg>
                Débloquer Premium
              </span>
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
                <!-- Supprimer (masqué sur les blocs principaux hero/full) -->
                <button v-if="!section.includes('hero') && !section.includes('full')"
                        @click.stop="deleteBlock(index)"
                        class="p-1.5 rounded-lg text-gray-300 hover:text-red-500 hover:bg-red-50 transition-colors shrink-0"
                        title="Supprimer ce bloc">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>
            </div>
          </section>

          <section class="pt-8 border-t border-gray-200">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest text-center mb-6">Ajouter une section</p>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="block in availableBlocks" :key="block.id"
                @click="block.premium && !isPremium ? showUpgradeModal = true : addBlock(block.id)"
                class="relative p-4 bg-white border border-gray-100 rounded-2xl hover:border-[#C5A059] hover:shadow-md transition-all text-center group"
                :class="block.premium && !isPremium ? 'opacity-70' : ''"
              >
                <!-- Verrou pour blocs Premium si Classic -->
                <span
                  v-if="block.premium && !isPremium"
                  class="absolute top-2 right-2 w-5 h-5 flex items-center justify-center bg-amber-100 rounded-full"
                  title="Forfait Premium requis"
                >
                  <svg class="w-3 h-3 text-[#C5A059]" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M18 8h-1V6A5 5 0 007 6v2H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10a2 2 0 00-2-2zM12 17a2 2 0 110-4 2 2 0 010 4zm3.1-9H8.9V6a3.1 3.1 0 016.2 0v2z"/>
                  </svg>
                </span>
                <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">{{ block.icon }}</div>
                <p class="text-[10px] font-bold text-gray-800 uppercase leading-tight">{{ block.label }}</p>
              </button>
            </div>
          </section>
        </div>

        <!-- ONGLET : MÉDIAS (images + musique) -->
        <div v-if="activeTab === 'media'" class="animate-in space-y-6">

          <!-- Images -->
          <div class="space-y-3">
            <p class="text-[9px] font-black uppercase text-gray-400 tracking-widest">Images</p>

            <!-- Image principale (couverture) -->
            <div class="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
              <p class="text-[10px] font-bold text-gray-700 uppercase tracking-wider">Image principale</p>
              <div class="flex gap-2">
                <input type="text" v-model="config.media.image_url" placeholder="https://..." class="flex-1 p-2.5 bg-gray-50 border border-transparent rounded-lg text-xs focus:border-[#C5A059] outline-none">
                <label class="p-2.5 bg-gray-100 hover:bg-gray-200 rounded-lg cursor-pointer transition-colors flex items-center justify-center shrink-0">
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                  <input type="file" class="hidden" accept="image/*" @change="handleFileUpload($event, 'media.image_url')">
                </label>
              </div>
              <div v-if="config.media.image_url" class="aspect-[4/3] rounded-lg overflow-hidden border border-gray-200 bg-gray-100">
                <img :src="config.media.image_url" class="w-full h-full object-cover">
              </div>
            </div>

            <!-- Image splash (écran d'accueil) -->
            <div class="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
              <p class="text-[10px] font-bold text-gray-700 uppercase tracking-wider">Écran d'accueil</p>
              <div class="flex gap-2">
                <input type="text" v-model="config.media.splash_url" placeholder="https://..." class="flex-1 p-2.5 bg-gray-50 border border-transparent rounded-lg text-xs focus:border-[#C5A059] outline-none">
                <label class="p-2.5 bg-gray-100 hover:bg-gray-200 rounded-lg cursor-pointer transition-colors flex items-center justify-center shrink-0">
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                  <input type="file" class="hidden" accept="image/*" @change="handleFileUpload($event, 'media.splash_url')">
                </label>
              </div>
              <div v-if="config.media.splash_url" class="aspect-[4/3] rounded-lg overflow-hidden border border-gray-200 bg-gray-100">
                <img :src="config.media.splash_url" class="w-full h-full object-cover">
              </div>
            </div>
          </div>

          <!-- Musique -->
          <div class="space-y-3">
            <p class="text-[9px] font-black uppercase text-gray-400 tracking-widest">Musique d'ambiance</p>

            <!-- Bloc Premium requis -->
            <div v-if="!isPremium" class="rounded-2xl overflow-hidden border border-amber-200 bg-amber-50">
              <div class="p-5 space-y-3 text-center">
                <div class="w-12 h-12 rounded-full bg-[#C5A059]/15 flex items-center justify-center mx-auto">
                  <svg class="w-6 h-6 text-[#C5A059]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"/>
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-black uppercase tracking-widest text-[#8B6914]">Fonctionnalité Premium</p>
                  <p class="text-[11px] text-amber-700 mt-1">Ajoutez une musique d'ambiance à votre invitation. Disponible avec le forfait Premium.</p>
                </div>
                <button @click="showUpgradeModal = true" class="w-full py-2.5 bg-[#C5A059] text-white rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#b08c47] transition-colors">
                  Passer Premium
                </button>
              </div>
            </div>

            <!-- Interface upload si Premium -->
            <template v-else>
              <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full bg-[#C5A059]"></div>
                  <p class="text-[10px] font-black uppercase tracking-widest text-gray-700">Musique d'ambiance</p>
                </div>

                <div v-if="config.media.music_url" class="space-y-3">
                  <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                    <svg class="w-4 h-4 text-[#C5A059] shrink-0" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"/>
                    </svg>
                    <audio :src="config.media.music_url" controls class="flex-1 h-8 w-full" style="min-width:0"></audio>
                  </div>
                  <button @click="removeMusic" class="w-full py-2 text-[10px] font-bold uppercase tracking-wider text-red-500 bg-red-50 rounded-xl hover:bg-red-100 transition-colors">
                    Supprimer la musique
                  </button>
                </div>

                <label v-else class="flex flex-col items-center gap-3 p-6 border-2 border-dashed border-gray-200 rounded-xl cursor-pointer hover:border-[#C5A059] hover:bg-amber-50/40 transition-all group">
                  <div class="w-10 h-10 rounded-full bg-gray-100 group-hover:bg-amber-100 flex items-center justify-center transition-colors">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-[#C5A059] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                    </svg>
                  </div>
                  <div class="text-center">
                    <p class="text-[11px] font-bold text-gray-600">Importer un fichier audio</p>
                    <p class="text-[10px] text-gray-400 mt-0.5">MP3, AAC, OGG — max 20 Mo</p>
                  </div>
                  <span v-if="uploadingMusic" class="w-4 h-4 border-2 border-[#C5A059]/30 border-t-[#C5A059] rounded-full animate-spin"></span>
                  <input type="file" class="hidden" accept="audio/*" @change="handleMusicUpload" :disabled="uploadingMusic">
                </label>

                <p class="text-[10px] text-gray-400 leading-relaxed">La musique est jouée en fond lors de la consultation de l'invitation par vos invités.</p>
              </div>
            </template>
          </div>
        </div>

      </div>

    </aside>

    <!-- ZONE PREVIEW -->
    <main class="order-1 lg:order-2 basis-2/5 lg:basis-auto lg:flex-1 min-h-0 relative flex flex-col items-center justify-center p-2 sm:p-8 bg-[#F3F4F6] overflow-hidden">

      <!-- Toolbar flottante Preview -->
      <div class="absolute top-2 sm:top-6 flex items-center space-x-2 bg-white/90 backdrop-blur-md px-3 sm:px-4 py-1.5 sm:py-2 rounded-full border border-gray-200 shadow-sm z-20">
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
        
        <div :class="previewDevice === 'mobile' ? 'w-[min(88vw,400px)] h-full max-h-[850px] rounded-[2.2rem] sm:rounded-[3rem] ring-8 sm:ring-[12px] ring-gray-900 shadow-2xl' : 'w-full max-w-5xl h-full max-h-[800px] rounded-xl shadow-2xl'"
             class="bg-white overflow-hidden relative flex flex-col transition-all duration-500 border border-gray-200">
          
          <div v-if="previewDevice === 'mobile'" class="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-gray-900 rounded-b-2xl z-50"></div>
          
          <div class="flex-1 overflow-y-auto overflow-x-hidden custom-scrollbar bg-white relative" @click.self="selectedBlock = null">
            <!-- INJECTION DU MOTEUR DE RENDU -->
            <CardRenderer :config="config" :event="eventData" :subEvents="subEvents" :selectedBlock="selectedBlock" @select-block="selectedBlock = $event" />

            <!-- Bouton retour carte (visible uniquement en mode préview garde) -->
            <Transition name="fade-up">
              <button v-if="selectedBlock === 'splash'"
                      @click="selectedBlock = null; activeTab = 'cover'"
                      class="absolute bottom-6 left-1/2 -translate-x-1/2 z-[500] flex items-center gap-2 px-5 py-2.5 bg-white/90 backdrop-blur-md border border-gray-200 rounded-full shadow-lg text-[10px] font-black uppercase tracking-widest text-gray-700 hover:bg-white hover:shadow-xl transition-all">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/>
                </svg>
                Retour à la carte
              </button>
            </Transition>
          </div>
        </div>
      </div>
      
    </main>

    </div><!-- fin corps sidebar+preview -->
  </div>

  <div v-else class="h-screen flex items-center justify-center bg-[#F9F7F2]">
     <div class="text-center space-y-6">
        <div class="w-12 h-1 bg-gray-200 mx-auto overflow-hidden"><div class="w-full h-full bg-[#C5A059] animate-pulse"></div></div>
        <p class="text-[10px] font-black uppercase tracking-[0.3em] text-[#C5A059]">Ouverture du Studio</p>
     </div>
  </div>

  <!-- INPUT CACHÉ POUR LES TÉLÉCHARGEMENTS RAPIDES (CLIC SUR IMAGE) -->
  <input ref="quickUploadInput" type="file" class="hidden" accept="image/*" @change="handleQuickUpload">

  <UpgradeModal v-model="showUpgradeModal" :cardId="cardId" />
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

/* Transition bouton retour carte */
.fade-up-enter-active, .fade-up-leave-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-up-enter-from, .fade-up-leave-to { opacity: 0; transform: translate(-50%, 12px); }

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
