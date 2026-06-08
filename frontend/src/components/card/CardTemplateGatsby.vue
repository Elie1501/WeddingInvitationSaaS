<script setup>
import { computed, ref, onMounted, inject } from 'vue';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, required: true },
  mode:   { type: String, default: 'full' }
});

const emit = defineEmits(['click-image']);
const isEditorMode = inject('isEditorMode', false);

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#100e08',
  text:   props.config.theme?.text       || '#F5E6C8',
  accent: props.config.theme?.accent     || '#D4A853',
}));

const displayNames = computed(() =>
  props.config.content?.names ||
  (props.event.groom_name && props.event.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const displayDate = computed(() =>
  (props.config.content?.date_display ||
   (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 JUIN 2026')).toUpperCase()
);
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');
const imageUrl = computed(() => props.config.content?.image_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1200');

// Deco lines progress (SVG animation driven by JS timer)
const decoProgress = ref(0);
let decoTimer = null;

const shimmer = ref(false);
const isLoaded = ref(false);

onMounted(() => {
  decoTimer = setInterval(() => {
    decoProgress.value = Math.min(decoProgress.value + 0.015, 1);
    if (decoProgress.value >= 1) clearInterval(decoTimer);
  }, 20);
  setTimeout(() => { isLoaded.value = true; }, 200);
  setTimeout(() => { shimmer.value = true; }, 2000);
});
</script>

<template>
  <div class="gatsby-wrap" :style="{ '--bg': theme.bg, '--text': theme.text, '--accent': theme.accent }">

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero">

      <!-- Background photo -->
      <div class="hero-bg"
           :style="{ backgroundImage: `url(${imageUrl})` }"
           :class="{ 'editor-img': isEditorMode }"
           @click="isEditorMode ? emit('click-image', 'image_url') : null" />

      <!-- Overlay -->
      <div class="deco-overlay" />

      <!-- Art deco geometric lines SVG -->
      <svg class="deco-svg" viewBox="0 0 400 600" fill="none" aria-hidden="true">
        <!-- Outer rectangle -->
        <rect x="20" y="20" width="360" height="560" stroke="#D4A853"
          stroke-width="0.8" opacity="0.45"
          :stroke-dasharray="1840"
          :stroke-dashoffset="1840 * (1 - decoProgress * 0.7)" />
        <!-- Inner rectangle -->
        <rect x="35" y="35" width="330" height="530" stroke="#D4A853"
          stroke-width="0.4" opacity="0.25"
          :stroke-dasharray="1720"
          :stroke-dashoffset="1720 * (1 - Math.max(0, decoProgress - 0.1) * 1.1)" />
        <!-- Fan top -->
        <path d="M200,35 L180,70 L200,60 L220,70 Z" stroke="#D4A853" stroke-width="0.7" fill="none" opacity="0.6"
          :stroke-dasharray="120" :stroke-dashoffset="120 * (1 - Math.max(0, decoProgress - 0.5) * 2)" />
        <!-- Fan bottom -->
        <path d="M200,565 L180,530 L200,540 L220,530 Z" stroke="#D4A853" stroke-width="0.7" fill="none" opacity="0.6"
          :stroke-dasharray="120" :stroke-dashoffset="120 * (1 - Math.max(0, decoProgress - 0.5) * 2)" />
        <!-- Horizontal top -->
        <line x1="35" y1="120" x2="365" y2="120" stroke="#D4A853" stroke-width="0.5" opacity="0.3"
          :stroke-dasharray="330" :stroke-dashoffset="330 * (1 - Math.max(0, decoProgress - 0.3) * 1.5)" />
        <line x1="35" y1="124" x2="365" y2="124" stroke="#D4A853" stroke-width="0.3" opacity="0.2"
          :stroke-dasharray="330" :stroke-dashoffset="330 * (1 - Math.max(0, decoProgress - 0.35) * 1.5)" />
        <!-- Horizontal bottom -->
        <line x1="35" y1="480" x2="365" y2="480" stroke="#D4A853" stroke-width="0.5" opacity="0.3"
          :stroke-dasharray="330" :stroke-dashoffset="330 * (1 - Math.max(0, decoProgress - 0.3) * 1.5)" />
        <!-- Diamond center -->
        <path d="M200,290 L220,310 L200,330 L180,310 Z" stroke="#D4A853" stroke-width="0.8" fill="none"
          opacity="0.5"
          :stroke-dasharray="80" :stroke-dashoffset="80 * (1 - Math.max(0, decoProgress - 0.6) * 2.5)" />
        <!-- Sunburst lines from center -->
        <g opacity="0.2">
          <line v-for="a in 12" :key="a" :x1="200" :y1="310"
            :x2="200 + 55 * Math.cos(a * Math.PI / 6)"
            :y2="310 + 55 * Math.sin(a * Math.PI / 6)"
            stroke="#D4A853" stroke-width="0.4"
            :stroke-dasharray="60"
            :stroke-dashoffset="60 * (1 - Math.max(0, decoProgress - 0.7) * 3.3)"
          />
        </g>
      </svg>

      <!-- Copy -->
      <div class="hero-copy" :class="{ reveal: isLoaded }">
        <p class="eyebrow">INVITATION · MCMXXVI</p>
        <div class="gold-rule" />
        <h1 class="names" :class="{ shimmer: shimmer }">{{ displayNames }}</h1>
        <div class="gold-rule" />
        <p class="sub-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="sub-loc">{{ displayLocation }}</p>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">

      <!-- Invitation card block -->
      <section class="invite-card">
        <!-- Art deco corner ornaments -->
        <svg class="corner-svg tl" viewBox="0 0 60 60" fill="none">
          <path d="M5,55 L5,5 L55,5" stroke="#D4A853" stroke-width="1" opacity="0.5" />
          <path d="M5,5 L22,22" stroke="#D4A853" stroke-width="0.5" opacity="0.35" />
          <circle cx="5" cy="5" r="3" fill="none" stroke="#D4A853" stroke-width="0.8" opacity="0.5" />
        </svg>
        <svg class="corner-svg tr" viewBox="0 0 60 60" fill="none">
          <path d="M55,55 L55,5 L5,5" stroke="#D4A853" stroke-width="1" opacity="0.5" />
          <path d="M55,5 L38,22" stroke="#D4A853" stroke-width="0.5" opacity="0.35" />
          <circle cx="55" cy="5" r="3" fill="none" stroke="#D4A853" stroke-width="0.8" opacity="0.5" />
        </svg>
        <svg class="corner-svg bl" viewBox="0 0 60 60" fill="none">
          <path d="M5,5 L5,55 L55,55" stroke="#D4A853" stroke-width="1" opacity="0.5" />
          <circle cx="5" cy="55" r="3" fill="none" stroke="#D4A853" stroke-width="0.8" opacity="0.5" />
        </svg>
        <svg class="corner-svg br" viewBox="0 0 60 60" fill="none">
          <path d="M55,5 L55,55 L5,55" stroke="#D4A853" stroke-width="1" opacity="0.5" />
          <circle cx="55" cy="55" r="3" fill="none" stroke="#D4A853" stroke-width="0.8" opacity="0.5" />
        </svg>

        <p class="card-label">AVEC LE PLAISIR DE</p>
        <div class="diamond-row">
          <span class="diam">◆</span>
          <span class="diam-line" />
          <span class="diam">◆</span>
          <span class="diam-line" />
          <span class="diam">◆</span>
        </div>
        <p class="card-body">{{ config.content?.intro_text || 'Vous convier à la célébration somptueuse de notre union dans la grande tradition des soirées d\'exception.' }}</p>
        <div class="diamond-row">
          <span class="diam">◆</span>
          <span class="diam-line" />
          <span class="diam">◆</span>
          <span class="diam-line" />
          <span class="diam">◆</span>
        </div>
      </section>

      <!-- Info grid -->
      <section class="info-grid">
        <div class="info-col">
          <p class="i-label">DATE</p>
          <p class="i-val">{{ displayDate }}</p>
        </div>
        <template v-if="displayLocation">
          <div class="info-div" />
          <div class="info-col">
            <p class="i-label">LIEU</p>
            <p class="i-val">{{ displayLocation }}</p>
          </div>
        </template>
        <div class="info-div" />
        <div class="info-col">
          <p class="i-label">TENUE</p>
          <p class="i-val">{{ config.content?.dress_code || 'Black Tie' }}</p>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cinzel+Decorative:wght@400;700&family=Cormorant:ital,wght@1,300&display=swap');

.gatsby-wrap {
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
  font-family: 'Playfair Display', serif;
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
  filter: sepia(0.4) brightness(0.28) contrast(1.1);
  transform: scale(1.04);
}
.hero-bg.editor-img { cursor: pointer; }
.hero-bg.editor-img:hover { filter: sepia(0.2) brightness(0.38); }

.deco-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(16,14,8,0.6) 0%, transparent 30%, transparent 65%, rgba(16,14,8,0.75) 100%);
}

.deco-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

/* Copy */
.hero-copy {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 40px;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 1.5s ease-out, transform 1.5s ease-out;
}
.hero-copy.reveal { opacity: 1; transform: translateY(0); }

.eyebrow {
  font-family: 'Cinzel Decorative', serif;
  font-size: 0.5rem;
  letter-spacing: 0.75em;
  color: var(--accent);
  opacity: 0.75;
  margin-bottom: 20px;
}

.gold-rule {
  width: 120px;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--accent), transparent);
  margin: 16px auto;
}

.names {
  font-family: 'Cinzel Decorative', serif;
  font-size: clamp(2rem, 10vw, 5.5rem);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--accent);
  line-height: 1.1;
  background: linear-gradient(135deg, #c8923a 0%, #F5E090 40%, #D4A853 65%, #b87a28 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 300% 100%;
}
.names.shimmer {
  animation: goldShimmer 3s ease-in-out infinite alternate;
}
@keyframes goldShimmer {
  from { background-position: 0% 50%; }
  to   { background-position: 100% 50%; }
}

.sub-date {
  font-size: 0.6rem;
  letter-spacing: 0.55em;
  text-transform: uppercase;
  opacity: 0.6;
  margin-top: 18px;
}
.sub-loc {
  font-size: 0.6rem;
  letter-spacing: 0.35em;
  color: var(--accent);
  margin-top: 7px;
  opacity: 0.8;
}

/* Body */
.body { background: var(--bg); }

.invite-card {
  max-width: 640px;
  margin: 0 auto;
  padding: 70px 80px;
  text-align: center;
  position: relative;
  border: 1px solid rgba(212,168,83,0.15);
  margin-top: 60px;
}
.corner-svg {
  position: absolute;
  width: 56px;
  height: 56px;
}
.tl { top: -2px; left: -2px; }
.tr { top: -2px; right: -2px; }
.bl { bottom: -2px; left: -2px; }
.br { bottom: -2px; right: -2px; }

.card-label {
  font-family: 'Cinzel Decorative', serif;
  font-size: 0.52rem;
  letter-spacing: 0.7em;
  color: var(--accent);
  opacity: 0.65;
  margin-bottom: 28px;
}

.diamond-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 22px 0;
}
.diam {
  color: var(--accent);
  font-size: 0.5rem;
  opacity: 0.6;
}
.diam-line {
  display: block;
  height: 1px;
  width: 40px;
  background: var(--accent);
  opacity: 0.3;
}

.card-body {
  font-family: 'Cormorant', serif;
  font-style: italic;
  font-size: 1.25rem;
  line-height: 1.9;
  opacity: 0.7;
}

.info-grid {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  padding: 48px 40px 72px;
  border-top: 1px solid rgba(212,168,83,0.12);
  flex-wrap: wrap;
}
.info-col {
  text-align: center;
  padding: 12px 48px;
}
.info-div {
  width: 1px;
  height: 44px;
  background: rgba(212,168,83,0.2);
}
.i-label {
  font-family: 'Cinzel Decorative', serif;
  font-size: 0.45rem;
  letter-spacing: 0.55em;
  color: var(--accent);
  opacity: 0.6;
  margin-bottom: 8px;
}
.i-val {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 1rem;
  opacity: 0.75;
}

@media (max-width: 768px) {
  .invite-card { padding: 48px 36px; }
  .info-col { padding: 12px 24px; }
  .info-div { display: none; }
}
</style>
