<script setup>
import { ref } from 'vue';
import CardCountdown from './CardCountdown.vue';

const props = defineProps(['event', 'config', 'templateId', 'isPreview']);
const emit = defineEmits(['close']);

const isVisible = ref(true);

const handleOpen = () => {
  if (props.isPreview) return;
  emit('play-music');
  isVisible.value = false;
  // On laisse la transition se faire
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
</script>

<template>
  <Transition name="splash-reveal">
    <div 
      v-if="isVisible || isPreview" 
      :class="[isPreview ? 'absolute' : 'fixed', 'theme-' + templateId]" 
      class="inset-0 z-[1000] flex flex-col items-center justify-center text-center p-6 overflow-hidden bg-[#0a0a0a]"
    >
      <!-- Background Image with Parallax-like scale -->
      <div 
        class="absolute inset-0 z-0 transition-transform duration-[10000ms] ease-linear scale-110"
        :class="{ 'animate-slow-zoom': isVisible }"
        :style="{ 
          backgroundImage: `url(${config?.media?.splash_url || config?.media?.banner_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2070'})`,
          backgroundPosition: 'center',
          backgroundSize: 'cover'
        }"
      >
        <!-- Overlay dégradé plus profond -->
        <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-black/30 to-black/70"></div>
      </div>

      <!-- Bordure élégante -->
      <div class="absolute inset-8 border border-white/20 z-10 pointer-events-none"></div>
      <div class="absolute inset-10 border border-white/10 z-10 pointer-events-none"></div>

      <!-- Contenu Principal -->
      <div class="relative z-50 flex flex-col items-center w-full max-w-2xl px-4">
        
        <!-- Top Text -->
        <div class="mb-8 overflow-hidden">
           <span class="block text-white/90 uppercase tracking-[0.6em] text-[11px] font-medium animate-reveal-up">
             {{ config?.content?.splash_top_text || 'Save the Date' }}
           </span>
        </div>
        
        <!-- Names -->
        <div class="mb-8 overflow-hidden">
          <h1 
            class="text-6xl md:text-8xl text-white drop-shadow-2xl font-serif animate-reveal-up-delay-1 italic"
            :style="{ 
              fontFamily: templateId === 'romantic-pink' || config?.typography?.headings === 'cursive' ? 'Great Vibes, cursive' : 'Cormorant Garamond, serif'
            }"
          >
            {{ config?.content?.splash_title || (event.groom_name + ' & ' + event.bride_name) }}
          </h1>
        </div>

        <!-- Date / Subtitle Divider -->
        <div class="w-24 h-[1px] bg-white/40 mb-8 animate-grow-width"></div>

        <div v-if="config?.content?.splash_subtitle" class="mb-6 overflow-hidden">
          <p class="text-white/90 text-xl md:text-2xl font-light tracking-[0.15em] italic font-serif animate-reveal-up-delay-2">
            {{ config.content.splash_subtitle }}
          </p>
        </div>

        <div class="mb-12 overflow-hidden">
          <p class="text-white/80 text-lg md:text-xl font-light tracking-[0.3em] uppercase animate-reveal-up-delay-2">
            {{ formatDate(event.date) }}
          </p>
        </div>

        <!-- Countdown -->
        <div v-if="config?.show_countdown_splash && event.date" class="mb-16 flex justify-center w-full scale-90 md:scale-100 opacity-0 animate-fade-in-delay-3">
          <CardCountdown :targetDate="event.date" themeColor="#ffffff" :templateId="templateId" />
        </div>

        <!-- Bouton Entrer -->
        <div class="relative z-[600] opacity-0 animate-fade-in-delay-4">
          <button 
            @click="handleOpen"
            class="group relative px-12 py-5 overflow-hidden rounded-none border border-white/50 bg-transparent text-white text-[12px] font-bold uppercase tracking-[0.3em] transition-all duration-500 hover:border-white"
          >
            <!-- Background Fill Effect -->
            <div class="absolute inset-0 w-0 bg-white transition-all duration-500 ease-out group-hover:w-full z-0"></div>
            
            <!-- Text -->
            <span class="relative z-10 transition-colors duration-500 group-hover:text-black">
              {{ config?.content?.splash_button_text || 'Entrer dans l\'invitation' }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Reveal Animations */
@keyframes reveal-up {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes grow-width {
  from { width: 0; opacity: 0; }
  to { width: 6rem; opacity: 1; }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slow-zoom {
  from { transform: scale(1.1); }
  to { transform: scale(1.2); }
}

.animate-reveal-up { animation: reveal-up 1s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
.animate-reveal-up-delay-1 { animation: reveal-up 1.2s cubic-bezier(0.19, 1, 0.22, 1) 0.2s forwards; opacity: 0; }
.animate-reveal-up-delay-2 { animation: reveal-up 1.2s cubic-bezier(0.19, 1, 0.22, 1) 0.4s forwards; opacity: 0; }
.animate-grow-width { animation: grow-width 1.5s cubic-bezier(0.19, 1, 0.22, 1) 0.6s forwards; opacity: 0; }
.animate-fade-in-delay-3 { animation: fade-in 1s ease-out 0.8s forwards; }
.animate-fade-in-delay-4 { animation: fade-in 1s ease-out 1s forwards; }
.animate-slow-zoom { animation: slow-zoom 20s linear infinite alternate; }

/* Splash Reveal Transition */
.splash-reveal-leave-active {
  transition: all 1.2s cubic-bezier(0.85, 0, 0.15, 1);
}
.splash-reveal-leave-to {
  transform: translateY(-100%);
  filter: brightness(1.5) blur(10px);
}

/* Theme specific overrides */
.theme-romantic-pink h1 {
  color: #fecdd3; /* text-rose-200 */
}
</style>
