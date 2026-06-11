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
  bg:     props.config.theme?.background || '#F7F4EE',
  text:   props.config.theme?.text       || '#2C2416',
  accent: props.config.theme?.accent     || '#C4718A',
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

// ── SVG ink stroke progress ────────────────────────────────
const inkProgress = ref(0);
let inkTimer = null;

// ── Cherry blossom petals ──────────────────────────────────
const petals = ref([]);
const NUM_PETALS = 18;
const initPetals = () => {
  petals.value = Array.from({ length: NUM_PETALS }, (_, i) => ({
    id: i,
    x: 5 + Math.random() * 90,
    y: -10 - Math.random() * 80,
    size: 6 + Math.random() * 8,
    rot: Math.random() * 360,
    dur: 6 + Math.random() * 8,
    delay: Math.random() * 10,
    sway: 20 + Math.random() * 40,
  }));
};

const isLoaded = ref(false);
onMounted(() => {
  initPetals();
  setTimeout(() => {
    isLoaded.value = true;
    inkTimer = setInterval(() => {
      inkProgress.value = Math.min(inkProgress.value + 0.018, 1);
      if (inkProgress.value >= 1) clearInterval(inkTimer);
    }, 30);
  }, 300);
});
onUnmounted(() => clearInterval(inkTimer));

// Ink stroke total length ≈ 800
const inkDash = computed(() => {
  const total = 800;
  const offset = total * (1 - inkProgress.value);
  return { strokeDasharray: total, strokeDashoffset: offset };
});
</script>

<template>
  <div class="wabi-wrap" :style="{ '--card-bg': theme.bg, '--card-text': theme.text, '--card-accent': theme.accent }">

    <!-- Paper texture overlay -->
    <div class="paper-tex" />

    <!-- Falling petals -->
    <div class="petals-layer" aria-hidden="true">
      <div
        v-for="p in petals" :key="p.id"
        class="petal"
        :style="{
          left: p.x + '%',
          top: p.y + '%',
          width: p.size + 'px',
          height: p.size + 'px',
          animationDuration: p.dur + 's',
          animationDelay: p.delay + 's',
          '--sway': p.sway + 'px',
        }"
      />
    </div>

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <!-- Photo half -->
      <div class="photo-half"
           :class="{ 'editor-img': isEditorMode }"
           :style="{ backgroundImage: `url(${imageUrl})` }"
           @click="isEditorMode ? emit('click-image', 'image_url') : null" />

      <!-- Ink brush SVG (horizontal stroke) -->
      <svg class="ink-stroke" viewBox="0 0 800 120" fill="none" aria-hidden="true">
        <path
          d="M0,60 C50,40 100,80 200,55 C320,28 400,75 500,50 C600,25 700,65 800,58"
          stroke="#2C2416"
          stroke-width="2.5"
          stroke-linecap="round"
          fill="none"
          opacity="0.18"
          v-bind="inkDash"
          style="transition: stroke-dashoffset 0.1s linear;"
        />
      </svg>

      <!-- Copy -->
      <div class="hero-copy" :class="{ reveal: isLoaded }">
        <div class="kana-dec" aria-hidden="true">婚礼</div>
        <h1 class="names">{{ displayNames }}</h1>
        <!-- Ink underline SVG -->
        <svg class="name-ink" viewBox="0 0 300 24" fill="none">
          <path d="M10,12 C60,4 120,20 180,10 C240,2 280,16 290,12"
            :stroke="theme.accent" stroke-width="2" stroke-linecap="round" fill="none"
            :stroke-dasharray="300" :stroke-dashoffset="300 * (1 - inkProgress)"
          />
        </svg>
        <p class="sub-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="sub-loc">{{ displayLocation }}</p>
      </div>

      <!-- Vignette -->
      <div class="vignette" />
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">

      <!-- Quote with brush divider -->
      <section class="quote-section">
        <svg class="brush-div" viewBox="0 0 240 20" fill="none">
          <path d="M0,10 C40,5 80,15 120,10 C160,5 200,15 240,10"
            :stroke="theme.accent" stroke-width="1.5" fill="none" opacity="0.45" />
        </svg>
        <p class="quote">{{ config.content?.intro_text || '"L\'imperfection est la plus belle des perfections."' }}</p>
        <svg class="brush-div mirror" viewBox="0 0 240 20" fill="none">
          <path d="M0,10 C40,5 80,15 120,10 C160,5 200,15 240,10"
            :stroke="theme.accent" stroke-width="1.5" fill="none" opacity="0.45" />
        </svg>
      </section>

      <!-- Details -->
      <section class="details-section">
        <div class="detail-row">
          <span class="d-key">日付 / Date</span>
          <span class="d-val">{{ displayDate }}</span>
        </div>
        <template v-if="displayLocation">
          <div class="ink-rule" />
          <div class="detail-row">
            <span class="d-key">場所 / Lieu</span>
            <span class="d-val">{{ displayLocation }}</span>
          </div>
        </template>
      </section>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400&family=Shippori+Mincho:wght@400;600&family=Dancing+Script:wght@600&display=swap');

.wabi-wrap {
  background: var(--card-bg);
  color: var(--card-text);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
  font-family: var(--card-font, 'Noto Serif JP'), serif;
}

.paper-tex {
  position: fixed;
  inset: 0;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.045;
  pointer-events: none;
  z-index: 0;
}

/* Petals */
.petals-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}
.petal {
  position: absolute;
  border-radius: 50% 0 50% 0;
  background: var(--card-accent);
  opacity: 0;
  animation: petalFall linear infinite;
}
@keyframes petalFall {
  0%   { transform: translateY(-5vh) translateX(0)    rotate(0deg);   opacity: 0; }
  10%  { opacity: 0.55; }
  90%  { opacity: 0.35; }
  100% { transform: translateY(110vh) translateX(var(--sway)) rotate(540deg); opacity: 0; }
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

.photo-half {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: sepia(0.35) brightness(0.55) contrast(1.05);
}
.photo-half.editor-img { cursor: pointer; }
.photo-half.editor-img:hover { filter: sepia(0.15) brightness(0.65); }

.vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 80% at 50% 50%, transparent 20%, rgba(30,18,8,0.88) 100%);
}

.ink-stroke {
  position: absolute;
  bottom: 25%;
  left: -5%;
  width: 110%;
  pointer-events: none;
  z-index: 3;
}

/* Copy */
.hero-copy {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 40px;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 1.6s ease-out, transform 1.6s ease-out;
}
.hero-copy.reveal { opacity: 1; transform: translateY(0); }

.kana-dec {
  font-family: var(--card-font, 'Noto Serif JP'), serif;
  font-size: 0.8rem;
  letter-spacing: 0.4em;
  color: var(--card-accent);
  opacity: 0.55;
  margin-bottom: 18px;
}

.names {
  font-family: var(--card-font, 'Shippori Mincho'), serif;
  font-size: var(--size-names, clamp(2.8rem, 13vw, 7rem));
  font-weight: 400;
  color: #fff;
  line-height: 1.1;
  letter-spacing: 0.02em;
  text-shadow: 0 2px 40px rgba(0,0,0,0.4);
}

.name-ink {
  display: block;
  width: 260px;
  margin: 12px auto 20px;
}

.sub-date {
  font-size: 0.72rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.65);
}
.sub-loc {
  font-size: 0.6rem;
  letter-spacing: 0.35em;
  color: var(--card-accent);
  margin-top: 7px;
  opacity: 0.9;
}

/* Body */
.body { background: var(--card-bg); position: relative; z-index: 2; }

.quote-section {
  padding: 72px 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}
.brush-div { width: 200px; display: block; }
.brush-div.mirror { transform: scaleX(-1); }

.quote {
  font-family: var(--card-font, 'Shippori Mincho'), serif;
  font-size: clamp(1.1rem, 3vw, 1.45rem);
  line-height: 2;
  opacity: 0.68;
  max-width: 540px;
}

.details-section {
  max-width: 480px;
  margin: 0 auto;
  padding: 0 40px 80px;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 20px;
  padding: 18px 0;
}
.d-key {
  font-size: 0.62rem;
  letter-spacing: 0.3em;
  color: var(--card-accent);
  opacity: 0.75;
  white-space: nowrap;
}
.d-val {
  font-family: var(--card-font, 'Shippori Mincho'), serif;
  font-size: 0.95rem;
  opacity: 0.8;
  text-align: right;
}
.ink-rule {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--card-accent), transparent);
  opacity: 0.3;
}

@media (max-width: 768px) {
  .hero-copy { padding: 0 24px; }
  .quote-section { padding: 48px 24px; }
  .details-section { padding: 0 24px 60px; }
}
</style>
