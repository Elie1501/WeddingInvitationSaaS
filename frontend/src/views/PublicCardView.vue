<script setup>
import { ref, computed, onMounted, provide } from 'vue';
import { useRoute } from 'vue-router';
import api from '../service/api';
import CardRenderer from '../components/card/CardRenderer.vue';
import CardSplashScreen from '../components/card/CardSplashScreen.vue';

provide('isEditorMode', false);

const route = useRoute();
const slug  = route.params.slug;

const cardData   = ref(null);
const loading    = ref(true);
const error      = ref('');
const showSplash = ref(false);
const showCard   = ref(false);

const cfg = computed(() => {
  if (!cardData.value?.config_json) return {};
  try {
    const c = cardData.value.config_json;
    return typeof c === 'string' ? JSON.parse(c) : c;
  } catch { return {}; }
});

// ── Musique d'ambiance ───────────────────────────────────────────────
// Les navigateurs bloquent l'autoplay audio sans interaction utilisateur.
// On démarre donc la musique au clic « Entrer » du splash (= geste valide),
// et on fournit un bouton flottant lecture/pause pour la contrôler ensuite.
const audioRef  = ref(null);
const musicUrl  = computed(() => cfg.value.media?.music_url || '');
const isPlaying = ref(false);

const startMusic = () => {
  if (!audioRef.value || !musicUrl.value) return;
  audioRef.value.play()
    .then(() => { isPlaying.value = true; })
    .catch(() => { isPlaying.value = false; });
};

const toggleMusic = () => {
  if (!audioRef.value || !musicUrl.value) return;
  if (audioRef.value.paused) {
    audioRef.value.play()
      .then(() => { isPlaying.value = true; })
      .catch(() => { isPlaying.value = false; });
  } else {
    audioRef.value.pause();
    isPlaying.value = false;
  }
};

const onSplashClose = () => {
  showSplash.value = false;
  showCard.value = true;
};

// CardRenderer reçoit toujours show_splash:false — le splash est géré ici
const cfgForRenderer = computed(() => ({ ...cfg.value, show_splash: false }));

const eventObj = computed(() => ({
  id:         cardData.value?.event_id || cardData.value?.id || null,
  groom_name: cardData.value?.groom_name  || '',
  bride_name: cardData.value?.bride_name  || '',
  date:       cardData.value?.date        || '',
  location:   cardData.value?.location    || '',
}));

const subEvents = computed(() => cardData.value?.sub_events || []);
const themeBg   = computed(() => cfg.value.theme?.background || '#F9F7F2');

onMounted(async () => {
  try {
    const res = await api.get(`/events/public/card/${slug}`);
    cardData.value = res.data;

    const ev    = res.data;
    const names = cfg.value.content?.names ||
      (ev.groom_name && ev.bride_name ? `${ev.groom_name} & ${ev.bride_name}` : '');
    document.title = names ? `${names} · Invitation` : 'Invitation de mariage';

    showSplash.value = !!cfg.value.show_splash;
    showCard.value   = !showSplash.value;
  } catch {
    error.value = 'Invitation introuvable.';
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="pv-loading">
    <div class="pv-spinner" />
  </div>

  <div v-else-if="error" class="pv-loading">
    <p class="pv-error">{{ error }}</p>
  </div>

  <template v-else>
    <!-- Page de garde — affiché seul en premier -->
    <CardSplashScreen
      v-if="showSplash"
      :config="cfg"
      :event="eventObj"
      :templateId="cfg.layout"
      :isPreview="false"
      @play-music="startMusic"
      @close="onSplashClose"
    />

    <!-- Invitation — affichée uniquement après fermeture de la garde -->
    <div v-if="showCard" class="pv-outer" :style="{ background: themeBg }">
      <div class="pv-col">
        <CardRenderer
          :config="cfgForRenderer"
          :event="eventObj"
          :subEvents="subEvents"
          :selectedBlock="null"
        />
      </div>
    </div>

    <!-- Musique d'ambiance (cachée, contrôlée par le bouton flottant) -->
    <audio
      v-if="musicUrl"
      ref="audioRef"
      :src="musicUrl"
      loop
      preload="auto"
      @play="isPlaying = true"
      @pause="isPlaying = false"
    ></audio>

    <!-- Bouton flottant lecture/pause — visible dès que la carte est affichée -->
    <button
      v-if="musicUrl && showCard"
      @click="toggleMusic"
      class="pv-music-btn"
      :class="{ 'is-playing': isPlaying }"
      :aria-label="isPlaying ? 'Couper la musique' : 'Jouer la musique'"
      :title="isPlaying ? 'Couper la musique' : 'Jouer la musique'"
    >
      <svg v-if="isPlaying" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
        <path d="M12 3v9.28a4.5 4.5 0 1 0 2 3.72V7h4V3h-6z"/>
      </svg>
      <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M9 18V5l12-2v13"/>
        <circle cx="6" cy="18" r="3"/>
        <circle cx="18" cy="16" r="3"/>
        <line x1="3" y1="3" x2="21" y2="21" stroke-opacity="0.5"/>
      </svg>
    </button>
  </template>
</template>

<style scoped>
/* overflow-x: clip coupe le débordement horizontal sans créer de contexte de scroll
   (contrairement à overflow-x: hidden qui force overflow-y: auto sur les deux éléments
   via la spec CSS, créant deux scrollbars verticales) */
:global(html), :global(body) {
  overflow-x: clip;
  margin: 0;
  padding: 0;
}

/* ── Loading / Error ── */
.pv-loading {
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #080810;
}
.pv-spinner {
  width: 28px;
  height: 28px;
  border: 1.5px solid rgba(201,169,110,.15);
  border-top-color: #c9a96e;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.pv-error {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.2rem;
  color: rgba(240,235,227,.4);
}

/* ── Fond page = couleur du thème ── */
.pv-outer {
  width: 100%;
  min-height: 100dvh;
}

/* ── Colonne carte : plein écran sur tous les appareils ── */
.pv-col {
  width: 100%;
}

/* ── Anti-zoom iOS sur les inputs ── */
:global(input), :global(textarea), :global(select) {
  font-size: max(16px, 1em) !important;
}

/* ── Bouton flottant musique ── */
.pv-music-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 2000;
  width: 46px;
  height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: #fff;
  background: rgba(20, 20, 24, 0.72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.28);
  transition: transform 0.25s ease, background 0.25s ease;
}
.pv-music-btn:hover { transform: scale(1.08); }
.pv-music-btn:active { transform: scale(0.96); }
.pv-music-btn.is-playing {
  background: rgba(201, 169, 110, 0.92);
}
/* Anneau pulsé pendant la lecture */
.pv-music-btn.is-playing::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid rgba(201, 169, 110, 0.45);
  animation: pv-pulse 1.8s ease-out infinite;
}
@keyframes pv-pulse {
  0%   { transform: scale(1);   opacity: 0.8; }
  100% { transform: scale(1.4); opacity: 0; }
}
@media (prefers-reduced-motion: reduce) {
  .pv-music-btn.is-playing::after { animation: none; }
}
</style>
