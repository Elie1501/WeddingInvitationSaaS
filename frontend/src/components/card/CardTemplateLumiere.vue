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

// Verset biblique/littéraire — identité éditoriale Lumière
const verse = computed(() => props.config.verse || props.config.content?.verse || '');
</script>

<template>
  <div class="lum-wrap">
    <!-- Halo lumineux — radial-gradient CSS, aucune image externe -->
    <div class="lum-halo" aria-hidden="true" />

    <!-- ── 1. PAGE DE GARDE ── -->
    <section class="lum-hero">
      <div class="lum-hero-content" :class="{ revealed: isLoaded }">
        <p class="lum-eyebrow">Mariage</p>
        <h1 class="lum-names template-title main-names">{{ displayNames }}</h1>
        <div class="lum-accent-bar" aria-hidden="true" />
        <p v-if="verse" class="lum-verse">{{ verse }}</p>
        <p class="lum-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="lum-loc">{{ displayLocation }}</p>
      </div>
    </section>

    <!-- ── 2. COMPTE À REBOURS ── -->
    <div class="lum-sep">
      <CardSectionCountdown :config="props.config" :event="props.event" />
    </div>

    <!-- ── 3. LE PROGRAMME ── -->
    <div class="lum-sep">
      <CardSectionProgramme :config="props.config" :event="props.event" />
    </div>

    <!-- ── 4. RSVP ── -->
    <div class="lum-sep">
      <div class="lum-rsvp-halo" aria-hidden="true" />
      <CardSectionRSVP :config="props.config" :event="props.event" />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400&family=Hanken+Grotesk:wght@300;400;500&display=swap');

/* ── Conteneur racine ── */
.lum-wrap {
  background: var(--color-bg, #FDFCFA);
  color: var(--color-text, #3A4050);
  font-family: 'Hanken Grotesk', var(--card-font, sans-serif);
  min-height: 100svh;
  overflow-x: hidden;
  position: relative;
}

/* Halo lumineux CSS — évoque la lumière sans image */
.lum-halo {
  position: fixed;
  top: -10%;
  left: 50%;
  transform: translateX(-50%);
  width: 140cqi;
  height: 90vh;
  background: radial-gradient(
    ellipse 55% 55% at 50% 5%,
    color-mix(in srgb, var(--color-countdown, #A8B89C) 18%, transparent) 0%,
    transparent 68%
  );
  pointer-events: none;
  z-index: 0;
}

/* ── 1. HERO ── */
.lum-hero {
  min-height: 100svh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.lum-hero-content {
  max-width: 600px;
  width: 100%;
  opacity: 0;
  transform: translateY(26px);
  transition: opacity 1.6s cubic-bezier(0.22, 1, 0.36, 1), transform 1.6s cubic-bezier(0.22, 1, 0.36, 1);
}
.lum-hero-content.revealed { opacity: 1; transform: translateY(0); }

.lum-eyebrow {
  font-size: 0.58rem;
  letter-spacing: 0.62em;
  text-transform: uppercase;
  opacity: 0.32;
  margin-bottom: 44px;
  font-weight: 400;
}

.lum-names {
  font-family: 'Newsreader', serif;
  font-weight: 300;
  font-size: var(--size-names, clamp(3rem, 14cqi, 8rem));
  line-height: 1.04;
  color: var(--color-names, #1C2028);
  letter-spacing: -0.015em;
}

.lum-accent-bar {
  width: 44px;
  height: 2px;
  background: var(--color-countdown, #A8B89C);
  border-radius: 2px;
  margin: 36px auto;
}

.lum-verse {
  font-family: 'Newsreader', serif;
  font-style: italic;
  font-weight: 300;
  font-size: clamp(0.9rem, 2.4cqi, 1.12rem);
  line-height: 1.95;
  opacity: 0.5;
  max-width: 440px;
  margin: 0 auto 36px;
}

.lum-date {
  font-size: 0.6rem;
  letter-spacing: 0.52em;
  text-transform: uppercase;
  opacity: 0.38;
  font-weight: 300;
  margin-bottom: 10px;
}

.lum-loc {
  font-size: 0.56rem;
  letter-spacing: 0.42em;
  text-transform: uppercase;
  color: var(--color-countdown, #A8B89C);
  opacity: 0.85;
}

/* Séparateurs de sections */
.lum-sep {
  border-top: 1px solid color-mix(in srgb, var(--color-text, #3A4050) 8%, transparent);
  position: relative;
  z-index: 1;
}

/* Halo décoratif avant la section RSVP */
.lum-rsvp-halo {
  width: 220px;
  height: 88px;
  background: radial-gradient(
    ellipse at center,
    color-mix(in srgb, var(--color-countdown, #A8B89C) 22%, transparent) 0%,
    transparent 70%
  );
  margin: 40px auto 0;
}

@media (max-width: 600px) {
  .lum-hero { padding: 60px 24px; }
}
</style>
