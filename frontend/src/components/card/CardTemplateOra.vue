<script setup>
import { computed, ref, onMounted } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true },
  mode:   { type: String, default: 'full' }
});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#FAF8F5',
  accent: props.config.theme?.accent     || '#C5A059',
  text:   props.config.theme?.text       || '#1A1A1A',
}));

const displayNames = computed(() =>
  props.config.content?.names ||
  (props.event.groom_name && props.event.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}`
    : '')
);

const displayDate = computed(() => {
  if (props.config.content?.date_display) return props.config.content.date_display;
  return props.event.date
    ? new Date(props.event.date).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
    : '15 juin 2026';
});

const location = computed(() =>
  props.config.content?.address || props.event.location || ''
);

const imageUrl = computed(() =>
  props.config.content?.image_url ||
  'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'
);

const introText = computed(() =>
  props.config.content?.intro_text ||
  'Nous avons le bonheur de vous convier à la célébration de notre mariage'
);

const isLoaded = ref(false);
onMounted(() => setTimeout(() => isLoaded.value = true, 80));
</script>

<template>
  <div class="eclat-template">

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <div class="hero-photo" :style="{ backgroundImage: `url(${imageUrl})` }"></div>
      <div class="hero-veil"></div>

      <div class="hero-content" :class="{ revealed: isLoaded }">
        <p class="eyebrow">Célébration de Mariage</p>

        <div class="rule"></div>
        <h1 class="main-names">{{ displayNames }}</h1>
        <div class="rule"></div>

        <p class="hero-date">{{ displayDate }}</p>
        <p v-if="location" class="hero-location">{{ location }}</p>
      </div>

      <div class="scroll-cue" :class="{ revealed: isLoaded }">
        <div class="scroll-line"></div>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">
      <div class="body-card">

      <section class="invite-section">
        <p class="invite-text">{{ introText }}</p>

        <div class="diamond-sep">
          <span class="sep-line"></span>
          <span class="diamond"></span>
          <span class="sep-line"></span>
        </div>
      </section>

      <section class="details-section">
        <div class="detail-item">
          <span class="detail-label">Date</span>
          <span class="detail-value">{{ displayDate }}</span>
        </div>
        <span class="detail-divider"></span>
        <div v-if="location" class="detail-item">
          <span class="detail-label">Lieu</span>
          <span class="detail-value">{{ location }}</span>
        </div>
      </section>

      </div><!-- /body-card -->
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Montserrat:wght@300;400&display=swap');

.eclat-template {
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  font-family: var(--card-font, 'Montserrat'), sans-serif;
  overflow-x: hidden;
}

/* ── Hero ── */
.hero {
  height: 100vh;
  min-height: 600px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-photo {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transform: scale(1.04);
}

.hero-veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(0,0,0,0.30) 0%,
    rgba(0,0,0,0.18) 40%,
    rgba(0,0,0,0.42) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 0 36px;
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 1.5s ease-out, transform 1.5s ease-out;
}
.hero-content.revealed { opacity: 1; transform: translateY(0); }

.eyebrow {
  font-size: 0.58rem;
  letter-spacing: 0.5em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.65);
  margin-bottom: 22px;
  font-weight: 300;
}

.rule {
  width: 72px;
  height: 1px;
  background: var(--color-countdown);
  margin: 16px auto;
  opacity: 0.85;
}

.main-names {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-weight: 300;
  font-size: var(--size-names, clamp(2.8rem, 11cqi, 6.5rem));
  color: #ffffff;
  line-height: 1.05;
  letter-spacing: 0.01em;
  text-shadow: 0 2px 28px rgba(0,0,0,0.25);
}

.hero-date {
  font-size: 0.68rem;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.72);
  margin-top: 18px;
  font-weight: 300;
}

.hero-location {
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-countdown);
  margin-top: 7px;
}

.scroll-cue {
  position: absolute;
  bottom: 36px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  opacity: 0;
  transition: opacity 2s ease 1.2s;
}
.scroll-cue.revealed { opacity: 0.45; }
.scroll-line {
  width: 1px;
  height: 48px;
  background: #fff;
  margin: 0 auto;
  animation: scrollDrop 2.4s ease-in-out infinite;
  transform-origin: top;
}
@keyframes scrollDrop {
  0%, 100% { transform: scaleY(0.15); opacity: 0; }
  35%, 65%  { transform: scaleY(1); opacity: 1; }
}

/* ── Body ── */
.body { background: var(--color-bg); padding: 0 20px 40px; }

.body-card {
  max-width: 640px;
  margin: 0 auto;
  background: #fff;
  border: 1px solid rgba(197,160,89,0.15);
  box-shadow: 0 8px 48px rgba(0,0,0,0.06), 0 2px 12px rgba(0,0,0,0.03);
  border-radius: 2px;
}

.invite-section {
  padding: 88px 36px 56px;
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.invite-text {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-weight: 300;
  font-size: clamp(1.1rem, 3cqi, 1.5rem);
  line-height: 1.8;
  opacity: 0.72;
}

.diamond-sep {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-top: 48px;
}
.sep-line {
  display: block;
  width: 56px;
  height: 1px;
  background: var(--color-countdown);
  opacity: 0.4;
}
.diamond {
  display: block;
  width: 7px;
  height: 7px;
  background: var(--color-countdown);
  transform: rotate(45deg);
  opacity: 0.65;
}

.details-section {
  padding: 12px 36px 64px;
  max-width: 480px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 26px 0;
  text-align: center;
  width: 100%;
}

.detail-divider {
  display: block;
  width: 28px;
  height: 1px;
  background: var(--color-countdown);
  opacity: 0.25;
}

.detail-label {
  font-size: 0.56rem;
  letter-spacing: 0.45em;
  text-transform: uppercase;
  color: var(--color-countdown);
  opacity: 0.8;
}

.detail-value {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-weight: 300;
  font-size: clamp(1rem, 3cqi, 1.35rem);
  opacity: 0.82;
  line-height: 1.45;
}

.rsvp-wrap {
  padding: 48px 36px 100px;
  max-width: 540px;
  margin: 0 auto;
  text-align: center;
}

.rsvp-heading {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-weight: 300;
  font-size: clamp(1.4rem, 4cqi, 2.1rem);
  margin-bottom: 40px;
  opacity: 0.82;
}

@media (max-width: 600px) {
  .hero { min-height: 100svh; }
  .invite-section  { padding: 64px 24px 40px; }
  .details-section { padding: 0 24px 44px; }
  .rsvp-wrap       { padding: 36px 24px 80px; }
}
</style>
