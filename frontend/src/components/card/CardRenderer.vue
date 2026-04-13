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

const showSplash = ref(props.showSplash !== null ? props.showSplash : (props.config?.has_cover_page && !props.isEditor));
const currentPageIndex = ref(props.activePageIndex); 

watch(() => props.showSplash, (newVal) => {
  if (newVal !== null) showSplash.value = newVal;
});

watch(() => props.activePageIndex, (newVal) => {
  currentPageIndex.value = newVal;
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
    
    if (props.config?.itinerary?.length > 0 && !sections.find(s => s.type === 'itinerary')) {
      sections.push({ type: 'itinerary', id: 'auto-itinerary' });
    }
  } else {
    sections = props.config?.pages?.[currentPageIndex.value - 1]?.sections || [];
  }
  return sections;
});

const templateStyles = computed(() => {
  const base = {
    fontFamily: props.config?.typography?.body || 'Inter, sans-serif',
    backgroundColor: activePageConfig.value.background_color,
    color: activePageConfig.value.text_color,
    transition: 'all 0.5s ease'
  };

  if (props.templateId === 'royal-gold') {
    return {
      ...base,
      fontFamily: "'Cormorant Garamond', serif",
      backgroundColor: '#0c0a09',
      color: '#f5f5f4',
      border: '1px solid #d4af37'
    };
  }
  if (props.templateId === 'bohemian-dream') {
    return {
      ...base,
      fontFamily: "'Montserrat', sans-serif",
      backgroundColor: '#fdf8f3',
      color: '#4a3728',
      backgroundImage: 'url("https://www.transparenttextures.com/patterns/natural-paper.png")'
    };
  }
  if (props.templateId === 'midnight-glamour') {
    return {
      ...base,
      fontFamily: "'Cormorant Garamond', serif",
      backgroundColor: '#020617',
      color: '#f8fafc',
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
  return base;
});
</script>

<template>
  <div :class="['relative w-full overflow-hidden min-h-[700px] flex flex-col', 'layout-' + templateId]" :style="templateStyles">
    
    <!-- Éléments décoratifs PREMIUM -->
    <div v-if="templateId === 'royal-gold'" class="absolute inset-0 pointer-events-none z-0 overflow-hidden">
       <div class="absolute -top-24 -left-24 w-64 h-64 border border-[#d4af37]/20 rounded-full"></div>
       <div class="absolute -bottom-24 -right-24 w-64 h-64 border border-[#d4af37]/20 rounded-full"></div>
    </div>

    <CardSplashScreen 
      v-if="forceSplash || (showSplash && config.has_cover_page)" 
      :event="event" 
      :config="config" 
      :templateId="templateId"
      :is-preview="forceSplash"
      @close="showSplash = false"
      @play-music="$emit('play-music')"
    />

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
        <div v-if="section.type === 'banner' && currentPageIndex === 0 && config?.show_countdown_invitation" class="py-16 px-4 flex justify-center w-full">
          <CardCountdown :targetDate="event.date" :themeColor="templateId === 'royal-gold' ? '#d4af37' : activePageConfig.accent_color" :templateId="templateId" />
        </div>
      </div>
    </div>

    <button 
      v-if="config.has_cover_page && !showSplash" 
      @click="showSplash = true" 
      class="fixed bottom-6 right-6 w-12 h-12 bg-white/90 shadow-2xl rounded-full flex items-center justify-center text-gray-400 hover:text-primary-600 transition-all z-40 border border-gray-100"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
    </button>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

/* Royal Gold */
.layout-royal-gold :deep(h1) {
  font-family: 'Great Vibes', cursive !important;
  @apply text-[#d4af37] text-7xl drop-shadow-[0_2px_2px_rgba(0,0,0,0.5)];
}
.layout-royal-gold :deep(.bg-neutral-50) {
  @apply bg-stone-900/50 border-stone-800 text-stone-200;
}

/* Bohemian Dream */
.layout-bohemian-dream :deep(h1) {
  font-family: 'Playfair Display', serif !important;
  @apply text-[#c46647] text-6xl italic;
}
.layout-bohemian-dream :deep(.bg-neutral-50) {
  @apply bg-[#fdf8f3] border-[#e6dcd3] text-[#4a3728];
}

/* Midnight Glamour */
.layout-midnight-glamour :deep(h1) {
  font-family: 'Cormorant Garamond', serif !important;
  @apply text-white text-6xl font-light tracking-widest;
}
</style>
