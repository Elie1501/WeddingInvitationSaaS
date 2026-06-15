<script setup>
import { computed, ref, onMounted, onUnmounted, inject } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  mode: { type: String, default: 'full' }
});

const emit = defineEmits(['click-image']);
const isEditorMode = inject('isEditorMode', false);

const theme = computed(() => {
  const bgColor = props.config.theme?.background || '#0D0D0D';
  const textColor = getContrastColor(bgColor);

  return {
    black: bgColor,
    cream: textColor,
    sepia: props.config.theme?.accent || '#8B6914',
    goldRose: '#C9956C',
    accent: props.config.theme?.accent || '#8B6914',
    text: textColor
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => props.config.content?.date_display || (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'GRAND ÉCRAN 2026'));
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

// Mouse spotlight effect
const spotlightPos = ref({ x: 50, y: 50 });
const handleMouseMove = (e) => {
  spotlightPos.value = {
    x: (e.clientX / window.innerWidth) * 100,
    y: (e.clientY / window.innerHeight) * 100
  };
};

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove);
});
onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove);
});

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 100);
});
</script>

<template>
  <div class="film-template" :style="{
      '--spot-x': spotlightPos.x + '%',
      '--spot-y': spotlightPos.y + '%',
    }">

    <!-- Film Grain & Projector Overlay -->
    <div class="film-grain"></div>
    <div class="projector-spotlight"></div>

    <!-- Hero Section: Film Reel -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section">
        <div class="film-perforations left"></div>
        <div class="film-perforations right"></div>

        <div class="hero-frame" :class="{ 'frame-shake': isLoaded }">
            <div class="vignette"></div>
            <img
              :src="config.content?.image_url || 'https://images.unsplash.com/photo-1437603565260-19658b689228?w=1200'"
              class="sepia-photo hero-img"
              :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
              @click="isEditorMode ? emit('click-image', 'image_url') : null"
            >

            <div class="hero-overlay-content">
                <p class="film-intro">UNE PRODUCTION ORIGINALE</p>
                <h1 class="main-title ArtDeco">{{ displayNames }}</h1>
                <div class="film-line"></div>
                <p class="film-date">{{ displayDate }}</p>
            </div>
        </div>
    </div>

    <!-- Content Sections -->
    <div v-if="mode === 'full'" class="body-content">

        <!-- Feature Presentation -->
        <section class="presentation-section">
            <div class="container">
                <div class="frame-border p-12">
                    <h2 class="section-title ArtDeco">{{ config.content?.section_title || 'Première Mondiale' }}</h2>
                    <p class="description italic">{{ config.content?.intro_text || '"Une histoire d\'amour pour l\'éternité."' }}</p>
                    <div class="film-divider-fancy"></div>
                    <div class="details-grid">
                        <div class="d-item">
                            <span class="d-label">DATE</span>
                            <p>{{ displayDate }}</p>
                        </div>
                        <div v-if="displayLocation" class="d-item">
                            <span class="d-label">LIEU</span>
                            <p>{{ displayLocation }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Gallery style "Contact Sheet" -->
        <section class="contact-sheet py-20">
            <div class="sheet-grid">
                <div v-for="(src, i) in [
                  config.content?.image_url   || 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400',
                  config.content?.image_url_2 || 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400',
                  config.content?.image_url_2 || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400',
                ]" :key="i" class="sheet-item">
                    <div class="frame-num">{{ 100 + i + 1 }}</div>
                    <img
                      :src="src"
                      class="sepia-photo"
                      :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
                      @click="isEditorMode ? emit('click-image', i === 0 ? 'image_url' : 'image_url_2') : null"
                    >
                </div>
            </div>
        </section>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@400;700&family=Playfair+Display:ital,wght@0,400;1,400&display=swap');

.ArtDeco { font-family: var(--card-font, 'Cormorant SC'), serif; letter-spacing: 0.1em; }

.film-template {
  background-color: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Film Grain Overlay */
.film-grain {
  position: absolute;
  inset: 0;
  z-index: 100;
  pointer-events: none;
  opacity: 0.05;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* Projector Spotlight Effect */
.projector-spotlight {
    position: absolute;
    inset: 0;
    z-index: 90;
    pointer-events: none;
    background: radial-gradient(circle 300px at var(--spot-x) var(--spot-y), transparent 0%, rgba(0,0,0,0.8) 100%);
}

.hero-section {
    height: 100vh;
    padding: 20px 60px;
    position: relative;
}

.film-perforations {
    position: absolute;
    top: 0; bottom: 0; width: 40px;
    background-image: radial-gradient(circle, var(--color-bg) 50%, transparent 50%);
    background-size: 20px 40px;
    background-repeat: repeat-y;
}
.film-perforations.left { left: 10px; }
.film-perforations.right { right: 10px; }

.hero-frame {
    width: 100%; height: 100%; border: 1px solid rgba(255,248,240,0.2); position: relative; overflow: hidden;
}

.frame-shake { animation: shake 0.2s infinite; }
@keyframes shake {
    0% { transform: translate(0.5px, 0.5px); }
    50% { transform: translate(-0.5px, -0.5px); }
    100% { transform: translate(0.5px, 0.5px); }
}

.vignette { position: absolute; inset: 0; background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.7) 100%); z-index: 2; }
.sepia-photo { filter: sepia(1) contrast(1.1) brightness(0.9); }
.hero-img { width: 100%; height: 100%; object-fit: cover; }

.hero-overlay-content {
    position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; text-align: center;
}

.film-intro { font-size: 0.7rem; letter-spacing: 0.5em; margin-bottom: 20px; opacity: 0.6; }
.main-title { font-size: var(--size-names, 5rem); text-shadow: 0 0 20px rgba(0,0,0,0.5); }
.film-line { width: 60px; height: 2px; background: var(--color-countdown); margin: 30px 0; }
.film-date { font-size: 1.2rem; letter-spacing: 0.3em; font-weight: 300; }

.body-content { background-color: var(--color-text); color: var(--color-bg); position: relative; z-index: 5; }
.container { max-width: 800px; margin: 0 auto; padding: 0 40px; }

.presentation-section { padding: 80px 0; }
.frame-border { border: 1px solid var(--color-bg); border-style: double; border-width: 6px; text-align: center; }
.section-title { font-size: 3.5rem; margin-bottom: 10px; }
.description { font-size: 1.1rem; line-height: 1.7; opacity: 0.75; margin-top: 10px; }
.film-divider-fancy { height: 1px; background: var(--color-bg); width: 100px; margin: 30px auto; position: relative; }
.film-divider-fancy::after { content: '◈'; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: var(--color-text); padding: 0 10px; }

.details-grid { display: flex; justify-content: center; gap: 60px; margin-top: 40px; }
.d-label { font-size: 0.7rem; opacity: 0.5; letter-spacing: 3px; }

.sheet-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
.sheet-item { width: 200px; position: relative; padding: 10px; background: #000; }
.frame-num { position: absolute; top: 0; left: 5px; color: #fff; font-size: 8px; font-family: monospace; }

@media (max-width: 768px) {
    .main-title { font-size: 14vw; line-height: 1; }
    .hero-section { padding: 10px 40px; }
    .film-perforations { width: 30px; background-size: 15px 30px; }
    .film-date { font-size: 0.9rem; letter-spacing: 0.2em; }
    .section-title { font-size: 12vw; }
    .sheet-item { width: calc(50% - 10px); }
    .container { padding: 0 20px; }
    .details-grid { gap: 20px; flex-wrap: wrap; }
    .frame-border { padding: 30px 16px; }
}

@media (max-width: 480px) {
    .main-title { font-size: 16vw; }
}
</style>
