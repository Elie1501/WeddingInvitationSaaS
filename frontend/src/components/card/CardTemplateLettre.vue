<script setup>
import { computed } from 'vue';
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

// Identité visuelle Lettre : initiales des deux prénoms
const monogram = computed(() => {
  const parts = displayNames.value.replace(/&/g, ' ').trim().split(/\s+/).filter(Boolean);
  if (parts.length >= 2) return parts[0][0].toUpperCase() + parts[parts.length - 1][0].toUpperCase();
  return parts[0]?.[0]?.toUpperCase() || '';
});
</script>

<template>
  <div class="ltr-wrap">
    <div class="ltr-grain" aria-hidden="true" />

    <!-- ── 1. PAGE DE GARDE ── -->
    <section class="ltr-hero">
      <div class="ltr-hero-inner" :class="{ revealed: isLoaded }">

        <div class="ltr-monogram" aria-hidden="true">{{ monogram }}</div>

        <div class="ltr-filet" aria-hidden="true">
          <div class="filet-line" /><div class="filet-diamond" /><div class="filet-line" />
        </div>

        <p class="ltr-eyebrow">Célébration de Mariage</p>
        <h1 class="ltr-names template-title main-names">{{ displayNames }}</h1>

        <div class="ltr-filet" aria-hidden="true">
          <div class="filet-line" /><div class="filet-diamond" /><div class="filet-line" />
        </div>

        <p class="ltr-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="ltr-loc">{{ displayLocation }}</p>
      </div>
    </section>

    <!-- ── 2. COMPTE À REBOURS ── -->
    <div class="ltr-sep">
      <div class="ltr-section-header">
        <div class="filet-line long" /><span class="filet-ornament">✦</span><div class="filet-line long" />
      </div>
      <CardSectionCountdown :config="props.config" :event="props.event" />
    </div>

    <!-- ── 3. LE PROGRAMME ── -->
    <div class="ltr-sep">
      <div class="ltr-section-header">
        <div class="filet-line long" /><span class="filet-ornament">✦</span><div class="filet-line long" />
      </div>
      <CardSectionProgramme :config="props.config" :event="props.event" />
    </div>

    <!-- ── 4. RSVP ── -->
    <div class="ltr-sep">
      <div class="ltr-section-header">
        <div class="filet-line long" /><span class="filet-ornament">✦</span><div class="filet-line long" />
      </div>
      <CardSectionRSVP :config="props.config" :event="props.event" />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Pinyon+Script&display=swap');

/* ── Conteneur racine ── */
.ltr-wrap {
  background: var(--color-bg, #FAF5EC);
  color: var(--color-text, #3D2E1E);
  font-family: 'Cormorant Garamond', var(--card-font, serif);
  min-height: 100svh;
  overflow-x: hidden;
  position: relative;
}

/* Grain papier (SVG inline, sans image externe) */
.ltr-grain {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.78' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.032;
  pointer-events: none;
  z-index: 0;
}

/* ── 1. HERO ── */
.ltr-hero {
  min-height: 100svh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.ltr-hero-inner {
  max-width: 540px;
  width: 100%;
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 1.7s cubic-bezier(0.22, 1, 0.36, 1), transform 1.7s cubic-bezier(0.22, 1, 0.36, 1);
}
.ltr-hero-inner.revealed { opacity: 1; transform: translateY(0); }

.ltr-monogram {
  font-family: 'Pinyon Script', cursive;
  font-size: clamp(2.2rem, 9vw, 4rem);
  color: var(--color-countdown, #B89850);
  opacity: 0.55;
  margin-bottom: 20px;
  line-height: 1;
  letter-spacing: 0.05em;
}

/* Filets décoratifs */
.ltr-filet {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 22px auto;
  max-width: 240px;
}
.ltr-section-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding-top: 52px;
  margin-bottom: 0;
}
.filet-line {
  flex: 1;
  max-width: 72px;
  height: 1px;
  background: var(--color-countdown, #B89850);
  opacity: 0.38;
}
.filet-line.long { max-width: 110px; }
.filet-diamond {
  width: 5px;
  height: 5px;
  background: var(--color-countdown, #B89850);
  transform: rotate(45deg);
  opacity: 0.52;
  flex-shrink: 0;
}
.filet-ornament {
  color: var(--color-countdown, #B89850);
  opacity: 0.5;
  font-size: 0.58rem;
}

.ltr-eyebrow {
  font-size: 0.56rem;
  letter-spacing: 0.5em;
  text-transform: uppercase;
  opacity: 0.35;
  margin-bottom: 20px;
  font-weight: 300;
}

.ltr-names {
  font-family: 'Pinyon Script', cursive !important;
  font-size: var(--size-names, clamp(3.5rem, 16vw, 8.5rem));
  line-height: 1.1;
  color: var(--color-names, #4A3220);
  letter-spacing: 0.03em;
}

.ltr-date {
  font-size: 0.62rem;
  letter-spacing: 0.42em;
  text-transform: uppercase;
  opacity: 0.42;
  margin-top: 18px;
  font-weight: 300;
}

.ltr-loc {
  font-size: 0.58rem;
  letter-spacing: 0.36em;
  text-transform: uppercase;
  color: var(--color-countdown, #B89850);
  margin-top: 9px;
  opacity: 0.78;
}

/* Séparateurs de sections : ornement filets + section partagée */
.ltr-sep {
  position: relative;
  z-index: 1;
}

@media (max-width: 600px) {
  .ltr-hero { padding: 60px 24px; }
}
</style>
