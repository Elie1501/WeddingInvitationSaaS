<script setup>
import { computed, ref, onMounted, onUnmounted, inject } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true },
  mode:   { type: String, default: 'full' }
});

const emit = defineEmits(['click-image']);
const isEditorMode = inject('isEditorMode', false);

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#080808',
  text:   props.config.theme?.text       || '#F0EAE0',
  accent: props.config.theme?.accent     || '#D4853A',
}));

const displayNames = computed(() =>
  props.config.content?.names ||
  (props.event.groom_name && props.event.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const displayDate = computed(() =>
  props.config.content?.date_display ||
  (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 juin 2026')
);
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');
const imageUrl = computed(() => props.config.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200');

// ── Film grain canvas ──────────────────────────────────────
const canvasRef = ref(null);
let grainFrame = null;
const drawGrain = () => {
  const c = canvasRef.value;
  if (!c) return;
  const ctx = c.getContext('2d');
  c.width  = c.offsetWidth  || window.innerWidth;
  c.height = c.offsetHeight || window.innerHeight;
  const img = ctx.createImageData(c.width, c.height);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = (Math.random() * 80) | 0;
    img.data[i] = img.data[i+1] = img.data[i+2] = v;
    img.data[i+3] = (Math.random() * 45) | 0;
  }
  ctx.putImageData(img, 0, 0);
  grainFrame = requestAnimationFrame(drawGrain);
};

// ── Letter-by-letter reveal ────────────────────────────────
const chars = ref([]);
const cursorVisible = ref(true);
let charTimers = [];
const revealLetters = (text) => {
  chars.value = [];
  charTimers.forEach(clearTimeout);
  charTimers = [];
  [...text].forEach((ch, i) => {
    charTimers.push(setTimeout(() => {
      chars.value.push(ch);
      if (i === text.length - 1) cursorVisible.value = false;
    }, 900 + i * 75));
  });
};

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => { isLoaded.value = true; revealLetters(displayNames.value); }, 400);
  drawGrain();
});
onUnmounted(() => { cancelAnimationFrame(grainFrame); charTimers.forEach(clearTimeout); });
</script>

<template>
  <div class="cinema-wrap">

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <!-- Background photo -->
      <div class="hero-bg"
           :style="{ backgroundImage: `url(${imageUrl})` }"
           :class="{ 'editor-img': isEditorMode }"
           @click="isEditorMode ? emit('click-image', 'image_url') : null" />

      <!-- Cinematic grading -->
      <div class="noir-veil" />
      <canvas ref="canvasRef" class="grain" />

      <!-- Letterbox bars -->
      <div class="bar bar-top" />
      <div class="bar bar-bottom" />

      <!-- Film perforations (decorative) -->
      <div class="perfs perfs-l">
        <div v-for="n in 14" :key="n" class="hole" />
      </div>
      <div class="perfs perfs-r">
        <div v-for="n in 14" :key="n" class="hole" />
      </div>

      <!-- Hero copy -->
      <div class="hero-copy" :class="{ reveal: isLoaded }">
        <p class="eyebrow">UNE HISTOIRE D'AMOUR</p>
        <div class="rule" />
        <h1 class="title" :aria-label="displayNames">
          <span v-for="(ch, i) in chars" :key="i">{{ ch }}</span>
          <span v-if="cursorVisible" class="cursor">_</span>
        </h1>
        <div class="rule" />
        <p class="sub-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="sub-loc">{{ displayLocation }}</p>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">

      <!-- Credits strip -->
      <section class="credits">
        <div class="c-item">
          <span class="c-role">RÉALISÉ PAR</span>
          <span class="c-val">L'Amour</span>
        </div>
        <div class="c-sep" />
        <div class="c-item">
          <span class="c-role">AVEC</span>
          <span class="c-val">{{ displayNames }}</span>
        </div>
        <div class="c-sep" />
        <div class="c-item">
          <span class="c-role">EN PRÉSENCE DE</span>
          <span class="c-val">Vous</span>
        </div>
      </section>

      <!-- Synopsis -->
      <section class="synopsis">
        <span class="syn-label">SYNOPSIS</span>
        <p class="syn-text">{{ config.content?.intro_text || 'Deux âmes que le destin avait prédestinées. Une rencontre, une histoire, une vie entière à écrire ensemble. Le film commence maintenant.' }}</p>
      </section>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Courier+Prime:ital,wght@0,400;1,400&family=Special+Elite&display=swap');

.cinema-wrap {
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
  font-family: var(--card-font, 'Courier Prime'), monospace;
}

/* Hero */
.hero {
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: grayscale(0.6) brightness(0.38) contrast(1.15);
  transform: scale(1.03);
  transition: filter 0.4s;
}
.hero-bg.editor-img { cursor: pointer; }
.hero-bg.editor-img:hover { filter: grayscale(0.3) brightness(0.5) contrast(1.15); }

.noir-veil {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 80% at 50% 50%, transparent 20%, rgba(0,0,0,0.88) 100%);
}

.grain {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  mix-blend-mode: overlay;
  opacity: 0.55;
}

.bar {
  position: absolute;
  left: 0; right: 0;
  height: 11vh;
  background: #000;
  z-index: 20;
}
.bar-top    { top: 0; }
.bar-bottom { bottom: 0; }

/* Perforations */
.perfs {
  position: absolute;
  top: 11vh; bottom: 11vh;
  width: 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  background: rgba(0,0,0,0.65);
  z-index: 21;
}
.perfs-l { left: 0; }
.perfs-r { right: 0; }
.hole {
  width: 13px;
  height: 9px;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 2px;
  background: transparent;
}

/* Copy */
.hero-copy {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 56px;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 1.6s ease-out, transform 1.6s ease-out;
}
.hero-copy.reveal { opacity: 1; transform: translateY(0); }

.eyebrow {
  font-size: 0.52rem;
  letter-spacing: 0.68em;
  color: var(--color-countdown);
  opacity: 0.9;
  margin-bottom: 22px;
}

.rule {
  width: 100px;
  height: 1px;
  background: var(--color-countdown);
  margin: 16px auto;
  opacity: 0.5;
}

.title {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: var(--size-names, clamp(3.2rem, 18cqi, 9.5rem));
  letter-spacing: 0.07em;
  color: #fff;
  line-height: 0.9;
  text-shadow: 0 0 100px rgba(212,133,58,0.25);
}

.cursor {
  color: var(--color-countdown);
  animation: blink 0.9s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

.sub-date {
  font-size: 0.66rem;
  letter-spacing: 0.38em;
  text-transform: uppercase;
  opacity: 0.58;
  margin-top: 20px;
}
.sub-loc {
  font-size: 0.58rem;
  letter-spacing: 0.32em;
  color: var(--color-countdown);
  margin-top: 7px;
  opacity: 0.85;
}

/* Body */
.body { background: var(--color-bg); }

.credits {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  padding: 56px 40px;
  border-top: 1px solid rgba(255,255,255,0.07);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  flex-wrap: wrap;
}
.c-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 0 48px;
}
.c-sep {
  width: 1px;
  height: 50px;
  background: rgba(255,255,255,0.12);
}
.c-role {
  font-size: 0.5rem;
  letter-spacing: 0.55em;
  color: var(--color-countdown);
  opacity: 0.7;
}
.c-val {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: 1.5rem;
  letter-spacing: 0.15em;
}

.synopsis {
  max-width: 680px;
  margin: 0 auto;
  padding: 64px 40px 88px;
  text-align: center;
}
.syn-label {
  display: block;
  font-size: 0.5rem;
  letter-spacing: 0.65em;
  color: var(--color-countdown);
  opacity: 0.6;
  margin-bottom: 28px;
}
.syn-text {
  font-family: var(--card-font, 'Special Elite'), cursive;
  font-size: 1.1rem;
  line-height: 2.1;
  opacity: 0.62;
}

@media (max-width: 768px) {
  .perfs { display: none; }
  .credits { gap: 24px; padding: 40px 20px; }
  .c-sep { display: none; }
  .c-item { padding: 12px 0; }
  .synopsis { padding: 48px 24px 72px; }
}
</style>
