<script setup>
import { useTemplateData } from '@/composables/useTemplateData';
import CardSectionCountdown from './CardSectionCountdown.vue';
import CardSectionProgramme from './CardSectionProgramme.vue';
import CardSectionRSVP      from './CardSectionRSVP.vue';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: () => ({}) },
});

defineEmits(['click-image']);

const { displayNames, displayDate, displayLocation, isLoaded }
  = useTemplateData(() => props.config, () => props.event);

// Étoiles du ciel crépusculaire
const stars = Array.from({ length: 22 }, () => ({
  top: (Math.random() * 100).toFixed(1) + '%',
  left: (Math.random() * 100).toFixed(1) + '%',
  size: (Math.random() * 1.4 + 0.6).toFixed(1) + 'px',
  delay: (Math.random() * 4).toFixed(2) + 's',
  duration: (Math.random() * 2 + 2.5).toFixed(2) + 's',
}));
</script>

<template>
  <div class="ecl-wrap">

    <!-- ── 1. PAGE DE GARDE ── -->
    <section class="ecl-hero">
      <!-- Ciel étoilé -->
      <div class="ecl-sky" aria-hidden="true">
        <span v-for="(s, i) in stars" :key="i" class="ecl-star"
              :style="{ top: s.top, left: s.left, width: s.size, height: s.size, '--d': s.delay, '--dur': s.duration }"></span>
      </div>

      <!-- L'éclipse -->
      <div class="ecl-eclipse" :class="{ revealed: isLoaded }" aria-hidden="true">
        <div class="ecl-corona"></div>
        <div class="ecl-disc"></div>
        <div class="ecl-diamond"></div>
      </div>

      <div class="ecl-hero-inner" :class="{ revealed: isLoaded }">
        <p class="ecl-eyebrow">Sous une même étoile</p>
        <h1 class="ecl-names template-title main-names">{{ displayNames }}</h1>
        <div class="ecl-rule" aria-hidden="true" />
        <p class="ecl-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="ecl-loc">{{ displayLocation }}</p>
      </div>
    </section>

    <!-- ── 2. COMPTE À REBOURS ── -->
    <div class="ecl-sep">
      <CardSectionCountdown :config="props.config" :event="props.event" />
    </div>

    <!-- ── 3. LE PROGRAMME ── -->
    <div class="ecl-sep">
      <CardSectionProgramme :config="props.config" :event="props.event" />
    </div>

    <!-- ── 4. RSVP ── -->
    <div class="ecl-sep">
      <CardSectionRSVP :config="props.config" :event="props.event" />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&family=Hanken+Grotesk:wght@300;400;500&display=swap');

.ecl-wrap {
  background:
    radial-gradient(ellipse 120% 80% at 50% 6%, color-mix(in srgb, var(--color-countdown, #F0A85C) 22%, transparent), transparent 60%),
    var(--color-bg, #1B1430);
  color: var(--color-text, #E8DFF0);
  font-family: 'Hanken Grotesk', var(--card-font, sans-serif);
  min-height: 100svh;
  overflow-x: clip;
}

.ecl-sep { border-top: 1px solid color-mix(in srgb, var(--color-text, #E8DFF0) 12%, transparent); }

/* HERO */
.ecl-hero {
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 90px 40px;
  text-align: center;
  position: relative;
  overflow: clip;
}

/* Ciel */
.ecl-sky { position: absolute; inset: 0; z-index: 0; }
.ecl-star {
  position: absolute; border-radius: 50%; background: var(--color-text, #E8DFF0);
  opacity: 0.2;
  animation: eclTwinkle var(--dur, 3s) ease-in-out var(--d, 0s) infinite;
}
@keyframes eclTwinkle { 0%,100% { opacity: 0.12; } 50% { opacity: 0.7; } }

/* Éclipse */
.ecl-eclipse {
  position: absolute;
  top: 26%; left: 50%;
  width: clamp(150px, 48cqi, 260px);
  aspect-ratio: 1;
  transform: translate(-50%, -50%) scale(0.7);
  opacity: 0;
  z-index: 1;
  transition: opacity 1.8s ease-out, transform 1.8s cubic-bezier(0.16,1,0.3,1);
}
.ecl-eclipse.revealed { opacity: 1; transform: translate(-50%, -50%) scale(1); }

.ecl-corona {
  position: absolute; inset: -40%;
  border-radius: 50%;
  background: radial-gradient(circle, color-mix(in srgb, var(--color-countdown, #F0A85C) 55%, transparent) 30%, transparent 62%);
  animation: eclPulse 5s ease-in-out infinite;
}
@keyframes eclPulse { 0%,100% { transform: scale(0.95); opacity: 0.7; } 50% { transform: scale(1.08); opacity: 1; } }

.ecl-disc {
  position: absolute; inset: 0;
  border-radius: 50%;
  background: var(--color-bg, #1B1430);
  box-shadow:
    0 0 0 2px color-mix(in srgb, var(--color-countdown, #F0A85C) 90%, transparent),
    inset 0 0 40px color-mix(in srgb, var(--color-bg, #1B1430) 80%, #000);
}

.ecl-diamond {
  position: absolute; top: 8%; right: 12%;
  width: 14px; height: 14px;
  background: #FFF;
  border-radius: 50%;
  box-shadow: 0 0 16px 6px color-mix(in srgb, var(--color-countdown, #F0A85C) 90%, #fff);
  animation: eclSparkle 5s ease-in-out infinite;
}
@keyframes eclSparkle { 0%,100% { opacity: 0.5; transform: scale(0.7); } 50% { opacity: 1; transform: scale(1.1); } }

/* Texte */
.ecl-hero-inner {
  position: relative;
  z-index: 2;
  margin-top: clamp(180px, 52cqi, 300px);
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 1.5s ease 0.4s, transform 1.5s ease 0.4s;
}
.ecl-hero-inner.revealed { opacity: 1; transform: translateY(0); }

.ecl-eyebrow {
  font-size: 0.6rem;
  letter-spacing: 0.55em;
  text-transform: uppercase;
  opacity: 0.55;
  margin-bottom: 28px;
}
.ecl-names {
  font-family: 'Fraunces', serif;
  font-weight: 300;
  font-size: var(--size-names, clamp(2.8rem, 15cqi, 6.5rem));
  line-height: 1;
  letter-spacing: -0.01em;
  color: var(--color-names, #FBF3E8);
}
.ecl-rule {
  width: 60px; height: 1px;
  background: var(--color-countdown, #F0A85C);
  margin: 32px auto;
  opacity: 0.8;
}
.ecl-date {
  font-size: 0.64rem; letter-spacing: 0.45em; text-transform: uppercase;
  opacity: 0.6; margin-bottom: 10px;
}
.ecl-loc {
  font-size: 0.58rem; letter-spacing: 0.32em; text-transform: uppercase;
  color: var(--color-countdown, #F0A85C); opacity: 0.85;
}
</style>
