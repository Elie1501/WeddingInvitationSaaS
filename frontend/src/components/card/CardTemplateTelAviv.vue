<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null },
  mode:   { type: String, default: 'full' }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#FBF9F4',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#FBF9F4'),
  accent: props.config.theme?.accent || '#0038B8',
}));

const displayNames = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const displayDate = computed(() => content.value.date_display || (props.event?.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 JUIN 2026'));
const displayLocation = computed(() => content.value.address || props.event?.location || '');
const introText = computed(() => content.value.intro_text || 'Avec la bénédiction de nos familles, nous vous convions à célébrer notre union.');

const isLoaded = ref(false);
onMounted(() => { setTimeout(() => { isLoaded.value = true; }, 120); });
</script>

<template>
  <div class="ta-hero">
    <!-- Cadre ornemental -->
    <div class="ta-frame" :class="{ loaded: isLoaded }" aria-hidden="true"></div>

    <!-- Formes Bauhaus (White City) -->
    <div class="ta-bauhaus" aria-hidden="true">
      <span class="bh bh-circle"></span>
      <span class="bh bh-arch"></span>
      <span class="bh bh-dot"></span>
    </div>

    <div class="ta-inner" :class="{ reveal: isLoaded }">
      <!-- Haut -->
      <div class="ta-top">
        <p class="ta-hebrew">מַזָּל טוֹב</p>
        <p class="ta-eyebrow">Tel Aviv · {{ (displayDate.match(/\d{4}/) || ['2026'])[0] }}</p>
      </div>

      <!-- Centre -->
      <div class="ta-center">
        <!-- Étoile de David -->
        <svg class="ta-star" viewBox="0 0 100 100" :class="{ loaded: isLoaded }" aria-hidden="true">
          <polygon points="50,8 88,72 12,72" class="star-tri t1" />
          <polygon points="50,92 12,28 88,28" class="star-tri t2" />
        </svg>

        <h1 class="ta-names template-title main-names">{{ displayNames }}</h1>

        <!-- Branche d'olivier -->
        <svg class="ta-olive" viewBox="0 0 240 24" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          <path d="M20,12 H105" class="ol-stem" />
          <path d="M220,12 H135" class="ol-stem" />
          <g class="ol-leaves">
            <ellipse cx="120" cy="12" rx="7" ry="3.4" transform="rotate(0 120 12)"/>
            <ellipse cx="108" cy="6" rx="6" ry="3" transform="rotate(-35 108 6)"/>
            <ellipse cx="132" cy="6" rx="6" ry="3" transform="rotate(35 132 6)"/>
            <ellipse cx="108" cy="18" rx="6" ry="3" transform="rotate(35 108 18)"/>
            <ellipse cx="132" cy="18" rx="6" ry="3" transform="rotate(-35 132 18)"/>
          </g>
        </svg>

        <p class="ta-intro">{{ introText }}</p>
      </div>

      <!-- Bas -->
      <div class="ta-bottom">
        <p class="ta-date">{{ displayDate }}</p>
        <p v-if="displayLocation" class="ta-loc">{{ displayLocation }}</p>
        <div class="ta-chuppah" aria-hidden="true">
          <svg viewBox="0 0 120 40" preserveAspectRatio="xMidYMid meet">
            <path d="M10,40 V14 Q60,-6 110,14 V40" class="chuppah-path" />
            <line x1="10" y1="14" x2="10" y2="40" class="chuppah-leg" />
            <line x1="110" y1="14" x2="110" y2="40" class="chuppah-leg" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300;500;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&display=swap');

.ta-hero {
  position: relative;
  min-height: 100vh;
  background: var(--color-bg, #FBF9F4);
  color: var(--color-text, #1A2238);
  font-family: var(--card-font, 'Jost'), sans-serif;
  overflow: clip;
  padding: clamp(26px, 7cqi, 46px);
}

/* Cadre ornemental */
.ta-frame {
  position: absolute; inset: clamp(14px, 4cqi, 26px);
  border: 1px solid color-mix(in srgb, var(--color-countdown, #0038B8) 40%, transparent);
  box-shadow: inset 0 0 0 4px var(--color-bg, #FBF9F4), inset 0 0 0 5px color-mix(in srgb, var(--color-countdown, #0038B8) 22%, transparent);
  opacity: 0; transform: scale(1.04);
  transition: opacity 1.2s ease-out, transform 1.2s cubic-bezier(0.16,1,0.3,1);
}
.ta-frame.loaded { opacity: 1; transform: scale(1); }

/* Bauhaus */
.ta-bauhaus { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.bh { position: absolute; opacity: 0.08; }
.bh-circle { top: 12%; left: 10%; width: 26cqi; height: 26cqi; border-radius: 50%; border: 2px solid var(--color-countdown, #0038B8); }
.bh-arch { bottom: 16%; right: 8%; width: 22cqi; height: 11cqi; border: 2px solid var(--color-countdown, #0038B8); border-bottom: none; border-radius: 50% 50% 0 0; }
.bh-dot { top: 22%; right: 18%; width: 8cqi; height: 8cqi; border-radius: 50%; background: var(--color-countdown, #0038B8); opacity: 0.06; }

/* Conteneur : remplit l'écran, contenu réparti */
.ta-inner {
  position: relative; z-index: 2;
  min-height: calc(100vh - clamp(52px, 14cqi, 92px));
  display: flex; flex-direction: column; justify-content: space-between;
  text-align: center;
  padding: clamp(26px, 7cqi, 46px) clamp(18px, 5cqi, 34px);
  opacity: 0; transform: translateY(18px);
  transition: opacity 1.4s ease 0.3s, transform 1.4s ease 0.3s;
}
.ta-inner.reveal { opacity: 1; transform: translateY(0); }

.ta-hebrew { font-family: 'Frank Ruhl Libre', serif; font-weight: 500; font-size: clamp(1.3rem, 6cqi, 2rem); color: var(--color-countdown, #0038B8); direction: rtl; margin-bottom: 8px; }
.ta-eyebrow { font-size: clamp(0.56rem, 2.2cqi, 0.7rem); letter-spacing: 0.45em; text-transform: uppercase; opacity: 0.5; }

.ta-center { display: flex; flex-direction: column; align-items: center; gap: clamp(16px, 4cqi, 26px); }

.ta-star { width: clamp(54px, 16cqi, 84px); aspect-ratio: 1; opacity: 0; transform: scale(0.8) rotate(-12deg); transition: opacity 1s ease 0.4s, transform 1.2s cubic-bezier(0.16,1,0.3,1) 0.4s; }
.ta-star.loaded { opacity: 0.95; transform: scale(1) rotate(0); }
.star-tri { fill: none; stroke: var(--color-countdown, #0038B8); stroke-width: 2.5; stroke-linejoin: round; stroke-dasharray: 230; stroke-dashoffset: 230; }
.ta-star.loaded .t1 { animation: drawTri 1.5s ease-out 0.6s forwards; }
.ta-star.loaded .t2 { animation: drawTri 1.5s ease-out 1s forwards; }
@keyframes drawTri { to { stroke-dashoffset: 0; } }

.ta-names {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: var(--size-names, clamp(2.6rem, 14cqi, 5rem));
  line-height: 1.04;
  color: var(--color-names, #16203A);
}

.ta-olive { width: clamp(160px, 56cqi, 240px); height: auto; }
.ol-stem { fill: none; stroke: var(--color-countdown, #0038B8); stroke-width: 1.4; opacity: 0.7; }
.ol-leaves ellipse { fill: var(--color-countdown, #0038B8); opacity: 0.55; }

.ta-intro {
  font-family: var(--card-font, 'Cormorant Garamond'), serif;
  font-style: italic;
  font-size: clamp(0.95rem, 3cqi, 1.18rem);
  line-height: 1.6;
  max-width: 30ch; margin: 0 auto;
  color: color-mix(in srgb, var(--color-text, #1A2238) 75%, transparent);
}

.ta-bottom { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.ta-date { font-size: clamp(0.64rem, 2.5cqi, 0.78rem); letter-spacing: 0.4em; text-transform: uppercase; opacity: 0.62; }
.ta-loc { font-size: clamp(0.56rem, 2.2cqi, 0.68rem); letter-spacing: 0.26em; text-transform: uppercase; color: var(--color-countdown, #0038B8); opacity: 0.85; }
.ta-chuppah { width: clamp(90px, 30cqi, 120px); margin-top: 12px; }
.ta-chuppah svg { width: 100%; height: auto; }
.chuppah-path, .chuppah-leg { fill: none; stroke: var(--color-countdown, #0038B8); stroke-width: 2; opacity: 0.5; }
</style>
