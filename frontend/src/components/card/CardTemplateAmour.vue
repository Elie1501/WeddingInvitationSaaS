<script setup>
import { useTemplateData } from '@/composables/useTemplateData';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: () => ({}) },
  mode:   { type: String, default: 'full' },
});

defineEmits(['click-image']);

const { displayNames, displayDate, displayLocation, isLoaded }
  = useTemplateData(() => props.config, () => props.event);

// Cœurs flottants
const hearts = Array.from({ length: 14 }, () => ({
  left: (Math.random() * 100).toFixed(1) + '%',
  size: (Math.random() * 14 + 10).toFixed(0) + 'px',
  delay: (Math.random() * 9).toFixed(2) + 's',
  duration: (Math.random() * 6 + 9).toFixed(2) + 's',
  drift: (Math.random() * 60 - 30).toFixed(0) + 'px',
  op: (Math.random() * 0.3 + 0.12).toFixed(2),
}));
</script>

<template>
  <!-- Hero uniquement — countdown / programme / RSVP sont des blocs gérés par CardRenderer -->
  <section class="amr-hero">
    <!-- Cœurs flottants -->
    <div class="amr-hearts" aria-hidden="true">
      <svg v-for="(h, i) in hearts" :key="i" class="fly-heart" viewBox="0 0 24 24"
           :style="{ left: h.left, width: h.size, height: h.size, '--delay': h.delay, '--dur': h.duration, '--drift': h.drift, '--op': h.op }">
        <path d="M12 21s-8-5.3-10-11C0.5 5.5 3 2 6.5 2 9 2 12 4.5 12 4.5S15 2 17.5 2C21 2 23.5 5.5 22 10c-2 5.7-10 11-10 11z" fill="var(--color-countdown, #D6677A)"/>
      </svg>
    </div>

    <div class="amr-glow" aria-hidden="true"></div>

    <div class="amr-inner" :class="{ revealed: isLoaded }">
      <!-- Cœur tracé + battement -->
      <div class="amr-beat" :class="{ go: isLoaded }">
        <svg viewBox="0 0 100 90" class="amr-heart-svg">
          <path d="M50 80 C 12 52, 4 30, 18 16 C 30 4, 46 10, 50 24 C 54 10, 70 4, 82 16 C 96 30, 88 52, 50 80 Z"
                class="heart-path" :class="{ draw: isLoaded }" />
        </svg>
      </div>

      <p class="amr-script">Pour toujours</p>
      <h1 class="amr-names template-title main-names">{{ displayNames }}</h1>
      <div class="amr-rule" aria-hidden="true"><span></span><span class="dot">♥</span><span></span></div>
      <p class="amr-date">{{ displayDate }}</p>
      <p v-if="displayLocation" class="amr-loc">{{ displayLocation }}</p>
    </div>
  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Dancing+Script:wght@500;600&family=Jost:wght@300;400&display=swap');

/* HERO */
.amr-hero {
  position: relative;
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  text-align: center;
  padding: clamp(50px, 11cqi, 90px) clamp(24px, 7cqi, 50px);
  background: var(--color-bg, #FDF1F0);
  color: var(--color-text, #4A2E33);
  font-family: var(--card-font, 'Jost'), sans-serif;
  overflow: clip;
}

/* Cœurs flottants */
.amr-hearts { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.fly-heart {
  position: absolute; bottom: -24px; opacity: 0;
  animation: heartRise var(--dur, 11s) ease-in-out var(--delay, 0s) infinite;
}
@keyframes heartRise {
  0%   { opacity: 0; transform: translate(0,0) rotate(0deg) scale(0.7); }
  12%  { opacity: var(--op, 0.2); }
  88%  { opacity: var(--op, 0.2); }
  100% { opacity: 0; transform: translate(var(--drift, 30px), -118vh) rotate(25deg) scale(1); }
}

.amr-glow {
  position: absolute; top: 24%; left: 50%; transform: translateX(-50%);
  width: 120%; aspect-ratio: 1; pointer-events: none; z-index: 0;
  background: radial-gradient(circle, color-mix(in srgb, var(--color-countdown, #D6677A) 20%, transparent) 0%, transparent 50%);
  animation: glowPulse 6s ease-in-out infinite;
}
@keyframes glowPulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }

.amr-inner { position: relative; z-index: 2; opacity: 0; transform: translateY(22px); transition: opacity 1.4s ease-out, transform 1.4s cubic-bezier(0.16,1,0.3,1); }
.amr-inner.revealed { opacity: 1; transform: translateY(0); }

/* Cœur tracé + battement */
.amr-beat { width: clamp(60px, 18cqi, 92px); margin: 0 auto clamp(22px, 6cqi, 34px); transform-origin: center 70%; }
.amr-beat.go { animation: heartbeat 1.6s ease-in-out 2.6s infinite; }
@keyframes heartbeat { 0%,100% { transform: scale(1); } 14% { transform: scale(1.12); } 28% { transform: scale(1); } 42% { transform: scale(1.08); } }
.amr-heart-svg { width: 100%; height: auto; display: block; }
.heart-path {
  fill: color-mix(in srgb, var(--color-countdown, #D6677A) 0%, transparent);
  stroke: var(--color-countdown, #D6677A); stroke-width: 2.5; stroke-linejoin: round;
  stroke-dasharray: 300; stroke-dashoffset: 300;
}
.heart-path.draw { animation: drawHeart 2.2s ease-out 0.4s forwards, fillHeart 1s ease-out 2.4s forwards; }
@keyframes drawHeart { to { stroke-dashoffset: 0; } }
@keyframes fillHeart { to { fill: color-mix(in srgb, var(--color-countdown, #D6677A) 88%, transparent); } }

.amr-script {
  font-family: 'Dancing Script', cursive;
  font-size: clamp(1.4rem, 6cqi, 2rem);
  color: var(--color-countdown, #D6677A);
  margin-bottom: 6px;
}
.amr-names {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic; font-weight: 400;
  font-size: var(--size-names, clamp(2.8rem, 15cqi, 5.5rem));
  line-height: 1.04;
  color: var(--color-names, #6B2737);
}
.amr-rule { display: flex; align-items: center; justify-content: center; gap: 12px; margin: clamp(22px,6cqi,32px) auto; }
.amr-rule span:not(.dot) { height: 1px; width: clamp(34px, 13cqi, 64px); background: color-mix(in srgb, var(--color-countdown, #D6677A) 50%, transparent); }
.amr-rule .dot { color: var(--color-countdown, #D6677A); font-size: 0.8rem; }
.amr-date { font-size: clamp(0.64rem, 2.5cqi, 0.78rem); letter-spacing: 0.4em; text-transform: uppercase; opacity: 0.6; margin-bottom: 8px; }
.amr-loc { font-size: clamp(0.56rem, 2.2cqi, 0.68rem); letter-spacing: 0.28em; text-transform: uppercase; color: var(--color-countdown, #D6677A); opacity: 0.85; }
</style>
