<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ 
      layout: 'arch',
      theme: { background: '#F9F7F2', accent: '#C5A059', text: '#1A1A1A', fontFamily: 'Playfair Display' },
      content: { names: 'Lui & Elle', date: '', location: '', message: '', image_url: '' },
      show_countdown: true,
      music_url: ''
    })
  },
  event: {
    type: Object,
    default: () => ({ groom_name: '', bride_name: '', date: '', location: '', title: '' })
  },
  subEvents: {
    type: Array,
    default: () => []
  }
});

// Sync des données pour l'affichage
const displayData = computed(() => ({
  names: `${props.event.groom_name || 'Lui'} & ${props.event.bride_name || 'Elle'}`,
  date: props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Date à venir',
  location: props.event.location || 'Lieu secret',
  message: props.config.content?.message || 'Nous nous marions !',
  image: props.config.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'
}));

// Countdown Logic - Sécurisée et réactive
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
  } else {
    timeLeft.value = { days: 0, hours: 0, mins: 0, secs: 0 };
  }
};

onMounted(() => {
  updateCountdown();
  timer = setInterval(updateCountdown, 1000);
});
onUnmounted(() => clearInterval(timer));

// Surveiller les changements de date pour mettre à jour le décompte
watch(() => props.event.date, updateCountdown);

const theme = computed(() => props.config.theme || {});
const layout = computed(() => props.config.layout || 'arch');
</script>

<template>
  <div class="card-engine w-full flex flex-col items-center bg-white overflow-x-hidden" :style="{ fontFamily: theme.fontFamily || 'Playfair Display' }">
    
    <!-- AUDIO -->
    <audio v-if="config.music_url" :src="config.music_url" autoplay loop class="hidden"></audio>

    <!-- CANVAS PRINCIPAL (Le visuel de la carte) -->
    <div class="main-canvas relative w-full aspect-[9/16] overflow-hidden shadow-2xl" :style="{ backgroundColor: theme.background || '#ffffff', color: theme.text || '#1A1A1A' }">
      
      <!-- LAYOUT 1 : L'ARCHE (Premium) -->
      <div v-if="layout === 'arch'" class="h-full flex flex-col items-center p-8 text-center relative justify-end">
        <div class="absolute top-12 w-[80%] aspect-[1/1.4] overflow-hidden shadow-2xl" style="border-radius: 1000px 1000px 0 0; border: 4px solid white;">
          <img :src="displayData.image" class="w-full h-full object-cover" />
        </div>
        <div class="relative z-10 w-full flex flex-col items-center bg-gradient-to-t from-[var(--bg-color)] via-[var(--bg-color)] to-transparent pt-32 pb-8 px-4" :style="{'--bg-color': theme.background}">
          <p class="text-[10px] uppercase tracking-[0.4em] mb-4" :style="{ color: theme.accent }">Save the Date</p>
          <h1 class="text-6xl font-light leading-none italic mb-8 drop-shadow-sm">{{ displayData.names }}</h1>
          <div class="w-12 h-[1px] mx-auto opacity-30 mb-6" :style="{ backgroundColor: theme.text }"></div>
          <p class="text-sm tracking-widest font-bold uppercase mb-1">{{ displayData.date }}</p>
          <p class="text-[10px] uppercase tracking-widest opacity-60">{{ displayData.location }}</p>
        </div>
      </div>

      <!-- LAYOUT 2 : EDITORIAL (Minimal) -->
      <div v-else-if="layout === 'typography-focus'" class="h-full flex flex-col p-10 relative overflow-hidden text-left justify-between" :style="{ backgroundColor: theme.background, color: theme.text }">
        <div class="absolute top-10 left-10 w-3/4 aspect-[4/5] overflow-hidden shadow-xl rounded-2xl opacity-90">
          <img :src="displayData.image" class="w-full h-full object-cover grayscale mix-blend-multiply" />
        </div>
        <div class="relative z-10 flex flex-col h-full justify-end pb-8 pt-48">
          <h1 class="text-[5.5rem] font-black tracking-tighter uppercase leading-[0.85] w-[120%] -ml-2 mix-blend-difference break-words">{{ displayData.names.replace(' & ', '&') }}</h1>
          <div class="mt-12 flex justify-between items-end border-t-2 pt-6" :style="{ borderColor: theme.text }">
            <div class="space-y-1">
              <p class="text-xs tracking-widest uppercase font-bold">{{ displayData.date }}</p>
              <p class="text-[9px] uppercase tracking-widest opacity-60">{{ displayData.location }}</p>
            </div>
            <div class="w-10 h-10 rounded-full border-2 flex items-center justify-center flex-shrink-0" :style="{ borderColor: theme.text }">
              <span class="text-[8px] font-bold">OUI</span>
            </div>
          </div>
        </div>
      </div>

      <!-- LAYOUT 3 : GLASSMORPHISM (Boho) -->
      <div v-else-if="layout === 'split'" class="h-full w-full relative flex items-center justify-center p-8">
        <div class="absolute inset-0">
          <img :src="displayData.image" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-black/20"></div>
        </div>
        <div class="relative z-10 w-full max-w-[90%] bg-white/20 backdrop-blur-xl border border-white/40 p-12 rounded-[2.5rem] text-center flex flex-col items-center space-y-8 shadow-2xl text-white">
          <p class="text-[9px] uppercase tracking-[0.4em] opacity-90 font-bold">Nous nous marions</p>
          <h1 class="text-5xl italic font-light drop-shadow-md leading-tight">{{ displayData.names }}</h1>
          <div class="w-12 h-[2px] bg-white/50 mx-auto"></div>
          <div class="space-y-3 pt-2">
            <p class="text-sm font-bold tracking-[0.2em] uppercase drop-shadow-sm">{{ displayData.date }}</p>
            <p class="text-[10px] uppercase tracking-widest opacity-80 font-medium">{{ displayData.location }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- COUNTDOWN SECTION - Toujours visible si activé -->
    <div v-if="config.show_countdown" class="w-full py-20 px-8 text-center bg-white border-t border-gray-50 z-10">
       <p class="text-[10px] font-black uppercase tracking-[0.4em] mb-10 opacity-30">Le grand décompte</p>
       <div class="flex justify-center space-x-8">
          <div v-for="(val, label) in { Jours:timeLeft.days, Heures:timeLeft.hours, Minutes:timeLeft.mins, Sec:timeLeft.secs }" :key="label" class="flex flex-col items-center">
             <span class="text-4xl font-light mb-1" :style="{ color: theme.accent }">{{ val }}</span>
             <span class="text-[8px] font-bold uppercase tracking-widest opacity-40">{{ label }}</span>
          </div>
       </div>
    </div>

    <!-- PROGRAM SECTION - Affichage garanti si données présentes -->
    <div v-if="subEvents && subEvents.length > 0" class="w-full py-24 px-12 bg-[#F9F7F2]/50 border-t border-gray-50 text-center space-y-16 z-10">
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

    <!-- FOOTER -->
    <div class="py-20 w-full text-center opacity-30 text-[9px] uppercase tracking-[0.5em] bg-white border-t border-gray-50">
      Fait avec amour • 2026
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;700;900&family=Inter:wght@300;400;700&display=swap');

.card-engine::-webkit-scrollbar { display: none; }
.card-engine { -ms-overflow-style: none; scrollbar-width: none; }
</style>
