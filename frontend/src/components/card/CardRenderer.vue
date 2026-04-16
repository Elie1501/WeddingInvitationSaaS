<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import CardSectionBanner from './CardSectionBanner.vue';
import CardTemplateOra from './CardTemplateOra.vue';
import CardTemplateES from './CardTemplateES.vue';
import CardTemplateEY from './CardTemplateEY.vue';

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

const displayData = computed(() => ({
  names: props.config.content?.names || `${props.event.groom_name || 'Lui'} & ${props.event.bride_name || 'Elle'}`,
  date: props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Date à venir',
  location: props.event.location || 'Lieu secret',
  image: props.config.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'
}));

// Logic de compte à rebours
const timeLeft = ref({ days: 0, hours: 0, mins: 0, secs: 0 });
let timer = null;
const updateCountdown = () => {
  const dateToUse = props.event?.date || props.config?.content?.date;
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

const theme = computed(() => props.config.theme || {});
const layout = computed(() => props.config.layout || 'arch');
</script>

<template>
  <div class="card-engine w-full flex flex-col items-center bg-white overflow-x-hidden pb-20 relative" 
       :style="{ 
         fontFamily: theme.fontFamily || 'Playfair Display',
         backgroundColor: theme.background || 'white'
       }">
    
    <audio v-if="config.music_url" :src="config.music_url" autoplay loop class="hidden"></audio>

    <div v-for="sectionId in sections" :key="sectionId" 
         @click="emit('select-block', sectionId)"
         class="w-full relative transition-all duration-300 cursor-pointer"
         :class="selectedBlock === sectionId ? 'ring-2 ring-[#C5A059] ring-inset z-50' : ''">
      
      <!-- HERO -->
      <CardSectionBanner v-if="sectionId === 'hero'" :layout="layout" :theme="theme" :displayData="displayData" />
      <CardTemplateOra v-if="sectionId === 'ora-hero'" :config="config" :event="event" mode="hero" />

      <!-- COUNTDOWN -->
      <div v-if="sectionId === 'countdown' && config.show_countdown" class="w-full py-20 px-8 text-center bg-white border-t border-gray-50 z-10 relative">
         <p class="text-[10px] font-black uppercase tracking-[0.4em] mb-10 opacity-30">Le grand décompte</p>
         <div class="flex justify-center space-x-8">
            <div v-for="(val, label) in { Jours:timeLeft.days, Heures:timeLeft.hours, Minutes:timeLeft.mins, Sec:timeLeft.secs }" :key="label" class="flex flex-col items-center">
               <span class="text-4xl font-light mb-1" :style="{ color: theme.accent }">{{ val }}</span>
               <span class="text-[8px] font-bold uppercase tracking-widest opacity-40">{{ label }}</span>
            </div>
         </div>
      </div>

      <!-- PROGRAMME -->
      <div v-if="sectionId === 'program' && subEvents && subEvents.length > 0" class="w-full py-24 px-12 border-t border-gray-50 text-center space-y-16 z-10 relative" :class="'bg-[#F9F7F2]/50'">
        <div class="space-y-4">
          <h2 class="text-3xl uppercase tracking-widest font-light">Le Programme</h2>
          <div class="w-12 h-[1px] mx-auto bg-black/10"></div>
        </div>
        <div class="space-y-12">
          <div v-for="(se, idx) in subEvents" :key="idx" class="relative">
            <p class="text-[10px] font-black uppercase tracking-[0.3em] text-[#C5A059] mb-2">{{ se.time }}</p>
            <h3 class="text-xl font-medium mb-1 italic">{{ se.title }}</h3>
            <p class="text-xs opacity-50">{{ se.location }}</p>
            <div v-if="idx < subEvents.length - 1" class="w-[1px] h-8 bg-black/5 mx-auto mt-12"></div>
          </div>
        </div>
      </div>

      <!-- ORA SPECIFIC BLOCKS -->
      <CardTemplateOra v-if="sectionId === 'ora-section1'" :config="config" :event="event" mode="section1" />
      <CardTemplateOra v-if="sectionId === 'ora-parallax'" :config="config" :event="event" mode="parallax" />
      <CardTemplateOra v-if="sectionId === 'ora-section2'" :config="config" :event="event" mode="section2" />
      <CardTemplateOra v-if="sectionId === 'ora-tribute'" :config="config" :event="event" mode="tribute" />
      <CardTemplateOra v-if="sectionId === 'ora-gallery'" :config="config" :event="event" mode="gallery" />

      <!-- ES SPECIFIC BLOCKS -->
      <CardTemplateES v-if="sectionId === 'es-hero'" :config="config" :event="event" mode="es-hero" />
      <CardTemplateES v-if="sectionId === 'es-intro'" :config="config" :event="event" mode="es-intro" />
      <CardTemplateES v-if="sectionId === 'es-details'" :config="config" :event="event" mode="es-details" />
      <CardTemplateES v-if="sectionId === 'es-footer'" :config="config" :event="event" mode="es-footer" />

      <!-- FOOTER -->
      <div v-if="sectionId === 'footer'" class="py-20 w-full text-center opacity-30 text-[9px] uppercase tracking-[0.5em] bg-white border-t border-gray-50 relative z-10">
        {{ config.content.footer_text || 'Fait avec amour • 2026' }}
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;700;900&family=Inter:wght@300;400;700&display=swap');
.card-engine::-webkit-scrollbar { display: none; }
.card-engine { -ms-overflow-style: none; scrollbar-width: none; }
</style>
