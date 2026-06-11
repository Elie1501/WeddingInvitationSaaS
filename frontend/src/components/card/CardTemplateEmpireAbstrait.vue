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
  <div class="hero-empire min-h-dvh relative overflow-hidden flex items-center p-6 md:p-20"
       :style="{ '--card-bg': theme.bg, '--card-text': theme.text, '--card-accent': theme.accent }">
    <!-- Éléments Décoratifs -->
    <div class="diag-line absolute top-0 left-[-10%] w-[120%] h-[1px] opacity-25 -rotate-12 pointer-events-none hidden md:block" :style="{ backgroundColor: 'var(--card-accent)' }"></div>
    <div class="absolute -right-20 top-1/2 -translate-y-1/2 opacity-[0.03] text-[30vw] font-display leading-none pointer-events-none uppercase" :style="{ color: 'var(--card-text)' }">
      {{ firstHeroName || 'UNION' }}
    </div>

    <div class="grid md:grid-cols-[1.5fr_1fr] w-full max-w-7xl mx-auto items-end gap-12 z-10">
      
      <!-- GAUCHE : NOMS -->
      <div class="relative">
        <div class="absolute -left-10 top-0 text-[8px] font-mono text-[#C4622D] uppercase rotate-90" aria-hidden="true">SEC. 01 // HERO</div>
        <svg class="absolute -left-20 -top-20 w-80 h-80 opacity-10 pointer-events-none" viewBox="0 0 100 100">
           <circle cx="50" cy="50" r="48" stroke="#8B7355" stroke-width="0.5" fill="none" />
        </svg>
        <h1 class="template-title font-display uppercase relative" :style="{ color: 'var(--card-accent)' }" :class="{ 'glitch': isGlitching }">
          {{ displayNames }}
        </h1>
      </div>

      <!-- DROITE : INFOS -->
      <div class="space-y-10 md:border-l md:pl-12 py-4" :style="{ borderColor: 'var(--card-accent)' }">
        <div class="space-y-2">
          <p class="font-mono text-[10px] font-bold tracking-widest" :style="{ color: 'var(--card-accent)' }">{{ content.date_display || '15 JUIN 2026' }}</p>
          <p v-if="content.address" class="template-subtitle font-sans uppercase tracking-tighter" :style="{ color: 'var(--card-text)' }">{{ content.address }}</p>
        </div>

        <p class="template-body font-serif leading-relaxed italic border-t border-[#D4C4B0] pt-6" :style="{ color: 'var(--card-text)' }">
          {{ content.intro_text || 'Nous vous convions à partager un moment d’exception pour célébrer notre union.' }}
        </p>

        <div class="flex gap-4 items-center">
           <div class="w-12 h-12 flex items-center justify-center font-display text-xl" :style="{ backgroundColor: 'var(--card-text)', color: 'var(--card-bg)' }">
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
  background: var(--card-bg, #F7F3EE);
  color: var(--card-text, #1A0F0A);
}
.hero-empire * { border-radius: 0 !important; }

.font-display { font-family: var(--card-font, 'Anton'), sans-serif; }
.template-title { font-size: var(--size-names, clamp(3.5rem, 12vw, 9rem)); line-height: 0.9; }
.template-subtitle { font-family: var(--card-font, 'Tenor Sans'), sans-serif; font-size: clamp(1.2rem, 3vw, 1.8rem); }
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
