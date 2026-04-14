<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import CardSectionBanner from './CardSectionBanner.vue';
import CardSectionDetails from './CardSectionDetails.vue';
import CardSectionText from './CardSectionText.vue';
import CardSectionItinerary from './CardSectionItinerary.vue';
import CardSectionGallery from './CardSectionGallery.vue';
import CardSplashScreen from './CardSplashScreen.vue';
import CardCountdown from './CardCountdown.vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ sections: [], pages: [], has_cover_page: false, colors: {}, typography: {}, media: {}, content: {} })
  },
  event: {
    type: Object,
    default: () => ({ groom_name: '', bride_name: '', date: '', location: '', title: '' })
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
  itinerary: CardSectionItinerary,
  gallery: CardSectionGallery
};

const internalShowSplash = ref(false);

// Calcul initial et synchronisation
const updateSplashVisibility = () => {
  if (props.forceSplash) {
    internalShowSplash.value = true;
  } else if (props.showSplash !== null) {
    internalShowSplash.value = props.showSplash;
  } else {
    internalShowSplash.value = (props.config?.has_cover_page && !props.isEditor);
  }
};

onMounted(updateSplashVisibility);

watch(() => [props.showSplash, props.forceSplash, props.config?.has_cover_page], updateSplashVisibility);

const currentPageIndex = ref(props.activePageIndex); 

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
  if (currentPageIndex.value <= 0) {
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
  const bg = activePageConfig.value.background_color;
  const text = activePageConfig.value.text_color;
  const accent = activePageConfig.value.accent_color;

  const base = {
    '--theme-bg': bg,
    '--theme-text': text,
    '--theme-accent': accent,
    '--theme-font-body': props.config?.typography?.body || 'Inter, sans-serif',
    '--theme-font-headings': props.config?.typography?.headings || 'Inter, sans-serif',
    backgroundColor: bg,
    color: text,
    fontFamily: 'var(--theme-font-body)',
  };

  // Specific Overrides for Premium Templates
  if (props.templateId === 'royal-gold') {
    return {
      ...base,
      backgroundColor: '#0c0a09',
      color: '#f5f5f4',
      '--theme-bg': '#0c0a09',
      '--theme-text': '#f5f5f4',
      '--theme-accent': '#d4af37',
      '--theme-font-headings': "'Great Vibes', cursive",
      '--theme-font-body': "'Cormorant Garamond', serif",
    };
  }
  if (props.templateId === 'bohemian-dream') {
    return {
      ...base,
      backgroundColor: '#fdf8f3',
      color: '#4a3728',
      '--theme-bg': '#fdf8f3',
      '--theme-text': '#4a3728',
      '--theme-accent': '#c46647',
      '--theme-font-headings': "'Playfair Display', serif",
      '--theme-font-body': "'Montserrat', sans-serif",
    };
  }
  if (props.templateId === 'midnight-glamour') {
    return {
      ...base,
      backgroundColor: '#020617',
      color: '#f8fafc',
      '--theme-bg': '#020617',
      '--theme-text': '#f8fafc',
      '--theme-accent': '#818cf8',
      '--theme-font-headings': "'Cormorant Garamond', serif",
      '--theme-font-body': "'Cormorant Garamond', serif",
    };
  }
  if (props.templateId === 'classic-elegance') {
    return {
      ...base,
      backgroundColor: '#fef3c7', 
      color: '#451a03',
      '--theme-bg': '#fef3c7', 
      '--theme-text': '#451a03',
      '--theme-accent': '#92400e',
      '--theme-font-headings': "'Playfair Display', serif",
      '--theme-font-body': "'Playfair Display', serif",
    };
  }
  
  return base;
});
</script>

<template>
  <div :class="['relative w-full overflow-hidden min-h-screen flex flex-col', 'layout-' + templateId]" :style="templateStyles">
    
    <!-- FONDS DÉCORATIFS SPÉCIFIQUES -->
    
    <!-- Royal Gold Background -->
    <div v-if="templateId === 'royal-gold'" class="absolute inset-0 z-0">
       <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-neutral-900 to-black"></div>
       <div class="absolute inset-10 border-[1px] border-[#d4af37]/20 rounded-lg pointer-events-none"></div>
       <div class="absolute inset-12 border-[2px] border-[#d4af37]/10 rounded-lg pointer-events-none"></div>
       <!-- Corners -->
       <div class="absolute top-0 left-0 w-48 h-48 opacity-40 bg-[url('https://www.transparenttextures.com/patterns/vintage-speckles.png')]"></div>
       <div class="absolute bottom-0 right-0 w-48 h-48 opacity-40 rotate-180 bg-[url('https://www.transparenttextures.com/patterns/vintage-speckles.png')]"></div>
    </div>

    <!-- Bohemian Dream Background -->
    <div v-if="templateId === 'bohemian-dream'" class="absolute inset-0 z-0">
       <div class="absolute inset-0 bg-[#fdf8f3]"></div>
       <div class="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/natural-paper.png')] opacity-50"></div>
       <!-- Abstract blobs -->
       <div class="absolute -top-24 -left-24 w-96 h-96 bg-[#e6dcd3]/30 rounded-full blur-3xl"></div>
       <div class="absolute -bottom-24 -right-24 w-96 h-96 bg-[#c46647]/10 rounded-full blur-3xl"></div>
    </div>

    <!-- Midnight Glamour Background -->
    <div v-if="templateId === 'midnight-glamour'" class="absolute inset-0 z-0">
       <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950"></div>
       <div class="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20"></div>
       <!-- Animated glow -->
       <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[120px] animate-pulse"></div>
    </div>

    <!-- Classic Elegance Background -->
    <div v-if="templateId === 'classic-elegance'" class="absolute inset-0 z-0">
       <div class="absolute inset-0 bg-[#fef3c7]"></div>
       <div class="absolute inset-8 border border-[#92400e]/10"></div>
       <div class="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-32 opacity-10">
         <svg viewBox="0 0 100 50" fill="currentColor" class="text-[#92400e]"><path d="M0 0 Q50 50 100 0 L100 10 Q50 60 0 10 Z"/></svg>
       </div>
    </div>

    <!-- SPLASH SCREEN -->
    <CardSplashScreen 
      v-if="internalShowSplash && (config.has_cover_page || isEditor)" 
      :event="event" 
      :config="config" 
      :templateId="templateId"
      :isPreview="isEditor && internalShowSplash"
      @close="internalShowSplash = false"
      @play-music="$emit('play-music')"
    />

    <!-- NAVIGATION -->
    <nav v-if="config.pages && config.pages.length > 0 && (!internalShowSplash || isEditor)" 
         class="relative z-30 flex justify-center bg-white/10 backdrop-blur-md border-b border-white/10 sticky top-0 overflow-x-auto no-scrollbar">
      <button 
        @click="currentPageIndex = 0"
        :class="currentPageIndex === 0 ? 'text-white border-b-2 border-accent' : 'text-white/60'"
        class="px-8 py-5 text-[10px] font-bold uppercase tracking-[0.3em] transition-all"
        :style="currentPageIndex === 0 ? { borderBottomColor: 'var(--theme-accent)' } : {}"
      >
        L'Invitation
      </button>
      <button 
        v-for="(page, idx) in config.pages" 
        :key="page.id"
        @click="currentPageIndex = idx + 1"
        :class="currentPageIndex === idx + 1 ? 'text-white border-b-2' : 'text-white/60'"
        class="px-8 py-5 text-[10px] font-bold uppercase tracking-[0.3em] transition-all border-transparent"
        :style="currentPageIndex === idx + 1 ? { borderBottomColor: 'var(--theme-accent)' } : {}"
      >
        {{ page.title }}
      </button>
    </nav>

    <!-- MAIN CONTENT -->
    <main v-if="!internalShowSplash || isEditor" class="relative z-10 flex-1 flex flex-col items-center w-full">
      
      <!-- ARCHITECTURE RADICALE PAR THÈME -->
      
      <!-- 1. ROYAL GOLD : Centré, Majestueux, Espacé -->
      <div v-if="templateId === 'royal-gold'" class="w-full max-w-3xl px-6 py-24 space-y-32">
        <div v-for="section in activeSections" :key="section.id" class="relative">
          <div class="absolute -left-8 top-0 bottom-0 w-[1px] bg-gradient-to-b from-transparent via-[#d4af37]/30 to-transparent"></div>
          <component
            :is="componentsMap[section.type]"
            :section="section"
            :event="event"
            :config="{...config, colors: {...config.colors, accent: 'var(--theme-accent)'}, activePageIndex: currentPageIndex, templateId: templateId}"
          />
          <div v-if="section.type === 'banner'" class="mt-16">
             <CardCountdown :targetDate="event.date" themeColor="#d4af37" :templateId="templateId" />
          </div>
        </div>
      </div>

      <!-- 2. BOHEMIAN DREAM : Organique, Cartes flottantes, Asymétrique -->
      <div v-if="templateId === 'bohemian-dream'" class="w-full max-w-5xl px-6 py-12 grid grid-cols-1 gap-12">
        <div v-for="(section, idx) in activeSections" :key="section.id" 
             :class="[
               'bg-white/60 backdrop-blur-sm rounded-[3rem] p-8 md:p-16 border border-[#e6dcd3] shadow-xl shadow-stone-200/50',
               idx % 2 === 0 ? 'md:ml-12' : 'md:mr-12'
             ]">
          <component
            :is="componentsMap[section.type]"
            :section="section"
            :event="event"
            :config="{...config, colors: {...config.colors, accent: 'var(--theme-accent)'}, activePageIndex: currentPageIndex, templateId: templateId}"
          />
        </div>
      </div>

      <!-- 3. MIDNIGHT GLAMOUR : Moderne, Full Width, Néon Soft -->
      <div v-if="templateId === 'midnight-glamour'" class="w-full space-y-0">
        <div v-for="section in activeSections" :key="section.id" class="w-full">
          <div :class="section.type === 'banner' ? 'h-screen' : 'py-24 max-w-5xl mx-auto px-6'">
            <component
              :is="componentsMap[section.type]"
              :section="section"
              :event="event"
              :config="{...config, colors: {...config.colors, accent: 'var(--theme-accent)'}, activePageIndex: currentPageIndex, templateId: templateId}"
            />
          </div>
        </div>
      </div>

      <!-- 4. MODERN CHIC : Typographie XXL, Grille Brutaliste -->
      <div v-if="templateId === 'modern-chic'" class="w-full max-w-6xl px-6 py-12 flex flex-col">
        <div v-for="section in activeSections" :key="section.id" class="border-b border-black/5 py-16">
          <component
            :is="componentsMap[section.type]"
            :section="section"
            :event="event"
            :config="{...config, colors: {...config.colors, accent: 'var(--theme-accent)'}, activePageIndex: currentPageIndex, templateId: templateId}"
          />
        </div>
      </div>

      <!-- 5. CLASSIC ELEGANCE : Traditionnel, Centré, Décoratif -->
      <div v-if="templateId === 'classic-elegance' || !['royal-gold', 'bohemian-dream', 'midnight-glamour', 'modern-chic'].includes(templateId)" 
           class="w-full max-w-2xl px-6 py-24 space-y-24 text-center">
        <div v-for="section in activeSections" :key="section.id" class="border-t border-[#92400e]/10 pt-16 first:border-t-0 first:pt-0">
          <component
            :is="componentsMap[section.type]"
            :section="section"
            :event="event"
            :config="{...config, colors: {...config.colors, accent: 'var(--theme-accent)'}, activePageIndex: currentPageIndex, templateId: templateId}"
          />
        </div>
      </div>

    </main>

    <!-- Editor Overlay (if needed) -->
    <div v-if="isEditor" class="absolute inset-0 pointer-events-none border-4 border-primary-500/20 z-50"></div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

h1, h2, h3 {
  font-family: var(--theme-font-headings);
}

/* Animations globale */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.animate-fade-in { animation: fadeIn 1.5s ease-out; }

/* Styles spécifiques injectés */
:deep(h1) { color: var(--theme-accent); }
:deep(.section-title) { font-family: var(--theme-font-headings); color: var(--theme-accent); }

/* Overrides de composants de section pour les thèmes */

/* Layout specific adjustments */
.layout-royal-gold :deep(.banner-img) { border: 8px solid #d4af37/20; padding: 10px; }
.layout-midnight-glamour :deep(.text-content) { text-shadow: 0 0 20px rgba(129, 140, 248, 0.3); }

/* Modern Chic radical adjustments */
.layout-modern-chic :deep(h1) {
  @apply text-7xl md:text-[12rem] font-black uppercase tracking-tighter leading-none;
}
</style>
