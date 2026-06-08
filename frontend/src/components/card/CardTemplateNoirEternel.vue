<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

// --- CONFIG & FALLBACKS ---
const content = computed(() => props.config.content || {});
const names = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);

// --- ANIMATION NOMS (Lettre par lettre) ---
const displayedNames = ref([]);
const pendingTimeouts = [];

const runNameAnimation = (text) => {
  pendingTimeouts.forEach(clearTimeout);
  pendingTimeouts.length = 0;
  displayedNames.value = [];
  text.split('').forEach((char, i) => {
    pendingTimeouts.push(setTimeout(() => { displayedNames.value.push(char); }, i * 80));
  });
};

onMounted(() => {
  runNameAnimation(names.value);
  initCanvas();
});

watch(names, (val) => runNameAnimation(val));

// --- PARTICULES CANVAS ---
const canvasRef = ref(null);
let raf;
const initCanvas = () => {
  if (window.matchMedia('(max-width: 768px)').matches || !canvasRef.value) return;
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const parent = canvas.parentElement;
  canvas.width = parent ? parent.offsetWidth : window.innerWidth;
  canvas.height = parent ? parent.offsetHeight : window.innerHeight;

  const particles = Array.from({ length: 60 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 2 + 1,
    speed: Math.random() * 0.5 + 0.2,
    opacity: Math.random() * 0.4 + 0.3
  }));

  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      ctx.fillStyle = `rgba(201, 168, 76, ${p.opacity})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      p.y -= p.speed;
      if (p.y < -10) p.y = canvas.height + 10;
    });
    raf = requestAnimationFrame(draw);
  };
  draw();
};

onUnmounted(() => {
  cancelAnimationFrame(raf);
  pendingTimeouts.forEach(clearTimeout);
});

// Contraste : #F5E6C8 sur #0A0A0A = ratio 15.2:1 (Exceptionnel AAA)
</script>

<template>
  <div class="hero-container relative h-screen bg-[#0A0A0A] overflow-hidden flex items-center justify-center">
    <canvas ref="canvasRef" class="absolute inset-0 z-0 pointer-events-none opacity-40"></canvas>
    
    <!-- Grain SVG Filter -->
    <svg class="hidden"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>
    <div class="absolute inset-0 pointer-events-none z-10 opacity-[0.04]" style="filter: url(#noise)"></div>
    <div class="vignette absolute inset-0 pointer-events-none z-20"></div>

    <div class="relative z-30 text-center space-y-12 px-6">
      <div class="monogram font-serif tracking-[0.5em] text-gold uppercase opacity-80 text-sm md:text-base">
        {{ content.monogram || 'E & L' }}
      </div>

      <h1 class="template-title font-serif italic text-[#F5E6C8]">
        <span v-for="(c, i) in displayedNames" :key="i" class="animate-letter">{{ c }}</span>
      </h1>

      <div class="divider w-24 h-[1px] bg-gold opacity-30 mx-auto"></div>

      <p class="template-body max-w-2xl mx-auto text-[#F5E6C8] font-serif italic">
        {{ content.intro_text || 'Nous vous convions à célébrer l’éternité d’un instant.' }}
      </p>

      <div class="info-block space-y-4">
        <p class="template-label text-gold">{{ content.date_display || '15 JUIN 2026' }}</p>
        <p v-if="content.address" class="template-label text-[#F5E6C8]">{{ content.address }}</p>
      </div>

      <div class="text-2xl pt-12 animate-pulse">{{ content.divider_symbol || '✦' }}</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Cormorant+Garamond:ital,wght@1,300&family=Playfair+Display:ital,wght@1,400&display=swap');

.hero-container { --gold: #C9A84C; }
.text-gold { color: var(--gold); }
.vignette { background: radial-gradient(circle, transparent 40%, rgba(0,0,0,0.8) 100%); }

.template-title { font-size: clamp(2.5rem, 12vw, 6rem); line-height: 1.1; }
.template-body  { font-size: clamp(1rem, 3vw, 1.4rem); }
.template-label { font-family: 'Cinzel', serif; letter-spacing: 0.3em; font-size: 0.7rem; }

.animate-letter { animation: fadeIn 0.5s forwards; opacity: 0; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
