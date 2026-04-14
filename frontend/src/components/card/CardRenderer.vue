<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({ canvas: { width: 1080, height: 1920, background_color: '#ffffff' }, elements: [], theme: {}, show_countdown: true })
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

// Countdown Logic
const timeLeft = ref({ days: 0, hours: 0, mins: 0, secs: 0 });
let timer = null;

const updateCountdown = () => {
  if (!props.event?.date) return;
  const target = new Date(props.event.date).getTime();
  const now = new Date().getTime();
  const diff = target - now;

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

const logicalWidth = computed(() => props.config?.canvas?.width || 1080);
const logicalHeight = computed(() => props.config?.canvas?.height || 1920);

const aspectRatio = computed(() => (logicalHeight.value / logicalWidth.value) * 100);

const canvasStyle = computed(() => ({
  width: '100%',
  backgroundColor: props.config?.canvas?.background_color || '#ffffff',
  backgroundImage: props.config?.canvas?.background_image ? `url(${props.config.canvas.background_image})` : 'none',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  position: 'relative',
  display: 'flex',
  flexDirection: 'column',
  color: props.config?.theme?.primaryColor || '#000000',
  fontFamily: props.config?.theme?.fontFamily || 'serif',
  containerType: 'inline-size'
}));

const subEventsList = computed(() => (props.subEvents && props.subEvents.length > 0) ? props.subEvents : (props.config?.sub_events || []));

const getElementStyle = (el) => ({
  position: 'absolute',
  left: (el.x / logicalWidth.value * 100) + '%',
  top: (el.y / logicalHeight.value * 100) + '%',
  width: (el.width / logicalWidth.value * 100) + '%',
  height: (el.height / logicalHeight.value * 100) + '%',
  zIndex: el.zIndex || 10,
  ...el.style,
  clipPath: el.style?.mask === 'arch' ? 'inset(0% 0% 0% 0% round 500px 500px 0 0)' : 'none',
  fontSize: (parseFloat(el.style?.fontSize) / logicalWidth.value * 100) + 'cqi'
});

const formatContent = (content) => {
  if (typeof content !== 'string') return content;
  return content
    .replace(/{groom_name}/g, props.event?.groom_name || 'Marié')
    .replace(/{bride_name}/g, props.event?.bride_name || 'Mariée')
    .replace(/{date}/g, props.event?.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Date')
    .replace(/{location}/g, props.event?.location || 'Lieu');
};
</script>

<template>
  <div :style="canvasStyle" class="main-canvas mx-auto shadow-2xl">
    
    <!-- CANVAS CONTENT -->
    <div :style="{ position: 'relative', width: '100%', height: aspectRatio + 'cqi', overflow: 'hidden' }">
      <template v-for="el in config.elements" :key="el.id">
        <div :style="getElementStyle(el)">
          <div v-if="el.type === 'text'" class="w-full h-full flex items-center justify-center">
            <span :style="{ textAlign: 'center', width: '100%', whiteSpace: 'pre-line' }">{{ formatContent(el.content) }}</span>
          </div>
          <img v-else-if="el.type === 'image'" :src="el.content" class="w-full h-full object-cover" />
          <div v-else-if="el.type === 'shape'" class="w-full h-full" :style="el.style"></div>
        </div>
      </template>
    </div>

    <!-- COUNTDOWN SECTION -->
    <div v-if="event.date" class="py-12 px-6 text-center border-t border-b border-black/5">
       <p class="text-[10px] font-black uppercase tracking-[0.4em] mb-6 opacity-40">Compte à rebours</p>
       <div class="flex justify-center space-x-6">
          <div v-for="(val, label) in { Jours:timeLeft.days, Hrs:timeLeft.hours, Min:timeLeft.mins, Sec:timeLeft.secs }" :key="label" class="flex flex-col">
             <span class="text-3xl font-light">{{ val }}</span>
             <span class="text-[8px] font-bold uppercase tracking-widest opacity-40">{{ label }}</span>
          </div>
       </div>
    </div>

    <!-- ITINERARY SECTION -->
    <div v-if="subEventsList.length > 0" class="px-8 py-16 space-y-12">
      <div class="text-center space-y-3">
        <h3 class="text-3xl font-black tracking-tighter uppercase">Le Programme</h3>
        <div class="w-12 h-[2px] mx-auto bg-current opacity-20"></div>
      </div>
      <div class="space-y-12">
        <div v-for="(se, idx) in subEventsList" :key="idx" class="flex flex-col items-center text-center space-y-3">
          <span class="text-[10px] font-black uppercase tracking-[0.3em] opacity-30">{{ se.time }}</span>
          <h4 class="text-xl font-bold italic">{{ se.title }}</h4>
          <p class="text-[12px] opacity-60 max-w-[260px]">{{ se.location }}</p>
          <div v-if="idx < subEventsList.length - 1" class="w-[1px] h-10 bg-current opacity-10 mt-4"></div>
        </div>
      </div>
    </div>

    <!-- FOOTER INFO -->
    <div class="py-20 px-8 text-center bg-black/5 mt-10">
       <p class="text-[10px] font-bold uppercase tracking-widest opacity-40 mb-2">Lieu de réception</p>
       <p class="text-sm font-medium">{{ event.location }}</p>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;700&family=Montserrat:wght@300;400;900&display=swap');
.main-canvas { min-height: 100vh; }
</style>
