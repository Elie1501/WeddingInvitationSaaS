<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true },
  mode:   { type: String, default: 'full' }
});

const theme = computed(() => {
  const bgColor = props.config.theme?.background || '#080808';
  return {
    bg: bgColor,
    text: props.config.theme?.text || getContrastColor(bgColor),
    accent: props.config.theme?.accent || '#D4853A',
  };
});

const displayNames = computed(() =>
  props.config.content?.names ||
  (props.event.groom_name && props.event.bride_name ? `${props.event.groom_name} & ${props.event.bride_name}` : ''));
const displayDate = computed(() =>
  props.config.content?.date_display ||
  (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 juin 2026'));
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');
const year = computed(() => (displayDate.value.match(/\d{4}/) || ['2026'])[0]);

// Révélation lettre par lettre du titre
const chars = ref([]);
const cursor = ref(true);
let timers = [];
const reveal = (text) => {
  chars.value = []; timers.forEach(clearTimeout); timers = [];
  [...text].forEach((ch, i) => {
    timers.push(setTimeout(() => {
      chars.value.push(ch);
      if (i === text.length - 1) cursor.value = false;
    }, 800 + i * 70));
  });
};

// Grain animé
const canvasRef = ref(null);
let raf = null;
const drawGrain = () => {
  const c = canvasRef.value;
  if (!c) return;
  const ctx = c.getContext('2d');
  c.width = c.offsetWidth || 390; c.height = c.offsetHeight || 700;
  const img = ctx.createImageData(c.width, c.height);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = (Math.random() * 70) | 0;
    img.data[i] = img.data[i+1] = img.data[i+2] = v;
    img.data[i+3] = (Math.random() * 30) | 0;
  }
  ctx.putImageData(img, 0, 0);
  raf = requestAnimationFrame(drawGrain);
};

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => { isLoaded.value = true; reveal(displayNames.value); }, 400);
  drawGrain();
});
onUnmounted(() => { cancelAnimationFrame(raf); timers.forEach(clearTimeout); });
</script>

<template>
  <div class="cin-wrap">
    <!-- Photo de fond floutée -->
    <div v-if="config.content?.image_url" class="cin-bg" :style="{ backgroundImage: `url(${config.content.image_url})` }" aria-hidden="true"></div>
    <div class="cin-veil" aria-hidden="true"></div>
    <canvas ref="canvasRef" class="cin-grain" aria-hidden="true"></canvas>

    <!-- Balayage lumineux du projecteur -->
    <div class="cin-sweep" aria-hidden="true"></div>

    <!-- Letterbox -->
    <div class="cin-bar top"><span class="rec" :class="{ on: isLoaded }">● REC</span><span class="tc">00:01:{{ year.slice(-2) }}</span></div>
    <div class="cin-bar bottom"></div>

    <div class="cin-content" :class="{ reveal: isLoaded }">
      <p class="cin-eyebrow">L'amour présente</p>
      <h1 class="cin-title main-title" :aria-label="displayNames">
        <span v-for="(ch, i) in chars" :key="i">{{ ch }}</span><span v-if="cursor" class="cin-cursor">_</span>
      </h1>
      <div class="cin-line"></div>
      <p class="cin-meta">UN FILM DE {{ year }}</p>
      <p class="cin-date">{{ displayDate }}</p>
      <p v-if="displayLocation" class="cin-loc">{{ displayLocation }}</p>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Courier+Prime:wght@400;700&display=swap');

.cin-wrap {
  position: relative;
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: var(--color-bg, #080808);
  color: var(--color-text, #F0EAE0);
  font-family: var(--card-font, 'Courier Prime'), monospace;
  overflow: clip;
  text-align: center;
}

.cin-bg {
  position: absolute; inset: 0; z-index: 0;
  background-size: cover; background-position: center;
  filter: grayscale(0.7) brightness(0.35) contrast(1.15);
  transform: scale(1.04);
}
.cin-veil {
  position: absolute; inset: 0; z-index: 1;
  background: radial-gradient(ellipse 75% 75% at 50% 50%, transparent 15%, color-mix(in srgb, var(--color-bg, #080808) 92%, #000) 100%);
}
.cin-grain { position: absolute; inset: 0; z-index: 2; width: 100%; height: 100%; pointer-events: none; mix-blend-mode: overlay; opacity: 0.5; }

.cin-sweep {
  position: absolute; top: 0; bottom: 0; width: 60%; z-index: 2; pointer-events: none;
  background: linear-gradient(100deg, transparent, color-mix(in srgb, var(--color-countdown, #D4853A) 10%, transparent), transparent);
  animation: sweep 9s ease-in-out infinite;
}
@keyframes sweep { 0% { transform: translateX(-120%); } 60%,100% { transform: translateX(220%); } }

/* Letterbox */
.cin-bar {
  position: absolute; left: 0; right: 0; height: clamp(34px, 9cqi, 56px);
  background: #000; z-index: 5; display: flex; align-items: center; justify-content: space-between;
  padding: 0 16px;
  font-size: clamp(0.5rem, 2cqi, 0.62rem); letter-spacing: 0.3em; color: rgba(255,255,255,0.5);
}
.cin-bar.top { top: 0; }
.cin-bar.bottom { bottom: 0; }
.rec { color: var(--color-countdown, #D4853A); opacity: 0; }
.rec.on { animation: blink 1.4s step-end infinite; }
@keyframes blink { 50% { opacity: 0.25; } 0%,100% { opacity: 1; } }
.tc { font-variant-numeric: tabular-nums; }

.cin-content { position: relative; z-index: 4; padding: 0 clamp(28px, 8cqi, 56px); opacity: 0; transform: translateY(16px); transition: opacity 1.4s ease-out, transform 1.4s ease-out; }
.cin-content.reveal { opacity: 1; transform: translateY(0); }

.cin-eyebrow {
  font-size: clamp(0.55rem, 2.2cqi, 0.68rem); letter-spacing: 0.5em; text-transform: uppercase;
  color: var(--color-countdown, #D4853A); opacity: 0.85; margin-bottom: 22px;
}
.cin-title {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: var(--size-names, clamp(3rem, 18cqi, 8rem));
  letter-spacing: 0.06em; line-height: 0.92;
  color: var(--color-names, #FFFFFF);
  text-shadow: 0 0 90px color-mix(in srgb, var(--color-countdown, #D4853A) 30%, transparent);
}
.cin-cursor { color: var(--color-countdown, #D4853A); animation: blink 0.9s step-end infinite; }
.cin-line { width: 90px; height: 1px; background: var(--color-countdown, #D4853A); margin: clamp(18px,5cqi,28px) auto; opacity: 0.6; }
.cin-meta { font-size: clamp(0.56rem, 2.2cqi, 0.7rem); letter-spacing: 0.42em; opacity: 0.55; margin-bottom: 14px; }
.cin-date { font-size: clamp(0.6rem, 2.4cqi, 0.74rem); letter-spacing: 0.34em; text-transform: uppercase; opacity: 0.6; }
.cin-loc { font-size: clamp(0.54rem, 2cqi, 0.64rem); letter-spacing: 0.28em; text-transform: uppercase; color: var(--color-countdown, #D4853A); margin-top: 7px; opacity: 0.85; }
</style>
