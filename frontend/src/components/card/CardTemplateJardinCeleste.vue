<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#0F2419',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#0F2419'),
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

// Ciel étoilé — positions aléatoires fixées au montage
const stars = Array.from({ length: 28 }, () => ({
  top: (Math.random() * 55).toFixed(1) + '%',
  left: (Math.random() * 100).toFixed(1) + '%',
  size: (Math.random() * 1.6 + 0.8).toFixed(1) + 'px',
  delay: (Math.random() * 5).toFixed(2) + 's',
  duration: (Math.random() * 2.5 + 2.5).toFixed(2) + 's',
}));

// Lucioles — montent lentement depuis le bas du jardin
const fireflies = Array.from({ length: 12 }, () => ({
  left: (Math.random() * 88 + 4).toFixed(1) + '%',
  bottom: (Math.random() * 18).toFixed(1) + '%',
  size: (Math.random() * 2.5 + 2.5).toFixed(1) + 'px',
  delay: (Math.random() * 7).toFixed(2) + 's',
  duration: (Math.random() * 5 + 7).toFixed(2) + 's',
  drift: (Math.random() * 60 - 30).toFixed(0) + 'px',
}));
</script>

<template>
  <div class="hero-jardin h-dvh relative overflow-clip flex items-center justify-center text-center px-6"
      >
    <!-- Ciel étoilé -->
    <div class="sky-overlay absolute inset-0 pointer-events-none" aria-hidden="true">
      <span v-for="(s, i) in stars" :key="'s' + i" class="star"
            :style="{ top: s.top, left: s.left, width: s.size, height: s.size, '--delay': s.delay, '--duration': s.duration }"></span>
      <svg class="moon" viewBox="0 0 100 100" aria-hidden="true">
        <path d="M62 8 A42 42 0 1 0 62 92 A32 32 0 1 1 62 8 Z" fill="var(--firefly-color)" opacity="0.5" />
      </svg>
    </div>

    <!-- Vignette de profondeur -->
    <div class="night-vignette absolute inset-0 pointer-events-none" aria-hidden="true"></div>

    <!-- Lucioles -->
    <div class="fireflies absolute inset-0 pointer-events-none" aria-hidden="true">
      <span v-for="(f, i) in fireflies" :key="'f' + i" class="firefly"
            :style="{ left: f.left, bottom: f.bottom, width: f.size, height: f.size, '--delay': f.delay, '--duration': f.duration, '--drift': f.drift }"></span>
    </div>

    <!-- Feuillage flottant (désactivé sur mobile) -->
    <div v-if="!isMobile" class="leaves-overlay absolute inset-0 pointer-events-none">
      <svg v-for="i in 5" :key="i" class="leaf-float" :class="'l-' + i" viewBox="0 0 24 24">
        <path d="M12 2C8 2 4 6 4 12C4 18 12 22 12 22C12 22 20 18 20 12C20 6 16 2 12 2Z" fill="var(--color-countdown)" opacity="0.12"/>
      </svg>
    </div>

    <div class="relative z-10 max-w-3xl space-y-10 animate-fadeScale">
      <!-- Cadre Organique Monogramme -->
      <div class="relative inline-block p-12">
        <svg class="absolute inset-0 w-full h-full" viewBox="0 0 100 100">
          <path d="M50 5 Q80 10 90 50 Q85 90 50 95 Q15 90 10 50 Q20 10 50 5"
                stroke="var(--color-countdown)" stroke-width="0.5" fill="none" class="organic-draw" />
          <path d="M50 5 Q44 -2 36 4" stroke="var(--color-countdown)" stroke-width="0.5" fill="none" opacity="0.6" class="organic-draw" style="animation-delay: 2.6s" />
          <path d="M50 95 Q56 102 64 96" stroke="var(--color-countdown)" stroke-width="0.5" fill="none" opacity="0.6" class="organic-draw" style="animation-delay: 2.8s" />
        </svg>
        <span class="text-3xl tracking-[0.4em] uppercase font-light" :style="{ color: 'var(--color-countdown)' }">
          {{ monogram }}
        </span>
      </div>

      <h1 class="template-title italic" :style="{ color: 'var(--color-text)' }">
        {{ displayNames }}
      </h1>

      <p class="template-body font-light max-w-xl mx-auto italic opacity-90" :style="{ color: 'var(--color-text)' }">
        {{ content.intro_text || 'Entrez dans la danse au cœur de notre jardin céleste.' }}
      </p>

      <div class="space-y-6 pt-10">
        <div class="flex items-center justify-center gap-4" :style="{ color: 'var(--color-countdown)' }">
           <div class="h-[1px] w-8 bg-current opacity-30"></div>
           <span class="text-xs tracking-[0.3em] font-light">{{ content.date_display || '15 JUIN 2026' }}</span>
           <div class="h-[1px] w-8 bg-current opacity-30"></div>
        </div>
        <p v-if="content.address" class="template-label uppercase opacity-70 tracking-widest" :style="{ color: 'var(--color-text)' }">
          {{ content.address }}
        </p>
      </div>

      <div class="pt-12 text-3xl twinkle-symbol" :style="{ color: 'var(--color-countdown)' }">{{ content.divider_symbol || '✦' }}</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Upright:wght@300;600&family=Josefin+Sans:wght@300&family=Lato:wght@300&display=swap');

.hero-jardin {
  font-family: var(--card-font, 'Lato'), sans-serif;
  background: var(--color-bg, #0F2419);
  color: var(--color-text, #F2EBE0);
  --firefly-color: #D9E86B;
}
.template-title { font-family: var(--card-font, 'Cormorant Upright'), serif; font-size: var(--size-names, clamp(3.5rem, 12cqi, 6.5rem)); line-height: 1; }
.template-body { font-size: clamp(1rem, 2.5cqi, 1.25rem); }
.template-label { font-family: var(--card-font, 'Josefin Sans'), sans-serif; font-size: 0.7rem; }

.organic-draw { stroke-dasharray: 300; stroke-dashoffset: 300; animation: draw 2.6s ease-out forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }

/* Ciel étoilé */
.sky-overlay { z-index: 1; }
.star {
  position: absolute;
  border-radius: 50%;
  background: #F5F2E0;
  box-shadow: 0 0 4px 1px rgba(245, 242, 224, 0.6);
  animation: twinkle var(--duration, 3s) ease-in-out var(--delay, 0s) infinite;
}
@keyframes twinkle {
  0%, 100% { opacity: 0.15; transform: scale(0.8); }
  50% { opacity: 0.95; transform: scale(1.15); }
}
.moon { position: absolute; top: 6%; right: 8%; width: clamp(28px, 9cqi, 56px); height: clamp(28px, 9cqi, 56px); opacity: 0.8; filter: drop-shadow(0 0 12px rgba(217, 232, 107, 0.35)); }

.night-vignette {
  z-index: 1;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(255,255,255,0.06), transparent 55%),
    radial-gradient(circle, transparent 35%, rgba(0,0,0,0.45) 100%);
}

/* Lucioles */
.fireflies { z-index: 2; }
.firefly {
  position: absolute;
  border-radius: 50%;
  background: var(--firefly-color);
  box-shadow: 0 0 6px 2px var(--firefly-color);
  opacity: 0;
  animation: fireflyDrift var(--duration, 9s) ease-in-out var(--delay, 0s) infinite;
}
@keyframes fireflyDrift {
  0%   { transform: translate(0, 0); opacity: 0; }
  12%  { opacity: 0.9; }
  50%  { transform: translate(var(--drift, 20px), -90px); opacity: 0.35; }
  85%  { opacity: 0.8; }
  100% { transform: translate(calc(var(--drift, 20px) * -1), -170px); opacity: 0; }
}

.leaves-overlay { z-index: 1; }
.leaf-float { position: absolute; width: 40px; height: 40px; }
.l-1 { top: 10%; left: 10%; animation: float 10s infinite alternate; }
.l-2 { top: 20%; right: 15%; animation: float 12s infinite alternate-reverse; }
.l-3 { bottom: 15%; left: 20%; animation: float 8s infinite alternate; }
.l-4 { bottom: 25%; right: 12%; animation: float 14s infinite alternate; }
.l-5 { top: 45%; left: 6%; animation: float 11s infinite alternate-reverse; }
@keyframes float { from { transform: translate(0,0) rotate(0deg); } to { transform: translate(30px, 40px) rotate(45deg); } }

.twinkle-symbol { animation: twinkle 2.4s ease-in-out infinite; }

@keyframes scale { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.animate-fadeScale { animation: scale 1.5s cubic-bezier(0.16, 1, 0.3, 1); }
</style>
