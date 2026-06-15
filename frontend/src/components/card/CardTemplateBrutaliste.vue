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
  const bgColor = props.config.theme?.background || '#9E9E9E';
  const textColor = getContrastColor(bgColor);

  return {
    concrete: bgColor,
    black: textColor,
    white: textColor === '#000000' ? '#FFFFFF' : '#000000',
    accent: props.config.theme?.accent || '#FF3E00'
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);

const nameParts = computed(() => {
  const names = displayNames.value;
  const sep = names.includes(' / ') ? ' / ' : names.includes('/') ? '/' : ' & ';
  const parts = names.split(sep);
  return [parts[0]?.trim() || names, parts[1]?.trim() || ''];
});
const displayDate = computed(() => props.config.content?.date_display || (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' }) : '00.00.2026'));
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

const isLoaded = ref(false);
onMounted(() => {
  setTimeout(() => isLoaded.value = true, 100);
});
</script>

<template>
  <div class="brutal-template">

    <!-- Hero Section -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section grid-modular">
      <div class="block-number">01</div>

      <div class="hero-content">
        <h1 class="main-names reveal-brutal" :class="{ 'active': isLoaded }">
            <span class="line-1">{{ nameParts[0] }}</span>
            <span v-if="nameParts[1]" class="line-2 text-accent">/ {{ nameParts[1] }}</span>
        </h1>

        <div class="hero-meta flex justify-between border-t-4 border-black mt-8 pt-4">
            <div v-if="displayLocation" class="meta-item">
                <span class="label">LIEU</span>
                <p class="val">{{ displayLocation }}</p>
            </div>
            <div class="meta-item text-right">
                <span class="label">TIMESTAMP</span>
                <p class="val">{{ displayDate }}</p>
            </div>
        </div>
      </div>
    </div>

    <!-- Content Blocks -->
    <div v-if="mode === 'full'" class="body-content">
        <!-- Section 02 -->
        <section class="brutal-section">
            <div class="absolute-bg-num">02</div>
            <div class="container-brutal">
                <div class="grid grid-cols-12 gap-0 border-4 border-black bg-white shadow-hard">
                    <div class="col-span-12 md:col-span-4 p-8 border-b-4 md:border-b-0 md:border-r-4 border-black bg-accent text-white">
                        <h2 class="section-title-brutal">THE EVENT</h2>
                    </div>
                    <div class="col-span-12 md:col-span-8 p-8">
                        <p class="brutal-text text-2xl font-black uppercase leading-none mb-8">
                            {{ config.content?.intro_text || 'Nous confirmons notre union dans une structure de forme et de fonction.' }}
                        </p>
                        <div class="technical-details text-xs uppercase tracking-tighter">
                            <p>TYPE: WEDDING_CELEBRATION</p>
                            <p>DRESS_CODE: RADICAL_MINIMAL</p>
                            <p>STATUS: CONFIRMED</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section Image -->
        <section class="brutal-section overflow-hidden">
            <div class="container-brutal">
                <div class="relative w-full aspect-video bg-concrete border-4 border-black shadow-hard-accent">
                    <img
                      :src="config.content?.image_url || 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200'"
                      class="w-full h-full object-cover grayscale contrast-150"
                      :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
                      @click="isEditorMode ? emit('click-image', 'image_url') : null"
                    >
                    <div class="absolute bottom-0 left-0 bg-black text-white p-4 text-[10px]">IMG_REF_042.RAW</div>
                </div>
            </div>
        </section>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@900&display=swap');

.brutal-template {
  --concrete: var(--color-bg, #9E9E9E);
  --black: var(--color-text, #000000);
  --white: #FFFFFF;
  --accent: var(--color-countdown, #FF3E00);
  background-color: var(--concrete);
  color: var(--black);
  font-family: var(--card-font, 'Inter'), sans-serif;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.text-accent { color: var(--accent); }
.bg-accent { background-color: var(--accent); }

.grid-modular {
    display: grid;
    padding: 40px;
}

.hero-section {
    height: 100vh;
    background-color: var(--white);
    border: 8px solid var(--black);
    margin: 20px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.block-number {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 8rem;
    font-weight: 900;
    line-height: 0.8;
    opacity: 0.1;
    pointer-events: none;
}

.hero-content { padding: 0 5vw; z-index: 10; }

.main-names {
    font-size: var(--size-names, 15vw);
    font-weight: 900;
    text-transform: uppercase;
    line-height: 0.8;
    letter-spacing: -0.05em;
}

.main-names span { display: block; }

.hero-meta .label { font-family: var(--card-font, 'Space Mono'), monospace; font-size: 0.7rem; opacity: 0.5; }
.hero-meta .val { font-weight: 900; text-transform: uppercase; font-size: 1.5rem; }

/* Animations Brutales */
.reveal-brutal { transform: translateY(100px); opacity: 0; transition: 1s cubic-bezier(0.17, 0.67, 0.16, 0.99); }
.reveal-brutal.active { transform: translateY(0); opacity: 1; }

.brutal-section { padding: 80px 0; position: relative; }
.absolute-bg-num {
    position: absolute;
    top: 0;
    right: 5%;
    font-size: 20rem;
    font-weight: 900;
    color: var(--black);
    opacity: 0.05;
    line-height: 0.8;
}

.container-brutal { max-width: 1000px; margin: 0 auto; padding: 0 40px; position: relative; z-index: 2; }

.shadow-hard { box-shadow: 12px 12px 0 var(--black); }
.shadow-hard-accent { box-shadow: 15px 15px 0 var(--accent); }
.shadow-hard-black { box-shadow: 8px 8px 0 var(--black); }

.section-title-brutal { font-size: 4rem; font-weight: 900; line-height: 0.8; }

.brutal-radio-box input:checked + span { text-decoration: underline; text-decoration-thickness: 4px; }

@media (max-width: 768px) {
    .main-names { font-size: 18vw; line-height: 0.9; }
    .section-title-brutal { font-size: 15vw; }
    .absolute-bg-num { font-size: 40vw; top: 10%; right: 0; }
    .hero-section { margin: 10px; border-width: 4px; padding: 20px; }
    .block-number { font-size: 20vw; top: 10px; left: 10px; }
    .hero-meta .val { font-size: 1.1rem; }
    .container-brutal { padding: 0 20px; }
}

@media (max-width: 480px) {
    .main-names { font-size: 22vw; }
}
</style>
