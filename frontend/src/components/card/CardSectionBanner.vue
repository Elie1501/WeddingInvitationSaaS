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
</script>

<template>
  <div 
    class="relative w-full flex flex-col items-center justify-center text-center overflow-hidden transition-all duration-1000"
    :class="[
      config.templateId === 'midnight-glamour' ? 'h-full min-h-screen' : 'min-h-[600px] rounded-3xl md:rounded-[4rem]'
    ]"
  >
    <!-- Image de fond avec effet parallax léger -->
    <div 
      class="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat transition-transform duration-1000 hover:scale-105"
      :style="{ backgroundImage: `url(${bannerUrl})` }"
    ></div>

    <!-- Overlay intelligent -->
    <div 
      class="absolute inset-0 z-1"
      :class="[
        config.templateId === 'royal-gold' ? 'bg-black/40' : 
        config.templateId === 'midnight-glamour' ? 'bg-indigo-950/30' : 
        config.templateId === 'modern-chic' ? 'bg-white/10' : 'bg-black/20'
      ]"
    ></div>
    
    <!-- Contenu -->
    <div class="relative z-10 p-8 md:p-16 flex flex-col items-center max-w-4xl">
      <p 
        class="uppercase tracking-[0.6em] text-[10px] md:text-xs font-bold mb-8 animate-fade-in drop-shadow-md"
        :style="{ color: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white' }"
      >
        {{ config.templateId === 'modern-chic' ? 'THE WEDDING OF' : 'Notre Mariage' }}
      </p>

      <h1 
        class="mb-8 leading-tight drop-shadow-2xl animate-reveal-up"
        :style="{ 
          fontFamily: 'var(--theme-font-headings)',
          color: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white'
        }"
      >
        <span class="block">{{ event.groom_name || 'Prénom' }}</span>
        <span class="text-3xl md:text-5xl block my-4 opacity-80">&</span>
        <span class="block">{{ event.bride_name || 'Prénom' }}</span>
      </h1>

      <div class="flex items-center justify-center space-x-6 mb-10 animate-fade-in-delayed">
        <div class="w-12 h-[1px]" :style="{ backgroundColor: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white', opacity: 0.4 }"></div>
        <p 
          class="uppercase tracking-[0.4em] text-xs md:text-sm font-medium"
          :style="{ color: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white', opacity: 0.9 }"
        >
          {{ event.date ? new Date(event.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Date de l\'événement' }}
        </p>
        <div class="w-12 h-[1px]" :style="{ backgroundColor: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white', opacity: 0.4 }"></div>
      </div>
      
      <p 
        class="text-lg md:text-xl font-light tracking-[0.2em] italic animate-fade-in-delayed"
        :style="{ color: config.templateId === 'modern-chic' ? 'var(--theme-text)' : 'white', opacity: 0.8 }"
      >
        {{ event.location || 'Lieu de la cérémonie' }}
      </p>
    </div>

    <!-- Scroll Indicator -->
    <div v-if="config.templateId !== 'modern-chic'" class="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce opacity-60 z-10">
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 13l-7 7-7-7m14-8l-7 7-7-7"></path></svg>
    </div>
  </div>
</template>

<style scoped>
@keyframes reveal-up {
  from { transform: translateY(60px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-reveal-up { animation: reveal-up 1.8s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
.animate-fade-in { animation: fade-in 1.5s ease-out forwards; }
.animate-fade-in-delayed { animation: fade-in 1.5s ease-out 0.8s forwards; opacity: 0; }

h1 {
  font-size: clamp(3rem, 10vw, 8rem);
}
</style>
