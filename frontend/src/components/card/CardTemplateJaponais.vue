<script setup>
import { computed, ref, onMounted } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  mode: { type: String, default: 'full' }
});

const theme = computed(() => {
  const bgColor = props.config.theme?.background || '#F7EEE3';
  return {
    bg: bgColor,
    text: props.config.theme?.text || getContrastColor(bgColor),
    accent: props.config.theme?.accent || '#D14B3D',
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => {
  if (props.config.content?.date_display) return props.config.content.date_display;
  return props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'DATE À VENIR';
});
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

// Pétales de sakura — positions/timings fixés au montage
const petals = Array.from({ length: 14 }, () => ({
  left: (Math.random() * 100).toFixed(1) + '%',
  delay: (Math.random() * 9).toFixed(2) + 's',
  duration: (Math.random() * 5 + 8).toFixed(2) + 's',
  size: (Math.random() * 6 + 8).toFixed(0) + 'px',
  sway: (Math.random() * 50 + 20).toFixed(0) + 'px',
}));

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 100);
});
</script>

<template>
  <div class="jp-template">
    <div class="washi-texture" aria-hidden="true"></div>

    <!-- Soleil levant -->
    <div class="rising-sun" :class="{ loaded: isLoaded }" aria-hidden="true"></div>

    <!-- Silhouette du Fuji -->
    <svg class="fuji" viewBox="0 0 400 140" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0,140 L150,30 Q165,18 175,30 L185,42 Q175,55 200,55 Q225,55 215,42 L225,30 Q235,18 250,30 L400,140 Z"
            :fill="'color-mix(in srgb, var(--color-text) 14%, transparent)'" />
    </svg>

    <!-- Pétales de sakura -->
    <div class="petals" aria-hidden="true">
      <span v-for="(p, i) in petals" :key="i" class="petal"
            :style="{ left: p.left, width: p.size, height: p.size, '--delay': p.delay, '--duration': p.duration, '--sway': p.sway }"></span>
    </div>

    <!-- Kanji vertical -->
    <div class="vrt-kanji" aria-hidden="true">結婚式</div>

    <div class="hero-section">
      <div class="hero-content" :class="{ reveal: isLoaded }">
        <div class="stamp">寿</div>
        <h1 class="main-title">{{ displayNames }}</h1>
        <div class="brush-divider">
          <svg viewBox="0 0 500 50" preserveAspectRatio="none">
            <path d="M10,25 C150,5 350,45 490,25" class="brush-path" :class="{ 'draw-brush': isLoaded }" />
          </svg>
        </div>
        <p class="date-text">{{ displayDate }}</p>
        <p v-if="displayLocation" class="loc-text">{{ displayLocation }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@200;500;700&family=Shippori+Mincho:wght@400;600&family=Cormorant+Garamond:ital,wght@1,400&display=swap');

.jp-template {
  background-color: var(--color-bg, #F7EEE3);
  color: var(--color-text, #2A1E18);
  font-family: var(--card-font, 'Shippori Mincho'), serif;
  min-height: 100vh;
  position: relative;
  overflow: clip;
}

.washi-texture {
  position: absolute; inset: 0; pointer-events: none; z-index: 1; opacity: 0.35;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}

/* Soleil levant — hinomaru */
.rising-sun {
  position: absolute;
  top: 18%; left: 50%;
  width: clamp(180px, 62cqi, 340px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: var(--color-countdown, #D14B3D);
  opacity: 0;
  transform: translate(-50%, 40px) scale(0.6);
  filter: drop-shadow(0 0 50px color-mix(in srgb, var(--color-countdown, #D14B3D) 45%, transparent));
  z-index: 0;
}
.rising-sun.loaded { animation: sunRise 2.6s cubic-bezier(0.16, 1, 0.3, 1) forwards, sunGlow 5s ease-in-out 2.6s infinite; }
@keyframes sunRise { to { opacity: 0.92; transform: translate(-50%, 0) scale(1); } }
@keyframes sunGlow {
  0%, 100% { filter: drop-shadow(0 0 40px color-mix(in srgb, var(--color-countdown, #D14B3D) 40%, transparent)); }
  50% { filter: drop-shadow(0 0 70px color-mix(in srgb, var(--color-countdown, #D14B3D) 60%, transparent)); }
}

.fuji {
  position: absolute; bottom: 0; left: 0; width: 100%;
  height: clamp(90px, 30cqi, 150px); z-index: 1;
}

/* Pétales */
.petals { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.petal {
  position: absolute; top: -20px;
  background: color-mix(in srgb, var(--color-countdown, #D14B3D) 35%, #fff);
  border-radius: 100% 0 100% 0;
  opacity: 0;
  animation: petalFall var(--duration, 10s) linear var(--delay, 0s) infinite;
}
@keyframes petalFall {
  0%   { opacity: 0; transform: translate(0, 0) rotate(0deg); }
  10%  { opacity: 0.8; }
  90%  { opacity: 0.7; }
  100% { opacity: 0; transform: translate(var(--sway, 30px), 105vh) rotate(420deg); }
}

.vrt-kanji {
  position: absolute; top: 8%; right: 7%;
  writing-mode: vertical-rl;
  font-size: clamp(0.7rem, 2.6cqi, 1rem);
  letter-spacing: 0.5em;
  color: color-mix(in srgb, var(--color-text) 45%, transparent);
  z-index: 3;
}

.hero-section {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  position: relative; z-index: 4;
  padding: clamp(40px, 10cqi, 80px) clamp(24px, 7cqi, 56px);
  text-align: center;
}
.hero-content { opacity: 0; transform: translateY(20px); transition: opacity 1.6s ease-out, transform 1.6s ease-out; }
.hero-content.reveal { opacity: 1; transform: translateY(0); }

.stamp {
  width: clamp(48px, 14cqi, 64px); height: clamp(48px, 14cqi, 64px);
  border: 2px solid var(--color-countdown, #D14B3D);
  color: var(--color-countdown, #D14B3D);
  font-family: 'Noto Serif JP', serif;
  font-size: clamp(1.4rem, 6cqi, 2rem);
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto clamp(24px, 7cqi, 36px);
  transform: rotate(-8deg);
  box-shadow: 2px 2px 0 color-mix(in srgb, var(--color-countdown, #D14B3D) 25%, transparent);
}

.main-title {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: var(--size-names, clamp(2.6rem, 14cqi, 5rem));
  line-height: 1.05;
  color: var(--color-names, #2A1E18);
  margin-bottom: 24px;
  text-shadow: 0 2px 20px color-mix(in srgb, var(--color-bg) 60%, transparent);
}

.brush-divider { width: clamp(160px, 50cqi, 300px); margin: 0 auto 28px; }
.brush-path {
  fill: none; stroke: var(--color-text); stroke-width: 4; stroke-linecap: round;
  stroke-dasharray: 500; stroke-dashoffset: 500;
}
.draw-brush { animation: drawBrush 2.4s ease-out 0.9s forwards; }
@keyframes drawBrush { to { stroke-dashoffset: 0; } }

.date-text {
  text-transform: uppercase; letter-spacing: 0.4em;
  font-size: clamp(0.7rem, 2.6cqi, 0.9rem);
  color: var(--color-countdown, #D14B3D);
}
.loc-text {
  margin-top: 10px; letter-spacing: 0.25em;
  font-size: clamp(0.6rem, 2.2cqi, 0.75rem);
  opacity: 0.6; text-transform: uppercase;
}
</style>
