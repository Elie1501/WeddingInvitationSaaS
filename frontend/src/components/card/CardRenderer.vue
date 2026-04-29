<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import CardSectionBanner from './CardSectionBanner.vue';
import CardTemplateOra from './CardTemplateOra.vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ 
      layout: 'arch',
      sections: ['hero', 'countdown', 'program', 'footer'],
      theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
      content: { names: 'Lui & Elle', date: '', location: '', message: '', image_url: '' },
      show_countdown: true,
      music_url: ''
    })
  },
  event: {
    type: Object,
    default: () => ({ groom_name: '', bride_name: '', date: '', location: '' })
  },
  subEvents: {
    type: Array,
    default: () => []
  },
  selectedBlock: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['select-block']);

// Moteur de sections : On ne se base QUE sur config.sections
const sections = computed(() => {
  if (props.config.sections && props.config.sections.length > 0) return props.config.sections;
  // Fallback par défaut si vide
  return ['hero', 'countdown', 'program', 'footer'];
});

const safeConfig = computed(() => {
  const defaults = {
    layout: 'arch',
    theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
    content: { 
      names: '', 
      image_url: '',
      footer_text: 'Fait avec amour • 2026'
    },
    show_countdown: true
  };
  
  return {
    ...defaults,
    ...props.config,
    theme: { ...defaults.theme, ...(props.config.theme || {}) },
    content: { ...defaults.content, ...(props.config.content || {}) }
  };
});

const displayData = computed(() => ({
  names: safeConfig.value.content?.names || `${props.event.groom_name || 'Lui'} & ${props.event.bride_name || 'Elle'}`,
  date: props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Date à venir',
  location: props.event.location || 'Lieu secret',
  image: safeConfig.value.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'
}));

// Logic de compte à rebours
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
</script>

<template>
  <div class="card-engine w-full flex flex-col items-center bg-white overflow-x-hidden pb-20 relative" 
       :style="{ 
         fontFamily: theme.fontFamily || 'Playfair Display',
         backgroundColor: theme.background || 'white'
       }">
    
    <div v-for="sectionId in sections" :key="sectionId" 
         @click="emit('select-block', sectionId)"
         class="w-full relative transition-all duration-300 cursor-pointer"
         :class="selectedBlock === sectionId ? 'ring-2 ring-[#C5A059] ring-inset z-50' : ''">
      
      <!-- HERO -->
      <CardSectionBanner v-if="sectionId === 'hero'" :layout="layout" :theme="theme" :displayData="displayData" />
      <CardTemplateOra v-if="sectionId === 'ora-hero'" :config="safeConfig" :event="event" mode="hero" />

      <!-- COUNTDOWN -->
      <div v-if="sectionId === 'countdown' && safeConfig.show_countdown" class="w-full py-20 px-8 text-center bg-white border-t border-gray-50 z-10 relative">
         <p class="text-[10px] font-black uppercase tracking-[0.4em] mb-10 opacity-30">Le grand décompte</p>
         <div class="flex justify-center space-x-8">
            <div v-for="(val, label) in { Jours:timeLeft.days, Heures:timeLeft.hours, Minutes:timeLeft.mins, Sec:timeLeft.secs }" :key="label" class="flex flex-col items-center">
               <span class="text-4xl font-light mb-1" :style="{ color: theme.accent }">{{ val }}</span>
               <span class="text-[8px] font-bold uppercase tracking-widest opacity-40">{{ label }}</span>
            </div>
         </div>
      </div>

      <!-- PROGRAMME -->
      <div v-if="sectionId === 'program'" class="w-full py-24 px-12 border-t border-gray-50 text-center space-y-16 z-10 relative" :class="'bg-[#F9F7F2]/50'">
        <div class="space-y-4">
          <h2 class="text-3xl uppercase tracking-widest font-light">Le Programme</h2>
          <div class="w-12 h-[1px] mx-auto bg-black/10"></div>
        </div>
        
        <div v-if="subEvents && subEvents.length > 0" class="space-y-12">
          <div v-for="(se, idx) in subEvents" :key="idx" class="relative">
            <div v-if="se.icon" class="text-3xl mb-4 transform hover:scale-110 transition-transform cursor-default">{{ se.icon }}</div>
            <p class="text-[10px] font-black uppercase tracking-[0.3em] text-[#C5A059] mb-2">{{ se.time }}</p>
            <h3 class="text-xl font-medium mb-1 italic">{{ se.title }}</h3>
            <p v-if="se.location" class="text-xs opacity-50 mb-2">{{ se.location }}</p>
            <p v-if="se.description" class="text-[11px] max-w-xs mx-auto opacity-40 leading-relaxed italic whitespace-pre-line">{{ se.description }}</p>
            <div v-if="idx < subEvents.length - 1" class="w-[1px] h-8 bg-black/5 mx-auto mt-12"></div>
          </div>
        </div>
        <div v-else class="py-10 border-2 border-dashed border-black/5 rounded-3xl">
           <p class="text-[10px] font-black uppercase tracking-widest opacity-20">Aucune étape définie</p>
        </div>
      </div>

      <!-- ORA SPECIFIC BLOCKS -->
      <CardTemplateOra v-if="sectionId === 'ora-section1'" :config="safeConfig" :event="event" mode="section1" />
      <CardTemplateOra v-if="sectionId === 'ora-parallax'" :config="safeConfig" :event="event" mode="parallax" />
      <CardTemplateOra v-if="sectionId === 'ora-section2'" :config="safeConfig" :event="event" mode="section2" />
      <CardTemplateOra v-if="sectionId === 'ora-tribute'" :config="safeConfig" :event="event" mode="tribute" />
      <CardTemplateOra v-if="sectionId === 'ora-gallery'" :config="safeConfig" :event="event" mode="gallery" />

      <!-- FOOTER -->
      <div v-if="sectionId === 'footer'" class="py-20 w-full text-center opacity-30 text-[9px] uppercase tracking-[0.5em] bg-white border-t border-gray-50 relative z-10">
        {{ safeConfig.content.footer_text || 'Fait avec amour • 2026' }}
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;700;900&family=Inter:wght@300;400;700&display=swap');
.card-engine::-webkit-scrollbar { display: none; }
.card-engine { -ms-overflow-style: none; scrollbar-width: none; }

/* Force font inheritance for all elements inside the card engine */
.card-engine, 
.card-engine *, 
.card-engine h1, 
.card-engine h2, 
.card-engine h3, 
.card-engine p, 
.card-engine span, 
.card-engine div, 
.card-engine a, 
.card-engine button, 
.card-engine input, 
.card-engine textarea {
  font-family: inherit !important;
}
</style>
