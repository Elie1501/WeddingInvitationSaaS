<script setup>
import { ref, computed, watch } from 'vue';
import CardSectionBanner from './CardSectionBanner.vue';
import CardSectionDetails from './CardSectionDetails.vue';
import CardSectionText from './CardSectionText.vue';
import CardSectionItinerary from './CardSectionItinerary.vue';
import CardSplashScreen from './CardSplashScreen.vue';
import CardCountdown from './CardCountdown.vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ sections: [], pages: [], has_cover_page: false, colors: {}, typography: {} })
  },
  event: {
    type: Object,
    required: true
  },
  templateId: {
    type: String,
    default: 'modern-chic'
  },
  activePageIndex: {
    type: Number,
    default: 0
  },
  forceSplash: {
    type: Boolean,
    default: false
  },
  isEditor: {
    type: Boolean,
    default: false
  },
  showSplash: {
    type: Boolean,
    default: null
  }
});

const componentsMap = {
  banner: CardSectionBanner,
  details: CardSectionDetails,
  text: CardSectionText,
  itinerary: CardSectionItinerary
};

// Sur le site public (!isEditor), on montre la couverture au début si elle est activée
const showSplash = ref(props.showSplash !== null ? props.showSplash : (props.config?.has_cover_page && !props.isEditor));
const currentPageIndex = ref(props.activePageIndex); 

watch(() => props.showSplash, (newVal) => {
  if (newVal !== null) showSplash.value = newVal;
});

watch(() => props.activePageIndex, (newVal) => {
  currentPageIndex.value = newVal;
});

watch(() => props.forceSplash, (newVal) => {
  if (newVal) showSplash.value = true;
  else if (props.isEditor) showSplash.value = false;
});

watch(() => props.config.has_cover_page, (newVal) => {
  if (!props.isEditor) showSplash.value = newVal;
});

const activePageConfig = computed(() => {
  if (currentPageIndex.value === 0) {
    return {
      title: 'Invitation',
      background_color: props.config?.colors?.background || '#ffffff',
      text_color: props.config?.colors?.text || '#1f2937',
      accent_color: props.config?.colors?.accent || '#4f46e5'
    };
  } else {
    const p = props.config?.pages?.[currentPageIndex.value - 1];
    return {
      title: p?.title || 'Page',
      background_color: p?.background_color || props.config?.colors?.background || '#ffffff',
      text_color: p?.text_color || props.config?.colors?.text || '#1f2937',
      accent_color: p?.accent_color || props.config?.colors?.accent || '#4f46e5'
    };
  }
});

const activeSections = computed(() => {
  let sections = [];
  if (currentPageIndex.value === 0) {
    sections = [...(props.config?.sections || [
      { type: 'banner', id: 'default-banner' },
      { type: 'text', id: 'default-text' },
      { type: 'details', id: 'default-details' }
    ])];
    
    // Auto-ajouter l'itinéraire s'il existe et n'est pas déjà dans les sections
    if (props.config?.itinerary?.length > 0 && !sections.find(s => s.type === 'itinerary')) {
      sections.push({ type: 'itinerary', id: 'auto-itinerary' });
    }
  } else {
    sections = props.config?.pages?.[currentPageIndex.value - 1]?.sections || [];
  }
  return sections;
});

const layoutClass = computed(() => `layout-${props.templateId}`);

const templateStyles = computed(() => {
  const base = {
    fontFamily: props.config?.typography?.body || 'sans-serif',
    backgroundColor: activePageConfig.value.background_color,
    color: activePageConfig.value.text_color,
    transition: 'all 0.5s ease'
  };

  if (props.templateId === 'romantic-pink') {
    return {
      ...base,
      fontFamily: "'Great Vibes', cursive",
      backgroundColor: '#fff1f2', 
      color: '#881337', 
      backgroundImage: 'linear-gradient(135deg, #ffe4e6 0%, #fff1f2 100%)',
    };
  }
  if (props.templateId === 'classic-elegance') {
    return {
      ...base,
      fontFamily: "'Playfair Display', serif",
      backgroundColor: '#fef3c7', 
      color: '#451a03',
      backgroundImage: 'url("https://www.transparenttextures.com/patterns/cream-paper.png")',
    };
  }
  if (props.templateId === 'luxury-minimal') {
    return {
      ...base,
      fontFamily: "'Montserrat', sans-serif",
      backgroundColor: '#000000',
      color: '#ffffff',
      border: '20px solid #ffffff',
      letterSpacing: '0.2em'
    };
  }
  return base;
});
</script>

<template>
  <div :class="['relative w-full overflow-hidden min-h-[700px] flex flex-col', 'layout-' + templateId]" :style="templateStyles">
    <!-- Overlay Floral pour le thème jardin -->
    <div v-if="templateId === 'romantic-pink'" class="absolute inset-0 pointer-events-none opacity-20 z-0 bg-[url('https://www.transparenttextures.com/patterns/vintage-speckle.png')]"></div>
    
    <CardSplashScreen 
      v-if="forceSplash || (showSplash && config.has_cover_page)" 
      :event="event" 
      :config="config" 
      :templateId="templateId"
      :is-preview="forceSplash"
      @close="showSplash = false"
      @play-music="$emit('play-music')"
    />

    <!-- Navigation Inter-pages améliorée -->
    <nav v-if="config.pages && config.pages.length > 0" class="flex border-b border-black/5 bg-white/60 backdrop-blur-md sticky top-0 z-30 overflow-x-auto no-scrollbar">
      <button 
        @click="currentPageIndex = 0"
        :style="currentPageIndex === 0 ? { borderBottomColor: activePageConfig.accent_color, color: activePageConfig.accent_color } : {}"
        class="flex-none px-6 py-4 text-[10px] font-bold uppercase tracking-[0.2em] transition-all border-b-2"
      >
        L'Invitation
      </button>
      <button 
        v-for="(page, idx) in config.pages" 
        :key="page.id"
        @click="currentPageIndex = idx + 1"
        :style="currentPageIndex === idx + 1 ? { borderBottomColor: activePageConfig.accent_color, color: activePageConfig.accent_color } : {}"
        class="flex-none px-6 py-4 text-[10px] font-bold uppercase tracking-[0.2em] transition-all border-b-2 border-transparent"
      >
        {{ page.title }}
      </button>
    </nav>

    <div v-if="!showSplash || isEditor" class="flex-1 relative z-10 flex flex-col items-center w-full">
      <div v-for="section in activeSections" :key="section.id" class="w-full">
        <component
          :is="componentsMap[section.type]"
          :section="section"
          :event="event"
          :config="{...config, colors: {...config.colors, accent: activePageConfig.accent_color}, activePageIndex: currentPageIndex, templateId: templateId}"
          class="w-full"
        />
        <!-- Compte à rebours dynamique -->
        <div v-if="section.type === 'banner' && currentPageIndex === 0 && config?.show_countdown_invitation" class="py-16 px-4 flex justify-center w-full">
          <CardCountdown :targetDate="event.date" :themeColor="templateId === 'luxury-minimal' ? '#ffffff' : activePageConfig.accent_color" :templateId="templateId" />
        </div>
      </div>
    </div>

    <!-- Petit bouton flottant pour revoir la couverture -->
    <button 
      v-if="config.has_cover_page && !showSplash" 
      @click="showSplash = true" 
      class="fixed bottom-6 right-6 w-12 h-12 bg-white/90 shadow-2xl rounded-full flex items-center justify-center text-gray-400 hover:text-primary-600 transition-all z-40 border border-gray-100"
      title="Voir la page de garde"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
    </button>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

/* Template Romantic Pink */
.layout-romantic-pink {
  @apply text-rose-900;
}
.layout-romantic-pink :deep(h1) {
  font-family: 'Great Vibes', cursive !important;
  @apply text-rose-600 text-6xl drop-shadow-sm;
}
.layout-romantic-pink :deep(.bg-primary-50\/50) {
  @apply bg-rose-100/50 border-rose-200;
}
.layout-romantic-pink :deep(button) {
  @apply bg-rose-600 text-white shadow-rose-200;
}

/* Template Classic Elegance */
.layout-classic-elegance :deep(h1) {
  font-family: 'Playfair Display', serif !important;
  @apply text-stone-800 text-5xl italic;
}
.layout-classic-elegance :deep(.bg-primary-50\/50) {
  @apply bg-stone-100 border-stone-200;
}

/* Template Modern Chic (Default) */
.layout-modern-chic :deep(h1) {
  @apply uppercase tracking-[0.3em] font-light text-3xl text-gray-900;
}

/* Template Luxury Minimal */
.layout-luxury-minimal :deep(h1) {
  @apply uppercase tracking-[0.5em] font-bold text-2xl text-black;
}
.layout-luxury-minimal :deep(.bg-primary-50\/50) {
  @apply bg-gray-50 border-gray-100 rounded-none;
}
</style>
