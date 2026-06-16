<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#F7F3EE',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#F7F3EE'),
  accent: props.config.theme?.accent || '#C4622D',
}));

const displayNames = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const isGlitching = ref(true);

onMounted(() => {
  setTimeout(() => { isGlitching.value = false; }, 800);
});

const firstHeroName = computed(() => {
  const n = displayNames.value;
  if (!n) return '';
  return n.trim().split(/\s*[&\/]\s*/)[0] || '';
});
const heroInitial = computed(() => {
  if (content.value.monogram) return content.value.monogram.charAt(0);
  return firstHeroName.value.charAt(0).toUpperCase() || '';
});
</script>

<template>
  <div class="hero-empire min-h-dvh relative overflow-hidden flex items-center p-6"
      >
    <!-- Éléments Décoratifs -->
    <div class="diag-line absolute top-0 left-[-10%] w-[120%] h-[1px] opacity-25 -rotate-12 pointer-events-none" :style="{ backgroundColor: 'var(--color-countdown)' }"></div>
    <div class="diag-line absolute top-[28%] left-[-10%] w-[120%] h-[1px] opacity-10 rotate-6 pointer-events-none" :style="{ backgroundColor: 'var(--color-text)' }"></div>
    <div class="absolute -right-10 top-1/2 -translate-y-1/2 opacity-[0.03] text-[30cqi] font-display leading-none pointer-events-none uppercase overflow-hidden" :style="{ color: 'var(--color-text)' }">
      {{ firstHeroName || 'UNION' }}
    </div>

    <!-- Collage abstrait -->
    <div class="abstract-cluster absolute inset-0 pointer-events-none" aria-hidden="true">
      <div class="shape shape-quarter" :style="{ backgroundColor: 'var(--color-countdown)' }"></div>
      <div class="shape shape-bar" :style="{ backgroundColor: 'var(--color-countdown)' }"></div>
      <svg class="shape shape-ring" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" stroke="var(--color-text)" stroke-width="0.6" fill="none" opacity="0.4" /></svg>
      <svg class="shape shape-triangle" viewBox="0 0 100 100"><polygon points="50,6 94,90 6,90" stroke="var(--color-countdown)" stroke-width="0.8" fill="none" /></svg>
    </div>

    <div class="flex flex-col w-full max-w-7xl mx-auto gap-12 z-10">

      <!-- NOMS -->
      <div class="relative">
        <div class="absolute -left-10 top-0 text-[8px] font-mono text-[#C4622D] uppercase rotate-90" aria-hidden="true">SEC. 01 // HERO</div>
        <svg class="absolute -left-20 -top-20 w-80 h-80 opacity-10 pointer-events-none" viewBox="0 0 100 100">
           <circle cx="50" cy="50" r="48" stroke="#8B7355" stroke-width="0.5" fill="none" />
        </svg>
        <div class="title-block absolute -inset-x-4 top-[0.2em] bottom-[0.15em] -z-10" :style="{ backgroundColor: 'var(--color-text)' }" aria-hidden="true"></div>
        <h1 class="template-title font-display uppercase relative" :style="{ color: 'var(--color-bg)' }" :class="{ 'glitch': isGlitching }">
          {{ displayNames }}
        </h1>
      </div>

      <!-- INFOS -->
      <div class="space-y-10 py-4">
        <div class="space-y-2">
          <p class="font-mono text-[10px] font-bold tracking-widest" :style="{ color: 'var(--color-countdown)' }">{{ content.date_display || '15 JUIN 2026' }}</p>
          <p v-if="content.address" class="template-subtitle font-sans uppercase tracking-tighter" :style="{ color: 'var(--color-text)' }">{{ content.address }}</p>
        </div>

        <p class="template-body font-serif leading-relaxed italic border-t border-[#D4C4B0] pt-6" :style="{ color: 'var(--color-text)' }">
          {{ content.intro_text || 'Nous vous convions à partager un moment d’exception pour célébrer notre union.' }}
        </p>

        <div class="flex gap-4 items-center">
           <div class="w-12 h-12 flex items-center justify-center font-display text-xl" :style="{ backgroundColor: 'var(--color-text)', color: 'var(--color-bg)' }">
             {{ heroInitial }}
           </div>
           <span v-if="content.divider_symbol" class="font-mono text-[10px] tracking-widest opacity-50 uppercase">{{ content.divider_symbol }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Spectral:ital,wght@1,300&family=Space+Mono:wght@400;700&family=Tenor+Sans&display=swap');

.hero-empire {
  border-radius: 0 !important;
  background: var(--color-bg, #F7F3EE);
  color: var(--color-text, #1A0F0A);
}
.hero-empire * { border-radius: 0 !important; }

.font-display { font-family: var(--card-font, 'Anton'), sans-serif; }
.template-title { font-size: var(--size-names, clamp(3.5rem, 12cqi, 9rem)); line-height: 0.9; padding: 0 0.15em; }
.title-block { transform-origin: left center; animation: blockReveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) both; }

/* Collage abstrait — assemblage Bauhaus */
.abstract-cluster { z-index: 0; overflow: hidden; }
.shape { position: absolute; opacity: 0; animation-fill-mode: forwards; }

.shape-quarter {
  width: clamp(80px, 30cqi, 220px); height: clamp(80px, 30cqi, 220px);
  top: -5%; right: -8%; border-radius: 0 0 0 100%;
  animation: quarterIn 1s ease-out 0.1s forwards, drift1 14s ease-in-out 1.1s infinite;
}
.shape-bar {
  width: clamp(60px, 22cqi, 160px); height: 10px;
  bottom: 14%; left: -4%;
  animation: barIn 0.8s ease-out 0.3s forwards, drift2 10s ease-in-out 1.1s infinite;
}
.shape-ring {
  width: clamp(70px, 26cqi, 180px); height: clamp(70px, 26cqi, 180px);
  bottom: -6%; right: 6%;
  animation: ringIn 1s ease-out 0.5s forwards, spin-slow 40s linear 1.5s infinite;
}
.shape-triangle {
  width: clamp(40px, 16cqi, 100px); height: clamp(40px, 16cqi, 100px);
  top: 8%; left: 4%;
  animation: triangleIn 0.9s ease-out 0.65s forwards, drift1 16s ease-in-out 1.5s infinite;
}

@keyframes quarterIn { from { opacity: 0; transform: scale(0.6) rotate(-8deg); } to { opacity: 0.12; transform: scale(1) rotate(0); } }
@keyframes barIn { from { opacity: 0; transform: scale(0.6) rotate(-20deg); } to { opacity: 0.18; transform: scale(1) rotate(-8deg); } }
@keyframes ringIn { from { opacity: 0; transform: scale(0.6); } to { opacity: 0.4; transform: scale(1); } }
@keyframes triangleIn { from { opacity: 0; transform: scale(0.6) rotate(-8deg); } to { opacity: 1; transform: scale(1) rotate(0); } }
@keyframes blockReveal { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes drift1 { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(8px, -10px); } }
@keyframes drift2 { 0%, 100% { transform: rotate(-8deg) translateX(0); } 50% { transform: rotate(-4deg) translateX(10px); } }
@keyframes spin-slow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.template-subtitle { font-family: var(--card-font, 'Tenor Sans'), sans-serif; font-size: clamp(1.2rem, 3cqi, 1.8rem); }
.template-body { font-family: var(--card-font, 'Spectral'), serif; font-size: 1rem; }
.font-mono { font-family: var(--card-font, 'Space Mono'), monospace; }

.glitch { animation: glitch-anim 0.2s infinite; }
@keyframes glitch-anim {
  0% { transform: translate(0) }
  33% { transform: translate(-4px, 2px) }
  66% { transform: translate(4px, -2px) }
  100% { transform: translate(0) }
}
</style>
