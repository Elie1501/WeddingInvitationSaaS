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
  bg:     props.config.theme?.background || '#05050f',
  text:   props.config.theme?.text       || '#E8E0FF',
  accent: props.config.theme?.accent     || '#F0D080',
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

// ── Stars canvas ───────────────────────────────────────────
const starsCanvas = ref(null);
const constellCanvas = ref(null);
let starsAnim = null;
let stars = [];
const NUM_STARS = 280;

const initStars = (canvas) => {
  stars = Array.from({ length: NUM_STARS }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 1.4 + 0.2,
    alpha: Math.random(),
    speed: Math.random() * 0.008 + 0.002,
    phase: Math.random() * Math.PI * 2,
  }));
};

const drawStars = (ts) => {
  const c = starsCanvas.value;
  if (!c) return;
  const ctx = c.getContext('2d');
  ctx.clearRect(0, 0, c.width, c.height);
  stars.forEach(s => {
    s.alpha = 0.2 + 0.8 * ((Math.sin(ts * s.speed + s.phase) + 1) / 2);
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(240,220,160,${s.alpha})`;
    ctx.fill();
  });
  starsAnim = requestAnimationFrame(drawStars);
};

// ── Constellation lines ────────────────────────────────────
const constellProgress = ref(0);
let constellTimer = null;
const CONSTELLATION_NODES = [
  [0.20, 0.35], [0.35, 0.20], [0.50, 0.30], [0.65, 0.18], [0.80, 0.32],
  [0.50, 0.50], [0.30, 0.65], [0.70, 0.62], [0.50, 0.78],
];

// ── Parallax ───────────────────────────────────────────────
const scrollY = ref(0);
const onScroll = () => { scrollY.value = window.scrollY; };

const isLoaded = ref(false);
onMounted(() => {
  const c = starsCanvas.value;
  if (c) {
    c.width  = c.offsetWidth  || window.innerWidth;
    c.height = c.offsetHeight || window.innerHeight;
    initStars(c);
    requestAnimationFrame(drawStars);
  }
  setTimeout(() => {
    isLoaded.value = true;
    constellTimer = setInterval(() => {
      constellProgress.value = Math.min(constellProgress.value + 0.025, 1);
      if (constellProgress.value >= 1) clearInterval(constellTimer);
    }, 30);
  }, 600);
  window.addEventListener('scroll', onScroll, { passive: true });
});
onUnmounted(() => {
  cancelAnimationFrame(starsAnim);
  clearInterval(constellTimer);
  window.removeEventListener('scroll', onScroll);
});

const parallaxStyle = (factor) => ({
  transform: `translateY(${scrollY.value * factor}px)`,
});
</script>

<template>
  <div class="celestial-wrap">

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <!-- Stars layer (parallax slow) -->
      <canvas ref="starsCanvas" class="stars-canvas" :style="parallaxStyle(-0.05)" />

      <!-- Moon (decorative, parallax medium) -->
      <div class="moon" :style="parallaxStyle(-0.12)" />

      <!-- Constellation SVG (draws progressively) -->
      <svg class="constell-svg" viewBox="0 0 100 100" preserveAspectRatio="none" :style="parallaxStyle(-0.08)">
        <template v-for="(node, i) in CONSTELLATION_NODES" :key="i">
          <template v-if="i < CONSTELLATION_NODES.length - 1">
            <line
              :x1="node[0]*100" :y1="node[1]*100"
              :x2="CONSTELLATION_NODES[i+1][0]*100" :y2="CONSTELLATION_NODES[i+1][1]*100"
              stroke="var(--color-countdown)"
              stroke-width="0.15"
              :stroke-dasharray="40"
              :stroke-dashoffset="Math.max(0, 40 - 40 * Math.max(0, constellProgress - i/CONSTELLATION_NODES.length) * CONSTELLATION_NODES.length)"
              opacity="0.4"
            />
          </template>
          <circle
            :cx="node[0]*100" :cy="node[1]*100" r="0.5"
            fill="var(--color-countdown)"
            :opacity="constellProgress > i/CONSTELLATION_NODES.length ? 0.9 : 0"
            style="transition: opacity 0.5s"
          />
        </template>
      </svg>

      <!-- Nebula glow -->
      <div class="nebula nebula-a" :style="parallaxStyle(-0.06)" />
      <div class="nebula nebula-b" :style="parallaxStyle(-0.09)" />

      <!-- Copy -->
      <div class="hero-copy" :class="{ reveal: isLoaded }">
        <p class="over-text">INVITATION COSMIQUE</p>
        <h1 class="names">{{ displayNames }}</h1>
        <svg class="orbit-ring" viewBox="0 0 200 20" aria-hidden="true">
          <ellipse cx="100" cy="10" rx="96" ry="7" fill="none" stroke="var(--color-countdown)" stroke-width="0.6" opacity="0.35" />
          <circle cx="100" cy="3" r="2" fill="var(--color-countdown)" opacity="0.7">
            <animateTransform attributeName="transform" type="rotate" from="0 100 10" to="360 100 10" dur="12s" repeatCount="indefinite" />
          </circle>
        </svg>
        <p class="sub-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="sub-loc">{{ displayLocation }}</p>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">
      <section class="quote-section">
        <div class="quote-star">✦</div>
        <p class="quote-text">{{ config.content?.intro_text || '"Nos âmes se sont reconnues parmi des milliers d\'étoiles."' }}</p>
        <div class="quote-star">✦</div>
      </section>

      <section class="details-grid">
        <div class="detail-card">
          <p class="d-label">DATE</p>
          <p class="d-val">{{ displayDate }}</p>
        </div>
        <div v-if="displayLocation" class="detail-card">
          <p class="d-label">LIEU</p>
          <p class="d-val">{{ displayLocation }}</p>
        </div>
      </section>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:ital,wght@1,300;1,400&display=swap');

.celestial-wrap {
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
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

.stars-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.moon {
  position: absolute;
  top: 8%;
  right: 10%;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #fffde8 0%, #F0D080 40%, #c8a830 100%);
  box-shadow: 0 0 40px 12px rgba(240,208,128,0.18), 0 0 120px 40px rgba(240,208,128,0.06);
  animation: moonGlow 6s ease-in-out infinite alternate;
}
@keyframes moonGlow {
  from { box-shadow: 0 0 40px 12px rgba(240,208,128,0.18), 0 0 120px 40px rgba(240,208,128,0.06); }
  to   { box-shadow: 0 0 60px 20px rgba(240,208,128,0.26), 0 0 160px 60px rgba(240,208,128,0.10); }
}

.constell-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.nebula {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
}
.nebula-a {
  width: 500px; height: 350px;
  left: -100px; top: 15%;
  background: radial-gradient(ellipse, rgba(80,40,180,0.22) 0%, transparent 70%);
}
.nebula-b {
  width: 400px; height: 280px;
  right: -80px; bottom: 20%;
  background: radial-gradient(ellipse, rgba(30,80,160,0.18) 0%, transparent 70%);
}

.hero-copy {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 40px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1.8s ease-out, transform 1.8s ease-out;
}
.hero-copy.reveal { opacity: 1; transform: translateY(0); }

.over-text {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: 0.5rem;
  letter-spacing: 0.75em;
  color: var(--color-countdown);
  opacity: 0.7;
  margin-bottom: 24px;
}

.names {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: var(--size-names, clamp(2.8rem, 14cqi, 7.5rem));
  font-weight: 700;
  letter-spacing: 0.05em;
  background: linear-gradient(135deg, #fff 30%, var(--color-countdown) 70%, #fff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.05;
  text-shadow: none;
}

.orbit-ring {
  display: block;
  width: 200px;
  margin: 20px auto;
}

.sub-date {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: 1.1rem;
  letter-spacing: 0.15em;
  opacity: 0.6;
  margin-top: 10px;
}
.sub-loc {
  font-size: 0.6rem;
  letter-spacing: 0.45em;
  text-transform: uppercase;
  color: var(--color-countdown);
  margin-top: 8px;
  opacity: 0.75;
}

/* Body */
.body { background: var(--color-bg); }

.quote-section {
  padding: 80px 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
}
.quote-star {
  color: var(--color-countdown);
  font-size: 1rem;
  opacity: 0.55;
}
.quote-text {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: clamp(1.1rem, 3cqi, 1.55rem);
  line-height: 1.8;
  opacity: 0.65;
  max-width: 560px;
}

.details-grid {
  display: flex;
  justify-content: center;
  gap: 60px;
  padding: 40px 40px 80px;
  border-top: 1px solid rgba(255,255,255,0.07);
  flex-wrap: wrap;
}
.detail-card { text-align: center; }
.d-label {
  font-family: var(--card-font, 'Cinzel'), serif;
  font-size: 0.5rem;
  letter-spacing: 0.55em;
  color: var(--color-countdown);
  opacity: 0.65;
  margin-bottom: 10px;
}
.d-val {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: 1.2rem;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .moon { width: 60px; height: 60px; right: 5%; }
  .nebula { display: none; }
  .details-grid { gap: 36px; padding: 36px 20px 60px; }
  .quote-section { padding: 60px 24px; }
}
</style>
