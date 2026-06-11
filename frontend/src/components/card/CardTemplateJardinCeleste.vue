<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#1A2E1F',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#1A2E1F'),
  accent: props.config.theme?.accent || '#E8A598',
}));

const displayNames = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const isMobile = ref(false);

onMounted(() => {
  isMobile.value = window.matchMedia('(max-width: 768px)').matches;
});

const monogram = computed(() => {
  if (content.value.monogram) return content.value.monogram;
  const n = displayNames.value;
  if (!n) return '';
  const parts = n.trim().split(/\s*[&\/]\s*/);
  if (parts.length >= 2) return `${parts[0].charAt(0).toUpperCase()} & ${parts[1].charAt(0).toUpperCase()}`;
  return parts[0]?.charAt(0).toUpperCase() || '';
});
</script>

<template>
  <div class="hero-jardin h-dvh relative overflow-hidden flex items-center justify-center text-center px-6"
       :style="{ '--card-bg': theme.bg, '--card-text': theme.text, '--card-accent': theme.accent }">
    <!-- Feuilles flottantes (désactivées sur mobile) -->
    <div v-if="!isMobile" class="leaves-overlay absolute inset-0 pointer-events-none">
      <svg v-for="i in 8" :key="i" class="leaf-float" :class="'l-' + i" viewBox="0 0 24 24">
        <path d="M12 2C8 2 4 6 4 12C4 18 12 22 12 22C12 22 20 18 20 12C20 6 16 2 12 2Z" fill="#E8A598" opacity="0.15"/>
      </svg>
    </div>

    <div class="relative z-10 max-w-3xl space-y-10 animate-fadeScale">
      <!-- Cadre Organique Monogramme -->
      <div class="relative inline-block p-12">
        <svg class="absolute inset-0 w-full h-full" viewBox="0 0 100 100">
          <path d="M50 5 Q80 10 90 50 Q85 90 50 95 Q15 90 10 50 Q20 10 50 5" 
                :stroke="theme.accent" stroke-width="0.5" fill="none" class="organic-draw" />
        </svg>
        <span class="text-3xl tracking-[0.4em] uppercase font-light" :style="{ color: 'var(--card-accent)' }">
          {{ monogram }}
        </span>
      </div>

      <h1 class="template-title italic" :style="{ color: 'var(--card-text)' }">
        {{ displayNames }}
      </h1>

      <p class="template-body font-light max-w-xl mx-auto italic opacity-90" :style="{ color: 'var(--card-text)' }">
        {{ content.intro_text || 'Entrez dans la danse au cœur de notre jardin céleste.' }}
      </p>

      <div class="space-y-6 pt-10">
        <div class="flex items-center justify-center gap-4" :style="{ color: 'var(--card-accent)' }">
           <div class="h-[1px] w-8 bg-current opacity-30"></div>
           <span class="text-xs tracking-[0.3em] font-light">{{ content.date_display || '15 JUIN 2026' }}</span>
           <div class="h-[1px] w-8 bg-current opacity-30"></div>
        </div>
        <p v-if="content.address" class="template-label uppercase opacity-70 tracking-widest" :style="{ color: 'var(--card-text)' }">
          {{ content.address }}
        </p>
      </div>

      <div class="pt-12 text-3xl" :style="{ color: 'var(--card-accent)' }">{{ content.divider_symbol || '❦' }}</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Upright:wght@300;600&family=Josefin+Sans:wght@300&family=Lato:wght@300&display=swap');

.hero-jardin {
  font-family: var(--card-font, 'Lato'), sans-serif;
  background: var(--card-bg, #1A2E1F);
  color: var(--card-text, #F2EBE0);
}
.template-title { font-family: var(--card-font, 'Cormorant Upright'), serif; font-size: var(--size-names, clamp(3.5rem, 12vw, 6.5rem)); line-height: 1; }
.template-body { font-size: clamp(1rem, 2.5vw, 1.25rem); }
.template-label { font-family: var(--card-font, 'Josefin Sans'), sans-serif; font-size: 0.7rem; }

.organic-draw { stroke-dasharray: 300; stroke-dashoffset: 300; animation: draw 3s ease-out forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }

.leaf-float { position: absolute; width: 40px; height: 40px; }
.l-1 { top: 10%; left: 10%; animation: float 10s infinite alternate; }
.l-2 { top: 20%; right: 15%; animation: float 12s infinite alternate-reverse; }
.l-3 { bottom: 15%; left: 20%; animation: float 8s infinite alternate; }
@keyframes float { from { transform: translate(0,0) rotate(0deg); } to { transform: translate(30px, 40px) rotate(45deg); } }

@keyframes scale { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.animate-fadeScale { animation: scale 1.5s cubic-bezier(0.16, 1, 0.3, 1); }
</style>
