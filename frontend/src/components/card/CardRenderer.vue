<script setup>
import { computed, ref, onMounted, onUnmounted, inject } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

// Composants de base
import CardSectionBanner from './CardSectionBanner.vue';
import CardSectionText from './CardSectionText.vue';
import CardSectionRSVP from './CardSectionRSVP.vue';
import CardSplashScreen from './CardSplashScreen.vue';

// Templates (Hero-only refactored)
import CardTemplateOra from './CardTemplateOra.vue';
import CardTemplateJaponais from './CardTemplateJaponais.vue';
import CardTemplateRiviera from './CardTemplateRiviera.vue';
import CardTemplateBrutaliste from './CardTemplateBrutaliste.vue';
import CardTemplateFilm from './CardTemplateFilm.vue';
import CardTemplateNoirEternel from './CardTemplateNoirEternel.vue';
import CardTemplateRivieraBlanche from './CardTemplateRivieraBlanche.vue';
import CardTemplateJardinCeleste from './CardTemplateJardinCeleste.vue';
import CardTemplateEmpireAbstrait from './CardTemplateEmpireAbstrait.vue';
import CardTemplateCouture from './CardTemplateCouture.vue';
import CardTemplateCinema from './CardTemplateCinema.vue';
import CardTemplateCelestial from './CardTemplateCelestial.vue';
import CardTemplateWabiSabi from './CardTemplateWabiSabi.vue';
import CardTemplateGatsby from './CardTemplateGatsby.vue';
import CardTemplateEditorial from './CardTemplateEditorial.vue';
import CardTemplateVelvetNoir from './CardTemplateVelvetNoir.vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ 
      layout: 'arch',
      sections: ['hero', 'countdown', 'program', 'footer'],
      theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
      content: { names: '' },
      show_countdown: true
    })
  },
  event: {
    type: Object,
    default: () => ({ groom_name: '', bride_name: '', date: '', location: '' })
  },
  subEvents: { type: Array, default: () => [] },
  selectedBlock: { type: String, default: null }
});

const emit = defineEmits(['select-block']);

const isEditorMode = inject('isEditorMode', false);
const triggerQuickUpload = inject('triggerQuickUpload', null);

const handleImageClick = (fieldPath) => {
  if (isEditorMode && triggerQuickUpload) {
    triggerQuickUpload(fieldPath);
  }
};

// Moteur de sections dynamique
const sections = computed(() => {
  if (props.config.sections && props.config.sections.length > 0) return props.config.sections;
  return ['hero', 'countdown', 'program', 'rsvp', 'footer'];
});

const isSplashVisible = ref(true);
const hideSplash = () => isSplashVisible.value = false;

const safeConfig = computed(() => {
  const defaults = {
    layout: 'arch',
    theme: { 
      background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', 
      fontFamily: 'Playfair Display', fontSize: '1rem', titleSize: '3.5rem' 
    },
    content: { names: '', image_url: '', footer_text: 'Fait avec amour • 2026' },
    show_countdown: true
  };

  const cfg = {
    ...defaults,
    ...props.config,
    theme: { ...defaults.theme, ...(props.config.theme || {}) },
    content: { ...defaults.content, ...(props.config.content || {}) }
  };

  // Auto-contraste uniquement si le texte est encore à la valeur par défaut
  if (!props.config.theme?.text || props.config.theme.text === '#1A1A1A') {
    const bgColor = cfg.theme.background || '#F9F7F2';
    cfg.theme.text = getContrastColor(bgColor);
  }

  return cfg;
});

const displayData = computed(() => ({
  names: safeConfig.value.content?.names || (props.event.groom_name && props.event.bride_name ? `${props.event.groom_name} & ${props.event.bride_name}` : ''),
  date: props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : (safeConfig.value.content?.date_display || '15 Juin 2026'),
  location: props.event.location || safeConfig.value.content?.address || '',
  image: safeConfig.value.media?.image_url || safeConfig.value.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'
}));

// Logic de compte à rebours global
const timeLeft = ref({ days: 0, hours: 0, mins: 0, secs: 0 });
let timer = null;
const updateCountdown = () => {
  const dateToUse = props.event?.date || safeConfig.value?.content?.date;
  if (!dateToUse) return;
  const targetDate = new Date(dateToUse).getTime();
  const now = new Date().getTime();
  const diff = targetDate - now;
  if (diff > 0) {
    timeLeft.value = {
      days: Math.floor(diff / (1000 * 60 * 60 * 24)),
      hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
      mins: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
      secs: Math.floor((diff % (1000 * 60)) / 1000)
    };
  }
};

onMounted(() => {
  updateCountdown();
  timer = setInterval(updateCountdown, 1000);
});
onUnmounted(() => clearInterval(timer));

const theme = computed(() => safeConfig.value.theme);
const layout = computed(() => safeConfig.value.layout);

// Helper pour identifier les blocs Hero des templates
const isTemplateHero = (id) => {
  return id.endsWith('-full') || id.endsWith('-hero') || id === 'hero';
};

const currentTemplate = computed(() => {
  const l = layout.value;
  if (l === 'noir-eternel') return CardTemplateNoirEternel;
  if (l === 'riviera-blanche') return CardTemplateRivieraBlanche;
  if (l === 'jardin-celeste') return CardTemplateJardinCeleste;
  if (l === 'empire-abstrait') return CardTemplateEmpireAbstrait;
  if (l === 'ora') return CardTemplateOra;
  if (l === 'japonais' || l === 'arch') return CardTemplateJaponais;
  if (l === 'riviera' || l === 'split') return CardTemplateRiviera;
  if (l === 'brutaliste' || l === 'es') return CardTemplateBrutaliste;
  if (l === 'film' || l === 'typography-focus') return CardTemplateFilm;
  if (l === 'couture') return CardTemplateCouture;
  if (l === 'cinema') return CardTemplateCinema;
  if (l === 'celestial') return CardTemplateCelestial;
  if (l === 'wabi-sabi') return CardTemplateWabiSabi;
  if (l === 'gatsby') return CardTemplateGatsby;
  if (l === 'editorial') return CardTemplateEditorial;
  if (l === 'velvet-noir') return CardTemplateVelvetNoir;
  return null;
});
</script>

<template>
  <!-- PAGE DE GARDE (SPLASH)
       En mode éditeur → seulement quand selectedBlock='splash' (préview onglet Garde)
       En vue publique → toujours affichée si activée -->
  <CardSplashScreen
    v-if="safeConfig.show_splash && isSplashVisible && (!isEditorMode || selectedBlock === 'splash')"
    :config="safeConfig"
    :event="event"
    :templateId="safeConfig.layout"
    :isPreview="selectedBlock === 'splash'"
    @close="hideSplash"
  />

  <div v-show="!(isEditorMode && selectedBlock === 'splash')"
       class="card-engine w-full flex flex-col items-center overflow-x-hidden pb-10 relative"
       :style="{
         fontFamily: theme.fontFamily || 'Playfair Display',
         backgroundColor: theme.background || 'white',
         color: theme.text,
         '--accent':       theme.accent      || '#C5A059',
         '--accent-color': theme.accent      || '#C5A059',
         '--names-color':  theme.namesColor  || null,
         '--title-color':  theme.titleColor  || null,
         '--names-size': theme.namesSize ? parseFloat(theme.namesSize) + 'rem' : '',
         '--title-size': theme.titleSize ? parseFloat(theme.titleSize) + 'rem' : '',
         '--body-size':  theme.fontSize  ? parseFloat(theme.fontSize)  + 'rem' : '',
       }">
    
    <div v-for="sectionId in sections" :key="sectionId"
         @click="isEditorMode && emit('select-block', sectionId)"
         class="w-full relative"
         :class="isEditorMode ? ['transition-all duration-300 cursor-pointer', selectedBlock === sectionId ? 'ring-4 ring-blue-500/30 z-50' : ''] : []">
      
      <!-- RENDU DYNAMIQUE DES TEMPLATES (HERO) -->
      <template v-if="isTemplateHero(sectionId)">
        <!-- Si un template spécifique est trouvé pour le layout actuel -->
        <component v-if="currentTemplate" :is="currentTemplate" :config="safeConfig" :event="event" @click-image="handleImageClick" />
        <!-- Sinon, fallback sur le Banner par défaut -->
        <CardSectionBanner v-else :layout="layout" :theme="theme" :displayData="displayData" />
      </template>

      <!-- BLOCS GÉNÉRIQUES -->
      <CardSectionText v-if="sectionId.startsWith('custom-text')" :id="sectionId" :config="safeConfig" :event="event" />

      <div v-if="sectionId === 'countdown' && safeConfig.show_countdown" class="w-full py-16 text-center z-10 relative" :style="{ color: theme.text }">
         <p class="text-[11px] font-bold uppercase tracking-[0.5em] mb-8 opacity-40">Le grand décompte</p>
         <div class="flex justify-center items-center space-x-8">
            <div v-for="(val, label) in { Jours:timeLeft.days, Heures:timeLeft.hours, Min:timeLeft.mins, Sec:timeLeft.secs }" :key="label" class="flex flex-col">
               <span class="text-5xl font-light" :style="{ color: theme.accent }">{{ val }}</span>
               <span class="text-[9px] uppercase tracking-widest opacity-40 mt-2">{{ label }}</span>
            </div>
         </div>
      </div>

      <div v-if="sectionId === 'program'" class="w-full py-20 px-8 text-center space-y-12 z-10 relative" :style="{ color: theme.text }">
        <h2 class="text-4xl md:text-5xl font-serif italic">Le Programme</h2>
        <div v-if="subEvents && subEvents.length > 0" class="max-w-xl mx-auto space-y-12">
          <div v-for="(se, idx) in subEvents" :key="idx" class="space-y-4">
              <p class="text-[11px] font-bold uppercase tracking-[0.4em]" :style="{ color: theme.accent }">{{ se.time }}</p>
              <h3 class="text-2xl font-light italic">{{ se.title }}</h3>
              <p v-if="se.location" class="text-xs uppercase tracking-widest opacity-60">{{ se.location }}</p>
              <p v-if="se.description" class="text-sm opacity-50 italic">{{ se.description }}</p>
          </div>
        </div>
      </div>

      <CardSectionRSVP v-if="sectionId === 'rsvp'" :config="safeConfig" :event="event" />

      <div v-if="sectionId === 'footer'" class="py-20 w-full text-center opacity-30 text-[9px] uppercase tracking-[0.5em] border-t border-black/5" :style="{ color: theme.text, borderColor: theme.text + '1a' }">
        {{ safeConfig.content.footer_text || 'Fait avec amour • 2026' }}
      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;700&family=Inter:wght@300;400;700&family=Bodoni+Moda:ital,wght@0,400;0,700;1,400&family=Noto+Serif+JP:wght@300;400;700&display=swap');

.card-engine * { transition: color 0.3s ease, background-color 0.3s ease; }

/* Annuler le text-gray-900 global sur les titres */
.card-engine h1,
.card-engine h2,
.card-engine h3,
.card-engine h4,
.card-engine h5,
.card-engine h6 {
  color: inherit;
}

/* ── PRÉNOMS : couleur + taille ────────────────────────────────────────── */
.card-engine h1,
.card-engine .names,
.card-engine .main-names,
.card-engine .name-part,
.card-engine .template-title,
.card-engine .hero-names {
  color:     var(--names-color, inherit) !important;
  font-size: var(--names-size, '')       !important;
}

/* ── TITRES DE SECTION : couleur + taille ─────────────────────────────── */
.card-engine h2,
.card-engine h3,
.card-engine .section-title,
.card-engine .feature-title {
  color:     var(--title-color, inherit) !important;
  font-size: var(--title-size, '')       !important;
}

/* ── CORPS DU TEXTE : taille ───────────────────────────────────────────── */
.card-engine .template-body,
.card-engine .feature-body,
.card-engine .section-desc {
  font-size: var(--body-size, '') !important;
}
</style>
