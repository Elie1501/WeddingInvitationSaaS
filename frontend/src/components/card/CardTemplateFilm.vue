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
  const bgColor = props.config.theme?.background || '#F2E9DB';
  return {
    bg: bgColor,
    text: props.config.theme?.text || getContrastColor(bgColor),
    accent: props.config.theme?.accent || '#C77F4E',
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => props.config.content?.date_display || (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 juin 2026'));
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

const heroImg  = computed(() => props.config.content?.image_url   || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800');
const heroImg2 = computed(() => props.config.content?.image_url_2 || 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800');

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 120);
});
</script>

<template>
  <div class="film-template">

    <!-- Hero : album argentique -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section">
      <div class="paper-grain" aria-hidden="true"></div>

      <div class="album" :class="{ loaded: isLoaded }">
        <p class="film-eyebrow">PELLICULE · {{ (displayDate.match(/\d{4}/) || ['2026'])[0] }}</p>

        <!-- Pile de polaroids -->
        <div class="photo-stack">
          <div class="polaroid p-back" aria-hidden="true">
            <div class="tape tape-2"></div>
            <div class="ph-frame">
              <img
                :src="heroImg2"
                class="ph-img"
                :class="{ 'cursor-pointer hover:opacity-90 transition': isEditorMode }"
                @click="isEditorMode ? emit('click-image', 'image_url_2') : null"
              >
            </div>
          </div>
          <div class="polaroid p-front">
            <div class="tape tape-1"></div>
            <div class="ph-frame">
              <img
                :src="heroImg"
                class="ph-img"
                :class="{ 'cursor-pointer hover:opacity-90 transition': isEditorMode }"
                @click="isEditorMode ? emit('click-image', 'image_url') : null"
              >
            </div>
            <p class="ph-caption">{{ displayNames }}</p>
          </div>
        </div>

        <h1 class="main-title">{{ displayNames }}</h1>
        <div class="film-line"></div>
        <p class="film-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="film-loc">{{ displayLocation }}</p>
        <p class="film-intro">{{ config.content?.intro_text || 'Quelques instants volés, à garder pour toujours.' }}</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400&display=swap');

.film-template {
  background-color: var(--color-bg, #F2E9DB);
  color: var(--color-text, #3A2E24);
  min-height: 100vh;
  position: relative;
  overflow-x: clip;
  font-family: var(--card-font, 'Jost'), sans-serif;
}

/* Léger grain papier */
.paper-grain {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

.hero-section {
  min-height: auto;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: clamp(56px, 16cqi, 110px) clamp(20px, 6cqi, 48px);
}

.album { width: 100%; max-width: 520px; }

.film-eyebrow {
  font-size: clamp(0.55rem, 2cqi, 0.7rem);
  letter-spacing: 0.5em;
  text-transform: uppercase;
  color: var(--color-countdown, #C77F4E);
  opacity: 0;
  margin-bottom: clamp(28px, 8cqi, 48px);
  animation: fadeUp 0.9s ease-out 0.1s forwards;
}

/* Pile de photos instantanées */
.photo-stack {
  position: relative;
  width: clamp(180px, 56cqi, 260px);
  margin: 0 auto clamp(36px, 9cqi, 56px);
  aspect-ratio: 1 / 1.18;
}

.polaroid {
  position: absolute;
  inset: 0;
  background: #FBF8F1;
  padding: 10px 10px 0;
  box-shadow: 0 12px 30px rgba(58, 46, 36, 0.22);
}
.ph-frame { width: 100%; aspect-ratio: 1 / 1; overflow: clip; background: #ddd; }
.ph-img { width: 100%; height: 100%; object-fit: cover; filter: sepia(0.35) saturate(1.05) contrast(1.02); display: block; }
.ph-caption {
  font-family: 'Caveat', cursive;
  font-size: clamp(1.1rem, 4cqi, 1.5rem);
  color: #4a3b2e;
  padding: 8px 4px 12px;
  line-height: 1;
}

.p-back {
  transform: rotate(-7deg) translate(-14px, 6px);
  opacity: 0;
}
.p-front {
  transform: rotate(4deg);
  opacity: 0;
}
.album.loaded .p-back  { animation: dropIn 0.9s cubic-bezier(0.16,1,0.3,1) 0.25s forwards; }
.album.loaded .p-front { animation: dropInFront 0.9s cubic-bezier(0.16,1,0.3,1) 0.45s forwards; }

/* Scotch */
.tape {
  position: absolute;
  width: 64px;
  height: 22px;
  background: color-mix(in srgb, var(--color-countdown, #C77F4E) 22%, #fff);
  opacity: 0.55;
  top: -10px;
  z-index: 3;
}
.tape-1 { left: 50%; transform: translateX(-50%) rotate(-3deg); }
.tape-2 { left: 30%; transform: rotate(6deg); }

.main-title {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: var(--size-names, clamp(2.4rem, 13cqi, 4.5rem));
  line-height: 1.05;
  color: var(--color-names, #2E2419);
  opacity: 0;
  animation: fadeUp 1s ease-out 0.6s forwards;
}

.film-line {
  width: 48px; height: 1px;
  background: var(--color-countdown, #C77F4E);
  margin: clamp(18px, 5cqi, 28px) auto;
  opacity: 0;
  animation: fadeUp 1s ease-out 0.7s forwards;
}

.film-date {
  font-size: clamp(0.7rem, 2.6cqi, 0.85rem);
  letter-spacing: 0.32em;
  text-transform: uppercase;
  opacity: 0;
  animation: fadeUp 1s ease-out 0.8s forwards;
}
.film-loc {
  font-size: clamp(0.6rem, 2.2cqi, 0.72rem);
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--color-countdown, #C77F4E);
  margin-top: 8px;
  opacity: 0;
  animation: fadeUp 1s ease-out 0.9s forwards;
}
.film-intro {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: clamp(0.95rem, 3cqi, 1.15rem);
  max-width: 26ch;
  margin: clamp(22px, 6cqi, 32px) auto 0;
  opacity: 0;
  animation: fadeUp 1s ease-out 1s forwards;
  color: color-mix(in srgb, var(--color-text, #3A2E24) 75%, transparent);
}

@keyframes fadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes dropIn { from { opacity: 0; transform: rotate(-14deg) translate(-30px, -30px); } to { opacity: 1; transform: rotate(-7deg) translate(-14px, 6px); } }
@keyframes dropInFront { from { opacity: 0; transform: rotate(12deg) translateY(-40px); } to { opacity: 1; transform: rotate(4deg) translateY(0); } }
</style>
