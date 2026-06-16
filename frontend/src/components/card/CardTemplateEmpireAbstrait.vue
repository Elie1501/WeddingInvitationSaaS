<script setup>
import { ref, onMounted, computed } from 'vue';
import { getContrastColor } from '../../service/colorUtils';

const props = defineProps({
  config: { type: Object, required: true },
  event:  { type: Object, default: null }
});

const content = computed(() => props.config.content || {});

const theme = computed(() => ({
  bg:     props.config.theme?.background || '#0E0C18',
  text:   props.config.theme?.text || getContrastColor(props.config.theme?.background || '#0E0C18'),
  accent: props.config.theme?.accent || '#FF6B6B',
}));

const displayNames = computed(() =>
  content.value.names ||
  (props.event?.groom_name && props.event?.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);

const displayDate = computed(() => content.value.date_display || '15 JUIN 2026');

const isLoaded = ref(false);
onMounted(() => { setTimeout(() => { isLoaded.value = true; }, 80); });
</script>

<template>
  <div class="hero-aurora min-h-dvh relative overflow-clip flex items-center justify-center text-center px-6">
    <!-- Aurora mesh : blobs animés -->
    <div class="aurora" :class="{ loaded: isLoaded }" aria-hidden="true">
      <span class="blob blob-1"></span>
      <span class="blob blob-2"></span>
      <span class="blob blob-3"></span>
    </div>
    <div class="grain" aria-hidden="true"></div>

    <!-- Contenu -->
    <div class="content relative z-10" :class="{ reveal: isLoaded }">
      <p class="eyebrow">— UNION · MMXXVI —</p>
      <h1 class="template-title">{{ displayNames }}</h1>
      <div class="meta">
        <span class="meta-date">{{ displayDate }}</span>
        <span v-if="content.address" class="meta-dot">·</span>
        <span v-if="content.address" class="meta-loc">{{ content.address }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Space+Grotesk:wght@300;400;500&display=swap');

.hero-aurora {
  background: var(--color-bg, #0E0C18);
  color: var(--color-text, #EDE9F5);
  font-family: var(--card-font, 'Space Grotesk'), sans-serif;
  /* couleurs d'identité de l'aurora : accent pilotable + violet/cyan fixes */
  --aurora-a: var(--color-countdown, #FF6B6B);
  --aurora-b: #7C6CF0;
  --aurora-c: #21D4C0;
}

/* Aurora mesh */
.aurora { position: absolute; inset: -20%; z-index: 0; filter: blur(60px); opacity: 0; transition: opacity 1.8s ease-out; }
.aurora.loaded { opacity: 0.85; }
.blob {
  position: absolute;
  width: 60cqi; height: 60cqi;
  border-radius: 50%;
  mix-blend-mode: screen;
  will-change: transform;
}
.blob-1 { top: 6%;  left: 4%;  background: var(--aurora-a); animation: drift1 16s ease-in-out infinite; }
.blob-2 { top: 30%; right: 0;  background: var(--aurora-b); animation: drift2 19s ease-in-out infinite; }
.blob-3 { bottom: 2%; left: 22%; background: var(--aurora-c); animation: drift3 22s ease-in-out infinite; }

@keyframes drift1 { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(26cqi, 18cqi) scale(1.25); } }
@keyframes drift2 { 0%,100% { transform: translate(0,0) scale(1.1); } 50% { transform: translate(-22cqi, 14cqi) scale(0.85); } }
@keyframes drift3 { 0%,100% { transform: translate(0,0) scale(0.95); } 50% { transform: translate(14cqi, -20cqi) scale(1.2); } }

.grain {
  position: absolute; inset: 0; z-index: 1; pointer-events: none; opacity: 0.06;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

.content { opacity: 0; transform: translateY(22px); transition: opacity 1.4s ease-out 0.3s, transform 1.4s ease-out 0.3s; }
.content.reveal { opacity: 1; transform: translateY(0); }

.eyebrow {
  font-size: clamp(0.6rem, 2.4cqi, 0.78rem);
  letter-spacing: 0.55em;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: clamp(20px, 6cqi, 34px);
}

.template-title {
  font-family: var(--card-font, 'Archivo'), sans-serif;
  font-weight: 900;
  font-size: var(--size-names, clamp(2.6rem, 16cqi, 7rem));
  line-height: 0.92;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  color: var(--color-names, #FFFFFF);
  text-wrap: balance;
}

.meta {
  margin-top: clamp(24px, 7cqi, 40px);
  display: flex; align-items: center; justify-content: center; flex-wrap: wrap;
  gap: 0.6em;
  font-size: clamp(0.66rem, 2.6cqi, 0.85rem);
  letter-spacing: 0.28em;
  text-transform: uppercase;
}
.meta-date { color: var(--color-countdown, #FF6B6B); font-weight: 500; }
.meta-dot { opacity: 0.4; }
.meta-loc { opacity: 0.65; }
</style>
