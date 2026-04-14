<script setup>
defineProps(['section', 'event', 'config']);
</script>

<template>
  <div class="py-12 px-6 text-center bg-transparent transition-all duration-700 animate-fade-in">
    <!-- Ornement supérieur pour certains thèmes -->
    <div v-if="config.templateId === 'royal-gold'" class="mb-8 opacity-40">
       <svg viewBox="0 0 100 20" class="w-32 mx-auto text-accent" fill="currentColor"><path d="M0 10 Q25 0 50 10 Q75 20 100 10 L100 12 Q75 22 50 12 Q25 2 0 12 Z"/></svg>
    </div>
    <div v-if="config.templateId === 'classic-elegance'" class="mb-6 opacity-20">
       <div class="w-8 h-8 mx-auto border border-accent rotate-45"></div>
    </div>

    <h2 
      class="text-3xl md:text-5xl mb-8 transition-all duration-700 section-title"
      :style="{ fontFamily: 'var(--theme-font-headings)' }"
    >
      {{ event.title || 'Notre Histoire' }}
    </h2>
    
    <div 
      class="text-content text-lg md:text-xl leading-[1.8] max-w-2xl mx-auto font-light tracking-wide whitespace-pre-line"
      :style="{ color: 'var(--theme-text)', opacity: 0.9 }"
    >
      {{ section?.content || config?.content?.intro_text || 'Nous serions honorés de votre présence pour célébrer notre union...' }}
    </div>

    <!-- Ornement inférieur -->
    <div v-if="config.templateId === 'bohemian-dream'" class="mt-12 flex justify-center space-x-2">
       <div class="w-2 h-2 rounded-full bg-accent/30"></div>
       <div class="w-2 h-2 rounded-full bg-accent/60"></div>
       <div class="w-2 h-2 rounded-full bg-accent/30"></div>
    </div>
  </div>
</template>

<style scoped>
@reference "tailwindcss";
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

.section-title {
  color: var(--theme-accent);
}

.layout-modern-chic .text-content {
  @apply uppercase font-bold tracking-[0.2em] text-sm md:text-base;
}

.layout-royal-gold .text-content {
  @apply italic font-serif;
}
</style>
