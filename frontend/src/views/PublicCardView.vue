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

const cfg = computed(() => {
  if (!cardData.value?.config_json) return {};
  try {
    const c = cardData.value.config_json;
    return typeof c === 'string' ? JSON.parse(c) : c;
  } catch { return {}; }
});

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
    <!-- Invitation — rendue en dessous, visible dès que le splash part -->
    <div class="pv-outer" :style="{ background: themeBg }">
      <div class="pv-col">
        <CardRenderer
          :config="cfgForRenderer"
          :event="eventObj"
          :subEvents="subEvents"
          :selectedBlock="null"
        />
      </div>
    </div>

    <!-- Page de garde en overlay fixe — séparée du scroll de la carte -->
    <!-- La transition de sortie est gérée par CardSplashScreen lui-même (1200ms) -->
    <CardSplashScreen
      v-if="showSplash"
      :config="cfg"
      :event="eventObj"
      :templateId="cfg.layout"
      :isPreview="false"
      @close="showSplash = false"
    />
  </template>
</template>

<style scoped>
/* Empêche uniquement le scroll horizontal parasite */
:global(html), :global(body) {
  overflow-x: hidden;
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
</style>
