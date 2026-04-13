<script setup>
import { computed } from 'vue';
const props = defineProps(['section', 'event', 'config']);

const bannerUrl = computed(() => {
  if (props.config.activePageIndex > 0) {
    const currentPage = props.config.pages?.[props.config.activePageIndex - 1];
    if (currentPage?.banner_url) return currentPage.banner_url;
  }
  return props.config.media?.banner_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2070';
});

const themeStyles = computed(() => {
  const templateId = props.config.templateId;
  if (templateId === 'luxury-minimal') {
    return {
      overlay: 'bg-black/40',
      titleClass: 'text-3xl md:text-5xl font-bold uppercase tracking-[0.4em]',
      font: 'Montserrat, sans-serif'
    };
  }
  if (templateId === 'romantic-pink') {
    return {
      overlay: 'bg-rose-900/20',
      titleClass: 'text-5xl md:text-7xl italic',
      font: 'Great Vibes, cursive'
    };
  }
  // Default / Classic
  return {
    overlay: 'bg-stone-900/30',
    titleClass: 'text-5xl md:text-6xl italic',
    font: 'Cormorant Garamond, serif'
  };
});
</script>

<template>
  <div 
    class="relative min-h-[500px] flex flex-col items-center justify-center text-center p-12 overflow-hidden bg-fixed bg-cover bg-center"
    :style="{ backgroundImage: `url(${bannerUrl})` }"
  >
    <!-- Overlay Dynamique -->
    <div class="absolute inset-0 z-0 transition-colors duration-700" :class="themeStyles.overlay"></div>
    
    <!-- Décoration de coin (optionnelle selon thème) -->
    <div v-if="config.templateId === 'classic-elegance'" class="absolute inset-4 border border-white/20 z-10 pointer-events-none"></div>

    <div class="relative z-10 text-white max-w-3xl">
      <div class="mb-6 overflow-hidden">
        <p class="uppercase tracking-[0.5em] text-[10px] font-bold opacity-80 animate-fade-in-down">
          Notre Mariage
        </p>
      </div>

      <h1 
        class="mb-6 leading-tight drop-shadow-2xl animate-reveal-up"
        :style="{ 
          color: '#FFFFFF', 
          fontFamily: themeStyles.font
        }"
        :class="themeStyles.titleClass"
      >
        {{ event.groom_name }} <span class="text-2xl md:text-4xl block md:inline opacity-70 my-2 md:my-0 md:mx-4">&</span> {{ event.bride_name }}
      </h1>

      <div class="flex items-center justify-center space-x-4 mb-8">
        <div class="w-8 h-[1px] bg-white/50"></div>
        <p class="uppercase tracking-[0.3em] text-[12px] font-medium italic">
          {{ event.date ? new Date(event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '' }}
        </p>
        <div class="w-8 h-[1px] bg-white/50"></div>
      </div>
      
      <p class="text-lg font-light tracking-widest opacity-90 italic font-serif">
        {{ event.location }}
      </p>
    </div>

    <!-- Scroll Indicator -->
    <div class="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-50">
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 13l-7 7-7-7m14-8l-7 7-7-7"></path></svg>
    </div>
  </div>
</template>

<style scoped>
@keyframes fade-in-down {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 0.8; }
}

@keyframes reveal-up {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.animate-fade-in-down { animation: fade-in-down 1.2s ease-out forwards; }
.animate-reveal-up { animation: reveal-up 1.5s cubic-bezier(0.19, 1, 0.22, 1) 0.3s forwards; opacity: 0; }
</style>
