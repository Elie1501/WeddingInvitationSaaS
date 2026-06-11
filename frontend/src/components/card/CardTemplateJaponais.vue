<script setup>
import { computed, ref, onMounted } from 'vue';
import { getContrastColor } from '../../service/colorUtils';
const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  mode: { type: String, default: 'full' }
});

const theme = computed(() => {
  const bgColor = props.config.theme?.background || '#F5F0E8';
  const textColor = getContrastColor(bgColor);
  
  return {
    bg: bgColor,
    ink: textColor,
    red: '#C0392B',
    gold: props.config.theme?.accent || '#B8960C',
    accent: props.config.theme?.accent || '#B8960C'
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => {
  if (props.config.content?.date_display) return props.config.content.date_display;
  return props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) : 'DATE À VENIR';
});
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');
const introText = computed(() => props.config.content?.intro_text || '"Le bonheur est une chose qui se multiplie quand on le partage."');

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 100);
});
</script>

<template>
  <div class="japonais-template" :style="{
      '--card-bg': theme.bg,
      '--card-text': theme.ink,
      '--card-accent': theme.accent
    }">
    <!-- Washi Paper Texture -->
    <div class="washi-texture"></div>

    <!-- Hero Section -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section">
      <div class="ink-blob" :class="{ 'animate-ink': isLoaded }"></div>
      
      <div class="hero-content" :class="{ 'reveal-text': isLoaded }">
        <div class="stamp">寿</div>
        <h1 class="main-title">{{ displayNames }}</h1>
        <div class="brush-divider">
          <svg viewBox="0 0 500 50" preserveAspectRatio="none">
            <path d="M10,25 C150,5 350,45 490,25" class="brush-path" :class="{ 'draw-brush': isLoaded }" />
          </svg>
        </div>
        <p class="date-text">{{ displayDate }}</p>
      </div>
    </div>

    <!-- Content Sections -->
    <div v-if="mode === 'full'" class="body-content">
      <div class="container">
        <!-- Section 1 -->
        <section class="japonais-section reveal-on-scroll">
          <div class="section-badge">結婚</div>
          <h2 class="section-title">{{ config.content?.section_title || 'Union Sacrée' }}</h2>
          <p class="section-desc">{{ introText }}</p>
          <div class="brush-divider-sm">
            <svg viewBox="0 0 200 30">
                <path d="M5,15 Q100,0 195,15" class="brush-path-sm" />
            </svg>
          </div>
          <p v-if="displayLocation" class="details">{{ displayLocation }}</p>
        </section>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@200;700&family=Playfair+Display:ital,wght@1,400&display=swap');

.japonais-template {
  background-color: var(--card-bg);
  color: var(--card-text);
  font-family: var(--card-font, 'Noto Serif JP'), serif;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.washi-texture {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  opacity: 0.4;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}

.hero-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
}

/* Ink Blob Animation */
.ink-blob {
  position: absolute;
  width: 300px;
  height: 300px;
  background: var(--card-text);
  filter: blur(40px);
  border-radius: 50%;
  opacity: 0;
  transform: scale(0.1);
  z-index: -1;
}

.animate-ink {
  animation: inkSpread 4s cubic-bezier(0.1, 0, 0.3, 1) forwards;
}

@keyframes inkSpread {
  0% { opacity: 0; transform: scale(0.1) rotate(0deg); }
  50% { opacity: 0.15; transform: scale(2) rotate(45deg); border-radius: 40% 60% 30% 70%; }
  100% { opacity: 0.1; transform: scale(4) rotate(90deg); border-radius: 50%; }
}

.hero-content { opacity: 0; transform: translateY(20px); transition: 2s ease-out; }
.reveal-text { opacity: 1; transform: translateY(0); }

.stamp {
  width: 60px;
  height: 60px;
  border: 3px solid var(--red);
  color: var(--red);
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 30px;
  font-weight: 700;
  transform: rotate(-10deg);
  box-shadow: 2px 2px 0 rgba(192, 57, 43, 0.2);
}

.main-title {
  font-family: var(--card-font, 'Playfair Display'), serif;
  font-size: var(--size-names, 4rem);
  font-style: italic;
  margin-bottom: 20px;
}

.brush-divider { width: 300px; margin: 0 auto 30px; }
.brush-path {
  fill: none;
  stroke: var(--card-text);
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 500;
  stroke-dashoffset: 500;
}

.draw-brush {
  animation: drawBrush 2.5s ease-out 1s forwards;
}

@keyframes drawBrush { to { stroke-dashoffset: 0; } }

.date-text {
  text-transform: uppercase;
  letter-spacing: 5px;
  font-size: 0.9rem;
  color: var(--card-accent);
}

.body-content { padding: 100px 0; position: relative; z-index: 2; }
.container { max-width: 600px; margin: 0 auto; padding: 0 20px; }

.section-badge { color: var(--red); font-size: 1.5rem; margin-bottom: 10px; }
.section-title { font-size: 2.5rem; margin-bottom: 20px; font-weight: 200; }
.section-desc { font-style: italic; opacity: 0.7; margin-bottom: 30px; }

.brush-path-sm { fill: none; stroke: var(--card-accent); stroke-width: 3; opacity: 0.5; }

.btn-jap {
    padding: 12px 30px;
    border: 1px solid var(--card-text);
    background: var(--card-text);
    color: var(--card-bg);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 0.7rem;
    margin: 10px;
    transition: 0.4s;
    cursor: pointer;
}
.btn-jap.outline { background: transparent; color: var(--card-text); }
.btn-jap:hover { transform: scale(1.05); background: var(--red); border-color: var(--red); color: white; }


@media (max-width: 600px) {
    .main-title { font-size: 14vw; line-height: 1.1; margin: 15px 0; }
    .stamp { width: 40px; height: 40px; font-size: 1.2rem; }
    .date-text { font-size: 0.9rem; letter-spacing: 0.3em; }
    .section-title { font-size: 2.5rem; }
    .stamp-grid { gap: 15px; }
    .stamp-item { width: 70px; height: 85px; }
    .stamp-item .val { font-size: 1.5rem; }
}

@media (max-width: 400px) {
    .main-title { font-size: 16vw; }
    .stamp-grid { gap: 10px; }
    .stamp-item { width: 60px; height: 75px; }
}
</style>
