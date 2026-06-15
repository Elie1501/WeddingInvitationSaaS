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
  bg:     props.config.theme?.background || '#1a0610',
  text:   props.config.theme?.text       || '#F5E8E0',
  accent: props.config.theme?.accent     || '#E8B4A0',
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
const imageUrl = computed(() =>
  props.config.content?.image_url ||
  props.config.media?.image_url ||
  'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80'
);

// ── Light particles rising ─────────────────────────────────
const particles = ref([]);
const NUM_PARTICLES = 22;
const initParticles = () => {
  particles.value = Array.from({ length: NUM_PARTICLES }, (_, i) => ({
    id: i,
    x: 10 + Math.random() * 80,
    size: 2 + Math.random() * 3.5,
    dur: 4 + Math.random() * 6,
    delay: Math.random() * 8,
    opacity: 0.2 + Math.random() * 0.5,
  }));
};

// ── Curtain reveal ─────────────────────────────────────────
const curtainOpen = ref(false);
const isLoaded = ref(false);
onMounted(() => {
  initParticles();
  setTimeout(() => { curtainOpen.value = true; }, 200);
  setTimeout(() => { isLoaded.value = true; }, 1600);
});
</script>

<template>
  <div class="velvet-wrap">

    <!-- Velvet texture overlay -->
    <div class="velvet-tex" />

    <!-- Rising light particles -->
    <div class="particles-layer" aria-hidden="true">
      <div
        v-for="p in particles" :key="p.id"
        class="particle"
        :style="{
          left: p.x + '%',
          width: p.size + 'px',
          height: p.size + 'px',
          animationDuration: p.dur + 's',
          animationDelay: p.delay + 's',
          opacity: p.opacity,
        }"
      />
    </div>

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <!-- Curtain panels (open on load) -->
      <div class="curtain curtain-l" :class="{ open: curtainOpen }" />
      <div class="curtain curtain-r" :class="{ open: curtainOpen }" />

      <!-- Background photo -->
      <div class="hero-bg"
           :style="{ backgroundImage: `url(${imageUrl})` }"
           :class="{ 'editor-img': isEditorMode }"
           @click="isEditorMode ? emit('click-image', 'image_url') : null" />

      <!-- Deep overlay -->
      <div class="dark-veil" />

      <!-- Candle flames (CSS pseudo-element decoration) -->
      <div class="candles-row" aria-hidden="true">
        <div v-for="n in 3" :key="n" class="candle-wrap">
          <div class="flame"></div>
          <div class="candle-body"></div>
        </div>
      </div>

      <!-- Copy -->
      <div class="hero-copy" :class="{ reveal: isLoaded }">
        <p class="eyebrow">Une Nuit Inoubliable</p>
        <div class="velvet-rule" />
        <h1 class="names">{{ displayNames }}</h1>
        <div class="velvet-rule" />
        <p class="sub-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="sub-loc">{{ displayLocation }}</p>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">

      <!-- Masked reveal text block -->
      <section class="reveal-section">
        <div class="reveal-inner">
          <p class="rev-label">L'INVITATION</p>
          <p class="rev-text">{{ config.content?.intro_text || '"Laissez-vous envelopper par la douceur d\'une nuit de velours, où l\'amour brille comme mille bougies."' }}</p>
        </div>
      </section>

      <!-- Details with glow -->
      <section class="details-section">
        <div class="detail-item">
          <span class="d-key">DATE</span>
          <span class="d-val glow-text">{{ displayDate }}</span>
        </div>
        <template v-if="displayLocation">
          <div class="d-sep" />
          <div class="detail-item">
            <span class="d-key">LIEU</span>
            <span class="d-val glow-text">{{ displayLocation }}</span>
          </div>
        </template>
        <div class="d-sep" />
        <div class="detail-item">
          <span class="d-key">TENUE</span>
          <span class="d-val">{{ config.content?.dress_code || 'Tenue de soirée' }}</span>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Cinzel:wght@400;600&display=swap');

.velvet-wrap {
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
}

.velvet-tex {
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='v'%3E%3CfeTurbulence type='turbulence' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23v)'/%3E%3C/svg%3E");
  opacity: 0.04;
  pointer-events: none;
  z-index: 0;
  mix-blend-mode: soft-light;
}

/* Particles */
.particles-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}
.particle {
  position: absolute;
  bottom: -10%;
  border-radius: 50%;
  background: radial-gradient(circle, var(--color-countdown) 0%, transparent 70%);
  animation: particleRise linear infinite;
}
@keyframes particleRise {
  0%   { transform: translateY(0) scale(1);    opacity: var(--op, 0.4); }
  60%  { opacity: calc(var(--op, 0.4) * 1.2); }
  100% { transform: translateY(-110vh) scale(0.4); opacity: 0; }
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

/* Curtain panels */
.curtain {
  position: absolute;
  top: 0; bottom: 0;
  width: 50%;
  z-index: 20;
  transition: transform 1.2s cubic-bezier(0.77, 0, 0.18, 1);
  background: linear-gradient(to bottom, #2a0820 0%, #1a0610 50%, #2a0820 100%);
}
.curtain-l { left: 0; transform-origin: left; }
.curtain-r { right: 0; transform-origin: right; }
.curtain-l.open { transform: scaleX(0); }
.curtain-r.open { transform: scaleX(0); }

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: brightness(0.28) saturate(0.6) contrast(1.1);
  transform: scale(1.04);
}
.hero-bg.editor-img { cursor: pointer; }
.hero-bg.editor-img:hover { filter: brightness(0.38) saturate(0.8); }

.dark-veil {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 70% at 50% 45%, transparent 10%, rgba(26,6,16,0.92) 100%),
    linear-gradient(180deg, rgba(26,6,16,0.5) 0%, transparent 20%, transparent 75%, rgba(26,6,16,0.7) 100%);
}

/* Candle decorations */
.candles-row {
  position: absolute;
  bottom: 12%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 60px;
  z-index: 5;
  opacity: 0.35;
}
.candle-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.candle-body {
  width: 5px;
  height: 36px;
  background: linear-gradient(to bottom, #f5e8d0 0%, #e0ccb0 100%);
  border-radius: 1px;
}
.flame {
  width: 8px;
  height: 12px;
  background: radial-gradient(ellipse at 50% 80%, #FFF5A0 0%, #FFA040 40%, transparent 100%);
  border-radius: 50% 50% 35% 35%;
  margin-bottom: 2px;
  animation: flicker 1.8s ease-in-out infinite alternate;
  transform-origin: bottom center;
}
@keyframes flicker {
  0%   { transform: scaleX(1) scaleY(1) rotate(-2deg); opacity: 1; }
  33%  { transform: scaleX(0.85) scaleY(1.1) rotate(1deg); opacity: 0.9; }
  66%  { transform: scaleX(1.1) scaleY(0.95) rotate(-1deg); opacity: 0.95; }
  100% { transform: scaleX(0.9) scaleY(1.05) rotate(2deg); opacity: 1; }
}

/* Copy */
.hero-copy {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 40px;
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 1.4s ease 0.8s, transform 1.4s ease 0.8s;
}
.hero-copy.reveal { opacity: 1; transform: translateY(0); }

.eyebrow {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: 0.5rem;
  letter-spacing: 0.75em;
  color: var(--color-countdown);
  opacity: 0.7;
  margin-bottom: 22px;
}

.velvet-rule {
  width: 80px;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--color-countdown), transparent);
  margin: 16px auto;
  opacity: 0.6;
}

.names {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-weight: 300;
  font-size: var(--size-names, clamp(3rem, 14vw, 7.5rem));
  color: #fff;
  line-height: 1.05;
  letter-spacing: 0.02em;
  text-shadow: 0 0 60px rgba(232,180,160,0.35), 0 2px 30px rgba(0,0,0,0.6);
}

.sub-date {
  font-size: 0.7rem;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  opacity: 0.55;
  margin-top: 20px;
  font-style: normal;
  font-family: var(--card-font, 'Cinzel'), serif;
}
.sub-loc {
  font-size: 0.6rem;
  letter-spacing: 0.35em;
  color: var(--color-countdown);
  margin-top: 7px;
  opacity: 0.8;
  font-family: var(--card-font, 'Cinzel'), serif;
}

/* Body */
.body { background: var(--color-bg); position: relative; z-index: 2; }

.reveal-section {
  padding: 80px 40px;
  max-width: 680px;
  margin: 0 auto;
  text-align: center;
  border-bottom: 1px solid rgba(232,180,160,0.1);
}
.rev-label {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: 0.48rem;
  letter-spacing: 0.72em;
  color: var(--color-countdown);
  opacity: 0.6;
  margin-bottom: 28px;
}
.rev-text {
  font-style: italic;
  font-size: clamp(1.1rem, 3vw, 1.55rem);
  line-height: 1.9;
  opacity: 0.65;
}

.details-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  padding: 56px 40px 80px;
  flex-wrap: wrap;
}
.detail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px 48px;
}
.d-sep {
  width: 1px;
  height: 50px;
  background: rgba(232,180,160,0.2);
}
.d-key {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: 0.45rem;
  letter-spacing: 0.6em;
  color: var(--color-countdown);
  opacity: 0.6;
}
.d-val {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: 1.1rem;
  opacity: 0.8;
}
.glow-text {
  text-shadow: 0 0 20px rgba(232,180,160,0.3);
}

@media (max-width: 768px) {
  .candles-row { gap: 40px; }
  .details-section { flex-direction: column; gap: 24px; }
  .d-sep { display: none; }
  .reveal-section { padding: 56px 24px; }
}
</style>
