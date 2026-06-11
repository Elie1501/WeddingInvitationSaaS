<script setup>
import { computed, ref, onMounted, inject } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event: { type: Object, required: true },
  mode: { type: String, default: 'full' }
});

const emit = defineEmits(['click-image']);
const isEditorMode = inject('isEditorMode', false);

const theme = computed(() => {
  const bgColor = props.config.theme?.background || '#FAF7F0';
  const idealTextColor = getContrastColor(bgColor);

  // If the background is too dark for the default terracotta, we use the ideal text color
  let textColor = '#C1440E'; // Terracotta
  if (getContrastColor(bgColor) === '#ffffff' && getContrastColor(textColor) === '#ffffff') {
      textColor = idealTextColor;
  }

  return {
    terracotta: textColor,
    sand: '#E8D5B0',
    turquoise: '#2E86AB',
    cream: bgColor,
    accent: props.config.theme?.accent || textColor
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => props.config.content?.date_display || (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'ÉTÉ 2026'));
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 100);
});
</script>

<template>
  <div class="riviera-template" :style="{
      '--card-bg': theme.cream,
      '--card-text': theme.terracotta,
      '--card-accent': theme.accent
    }">

    <!-- Mosaic Pattern Background -->
    <div class="mosaic-bg"></div>

    <!-- Hero Section with Sunset Animation -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section">
      <div class="sunset-gradient" :class="{ 'animate-sunset': isLoaded }"></div>

      <div class="hero-content">
        <div class="vintage-badge">ST TROPEZ</div>
        <h1 class="main-title italic">{{ displayNames }}</h1>
        <div class="hero-image-wrapper">
            <img
              :src="config.content?.image_url || 'https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800'"
              alt="Riviera"
              class="hero-img-vintage"
              :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
              @click="isEditorMode ? emit('click-image', 'image_url') : null"
            >
            <div class="photo-overlay"></div>
        </div>
        <p class="hero-date">{{ displayDate }}</p>
      </div>
    </div>

    <!-- Asymmetric Content Blocks -->
    <div v-if="mode === 'full'" class="body-content">
        <!-- Angled Block 1 -->
        <div class="angled-block bg-sand">
            <div class="container py-20">
                <div class="flex-asymmetric">
                    <div class="text-block">
                        <span class="label">La Dolce Vita</span>
                        <h2 class="section-title">{{ config.content?.section_title || 'Le Grand OUI' }}</h2>
                        <p class="description">{{ config.content?.intro_text || 'Rejoignez-nous pour une célébration sous le soleil de la Méditerranée.' }}</p>
                    </div>
                    <div class="decorative-icon">
                        <svg viewBox="0 0 100 100" class="lemon-svg">
                            <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="2" />
                            <path d="M50,10 L50,90 M10,50 L90,50" stroke="currentColor" stroke-width="1" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section Image Turquoise -->
        <div class="overlap-section">
            <div class="image-card turquoise-border">
                <img
                  :src="config.content?.image_url_2 || 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=800'"
                  class="vintage-photo"
                  :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
                  @click="isEditorMode ? emit('click-image', 'image_url_2') : null"
                >
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@1,300;1,600&family=Montserrat:wght@800&display=swap');

.riviera-template {
  background-color: var(--card-bg);
  color: var(--card-text);
  font-family: var(--card-font, 'Cormorant'), serif;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.mosaic-bg {
    position: absolute;
    inset: 0;
    opacity: 0.05;
    background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h20v20H0V0zm20 20h20v20H20V20z' fill='%23C1440E' fill-opacity='0.4' fill-rule='evenodd'/%3E%3C/svg%3E");
    pointer-events: none;
}

.hero-section {
    height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.sunset-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, #2E86AB 0%, #FAF7F0 100%);
    transition: 5s ease-in-out;
}

.animate-sunset {
    background: linear-gradient(180deg, #2E86AB 0%, #E8D5B0 40%, #C1440E 100%);
}

.hero-content { position: relative; z-index: 10; }

.vintage-badge {
    display: inline-block;
    padding: 5px 15px;
    border: 2px solid var(--card-text);
    font-family: var(--card-font, 'Montserrat'), sans-serif;
    font-weight: 800;
    font-size: 0.7rem;
    letter-spacing: 3px;
    margin-bottom: 20px;
}

.main-title {
    font-size: var(--size-names, 5rem);
    font-weight: 600;
    line-height: 0.9;
    margin-bottom: 30px;
}

.hero-image-wrapper {
    width: 280px;
    height: 400px;
    margin: 0 auto 30px;
    position: relative;
    transform: rotate(-3deg);
    box-shadow: 20px 20px 0 var(--sand);
}

.hero-img-vintage { width: 100%; height: 100%; object-fit: cover; filter: sepia(0.3) contrast(1.1); }
.photo-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, transparent 50%, rgba(193, 68, 14, 0.2) 100%);
    pointer-events: none;
}

.hero-date { font-family: var(--card-font, 'Montserrat'), sans-serif; font-size: 1.2rem; letter-spacing: 5px; font-weight: 800; }

.body-content { position: relative; }

.angled-block {
    transform: skewY(-5deg);
    margin: 100px 0;
    padding: 50px 0;
}
.angled-block > * { transform: skewY(5deg); }
.bg-sand { background-color: var(--sand); color: var(--card-text); }

.container { max-width: 800px; margin: 0 auto; padding: 0 40px; }

.flex-asymmetric { display: flex; align-items: center; justify-content: space-between; }
.label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 3px; opacity: 0.7; }
.section-title { font-size: 4rem; font-weight: 600; margin: 10px 0 20px; font-style: italic; }
.description { font-size: 1.1rem; line-height: 1.6; opacity: 0.8; margin-bottom: 20px; }

.btn-riviera {
    padding: 15px 40px;
    background: transparent;
    border: 2px solid var(--card-text);
    color: var(--card-text);
    font-family: var(--card-font, 'Montserrat'), sans-serif;
    font-weight: 800;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    cursor: pointer;
    transition: 0.3s;
}
.btn-riviera:hover { background: var(--card-text); color: var(--card-bg); }
.btn-riviera.solid { background: var(--card-text); color: var(--card-bg); width: 100%; margin-top: 20px; }

.lemon-svg { width: 150px; opacity: 0.2; }

.overlap-section { margin-top: -100px; display: flex; justify-content: flex-end; padding-right: 10%; }
.image-card { width: 350px; padding: 15px; background: white; transform: rotate(2deg); box-shadow: 0 20px 50px rgba(0,0,0,0.1); }
.turquoise-border { border-bottom: 15px solid var(--turquoise); }
.vintage-photo { width: 100%; height: 100%; object-fit: cover; filter: sepia(0.3) contrast(1.1); }

@media (max-width: 768px) {
    .main-title { font-size: 15vw; line-height: 1; margin: 15px 0; }
    .hero-image-wrapper { width: 220px; height: 320px; }
    .hero-date { font-size: 0.9rem; letter-spacing: 0.3em; }
    .section-title { font-size: 14vw; }
    .angled-block { margin: 60px 0; }
    .image-card { width: 80%; margin: 0 auto; }
}

@media (max-width: 480px) {
    .main-title { font-size: 18vw; }
    .section-title { font-size: 16vw; }
}
</style>
