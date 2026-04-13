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
  setTimeout(() => emit('close'), 850);
};
</script>

<template>
  <Transition name="fade-overlay">
    <div 
      v-if="isVisible || isPreview" 
      :class="[isPreview ? 'absolute' : 'fixed', 'layout-' + templateId]" 
      class="inset-0 z-[500] flex flex-col items-center justify-center text-center p-6 overflow-hidden bg-black"
    >
      <!-- Background Image -->
      <div 
        v-if="config?.splash?.use_image !== false"
        class="absolute inset-0 bg-cover bg-center z-0 opacity-60"
        :style="{ 
          backgroundImage: `url(${config?.media?.splash_url || config?.media?.banner_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2070'})`,
          backgroundColor: config?.splash?.background_color || '#000000'
        }"
      ></div>

      <!-- Overlay de sécurité pour la lisibilité -->
      <div class="absolute inset-0 bg-black/40 z-10"></div>

      <!-- Contenu -->
      <div class="relative z-50 flex flex-col items-center max-w-lg w-full">
        <div class="mb-4 opacity-100 translate-y-0 transition-all duration-700">
           <span class="text-white/80 uppercase tracking-[0.4em] text-[10px] font-bold">
             {{ config?.content?.splash_top_text || 'Save the Date' }}
           </span>
        </div>
        
        <h1 
          class="text-5xl md:text-7xl mb-6 text-white drop-shadow-2xl w-full font-serif"
          :style="{ 
            fontFamily: templateId === 'romantic-pink' || config?.typography?.headings === 'cursive' ? 'Great Vibes' : 'Playfair Display',
            letterSpacing: templateId === 'luxury-minimal' ? '0.15em' : 'normal'
          }"
        >
          {{ config?.content?.splash_title || (event.groom_name + ' & ' + event.bride_name) }}
        </h1>

        <div v-if="config?.content?.splash_subtitle" class="mb-8">
          <p class="text-white/90 text-lg md:text-xl font-light tracking-[0.1em] italic">
            {{ config.content.splash_subtitle }}
          </p>
        </div>

        <p class="text-white/90 text-xl md:text-2xl font-light tracking-widest mb-12">
          {{ event.date ? new Date(event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '' }}
        </p>

        <!-- Countdown -->
        <div v-if="config?.show_countdown_splash && event.date" class="mb-12 flex justify-center w-full scale-75 md:scale-90">
          <CardCountdown :targetDate="event.date" themeColor="#ffffff" :templateId="templateId" />
        </div>

        <!-- BOUTON CRITIQUE -->
        <div class="relative z-[600] pointer-events-auto">
          <button 
            @click="handleOpen"
            class="px-10 py-4 rounded-full font-bold uppercase tracking-[0.2em] text-[11px] transition-all shadow-2xl border-2 bg-white text-black hover:scale-105 active:scale-95 border-white cursor-pointer"
          >
            {{ config?.content?.splash_button_text || 'Ouvrir l\'invitation' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-overlay-leave-active {
  transition: all 0.8s cubic-bezier(0.7, 0, 0.3, 1);
}
.fade-overlay-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style>

