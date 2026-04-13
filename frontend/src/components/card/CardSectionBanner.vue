<script setup>
import { computed } from 'vue';
const props = defineProps(['section', 'event', 'config']);

const bannerUrl = computed(() => {
  // On récupère l'index de la page active depuis la config si elle y est (passée par CardRenderer)
  if (props.config.activePageIndex > 0) {
    const currentPage = props.config.pages?.[props.config.activePageIndex - 1];
    if (currentPage?.banner_url) return currentPage.banner_url;
  }
  return props.config.media?.banner_url || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=2070';
});
</script>

<template>
  <div 
    class="relative h-80 flex flex-col items-center justify-center text-center p-8 bg-cover bg-center"
    :style="{ backgroundImage: `url(${bannerUrl})` }"
  >
    <div class="absolute inset-0 bg-black/30"></div>
    <div class="relative z-10 text-white">
      <h1 class="text-4xl md:text-5xl font-serif mb-2" :style="{ color: config?.colors?.primary || '#FFFFFF', fontFamily: config?.typography?.headings || 'serif' }">
        {{ event.groom_name }} & {{ event.bride_name }}
      </h1>
      <p class="uppercase tracking-widest text-sm opacity-90">Se marient !</p>
    </div>
  </div>
</template>
