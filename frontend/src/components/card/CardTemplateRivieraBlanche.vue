<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#FAFAF8',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#FAFAF8'),
  accent: props.config.theme?.accent || '#2E6E8E',
}));

const displayNames = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const isDrawn = ref(false);

onMounted(() => {
  setTimeout(() => { isDrawn.value = true; }, 300);
});

const monogram = computed(() => {
  if (content.value.monogram) return content.value.monogram;
  const n = displayNames.value;
  if (!n) return '';
  return n.trim().split(/\s*[&\/]\s*/)[0]?.charAt(0).toUpperCase() || '';
});
</script>

<template>
  <div class="hero-riviera min-h-dvh relative overflow-hidden flex flex-col justify-center px-6 md:px-20 py-20"
       :style="{ '--card-bg': theme.bg, '--card-text': theme.text, '--card-accent': theme.accent }">
    <div class="grid md:grid-cols-2 gap-12 items-center max-w-7xl mx-auto w-full">
      
      <!-- GAUCHE : CONTENU -->
      <div class="order-2 md:order-1 space-y-10 text-center md:text-left animate-slideRight">
        <div class="inline-block text-white px-4 py-1 text-[10px] font-bold tracking-[0.4em] uppercase" :style="{ backgroundColor: theme.accent }">
          SAVE THE DATE
        </div>

        <h1 class="template-title italic" :style="{ color: 'var(--card-text)' }">
          {{ displayNames }}
        </h1>

        <p class="template-body max-w-md font-light leading-relaxed opacity-70" :style="{ color: 'var(--card-text)' }">
          {{ content.intro_text || 'Nous serions honorés de votre présence pour célébrer notre union.' }}
        </p>

        <div class="space-y-2 pt-6">
          <p class="text-xs tracking-tighter" :style="{ color: 'var(--card-accent)' }">{{ content.date_display || '15.06.2026' }}</p>
          <p v-if="content.address" class="template-label" :style="{ color: 'var(--card-text)' }">{{ content.address }}</p>
        </div>
      </div>

      <!-- DROITE : SVG ILLUSTRATION -->
      <div class="order-1 md:order-2 flex justify-center relative overflow-hidden">
        <div class="absolute inset-0 flex items-center justify-center opacity-[0.03] pointer-events-none scale-150">
           <span class="text-[25vw] italic" :style="{ color: '#1C2B3A', fontFamily: 'var(--card-font)' }">{{ monogram }}</span>
        </div>
        
        <svg class="w-full max-w-[320px] h-auto" viewBox="0 0 200 400" fill="none">
          <!-- Branche principale -->
          <path d="M100 400 Q120 300 80 200 T100 0" :stroke="theme.accent" stroke-width="1" class="olive-path" :class="{ 'drawn': isDrawn }" />
          <!-- Feuilles -->
          <path d="M100 300 Q140 280 130 240 Q110 250 100 300" fill="#C8D8C0" class="leaf opacity-0" :class="{ 'fade-in': isDrawn }" />
          <path d="M100 150 Q60 130 70 90 Q90 100 100 150" fill="#D4A853" class="leaf opacity-0" :class="{ 'fade-in': isDrawn }" />
        </svg>
      </div>
    </div>

    <!-- Séparateur -->
    <div class="absolute bottom-10 left-1/2 -translate-x-1/2 text-2xl opacity-40 animate-bounce">
      {{ content.divider_symbol || '🌿' }}
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono&family=Jost:wght@300;500&family=Libre+Baskerville:ital@1&display=swap');

.hero-riviera {
  font-family: var(--card-font, 'Jost'), sans-serif;
  background: var(--card-bg, #FAFAF8);
  color: var(--card-text, #1C2B3A);
}
.template-title { font-family: var(--card-font, 'Libre Baskerville'), serif; font-size: var(--size-names, clamp(3rem, 10vw, 5.5rem)); line-height: 1.1; }
.template-body { font-size: clamp(1.1rem, 2.5vw, 1.25rem); }
.template-label { font-size: 0.75rem; letter-spacing: 0.2em; font-weight: 500; }

.olive-path { stroke-dasharray: 600; stroke-dashoffset: 600; transition: stroke-dashoffset 3s ease-out; }
.olive-path.drawn { stroke-dashoffset: 0; }
.leaf { transition: opacity 2s 1s ease-out; }
.leaf.fade-in { opacity: 0.6; }

@keyframes slide { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
.animate-slideRight { animation: slide 1.2s ease-out; }
</style>
