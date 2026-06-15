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
  bg:     props.config.theme?.background || '#FFFFFF',
  text:   props.config.theme?.text       || '#0A0A0A',
  accent: props.config.theme?.accent     || '#E63946',
}));

const displayNames = computed(() =>
  props.config.content?.names ||
  (props.event.groom_name && props.event.bride_name
    ? `${props.event.groom_name} & ${props.event.bride_name}` : '')
);
const firstName = computed(() => {
  const n = displayNames.value;
  const sep = n.includes(' & ') ? ' & ' : n.includes('/') ? '/' : null;
  return sep ? n.split(sep)[0].trim() : n;
});
const secondName = computed(() => {
  const n = displayNames.value;
  const sep = n.includes(' & ') ? ' & ' : n.includes('/') ? '/' : null;
  return sep ? n.split(sep)[1]?.trim() || '' : '';
});
const displayDate = computed(() =>
  (props.config.content?.date_display ||
   (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '15 JUIN 2026')).toUpperCase()
);
const displayLocation = computed(() => (props.config.content?.address || props.event.location || '').toUpperCase());
const imageUrl = computed(() => props.config.content?.image_url || 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200');

// Grid reveal snap animation
const gridRevealed = ref(false);
const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => { isLoaded.value = true; }, 100);
  setTimeout(() => { gridRevealed.value = true; }, 400);
});

// Date digit flip
const dateDigits = computed(() => {
  const d = props.event.date ? new Date(props.event.date) : null;
  return {
    day:   d ? String(d.getDate()).padStart(2, '0') : '15',
    month: d ? String(d.getMonth() + 1).padStart(2, '0') : '06',
    year:  d ? String(d.getFullYear()) : '2026',
  };
});
</script>

<template>
  <div class="editorial-wrap">

    <!-- ── HERO ── -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero" :class="{ loaded: isLoaded }">

      <!-- Issue number / volume label -->
      <div class="vol-label">VOL. I — ÉDITION UNIQUE</div>

      <!-- Giant names grid -->
      <div class="names-grid" :class="{ snap: gridRevealed }">
        <div class="name-row name-row-1">
          <span class="name-giant">{{ firstName }}</span>
          <span class="amp-mark" :style="{ color: 'var(--color-countdown)' }">&amp;</span>
        </div>
        <div class="name-row name-row-2">
          <span class="name-giant">{{ secondName || displayNames }}</span>
        </div>
      </div>

      <!-- Horizontal marquee band -->
      <div class="marquee-band" :style="{ background: 'var(--color-countdown)' }">
        <div class="marquee-inner">
          <span v-for="n in 6" :key="n" class="marquee-item">
            {{ displayNames }} · {{ displayDate }}<template v-if="displayLocation"> · {{ displayLocation }}</template> ·&nbsp;
          </span>
        </div>
      </div>

      <!-- Bottom meta row -->
      <div class="meta-row" :class="{ reveal: isLoaded }">
        <div class="meta-col">
          <p class="meta-key">DATE</p>
          <p class="meta-val">{{ displayDate }}</p>
        </div>
        <div class="meta-col center-col">
          <!-- Date as clock/mechanical digits -->
          <div class="clock-digits">
            <span class="digit">{{ dateDigits.day }}</span>
            <span class="dot">.</span>
            <span class="digit">{{ dateDigits.month }}</span>
            <span class="dot">.</span>
            <span class="digit">{{ dateDigits.year }}</span>
          </div>
        </div>
        <div class="meta-col right-col">
          <template v-if="displayLocation">
            <p class="meta-key">LIEU</p>
            <p class="meta-val">{{ displayLocation }}</p>
          </template>
        </div>
      </div>
    </div>

    <!-- ── BODY ── -->
    <div v-if="mode === 'full'" class="body">

      <!-- Photo + text editorial layout -->
      <section class="editorial-section">
        <div class="ed-photo-wrap"
             :class="{ 'editor-img': isEditorMode }"
             @click="isEditorMode ? emit('click-image', 'image_url') : null">
          <img :src="imageUrl" class="ed-photo" alt="" />
          <div class="ed-photo-label">PHOTO 01</div>
        </div>

        <div class="ed-text-col">
          <p class="ed-issue-n">No. 01</p>
          <div class="ed-rule" />
          <p class="ed-body">{{ config.content?.intro_text || 'Une invitation à témoigner de l\'union la plus importante de l\'année. Une soirée hors du temps. Un événement sans précédent.' }}</p>
          <div class="ed-rule accent-rule" />
          <div class="ed-tags">
            <span class="tag">CÉRÉMONIE</span>
            <span class="tag">CÉLÉBRATION</span>
            <span class="tag">INVITATION</span>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@300;400;700&family=Playfair+Display:ital@1&display=swap');

.editorial-wrap {
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  overflow-x: hidden;
  font-family: var(--card-font, 'Space Grotesk'), sans-serif;
}

/* Hero */
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 0;
  position: relative;
  opacity: 0;
  transition: opacity 0.6s ease;
}
.hero.loaded { opacity: 1; }

.vol-label {
  font-size: 0.52rem;
  letter-spacing: 0.65em;
  opacity: 0.35;
  padding: 28px 32px 0;
  font-weight: 700;
}

/* Giant names grid */
.names-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 16px 0;
  transform: translateY(30px);
  opacity: 0;
  transition: transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.5s ease;
}
.names-grid.snap { transform: translateY(0); opacity: 1; }

.name-row {
  display: flex;
  align-items: baseline;
  overflow: hidden;
  line-height: 0.88;
}
.name-giant {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: var(--size-names, clamp(4rem, 22vw, 14rem));
  letter-spacing: -0.01em;
  line-height: 0.88;
  text-transform: uppercase;
}
.amp-mark {
  font-family: var(--card-font, 'Playfair Display'), serif;
  font-style: italic;
  font-size: clamp(2rem, 10vw, 7rem);
  margin-left: 12px;
  line-height: 1.2;
}

/* Marquee */
.marquee-band {
  width: 100%;
  overflow: hidden;
  padding: 10px 0;
  margin: 16px 0 0;
}
.marquee-inner {
  display: flex;
  white-space: nowrap;
  animation: marqueeScroll 18s linear infinite;
}
.marquee-item {
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  font-weight: 700;
  color: var(--color-bg);
  padding: 0 8px;
  opacity: 0.95;
}
@keyframes marqueeScroll {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

/* Meta row */
.meta-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 20px 32px;
  border-top: 2px solid var(--color-text);
  opacity: 0;
  transition: opacity 1s ease 0.5s;
}
.meta-row.reveal { opacity: 1; }

.meta-col { }
.center-col { text-align: center; }
.right-col { text-align: right; }

.meta-key {
  font-size: 0.45rem;
  letter-spacing: 0.6em;
  text-transform: uppercase;
  opacity: 0.4;
  margin-bottom: 5px;
}
.meta-val {
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  font-weight: 700;
}

.clock-digits {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: clamp(1.8rem, 5vw, 3rem);
  letter-spacing: 0.08em;
  color: var(--color-countdown);
  line-height: 1;
}
.dot { color: var(--color-text); opacity: 0.4; margin: 0 2px; }

/* Body */
.body { background: var(--color-bg); }

.editorial-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 80vh;
  border-top: 2px solid var(--color-text);
}

.ed-photo-wrap {
  position: relative;
  overflow: hidden;
  border-right: 2px solid var(--color-text);
}
.ed-photo-wrap.editor-img { cursor: pointer; }
.ed-photo { width: 100%; height: 100%; object-fit: cover; display: block; }
.ed-photo-wrap.editor-img:hover .ed-photo { opacity: 0.85; }

.ed-photo-label {
  position: absolute;
  bottom: 16px;
  left: 16px;
  font-size: 0.45rem;
  letter-spacing: 0.6em;
  font-weight: 700;
  background: var(--color-text);
  color: var(--color-bg);
  padding: 4px 8px;
}

.ed-text-col {
  padding: 60px 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.ed-issue-n {
  font-family: var(--card-font, 'Bebas Neue'), sans-serif;
  font-size: 5rem;
  color: var(--color-countdown);
  opacity: 0.12;
  line-height: 1;
  margin-bottom: 12px;
}
.ed-rule {
  height: 2px;
  background: var(--color-text);
  margin: 20px 0;
}
.ed-rule.accent-rule { background: var(--color-countdown); height: 3px; width: 60px; }

.ed-body {
  font-family: var(--card-font, 'Playfair Display'), serif;
  font-style: italic;
  font-size: 1.3rem;
  line-height: 1.75;
  opacity: 0.7;
}

.ed-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 24px;
}
.tag {
  font-size: 0.48rem;
  letter-spacing: 0.45em;
  font-weight: 700;
  border: 1.5px solid var(--color-text);
  padding: 5px 10px;
  opacity: 0.5;
}

@media (max-width: 768px) {
  .editorial-section { grid-template-columns: 1fr; }
  .ed-photo-wrap { height: 55vw; border-right: none; border-bottom: 2px solid var(--color-text); }
  .ed-text-col { padding: 40px 24px; }
  .meta-row { padding: 16px 24px; }
}

@media (max-width: 480px) {
  .name-giant { font-size: clamp(3rem, 22vw, 14rem); }
}
</style>
