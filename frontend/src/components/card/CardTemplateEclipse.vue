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

// Hero uniquement — countdown/subEvents délégués aux sections partagées
const { displayNames, displayDate, displayLocation, isLoaded }
  = useTemplateData(() => props.config, () => props.event);
</script>

<template>
  <div class="ecl-wrap">

    <!-- ── 1. PAGE DE GARDE ── -->
    <section class="ecl-hero">
      <div class="ecl-hero-inner" :class="{ revealed: isLoaded }">
        <p class="ecl-eyebrow">Mariage</p>
        <h1 class="ecl-names template-title main-names">{{ displayNames }}</h1>
        <div class="ecl-rule" aria-hidden="true" />
        <p class="ecl-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="ecl-loc">{{ displayLocation }}</p>
      </div>
      <div class="ecl-scroll-hint" :class="{ revealed: isLoaded }" aria-hidden="true">
        <div class="ecl-scroll-line" />
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
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100;0,9..144,300;0,9..144,400;1,9..144,100;1,9..144,300&family=Hanken+Grotesk:wght@300;400;500&display=swap');

/* ── Conteneur racine ── */
.ecl-wrap {
  background: var(--color-bg, #F5F0E8);
  color: var(--color-text, #3D3730);
  font-family: 'Hanken Grotesk', var(--card-font, sans-serif);
  min-height: 100svh;
  overflow-x: hidden;
}

/* Séparateur de sections — reprend la règle visuelle d'origine */
.ecl-sep {
  border-top: 1px solid color-mix(in srgb, var(--color-text, #3D3730) 9%, transparent);
}

/* ── HERO ── */
.ecl-hero {
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
  position: relative;
}

.ecl-hero-inner {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 1.5s cubic-bezier(0.22, 1, 0.36, 1), transform 1.5s cubic-bezier(0.22, 1, 0.36, 1);
}
.ecl-hero-inner.revealed { opacity: 1; transform: translateY(0); }

.ecl-eyebrow {
  font-size: 0.58rem;
  letter-spacing: 0.65em;
  text-transform: uppercase;
  font-weight: 400;
  opacity: 0.35;
  margin-bottom: 48px;
}

.ecl-names {
  font-family: 'Fraunces', serif;
  font-weight: 100;
  font-size: var(--size-names, clamp(3.5rem, 17cqi, 9.5rem));
  line-height: 0.92;
  letter-spacing: -0.025em;
  color: var(--color-names, #1A1512);
  text-transform: lowercase;
}

.ecl-rule {
  width: 56px;
  height: 1px;
  background: var(--color-countdown, #C0603A);
  margin: 40px auto;
}

.ecl-date {
  font-size: 0.62rem;
  letter-spacing: 0.52em;
  text-transform: uppercase;
  font-weight: 300;
  opacity: 0.45;
  margin-bottom: 10px;
}

.ecl-loc {
  font-size: 0.58rem;
  letter-spacing: 0.42em;
  text-transform: uppercase;
  color: var(--color-countdown, #C0603A);
  opacity: 0.85;
}

.ecl-scroll-hint {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 1.8s ease 1.2s;
}
.ecl-scroll-hint.revealed { opacity: 0.3; }
.ecl-scroll-line {
  width: 1px;
  height: 52px;
  background: var(--color-text, #3D3730);
  animation: scrollPulse 2.2s ease-in-out infinite;
  transform-origin: top;
}
@keyframes scrollPulse {
  0%, 100% { transform: scaleY(0.1); opacity: 0; }
  40%, 60%  { transform: scaleY(1);   opacity: 1; }
}

@media (max-width: 600px) {
  .ecl-hero { padding: 60px 24px; }
}
</style>
