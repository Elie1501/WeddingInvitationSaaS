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

// Symbole spirituel configurable — identité Sanctuaire
const symbolGlyph = computed(() => {
  const s = props.config.symbol || props.config.content?.symbol || '';
  if (s === 'cross')    return '✝';
  if (s === 'star')     return '✡';
  if (s === 'crescent') return '☽';
  return '';
});

const verse = computed(() => props.config.verse || props.config.content?.verse || '');
</script>

<template>
  <div class="san-wrap">

    <!-- ── 1. PAGE DE GARDE ── -->
    <section class="san-hero">
      <div class="san-hero-inner" :class="{ revealed: isLoaded }">

        <div v-if="symbolGlyph" class="san-symbol">{{ symbolGlyph }}</div>

        <div class="san-top-rule" aria-hidden="true" />

        <p class="san-eyebrow">Célébration du Mariage</p>

        <h1 class="san-names template-title main-names">{{ displayNames }}</h1>

        <div class="san-ornament" aria-hidden="true">
          <div class="orn-line" /><div class="orn-diamond" /><div class="orn-line" />
        </div>

        <p v-if="verse" class="san-verse">{{ verse }}</p>

        <p class="san-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="san-loc">{{ displayLocation }}</p>

        <div class="san-bottom-rule" aria-hidden="true" />
      </div>
    </section>

    <!-- ── 2. COMPTE À REBOURS ── -->
    <div class="san-sep">
      <div class="san-divider" aria-hidden="true" />
      <CardSectionCountdown :config="props.config" :event="props.event" />
      <div class="san-divider" aria-hidden="true" />
    </div>

    <!-- ── 3. LE PROGRAMME ── -->
    <div class="san-sep">
      <CardSectionProgramme :config="props.config" :event="props.event" />
      <div class="san-divider" aria-hidden="true" />
    </div>

    <!-- ── 4. RSVP ── -->
    <div class="san-sep">
      <CardSectionRSVP :config="props.config" :event="props.event" />
      <div class="san-ornament san-rsvp-orn" aria-hidden="true">
        <div class="orn-line" /><div class="orn-diamond" /><div class="orn-line" />
      </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Spectral:ital,wght@0,300;0,400;1,300;1,400&display=swap');

/* ── Conteneur racine ── */
.san-wrap {
  background: var(--color-bg, #F4EEE0);
  color: var(--color-text, #2C2010);
  font-family: 'Spectral', var(--card-font, serif);
  min-height: 100svh;
  overflow-x: hidden;
}

/* ── 1. HERO ── */
.san-hero {
  min-height: 100svh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
  position: relative;
}

.san-hero-inner {
  max-width: 560px;
  width: 100%;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 1.9s cubic-bezier(0.22, 1, 0.36, 1), transform 1.9s cubic-bezier(0.22, 1, 0.36, 1);
}
.san-hero-inner.revealed { opacity: 1; transform: translateY(0); }

.san-symbol {
  font-family: 'EB Garamond', serif;
  font-size: clamp(1.8rem, 6cqi, 2.8rem);
  color: var(--color-countdown, #B8963C);
  opacity: 0.72;
  margin-bottom: 28px;
  line-height: 1;
}

.san-top-rule, .san-bottom-rule {
  width: 100%;
  max-width: 260px;
  height: 1px;
  background: var(--color-text, #2C2010);
  opacity: 0.08;
  margin: 0 auto 28px;
}

.san-eyebrow {
  font-family: 'EB Garamond', serif;
  font-size: 0.6rem;
  letter-spacing: 0.52em;
  text-transform: uppercase;
  opacity: 0.32;
  margin-bottom: 28px;
}

.san-names {
  font-family: 'EB Garamond', serif;
  font-weight: 400;
  font-size: var(--size-names, clamp(2.8rem, 12cqi, 7rem));
  line-height: 1.06;
  color: var(--color-names, #1A1208);
  letter-spacing: 0.05em;
}

/* Ornement en losange */
.san-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 28px auto;
  max-width: 220px;
}
.san-rsvp-orn {
  margin-top: 40px;
  margin-bottom: 80px;
}
.orn-line {
  flex: 1;
  height: 1px;
  background: var(--color-countdown, #B8963C);
  opacity: 0.38;
}
.orn-diamond {
  width: 5px;
  height: 5px;
  background: var(--color-countdown, #B8963C);
  transform: rotate(45deg);
  opacity: 0.52;
  flex-shrink: 0;
}

.san-verse {
  font-family: 'EB Garamond', serif;
  font-style: italic;
  font-weight: 400;
  font-size: clamp(0.95rem, 2.5cqi, 1.18rem);
  line-height: 2.05;
  opacity: 0.46;
  max-width: 420px;
  margin: 0 auto 28px;
}

.san-date {
  font-family: 'EB Garamond', serif;
  font-size: 0.62rem;
  letter-spacing: 0.46em;
  text-transform: uppercase;
  opacity: 0.38;
  margin-bottom: 10px;
}

.san-loc {
  font-family: 'EB Garamond', serif;
  font-size: 0.58rem;
  letter-spacing: 0.42em;
  text-transform: uppercase;
  color: var(--color-countdown, #B8963C);
  opacity: 0.78;
}

/* Séparateur dégradé — identité visuelle Sanctuaire */
.san-divider {
  width: 110px;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--color-countdown, #B8963C), transparent);
  margin: 40px auto;
  opacity: 0.28;
}

/* Conteneur de section */
.san-sep {
  text-align: center;
}

@media (max-width: 600px) {
  .san-hero { padding: 60px 24px; }
}
</style>
