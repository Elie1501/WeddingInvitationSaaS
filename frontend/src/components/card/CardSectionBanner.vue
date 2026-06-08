<script setup>
import { computed } from 'vue';

const props = defineProps({
  layout: { type: String, default: 'arch' },
  theme: { type: Object, required: true },
  displayData: { type: Object, required: true }
});
</script>

<template>
  <div class="hero-block-main relative w-full min-h-[500px] md:min-h-[700px] overflow-hidden" :style="{ backgroundColor: theme.background, color: theme.text }">
    
    <!-- Paper Texture Overlay Global -->
    <div class="paper-texture"></div>

    <!-- STYLE : L'ARCHE (ARCH) -->
    <div v-if="layout === 'arch'" class="h-full min-h-[500px] md:min-h-[700px] flex flex-col items-center p-8 text-center relative justify-end layout-arch">
      <div class="absolute top-16 w-[85%] max-w-[450px] aspect-[1/1.4] overflow-hidden shadow-2xl arch-frame-wrapper reveal-zoom">
        <div class="arch-inner-border"></div>
        <img :src="displayData.image" class="w-full h-full object-cover zoom-slow" />
      </div>
      
      <div class="relative z-10 w-full flex flex-col items-center pt-32 pb-16 px-4 bg-gradient-to-t from-[var(--bg-color)] via-[var(--bg-color)] to-transparent" :style="{'--bg-color': theme.background}">
        <div class="reveal-up delay-1">
            <p class="text-[10px] uppercase tracking-[0.6em] mb-6 font-bold" :style="{ color: theme.accent }">Célébration Unique</p>
        </div>
        <h1 class="text-7xl md:text-8xl font-light leading-none italic mb-10 drop-shadow-sm font-playfair reveal-up delay-2">{{ displayData.names }}</h1>
        <div class="w-16 h-[1px] mx-auto opacity-30 mb-8 reveal-up delay-3" :style="{ backgroundColor: theme.text }"></div>
        <div class="space-y-2 reveal-up delay-4">
            <p class="text-base tracking-[0.3em] font-bold uppercase">{{ displayData.date }}</p>
            <p class="text-[11px] uppercase tracking-[0.4em] opacity-50">{{ displayData.location }}</p>
        </div>
      </div>
      
      <!-- Floating Elements for Arch -->
      <div class="floating-petal p1">❀</div>
      <div class="floating-petal p2">❀</div>
    </div>

    <!-- STYLE : EDITORIAL (TYPOGRAPHY-FOCUS) -->
    <div v-else-if="layout === 'typography-focus'" class="h-full min-h-[500px] md:min-h-[700px] flex flex-col p-12 relative overflow-hidden text-left justify-between layout-editorial">
      <div class="absolute top-12 right-0 w-[80%] max-w-[600px] aspect-[4/5] overflow-hidden shadow-2xl reveal-right">
        <img :src="displayData.image" class="w-full h-full object-cover grayscale brightness-110 contrast-125" />
        <div class="absolute inset-0 bg-[#C5A059]/10 mix-blend-multiply"></div>
      </div>
      
      <div class="relative z-20 flex flex-col h-full justify-end pb-12 pt-48">
        <div class="overflow-hidden mb-4">
            <p class="text-xs tracking-[0.5em] uppercase font-black opacity-40 reveal-up">The Wedding of</p>
        </div>
        <h1 class="text-[6rem] md:text-[10rem] font-black tracking-tighter uppercase leading-[0.8] -ml-4 mix-blend-difference break-words font-montserrat reveal-left text-white drop-shadow-2xl">
            {{ displayData.names.split('&')[0] }}<br>
            <span class="text-[#C5A059]">&</span>{{ displayData.names.split('&')[1] }}
        </h1>
        
        <div class="mt-16 flex justify-between items-end border-t-4 pt-10 reveal-up delay-3" :style="{ borderColor: theme.text }">
          <div class="space-y-2">
            <p class="text-lg tracking-widest uppercase font-black">{{ displayData.date }}</p>
            <p class="text-xs uppercase tracking-[0.3em] opacity-60">{{ displayData.location }}</p>
          </div>
          <div class="editorial-badge">
            <svg viewBox="0 0 100 100" class="w-24 h-24 animate-spin-slow">
                <path id="circlePath" d="M 50, 50 m -37, 0 a 37,37 0 1,1 74,0 a 37,37 0 1,1 -74,0" fill="transparent" />
                <text class="text-[10px] uppercase tracking-[0.2em] font-black" :fill="theme.text">
                    <textPath xlink:href="#circlePath">Save the Date • Nous nous marions • </textPath>
                </text>
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xl">💍</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- STYLE : SPLIT (DYNAMIC & MODERN) -->
    <div v-else-if="layout === 'split'" class="h-full min-h-[500px] md:min-h-[700px] w-full relative flex items-center justify-center p-8 layout-split">
      <div class="absolute inset-0 overflow-hidden">
        <img :src="displayData.image" class="w-full h-full object-cover zoom-slow" />
        <div class="absolute inset-0 bg-black/40 backdrop-grayscale-[0.5]"></div>
      </div>
      
      <div class="relative z-10 w-full max-w-[600px] bg-white/5 backdrop-blur-3xl border border-white/20 p-16 rounded-[3rem] text-center flex flex-col items-center space-y-10 shadow-2xl text-white split-card reveal-zoom">
        <div class="w-12 h-12 rounded-full border border-white/30 flex items-center justify-center mb-2">
            <span class="text-lg">✦</span>
        </div>
        <p class="text-[10px] uppercase tracking-[0.6em] opacity-90 font-black">L'Union Sacrée</p>
        <h1 class="text-6xl md:text-7xl italic font-light drop-shadow-2xl leading-tight font-playfair">{{ displayData.names }}</h1>
        <div class="flex items-center space-x-6 w-full opacity-60">
            <div class="h-[1px] flex-1 bg-white"></div>
            <span class="text-sm font-serif">A.D. 2026</span>
            <div class="h-[1px] flex-1 bg-white"></div>
        </div>
        <div class="space-y-4">
          <p class="text-xl font-bold tracking-[0.3em] uppercase">{{ displayData.date }}</p>
          <p class="text-xs uppercase tracking-[0.4em] opacity-80">{{ displayData.location }}</p>
        </div>
        <div class="pt-8">
            <div class="mouse-icon">
                <div class="wheel"></div>
            </div>
        </div>
      </div>
    </div>

    <!-- STYLE : LUXE MINIMAL (ES) -->
    <div v-else-if="layout === 'es'" class="h-full min-h-[500px] md:min-h-[700px] w-full flex flex-col items-center justify-center p-12 text-center relative bg-white layout-es">
      <div class="absolute inset-0 opacity-20 reveal-zoom">
        <img :src="displayData.image" class="w-full h-full object-cover grayscale contrast-125" />
      </div>
      <div class="relative z-10 p-16 bg-white shadow-[0_50px_100px_-20px_rgba(0,0,0,0.2)] max-w-[450px] es-box-wrapper reveal-up">
        <div class="absolute inset-4 border-2 border-black/5 pointer-events-none"></div>
        <p class="text-[11px] font-black uppercase tracking-[0.8em] mb-10 text-black/40">Premium Wedding</p>
        <h1 class="text-6xl md:text-7xl font-black uppercase tracking-tighter leading-[0.85] mb-12 text-black font-inter">
            {{ displayData.names.replace(' & ', '\n&\n') }}
        </h1>
        <div class="w-12 h-[6px] bg-[#C5A059] mx-auto mb-12"></div>
        <div class="space-y-2">
            <p class="text-sm font-black tracking-[0.4em] uppercase text-black">{{ displayData.date }}</p>
            <p class="text-[10px] font-bold tracking-[0.2em] uppercase text-black/40">{{ displayData.location }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@900&family=Inter:wght@900&display=swap');

.font-playfair { font-family: 'Playfair Display', serif !important; }
.font-montserrat { font-family: 'Montserrat', sans-serif !important; font-weight: 900 !important; }
.font-inter { font-family: 'Inter', sans-serif !important; font-weight: 900 !important; }

.hero-block-main {
    min-height: 700px;
}

/* Global Paper Texture */
.paper-texture {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 50;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.05;
    mix-blend-mode: multiply;
}

/* Animations */
.reveal-up { opacity: 0; transform: translateY(40px); animation: fadeInUp 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.reveal-left { opacity: 0; transform: translateX(-60px); animation: fadeInLeft 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.reveal-right { opacity: 0; transform: translateX(60px); animation: fadeInRight 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.reveal-zoom { opacity: 0; transform: scale(0.9); animation: fadeInZoom 2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }
.delay-4 { animation-delay: 0.8s; }

@keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInLeft { to { opacity: 1; transform: translateX(0); } }
@keyframes fadeInRight { to { opacity: 1; transform: translateX(0); } }
@keyframes fadeInZoom { to { opacity: 1; transform: scale(1); } }

.zoom-slow { animation: zoomSlow 30s ease-in-out infinite alternate; }
@keyframes zoomSlow { from { transform: scale(1); } to { transform: scale(1.15); } }

/* Layout Arch Specifics */
.arch-frame-wrapper {
    border-radius: 1000px 1000px 0 0;
    border: 8px solid white;
    position: relative;
}
.arch-inner-border {
    position: absolute;
    inset: 12px;
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 1000px 1000px 0 0;
    z-index: 10;
}
.floating-petal {
    position: absolute;
    color: var(--gold, #C5A059);
    font-size: 1.5rem;
    opacity: 0.3;
    animation: float 6s ease-in-out infinite;
}
.p1 { top: 10%; left: 10%; animation-delay: 0s; }
.p2 { top: 20%; right: 15%; animation-delay: 2s; }
@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(20deg); }
}

/* Editorial Badge */
.editorial-badge {
    position: relative;
    width: 100px;
    height: 100px;
}
.animate-spin-slow {
    animation: spin 12s linear infinite;
}
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Split Card */
.split-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
}
.mouse-icon {
    width: 24px;
    height: 40px;
    border: 2px solid white;
    border-radius: 15px;
    position: relative;
    opacity: 0.5;
}
.mouse-icon .wheel {
    width: 2px;
    height: 6px;
    background: white;
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    animation: mouseWheel 2s infinite;
}
@keyframes mouseWheel {
    0% { transform: translateX(-50%) translateY(0); opacity: 1; }
    100% { transform: translateX(-50%) translateY(10px); opacity: 0; }
}

/* ES Box Wrapper */
.es-box-wrapper {
    transition: 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.es-box-wrapper:hover {
    transform: translateY(-10px);
    box-shadow: 0 60px 120px -20px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
    .layout-editorial h1 { font-size: 5rem; line-height: 0.9; }
    .es-box-wrapper { padding: 40px 20px; }
    .layout-arch h1 { font-size: 4rem; }
}
</style>