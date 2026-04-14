<script setup>
import { ref, computed } from 'vue';
import CardCountdown from './CardCountdown.vue';

const props = defineProps(['event', 'config', 'templateId', 'isPreview']);
const emit = defineEmits(['close', 'play-music']);

const isVisible = ref(true);

const handleOpen = () => {
  if (props.isPreview) return;
  emit('play-music');
  isVisible.value = false;
  setTimeout(() => emit('close'), 1200);
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('fr-FR', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  });
};

const themeStyles = computed(() => {
  const base = {
    overlay: 'bg-black/40',
    font: 'Cormorant Garamond, serif',
    accent: '#ffffff'
  };

  if (props.templateId === 'royal-gold') {
    return {
      overlay: 'bg-neutral-900/60',
      font: "'Great Vibes', cursive",
      accent: '#d4af37'
    };
  }
  if (props.templateId === 'bohemian-dream') {
    return {
      overlay: 'bg-stone-900/30',
      font: "'Playfair Display', serif",
      accent: '#c46647'
    };
  }
  if (props.templateId === 'midnight-glamour') {
    return {
      overlay: 'bg-indigo-950/40',
      font: "'Cormorant Garamond', serif",
      accent: '#818cf8'
    };
  }
  return base;
});
</script>

<template>
  <Transition name="splash-reveal">
    <div 
      v-if="isVisible || isPreview" 
      :class="[isPreview ? 'absolute' : 'fixed', 'layout-' + templateId]" 
      class="inset-0 z-[1000] flex flex-col items-center justify-center text-center p-6 overflow-hidden bg-neutral-950"
    >
      <!-- Background Image -->
      <div 
        class="absolute inset-0 z-0 transition-transform duration-[10000ms] scale-110"
        :class="{ 'animate-slow-zoom': isVisible }"
        :style="{ 
          backgroundImage: `url(${config?.media?.splash_url || config?.media?.banner_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2070'})`,
          backgroundPosition: 'center',
          backgroundSize: 'cover'
        }"
      >
        <div class="absolute inset-0 transition-colors duration-1000" :class="themeStyles.overlay"></div>
      </div>

      <!-- Bordures décoratives thématiques -->
      <div v-if="templateId === 'royal-gold'" class="absolute inset-8 border border-[#d4af37]/30 z-10 pointer-events-none"></div>
      <div v-if="templateId === 'royal-gold'" class="absolute inset-12 border border-[#d4af37]/10 z-10 pointer-events-none"></div>
      <div v-if="templateId === 'classic-elegance'" class="absolute inset-10 border border-white/20 z-10 pointer-events-none"></div>

      <!-- Contenu -->
      <div class="relative z-50 flex flex-col items-center w-full max-w-2xl px-4">
        
        <div class="mb-8 overflow-hidden">
           <span class="block text-white/90 uppercase tracking-[0.6em] text-[10px] md:text-xs font-bold animate-reveal-up">
             {{ config?.content?.splash_top_text || 'Save the Date' }}
           </span>
        </div>
        
        <div class="mb-10 overflow-hidden">
          <h1 
            class="text-6xl md:text-8xl drop-shadow-2xl animate-reveal-up-delay-1 italic"
            :style="{ 
              fontFamily: themeStyles.font,
              color: templateId === 'royal-gold' ? '#d4af37' : '#ffffff'
            }"
          >
            {{ config?.content?.splash_title || (event.groom_name + ' & ' + event.bride_name) }}
          </h1>
        </div>

        <div class="w-24 h-[1px] mb-10 animate-grow-width" :style="{ backgroundColor: themeStyles.accent + '66' }"></div>

        <div v-if="config?.content?.splash_subtitle" class="mb-8 overflow-hidden">
          <p class="text-white text-xl md:text-3xl font-light tracking-[0.1em] italic font-serif animate-reveal-up-delay-2">
            {{ config.content.splash_subtitle }}
          </p>
        </div>

        <div class="mb-12 overflow-hidden">
          <p class="text-white/80 text-lg md:text-xl font-light tracking-[0.4em] uppercase animate-reveal-up-delay-2">
            {{ formatDate(event.date) }}
          </p>
        </div>

        <div v-if="config?.show_countdown_splash && event.date" class="mb-16 flex justify-center w-full scale-90 md:scale-100 opacity-0 animate-fade-in-delay-3">
          <CardCountdown :targetDate="event.date" :themeColor="themeStyles.accent" :templateId="templateId" />
        </div>

        <div class="relative z-[600] opacity-0 animate-fade-in-delay-4">
          <button 
            @click="handleOpen"
            class="group relative px-12 py-5 overflow-hidden rounded-none border transition-all duration-500"
            :class="[
               templateId === 'modern-chic' ? 'border-white bg-white text-black' : 'border-white/50 text-white hover:border-white'
            ]"
          >
            <div v-if="templateId !== 'modern-chic'" class="absolute inset-0 w-0 bg-white transition-all duration-500 ease-out group-hover:w-full z-0"></div>
            <span class="relative z-10 transition-colors duration-500" :class="templateId !== 'modern-chic' ? 'group-hover:text-black' : ''">
              {{ config?.content?.splash_button_text || 'Entrer dans l\'invitation' }}
            </span>
          </button>
          <p v-if="isPreview" class="text-[9px] text-white/40 mt-4 uppercase tracking-widest font-bold">(Aperçu du Splash Screen)</p>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
@keyframes reveal-up { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes grow-width { from { width: 0; opacity: 0; } to { width: 8rem; opacity: 1; } }
@keyframes fade-in { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slow-zoom { from { transform: scale(1.1); } to { transform: scale(1.2); } }

.animate-reveal-up { animation: reveal-up 1.2s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
.animate-reveal-up-delay-1 { animation: reveal-up 1.4s cubic-bezier(0.19, 1, 0.22, 1) 0.2s forwards; opacity: 0; }
.animate-reveal-up-delay-2 { animation: reveal-up 1.4s cubic-bezier(0.19, 1, 0.22, 1) 0.4s forwards; opacity: 0; }
.animate-grow-width { animation: grow-width 1.5s cubic-bezier(0.19, 1, 0.22, 1) 0.6s forwards; opacity: 0; }
.animate-fade-in-delay-3 { animation: fade-in 1s ease-out 0.8s forwards; }
.animate-fade-in-delay-4 { animation: fade-in 1s ease-out 1s forwards; }
.animate-slow-zoom { animation: slow-zoom 30s linear infinite alternate; }

.splash-reveal-leave-active { transition: all 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
.splash-reveal-leave-to { transform: translateY(-100%); filter: brightness(1.5) blur(10px); }
</style>
