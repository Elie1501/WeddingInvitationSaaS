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
  const bgColor = props.config.theme?.background || '#FFFFFF';
  const textColor = getContrastColor(bgColor);

  return {
    white: bgColor,
    black: textColor,
    nude: '#E8DDD0',
    platinum: '#CECECE',
    accent: props.config.theme?.accent || textColor
  };
});

const displayNames = computed(() => props.config.content?.names || `${props.event.groom_name} & ${props.event.bride_name}`);
const displayDate = computed(() => (props.config.content?.date_display || (props.event.date ? new Date(props.event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'SAISON HIVER 2026')).toUpperCase());
const displayLocation = computed(() => props.config.content?.address || props.event.location || '');

const isLoaded = ref(false);
onMounted(() => setTimeout(() => isLoaded.value = true, 100));

// SVG Handwriting Animation state
const signatureDrawn = ref(false);
onMounted(() => {
  setTimeout(() => signatureDrawn.value = true, 1000);
});
</script>

<template>
  <div class="couture-template" :style="{ '--accent': theme.accent }">

    <!-- Hero Section: The Unboxing / Cover -->
    <div v-if="mode === 'hero' || mode === 'full'" class="hero-section">
      <div class="paper-texture"></div>

      <div class="hero-content text-center">
        <div class="monogram-box mb-12">
            <svg viewBox="0 0 100 100" class="w-24 h-24 mx-auto">
                <path d="M30,30 Q50,10 70,30 T70,70 Q50,90 30,70 T30,30"
                      fill="none" stroke="black" stroke-width="0.5"
                      class="monogram-path" :class="{ 'animate-draw': isLoaded }" />
                <text x="50" y="55" font-family="Bodoni Moda, serif" font-size="20" text-anchor="middle" class="opacity-0 transition-opacity duration-1000 delay-1000" :class="{ 'opacity-100': isLoaded }">
                    {{ event.groom_name?.[0] }}{{ event.bride_name?.[0] }}
                </text>
            </svg>
        </div>

        <span class="collection-label">COLLECTION PRIVÉE</span>
        <h1 class="main-title couture-serif">{{ displayNames }}</h1>
        <div class="fine-line w-20 mx-auto my-8"></div>
        <p class="couture-date">{{ displayDate }}</p>
      </div>

      <!-- Signature Script -->
      <div class="signature-wrap">
          <svg viewBox="0 0 400 100" class="w-64 opacity-20">
              <text x="50%" y="50%" text-anchor="middle" font-family="Dancing Script, cursive" font-size="40" fill="none" stroke="black" stroke-width="0.5" class="sig-path" :class="{ 'sig-animate': signatureDrawn }">
                {{ displayNames }}
              </text>
          </svg>
      </div>
    </div>

    <!-- Body Content -->
    <div v-if="mode === 'content' || mode === 'full'" class="body-content">

        <!-- Lookbook Gallery Section -->
        <section class="lookbook-section py-32 overflow-hidden">
            <div class="flex items-center gap-8 pl-10 md:pl-20">
                <div class="look-item main-look border border-black/5 p-2 bg-white shadow-2xl">
                    <img
                      :src="config.content?.image_url || 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1200'"
                      class="w-full h-full object-cover grayscale brightness-110"
                      :class="{ 'cursor-pointer ring-0 hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
                      @click="isEditorMode ? emit('click-image', 'image_url') : null"
                    >
                </div>
                <div class="look-item side-look border border-black/5 p-2 bg-white shadow-xl opacity-50">
                    <img
                      :src="config.content?.image_url_2 || 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800'"
                      class="w-full h-full object-cover grayscale"
                      :class="{ 'cursor-pointer hover:ring-2 hover:ring-blue-400 transition-all': isEditorMode }"
                      @click="isEditorMode ? emit('click-image', 'image_url_2') : null"
                    >
                </div>
            </div>
            <div class="mt-12 px-10 md:px-20">
                <span class="collection-label">LOOK N°01 — L'UNION</span>
                <p class="max-w-md couture-serif text-2xl mt-4 leading-tight italic">
                    {{ config.content?.intro_text || '"La simplicité est la sophistication suprême."' }}
                </p>
            </div>
        </section>

        <!-- Information Minimaliste -->
        <section class="py-32 px-10 border-t border-black/5">
            <div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-20">
                <div class="info-block">
                    <span class="collection-label mb-6 block">DÉFILÉ / CÉRÉMONIE</span>
                    <h2 class="couture-serif text-4xl mb-6">Le Rendez-vous</h2>
                    <p class="text-sm tracking-widest leading-loose uppercase">
                        NOUS SERONS HONORÉS DE VOUS RECEVOIR POUR LA PRÉSENTATION DE NOTRE UNION.<br>
                        TENUE DE RIGUEUR : BLACK TIE / HAUTE COUTURE.
                    </p>
                </div>
                <div v-if="displayLocation" class="info-block">
                    <span class="collection-label mb-6 block">LIEU</span>
                    <p class="couture-serif text-2xl mb-2">{{ displayLocation }}</p>
                </div>
            </div>
        </section>
    </div>

    <!-- Footer -->
    <footer v-if="mode === 'full'" class="py-20 text-center border-t border-black/5">
        <p class="collection-label opacity-40">MAISON {{ event.groom_name?.[0] }}{{ event.bride_name?.[0] }} — PARIS — SAISON 2026</p>
    </footer>

  </div>
</template>

<style scoped>
@reference "../../style.css";
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,700;1,400&family=Dancing+Script&family=Montserrat:wght@200;400&display=swap');

.couture-serif { font-family: 'Bodoni Moda', serif; }

.couture-template {
  background-color: var(--white);
  color: var(--black);
  min-height: 100vh;
  overflow-x: hidden;
  font-family: 'Montserrat', sans-serif;
}

.paper-texture {
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    mix-blend-mode: multiply;
}

.hero-section {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 40px;
}

.collection-label {
    font-size: 10px;
    letter-spacing: 0.5em;
    font-weight: 400;
    opacity: 0.6;
    display: block;
}

.main-title {
    font-size: 5rem;
    font-weight: 400;
    margin: 20px 0;
    letter-spacing: -0.02em;
}

.fine-line { height: 0.5px; background: var(--black); }

.couture-date {
    font-size: 14px;
    letter-spacing: 0.4em;
    font-weight: 200;
}

.monogram-path {
    stroke-dasharray: 400;
    stroke-dashoffset: 400;
    transition: stroke-dashoffset 3s ease-out;
}
.animate-draw { stroke-dashoffset: 0; }

.signature-wrap {
    position: absolute;
    bottom: 100px;
    right: 10%;
}

.sig-path {
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
}
.sig-animate {
    animation: drawSig 5s forwards ease-in-out;
}

@keyframes drawSig {
    to { stroke-dashoffset: 0; fill: var(--black); opacity: 0.05; }
}

/* Lookbook */
.look-item {
    transition: 1s cubic-bezier(0.16, 1, 0.3, 1);
}
.main-look { width: 70vw; height: 80vh; z-index: 2; }
.side-look { width: 40vw; height: 60vh; z-index: 1; }

.couture-link {
    font-size: 10px;
    letter-spacing: 0.2em;
    font-weight: 400;
    border-bottom: 0.5px solid var(--black);
    padding-bottom: 4px;
    transition: 0.3s;
}
.couture-link:hover { opacity: 0.5; transform: translateY(-2px); }

@media (max-width: 768px) {
    .main-title { font-size: 14vw; line-height: 1; margin: 15px 0; }
    .monogram-box { transform: scale(0.8); margin-bottom: 2rem; }
    .couture-date { font-size: 11px; letter-spacing: 0.3em; }
    .lookbook-section { padding-top: 4rem; padding-bottom: 4rem; }
    .look-item.main-look { width: 90vw; height: 50vh; }
    .look-item.side-look { display: none; }
    .info-block h2 { font-size: 2.2rem; }
    .signature-wrap { bottom: 40px; right: 5%; transform: scale(0.7); }
}

@media (max-width: 480px) {
    .main-title { font-size: 16vw; }
}
</style>
